# -*- coding: utf-8 -*-
"""
현대 캐스퍼 배송지 코드 상수 (예시)

실제로는 fetch_regions.py를 실행하여 생성됩니다.
"""

# 시도 코드
SIDO_CODES = {
    "서울": "B",
    "인천": "D",
    "경기": "E",
    "강원": "F",
    "세종": "W",
    "충남": "I",
    "대전": "H",
    "충북": "G",
    "대구": "M",
    "경북": "N",
    "부산": "P",
    "경남": "S",
    "울산": "U",
    "전북": "J",
    "전남": "L",
    "광주": "K",
    "제주": "T",
}

# 시군구 코드 (경북 예시)
SIGUN_CODES_EXAMPLE = {
    "경북": {
        "경산시": "N0",
        "경주시": "N1",
        "고령군": "N2",
        "구미시": "N3",
        "김천시": "N5",
        "문경시": "N6",
        "봉화군": "N7",
        "상주시": "N8",
        "성주군": "N9",
        "안동시": "NA",
        "영덕군": "NB",
        "영양군": "NC",
        "영주시": "ND",
        "영천시": "NE",
        "예천군": "NF",
        "울진군": "NG",
        "의성군": "NH",
        "청도군": "NI",
        "청송군": "NJ",
        "칠곡군": "NK",
        "포항시": "NL",
    },
    "서울": {
        "서울특별시": "B0",  # 시군구 구분 없음
    },
    # ... 실제로는 전체 지역 데이터가 포함됩니다
}


def get_delivery_codes(sido_name: str, sigun_name: str = None):
    """
    배송지 코드를 반환합니다.
    
    Args:
        sido_name: 시도명 (예: "경북")
        sigun_name: 시군구명 (예: "포항시", 없으면 시도 코드만)
    
    Returns:
        (deliveryAreaCode, deliveryLocalAreaCode) 튜플
    
    Examples:
        >>> get_delivery_codes("경북", "포항시")
        ('N', 'NL')
        
        >>> get_delivery_codes("서울")
        ('B', 'B0')
    """
    sido_code = SIDO_CODES.get(sido_name)
    
    if not sido_code:
        raise ValueError(f"알 수 없는 시도명: {sido_name}")
    
    if sigun_name:
        sigun_codes = SIGUN_CODES_EXAMPLE.get(sido_name, {})
        sigun_code = sigun_codes.get(sigun_name)
        
        if not sigun_code:
            raise ValueError(f"{sido_name}에서 {sigun_name}을(를) 찾을 수 없습니다")
        
        return sido_code, sigun_code
    else:
        # 시군구가 없으면 시도 코드 + "0"
        return sido_code, f"{sido_code}0"


# 사용 예시
if __name__ == "__main__":
    # 예시 1: 경북 포항
    area_code, local_code = get_delivery_codes("경북", "포항시")
    print(f"경북 포항시: deliveryAreaCode={area_code}, deliveryLocalAreaCode={local_code}")
    # 출력: 경북 포항시: deliveryAreaCode=N, deliveryLocalAreaCode=NL
    
    # 예시 2: 서울
    area_code, local_code = get_delivery_codes("서울")
    print(f"서울: deliveryAreaCode={area_code}, deliveryLocalAreaCode={local_code}")
    # 출력: 서울: deliveryAreaCode=B, deliveryLocalAreaCode=B0
