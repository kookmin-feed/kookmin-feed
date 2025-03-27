from enum import Enum
from typing import Optional
from discord import app_commands


class ScraperType(Enum):
    """스크래퍼 종류를 정의하는 열거형 클래스

    각 스크래퍼는 다음과 같은 4개의 값을 튜플로 가집니다:
        1. collection_name (str): MongoDB 컬렉션 이름으로 사용될 식별자
        2. korean_name (str): 사용자에게 보여질 한글 이름
        3. url (str): 크롤링할 웹페이지의 URL
        4. scraper_class_name (str): 사용할 스크래퍼 클래스 이름

    예시:
        UNIVERSITY_ACADEMIC = (
            "university_academic",      # MongoDB 컬렉션 이름
            "대학 학사공지",            # 한글 이름
            "https://example.com",      # 크롤링 URL
            "UniversityAcademicScraper" # 스크래퍼 클래스 이름
        )

    Methods:
        get_collection_name(): MongoDB 컬렉션 이름 반환
        get_korean_name(): 한글 이름 반환
        get_url(): 크롤링 URL 반환
        get_scrpper_class_name(): 스크래퍼 클래스 이름 반환
        from_str(value: str): 문자열로부터 ScraperType 객체 생성
        get_choices(): 디스코드 명령어용 선택지 목록 반환
        get_active_scrapers(): 활성화된 모든 스크래퍼 타입 목록 반환
    """

    UNIVERSITY_ACADEMIC = (
        "university_academic",  # collection_name
        "대학 학사공지",  # korean_name
        "https://cs.kookmin.ac.kr/news/kookmin/academic/",  # url
        "UniversityAcademicScraper",  # scraper_class_name
    )
    UNIVERSITY_SCHOLARSHIP = (
        "university_scholarship",
        "대학 장학공지",
        "https://cs.kookmin.ac.kr/news/kookmin/scholarship/",
        "UniversityScholarshipScraper",
    )
    COMPUTERSCIENCE_ACADEMIC_RSS = (
        "computerscience_academic_rss",
        "소융대 학사공지",
        "https://cs.kookmin.ac.kr/news/notice/rss",
        "RSSNoticeScraper",
    )
    SOFTWARECENTERED_ACADEMIC = (
        "softwarecentered_academic",
        "SW중심대학사업단 학사공지",
        "https://software.kookmin.ac.kr/software/bulletin/notice.do",
        "SoftwarecenteredAcademicScraper",
    )
    BUSINESSADMINISTRATION_ACADEMIC_RSS = (
        "businessadministration_academic_rss",
        "경영대 학사공지",
        "https://biz.kookmin.ac.kr/community/notice/rss",
        "RSSNoticeScraper",
    )
    ARCHITECTURE_ACADEMIC = (
        "architecture_academic",
        "건축대 학사공지",
        "https://archi.kookmin.ac.kr/life/notice/",
        "ArchitectureAcademicScraper",
    )
    SOCIALSCIENCE_PUBLICADMINISTRATION_ACADEMIC = (
        "socialscience_publicadministration_academic",
        "행정학과 학사공지",
        "http://cms.kookmin.ac.kr/paap/notice/notice.do",
        "SocialsciencePublicadministrationAcademicScraper",
    )
    CREATIVEENGINEERING_MECHANICAL_ACADEMIC = (
        "creativeengineering_mechanical_academic",
        "기계공학부 학사공지",
        "http://cms.kookmin.ac.kr/mech/bbs/notice.do",
        "CreativeengineeringMechanicalAcademicScraper",
    )
    DESIGN_INDUSTRIAL_ACADEMIC = (
        "design_industrial_academic",
        "공업디자인학과 학사공지",
        "https://id.kookmin.ac.kr/id/intro/notice.do",
        "DesignIndustrialAcademicScraper",
    )
    DESIGN_METALWORK_ACADEMIC = (
        "design_metalwork_academic",
        "금속공예학과 학사공지",
        "http://mcraft.kookmin.ac.kr/?page_id=516",
        "DesignMetalworkAcademicScraper",
    )
    LINC_ACADEMIC = (
        "linc_academic",
        "LINC 3.0 사업단 학사공지",
        "https://linc.kookmin.ac.kr/main/menu?gc=605XOAS",
        "LincAcademicScraper",
    )
    DESIGN_VISUAL_ACADEMIC = (
        "design_visual_academic",
        "시각디자인학과 학사공지",
        "https://vcd.kookmin.ac.kr/vcd/etc-board/vcdnotice.do",
        "DesignVisualAcademicScraper",
    )
    CREATIVEENGINEERING_ELECTRICAL_ACADEMIC_RSS = (
        "creativeengineering_electrical_academic_rss",
        "전자공학부 학사공지",
        "https://ee.kookmin.ac.kr/community/board/notice/rss",
        "RSSNoticeScraper",
    )
    AUTOMATIVEENGINEERING_ACADEMIC = (
        "automativeengineering_academic",
        "자동차융합대학 학사공지",
        "https://auto.kookmin.ac.kr/board/notice/?&pn=0",
        "AutomativeengineeringAcademicScraper",
    )
    CREATIVEENGINEERING_ADVANCEDMATERIALS_ACADEMIC = (
        "creativeengineering_advancedmaterials_academic",
        "신소재공학부 학사공지",
        "https://cms.kookmin.ac.kr/mse/bbs/notice.do",
        "CreativeengineeringAdvancedmaterialsAcademicScraper",
    )
    LAW_ACADEMIC = (
        "law_academic",
        "법과대학 학사공지",
        "https://law.kookmin.ac.kr/law/etc-board/notice01.do",
        "LawAcademicScraper",
    )
    UNIVERSITY_SPECIALLECTURE = (
        "university_speciallecture",
        "대학 특강공지",
        "https://cs.kookmin.ac.kr/news/kookmin/special_lecture/",
        "UniversitySpeciallectureScraper",
    )
    UNIVERSITY_CONTESTEVENT = (
        "university_contestevent",
        "대학 공모행사공지",
        "https://www.kookmin.ac.kr/user/kmuNews/notice/9/index.do",
        "UniversityContesteventScraper",
    )
    DORMITORY_GENERAL_RSS = (
        "dormitory_general_rss",
        "생활관 일반공지",
        "https://dormitory.kookmin.ac.kr/notice/notice/rss",
        "RSSNoticeScraper",
    )
    SCIENCETECHNOLOGY_CHEMISTRY_ACADEMIC = (
        "sciencetechnology_chemistry_academic",
        "응용화학부 학사공지",
        "http://chem.kookmin.ac.kr/sub6/menu1.php",
        "SciencetechnologyChemistryAcademicScraper",
    )
    CREATIVEENGINEERING_CIVIL_ACADEMIC = (
        "creativeengineering_civil_academic",
        "건설시스템공학부 학사공지",
        "https://cms.kookmin.ac.kr/cee/bbs/notice.do",
        "CreativeengineeringCivilAcademicScraper",
    )
    SCIENCETECHNOLOGY_SECURITY_ACADEMIC = (
        "sciencetechnology_security_academic",
        "정보보안암호수학과 학사공지",
        "https://cns.kookmin.ac.kr/cns/notice/academic-notice.do",
        "SciencetechnologySecurityAcademicScraper",
    )
    DESIGN_AUTOMOTIVE_ACADEMIC = (
        "design_automotive_academic",
        "자동차·운송디자인학과 학사공지",
        "https://mobility.kookmin.ac.kr/mobility/etc-board/employment-information.do",
        "DesignAutomotiveAcademicScraper",
    )
    SOCIALSCIENCE_EDUCATION_ACADEMIC = (
        "socialscience_education_academic",
        "교육학과 학사공지",
        "https://cms.kookmin.ac.kr/kmuedu/community/notice.do",
        "SocialscienceEducationAcademicScraper",
    )
    SOCIALSCIENCE_POLITICALSCIENCE_ACADEMIC = (
        "socialscience_politicalscience_academic",
        "정치외교학과 학사공지",
        "https://polisci.kookmin.ac.kr/polisci/etc-board/board02.do",
        "SocialsciencePoliticalscienceAcademicScraper",
    )
    ECONOMICCOMMERCE_ACADEMIC_RSS = (
        "economiccommerce_academic_rss",
        "경상대학 학사공지",
        "https://kyungsang.kookmin.ac.kr/community/board/notice/rss",
        "RSSNoticeScraper",
    )
    CREATIVEENGINEERING_ACADEMIC_RSS = (
        "creativeengineering_academic_rss",
        "창의공과대학 학사공지",
        "https://engineering.kookmin.ac.kr/board/engineering_notice/rss",
        "RSSNoticeScraper",
    )
    CULTURE_ACADEMIC_RSS = (
        "culture_academic_rss",
        "교양대학 학사공지",
        "https://culture.kookmin.ac.kr/community/notice/rss",
        "RSSNoticeScraper",
    )
    TEACHING_ACADEMIC_RSS = (
        "teaching_academic_rss",
        "교직과정부 학사공지",
        "https://teaching.kookmin.ac.kr/introduce/notice/rss",
        "RSSNoticeScraper",
    )
    SOCIALSCIENCE_SOCIOLOGY_ACADEMIC = (
        "socialscience_sociology_academic",
        "사회학과 학사공지",
        "https://kmusoc.kookmin.ac.kr/kmusoc/etc-board/major_notice.do",
        "SocialscienceSociologyAcademicScraper",
    )
    SOCIALSCIENCE_COMMUNICATION_MEDIA_ACADEMIC = (
        "socialscience_communication_media_academic",
        "미디어전공 학사공지",
        "https://kmumedia.kookmin.ac.kr/kmumedia/community/major-notice.do",
        "SocialscienceCommunicationMediaAcademicScraper",
    )
    ARTS_ACADEMIC = (
        "arts_academic",
        "예술대학 학사공지",
        "https://art.kookmin.ac.kr/community/notice/",
        "ArtsAcademicScraper",
    )
    PHYSICALEDUCATION_ACADEMIC = (
        "physicaleducation_academic",
        "체육대학 학사공지",
        "https://sport.kookmin.ac.kr/sports/notice/notice01.do",
        "PhysicaleducationAcademicScraper",
    )
    DESIGN_CERAMICS_ACADEMIC = (
        "design_ceramics_academic",
        "도자공예학과 학사공지",
        "https://kmuceramics.com/news/",
        "DesignCeramicsAcademicScraper",
    )
    SOCIALSCIENCE_COMMUNICATION_ADVERTISING_ACADEMIC = (
        "socialscience_communication_advertising_academic",
        "광고홍보학전공 학사공지",
        "https://adpr.kookmin.ac.kr/adpr/menu/undergraduate-notice.do",
        "SocialscienceCommunicationAdvertisingAcademicScraper",
    )
    SOCIALSCIENCE_ACADEMIC = (
        "socialscience_academic",
        "사회과학대학 학사공지",
        "https://social.kookmin.ac.kr/social/menu/social_notice.do",
        "SocialscienceAcademicScraper",
    )
    GLOBALHUMANITIES_EURASIAN_ACADEMIC = (
        "globalhumanities_eurasian_academic",
        "러시아유라시아학과 학사공지",
        "https://cms.kookmin.ac.kr/Russian-EurasianStudies/community/department-notice.do",
        "GlobalhumanitiesEurasianAcademicScraper",
    )

    GLOBALHUMANITIES_ACADEMIC_RSS = (
        "globalhumanities_academic_rss",
        "글로벌인문지역대학 학사공지",
        "https://cha.kookmin.ac.kr/community/college/notice/rss",
        "RSSNoticeScraper",
    )
    GLOBALHUMANITIES_KOREAN_ACADEMIC_RSS = (
        "globalhumanities_korean_academic_rss",
        "한국어문학부 학사공지",
        "https://cha.kookmin.ac.kr/korea/korea_notice/rss",
        "RSSNoticeScraper",
    )
    GLOBALHUMANITIES_ENGLISH_ACADEMIC_RSS = (
        "globalhumanities_english_academic_rss",
        "영어영문학부 학사공지",
        "https://cha.kookmin.ac.kr/english/english_notice/rss",
        "RSSNoticeScraper",
    )
    GLOBALHUMANITIES_CHINESE_ACADEMIC_RSS = (
        "globalhumanities_chinese_academic_rss",
        "중국어문학부 학사공지",
        "https://cha.kookmin.ac.kr/china/china_notice/rss",
        "RSSNoticeScraper",
    )
    GLOBALHUMANITIES_KOREANHISTORY_ACADEMIC_RSS = (
        "globalhumanities_koreanhistory_academic_rss",
        "한국역사학과 학사공지",
        "https://cha.kookmin.ac.kr/history/history_notice/rss",
        "RSSNoticeScraper",
    )

    COSS_ACADEMIC = (
        "coss_academic",
        "미래자동차사업단 학사공지",
        "https://coss.kookmin.ac.kr/fvedu/community/notice.do",
        "CossAcademicScraper",
    )

    FUTUREMOBILITY_ACADEMIC = (
        "futuremobility_academic",
        "미래모빌리티학과 학사공지",
        "https://cms.kookmin.ac.kr/futuremobility/board/notice.do",
        "FuturemobilityAcademicScraper",
    )

    NCCOSS_GENERAL = (
        "nccoss_general",
        "차세대통신사업단 학사공지",
        "https://nccoss.kookmin.ac.kr/NCCOSS/community/notice.do",
        "NccossGeneralScraper",
    )

    JO_CODING_YOUTUBE = (
        "jo_coding_youtube",
        "조코딩 유튜브",
        "https://www.youtube.com/@jocoding/shorts",
        "JoCodingYoutubeScraper",
    )

    def get_collection_name(self) -> str:
        """MongoDB 컬렉션 이름을 반환합니다."""
        return self.value[0]

    def get_korean_name(self) -> str:
        """스크래퍼 타입의 한글 이름을 반환합니다."""
        return self.value[1]

    def get_url(self) -> str:
        """스크래퍼의 URL을 반환합니다."""
        return self.value[2]

    def get_scraper_class_name(self) -> str:
        """스크래퍼 클래스 이름을 반환합니다."""
        return self.value[3]

    @classmethod
    def from_str(cls, value: str) -> Optional["ScraperType"]:
        """문자열로부터 ScraperType을 생성합니다.

        Args:
            value (str): ScraperType의 이름 (예: "UNIVERSITY_ACADEMIC")

        Returns:
            Optional[ScraperType]: 해당하는 ScraperType 객체 또는 None
        """
        try:
            return cls[value.upper()]
        except ValueError:
            return None

    @classmethod
    def get_choices(cls) -> list:
        """디스코드 명령어용 선택지 목록을 반환합니다.

        Returns:
            list[app_commands.Choice]: 한글 이름과 enum 이름으로 구성된 선택지 목록
        """
        return [
            app_commands.Choice(name=type.get_korean_name(), value=type.name)
            for type in cls
        ]

    @classmethod
    def get_active_scrapers(cls) -> list:
        """활성화된 스크래퍼 타입들을 반환합니다.

        Returns:
            list[ScraperType]: 현재 활성화된 모든 스크래퍼 타입 목록
        """
        return list(cls)
