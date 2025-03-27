from enum import Enum
from typing import List, Dict
from utils.scraper_type import ScraperType


class ScraperCategory(Enum):
    """스크래퍼 카테고리를 정의하는 열거형 클래스"""

    UNIVERSITY_CATEGORY = (
        "국민대",
        [
            ScraperType.UNIVERSITY_ACADEMIC,
            ScraperType.UNIVERSITY_SCHOLARSHIP,
            ScraperType.UNIVERSITY_SPECIALLECTURE,
            ScraperType.UNIVERSITY_CONTESTEVENT,
        ],
    )

    COMPUTERSCIENCE_CATEGORY = (
        "소프트웨어융합대학",
        [
            ScraperType.COMPUTERSCIENCE_ACADEMIC_RSS,
            ScraperType.SOFTWARECENTERED_ACADEMIC,
        ],
    )

    BUSINESSADMINISTRATION_CATEGORY = (
        "경영대학",
        [
            ScraperType.BUSINESSADMINISTRATION_ACADEMIC_RSS,
        ],
    )

    ARCHITECTURE_CATEGORY = (
        "건축대학",
        [
            ScraperType.ARCHITECTURE_ACADEMIC,
        ],
    )

    SOCIALSCIENCE_CATEGORY = (
        "사회과학대학",
        [
            ScraperType.SOCIALSCIENCE_ACADEMIC,
            ScraperType.SOCIALSCIENCE_PUBLICADMINISTRATION_ACADEMIC,
            ScraperType.SOCIALSCIENCE_EDUCATION_ACADEMIC,
            ScraperType.SOCIALSCIENCE_POLITICALSCIENCE_ACADEMIC,
            ScraperType.SOCIALSCIENCE_SOCIOLOGY_ACADEMIC,
            ScraperType.SOCIALSCIENCE_COMMUNICATION_MEDIA_ACADEMIC,
            ScraperType.SOCIALSCIENCE_COMMUNICATION_ADVERTISING_ACADEMIC,
        ],
    )

    CREATIVEENGINEERING_CATEGORY = (
        "창의공과대학",
        [
            ScraperType.CREATIVEENGINEERING_ACADEMIC_RSS,
            ScraperType.CREATIVEENGINEERING_MECHANICAL_ACADEMIC,
            ScraperType.CREATIVEENGINEERING_ELECTRICAL_ACADEMIC_RSS,
            ScraperType.CREATIVEENGINEERING_ADVANCEDMATERIALS_ACADEMIC,
            ScraperType.CREATIVEENGINEERING_CIVIL_ACADEMIC,
        ],
    )

    DESIGN_CATEGORY = (
        "조형대학",
        [
            ScraperType.DESIGN_INDUSTRIAL_ACADEMIC,
            ScraperType.DESIGN_VISUAL_ACADEMIC,
            ScraperType.DESIGN_METALWORK_ACADEMIC,
            ScraperType.DESIGN_AUTOMOTIVE_ACADEMIC,
            ScraperType.DESIGN_CERAMICS_ACADEMIC,
        ],
    )

    OTHERS_CATEGORY = (
        "사업단 및 부속기관",
        [
            ScraperType.LINC_ACADEMIC,
            ScraperType.DORMITORY_GENERAL_RSS,
            ScraperType.NCCOSS_GENERAL,
        ],
    )

    AUTOMOTIVEENGINEERING_CATEGORY = (
        "자동차융합대학",
        [
            ScraperType.AUTOMATIVEENGINEERING_ACADEMIC,
            ScraperType.COSS_ACADEMIC,
            ScraperType.FUTUREMOBILITY_ACADEMIC,
        ],
    )

    LAW_CATEGORY = (
        "법과대학",
        [
            ScraperType.LAW_ACADEMIC,
        ],
    )

    SCIENCETECHNOLOGY_CATEGORY = (
        "과학기술대학",
        [
            ScraperType.SCIENCETECHNOLOGY_CHEMISTRY_ACADEMIC,
            ScraperType.SCIENCETECHNOLOGY_SECURITY_ACADEMIC,
        ],
    )

    ECONOMICCOMMERCE_CATEGORY = (
        "경상대학",
        [
            ScraperType.ECONOMICCOMMERCE_ACADEMIC_RSS,
        ],
    )

    CULTURE_CATEGORY = (
        "교양대학",
        [
            ScraperType.CULTURE_ACADEMIC_RSS,
        ],
    )

    TEACHING_CATEGORY = (
        "교직과정부",
        [
            ScraperType.TEACHING_ACADEMIC_RSS,
        ],
    )

    ARTS_CATEGORY = (
        "예술대학",
        [
            ScraperType.ARTS_ACADEMIC,
        ],
    )

    PHYSICALEDUCATION_CATEGORY = (
        "체육대학",
        [
            ScraperType.PHYSICALEDUCATION_ACADEMIC,
        ],
    )

    GLOBALHUMANITIES_CATEGORY = (
        "글로벌인문지역대학",
        [
            ScraperType.GLOBALHUMANITIES_ACADEMIC_RSS,
            ScraperType.GLOBALHUMANITIES_KOREAN_ACADEMIC_RSS,
            ScraperType.GLOBALHUMANITIES_KOREANHISTORY_ACADEMIC_RSS,
            ScraperType.GLOBALHUMANITIES_ENGLISH_ACADEMIC_RSS,
            ScraperType.GLOBALHUMANITIES_CHINESE_ACADEMIC_RSS,
            ScraperType.GLOBALHUMANITIES_EURASIAN_ACADEMIC,
        ],
    )

    YOUTUBE_CATEGORY = (
        "유튜브",
        [
            ScraperType.JO_CODING_YOUTUBE,
        ],
    )

    def __init__(self, korean_name: str, scraper_types: List[ScraperType]):
        self.korean_name = korean_name
        self.scraper_types = scraper_types

    @classmethod
    def get_category_choices(cls) -> List[Dict]:
        """디스코드 명령어용 카테고리 선택지 목록을 반환합니다."""
        return [
            {"name": category.korean_name, "value": category.name} for category in cls
        ]

    @classmethod
    def get_scraper_choices(cls, category_name: str) -> List[Dict]:
        """특정 카테고리의 스크래퍼 선택지 목록을 반환합니다."""
        try:
            category = cls[category_name]
            return [
                {"name": scraper_type.get_korean_name(), "value": scraper_type.name}
                for scraper_type in category.scraper_types
            ]
        except KeyError:
            return []

    @classmethod
    def get_all_scrapers(cls) -> List[ScraperType]:
        """모든 스크래퍼 타입을 반환합니다."""
        all_scrapers = []
        for category in cls:
            all_scrapers.extend(category.scraper_types)
        return all_scrapers

    @classmethod
    def find_category_by_scraper(cls, scraper_type: ScraperType) -> "ScraperCategory":
        """스크래퍼 타입이 속한 카테고리를 반환합니다."""
        for category in cls:
            if scraper_type in category.scraper_types:
                return category
        return None
