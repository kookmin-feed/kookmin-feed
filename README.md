# 국민대학교 공지사항 알리미 봇

디스코드를 통해 국민대학교의 각 학과/단과대학의 공지사항을 실시간으로 전달하는 봇입니다.

## 기능

- 실시간 공지사항 알림
  - 소프트웨어학부
    - 대학 학사공지
    - 대학 장학공지
    - 소융대 학사공지 (RSS)
    - SW중심대학사업단 학사공지
  - 경영대학
    - 경영대 학사공지 (RSS)
  - 건축대학
    - 건축대 학사공지
  - 사회과학대학
    - 행정학과 학사공지
  - 창의공과대학
    - 기계공학부 학사공지
    - 전자공학부 학사공지 (RSS)
  - 조형대학
    - 공업디자인학과 학사공지
    - 금속공예학과 학사공지
    - 시각디자인학과 학사공지
  - 자동차융합대학
    - 자동차융합대학 학사공지
  - 기타
    - LINC 3.0 사업단 학사공지
- 디스코드 채널 또는 DM으로 알림 수신
- 공지사항 종류별 구독 관리
- 개발 환경별 설정 (개발/운영)

## 설치 방법

1. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

2. 환경 설정 파일 구성
- 운영 환경: `.env` (프로젝트 루트)
- 개발 환경: `envs/.dev.env`

```env
# 필수 환경 변수
DISCORD_TOKEN=your_discord_bot_token
MONGODB_URI=your_mongodb_connection_string
DB_NAME=your_database_name
YOUTUBE_API_KEY=your_youtube_api_key
```

## 프로젝트 구조

```
.
├── config/
│   ├── env_loader.py           # 환경 설정 로더
│   ├── db_config.py             # 데이터베이스 설정
│   └── logger_config.py         # 로깅 설정
├── discord_bot/
│   ├── discord_bot.py          # 디스코드 봇 코어
│   ├── scraper_config.py       # 스크래퍼 설정
│   └── commands/               # 디스코드 명령어
│       ├── register.py         # 공지 등록 명령어
│       └── test.py             # 테스트 명령어
├── template/
│   └── notice_data.py          # 공지사항 데이터 모델
├── utils/
│   ├── scraper_type.py        # 스크래퍼 타입 정의
│   ├── scraper_factory.py     # 스크래퍼 생성 팩토리
│   ├── scraper_category.py    # 스크래퍼 카테고리 정의
│   ├── web_scraper.py         # 웹 스크래퍼 슈퍼 클래스
│   └── rss_notice_scraper.py  # RSS 스크래퍼 클래스
└── main.py                     # 프로그램 진입점
```

## 데이터베이스 구조

### MongoDB 컬렉션

- 컬렉션명: 각 스크래퍼 타입의 `collection_name`
- 문서 구조:
  - `title`: 공지사항 제목
  - `link`: 공지사항 링크
  - `published`: 작성일 (ISO 형식)
  - `scraper_type`: 스크래퍼 타입 식별자

## 개발 정보

### 환경 구분
- 운영(PROD): Ubuntu 환경
- 개발(DEV): 그 외 환경

### 크롤링 주기
- 운영 환경: 10분
- 개발 환경: 2분

## 디스코드 명령어

- `/게시판_선택`: 공지사항 알림 등록
- `/게시판_선택취소`: 공지사항 알림 삭제
- `/선택된_게시판`: 현재 등록된 알림 목록 확인
- `/testnotice`: 테스트 공지사항 전송 (개발 환경 전용)
- `/test-list`: 등록된 채널/유저 목록 확인 (개발 환경 전용)

## 주의사항

- 환경 변수 파일 보안 관리 (.env, .dev.env)
- MongoDB 연결 정보 보안
- 크롤링 간격 조절 시 서버 부하 고려
- 봇 권한 확인 (메시지 전송, 임베드 등)
- 운영 환경과 개발 환경의 설정 차이 주의

## 라이선스

MIT License

## 기여하기

1. Fork the Project
2. Create your Feature Branch
3. Commit your Changes
4. Push to the Branch
5. Open a Pull Request