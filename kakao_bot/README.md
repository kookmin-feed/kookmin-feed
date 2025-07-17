# 카카오 봇 API 서버

카카오톡 챗봇을 위한 FastAPI 기반 API 서버입니다.

## 📋 목차

- [기능](#기능)
- [설치 및 실행](#설치-및-실행)
- [환경 변수 설정](#환경-변수-설정)
- [API 엔드포인트](#api-엔드포인트)
- [프로젝트 구조](#프로젝트-구조)

## 🚀 기능

- 카카오톡 스킬 서버 API
- 사용자 인증 및 권한 관리
- 게시판 등록/관리 기능
- 카카오 OAuth 로그인
- 미들웨어 기반 로깅 및 인증
- 데이터 서버 연동

## 📦 설치 및 실행

### 1. 의존성 설치

```bash
cd kakao_bot
pip install -r requirements.txt
```

### 2. 환경 변수 설정

환경에 따라 다른 환경 변수 파일을 사용합니다:

- **개발 환경**: `kakao_bot/envs/.dev.env`
- **운영 환경**: `kakao_bot/.env`

시스템이 Ubuntu인지 여부에 따라 자동으로 환경 파일을 선택합니다.

### 3. 환경 변수 파일 생성

**두 위치에 환경 변수 파일을 생성해야 합니다:**

#### 개발 환경

1. **루트 폴더** (`envs/.dev.env`)
2. **카카오 봇 폴더** (`kakao_bot/envs/.dev.env`)

```env
# 서버 설정
HOST=0.0.0.0
PORT=8000
SERVER_URL=http://localhost:8000

# API 키
API_KEY=your_api_key_here

# 데이터 서버 설정
DATA_SERVER_URL=localhost:8080
DATA_SERVER_API_KEY=your_data_server_api_key

# 카카오 OAuth 설정
KAKAO_CLIENT_ID=your_kakao_client_id
KAKAO_REDIRECT_URL=http://localhost:8000/api/v1/auth/redirect
```

#### 운영 환경

1. **루트 폴더** (`.env`)
2. **카카오 봇 폴더** (`kakao_bot/.env`)

```env
# 서버 설정
HOST=0.0.0.0
PORT=8000
SERVER_URL=https://your-domain.com

# API 키
API_KEY=your_production_api_key

# 데이터 서버 설정
DATA_SERVER_URL=your-data-server-url:port
DATA_SERVER_API_KEY=your_production_data_server_api_key

# 카카오 OAuth 설정
KAKAO_CLIENT_ID=your_production_kakao_client_id
KAKAO_REDIRECT_URL=https://your-domain.com/api/v1/auth/redirect
```

### 4. 서버 실행

```bash
cd kakao_bot
python main.py
```

또는 uvicorn을 직접 사용:

```bash
cd kakao_bot
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 🔧 환경 변수 설정

### 필수 환경 변수

| 변수명 | 설명 | 예시 |
|--------|------|------|
| `HOST` | 서버 호스트 | `0.0.0.0` |
| `PORT` | 서버 포트 | `8000` |
| `SERVER_URL` | 서버 URL | `http://localhost:8000` |
| `API_KEY` | API 인증 키 | `your_api_key_here` |
| `DATA_SERVER_URL` | 데이터 서버 URL | `localhost:8080` |
| `DATA_SERVER_API_KEY` | 데이터 서버 API 키 | `your_data_server_api_key` |
| `KAKAO_CLIENT_ID` | 카카오 클라이언트 ID | `your_kakao_client_id` |
| `KAKAO_REDIRECT_URL` | 카카오 리다이렉트 URL | `http://localhost:8000/api/v1/auth/redirect` |

### 환경 변수 파일 위치

카카오 봇은 다음 위치의 환경 변수 파일을 사용합니다:

- **개발 환경**: `kakao_bot/envs/.dev.env`
- **운영 환경**: `kakao_bot/.env`

**⚠️ 중요**: 루트 폴더에도 환경 변수 파일이 필요합니다:
- **개발 환경**: `envs/.dev.env` (루트 폴더)
- **운영 환경**: `.env` (루트 폴더)

환경 감지는 `kakao_bot/config/env_loader.py`에서 자동으로 처리됩니다:
- Ubuntu 시스템: 운영 환경으로 인식 (`.env` 파일 사용)
- 기타 시스템: 개발 환경으로 인식 (`.dev.env` 파일 사용)

## 📡 API 엔드포인트

### 인증 관련
- `GET /api/v1/auth/redirect` - 카카오 OAuth 리다이렉트

### 게시판 관련
- `POST /api/v1/board/` - 게시판 등록

### API 문서
서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🏗️ 프로젝트 구조

```
kakao_bot/
├── api/                    # API 관련 모듈
│   ├── deps.py            # 의존성 주입
│   ├── models/            # 데이터 모델
│   └── v1/                # API v1 엔드포인트
├── commands/              # 명령어 처리
├── config/                # 설정 관련
│   ├── env_loader.py      # 환경 변수 로더
│   └── logger_config.py   # 로깅 설정
├── envs/                  # 환경 변수 파일
│   └── .dev.env          # 개발 환경 변수
├── middleware/            # 미들웨어
│   ├── auth_middleware.py # 인증 미들웨어
│   └── logging_middleware.py # 로깅 미들웨어
├── utils/                 # 유틸리티 함수
├── main.py               # 메인 애플리케이션
├── requirements.txt      # 의존성 목록
└── README.md            # 프로젝트 설명서
```

## 🔍 주요 기능

### 미들웨어
- **인증 미들웨어**: 사용자 등록 상태 확인 및 로그인 리다이렉트
- **로깅 미들웨어**: 요청/응답 로깅 및 컨텍스트 관리

### 데이터 서버 연동
- 비동기 HTTP 클라이언트를 통한 데이터 서버 통신
- 자동 재시도 및 에러 처리

### 카카오 OAuth
- 카카오 로그인 연동
- 토큰 관리 및 사용자 정보 처리

## 🚨 주의사항

1. **환경 변수 파일 보안**: `.env` 파일들은 민감한 정보를 포함하므로 버전 관리에 포함하지 마세요.
2. **환경 변수 파일 위치**: 루트 폴더와 `kakao_bot` 폴더 **두 곳 모두**에 환경 변수 파일을 생성해야 합니다.
3. **데이터 서버 연결**: 서버 시작 전 데이터 서버가 실행 중인지 확인하세요.
4. **포트 설정**: 다른 서비스와 포트 충돌이 없는지 확인하세요.

## 📝 로그

로그는 환경에 따라 다른 레벨로 출력됩니다:
- **개발 환경**: DEBUG 레벨
- **운영 환경**: INFO 레벨

로그에는 클라이언트 IP, User-Agent, 요청 경로 등의 컨텍스트 정보가 포함됩니다. 