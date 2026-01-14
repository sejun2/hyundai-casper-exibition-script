#!/usr/bin/env python3
"""
지역 코드를 사용한 캐스퍼 재고 검색 예시

fetch_regions.py로 수집한 지역 정보를 활용하여
특정 지역의 재고를 검색하는 방법을 보여줍니다.
"""

from casper_checker import CasperChecker, CarModel


def search_by_region_example():
    """지역별 재고 검색 예시"""
    
    checker = CasperChecker()
    
    print("="*70)
    print("🗺️  지역별 캐스퍼 재고 검색")
    print("="*70)
    
    # 예시 1: 경북 포항 지역 검색
    print("\n[예시 1] 경북 포항시 - 2026 캐스퍼 일렉트릭")
    print("-"*70)
    
    params_pohang = {
        "carCode": "AX05",                    # 2026 캐스퍼 일렉트릭
        "subsidyRegion": "2800",              # 보조금 지역
        "exhbNo": "R0003",
        "sortCode": "10",
        "deliveryAreaCode": "N",              # 경북
        "deliveryLocalAreaCode": "NL",        # 포항시
        "carBodyCode": "",
        "carEngineCode": "",
        "carTrimCode": "",
        "exteriorColorCode": "",
        "interiorColorCode": [],
        "deliveryCenterCode": "",
        "wpaScnCd": "",
        "optionFilter": "",
        "minSalePrice": "35877000",
        "maxSalePrice": "37306000",
        "choiceOptYn": "Y",
        "pageNo": 1,
        "pageSize": 18
    }
    
    count = checker.get_car_count(custom_params=params_pohang)
    print(f"경북 포항시 재고: {count}대")
    
    if count > 0:
        cars = checker.get_car_list(custom_params=params_pohang)
        for i, car in enumerate(cars[:3], 1):
            print(f"  {i}. {car['exteriorColorName']} - {int(car['finalAmount']):,}원")
    
    # 예시 2: 서울 지역 검색
    print("\n[예시 2] 서울 - 2026 캐스퍼")
    print("-"*70)
    
    params_seoul = {
        "carCode": "AX06",                    # 2026 캐스퍼
        "subsidyRegion": "",
        "exhbNo": "R0003",
        "sortCode": "10",
        "deliveryAreaCode": "B",              # 서울
        "deliveryLocalAreaCode": "B0",        # 서울특별시 (시군구 구분 없음)
        "carBodyCode": "",
        "carEngineCode": "",
        "carTrimCode": "",
        "exteriorColorCode": "",
        "interiorColorCode": [],
        "deliveryCenterCode": "",
        "wpaScnCd": "",
        "optionFilter": "",
        "minSalePrice": "",
        "maxSalePrice": "",
        "choiceOptYn": "Y",
        "pageNo": 1,
        "pageSize": 18
    }
    
    count = checker.get_car_count(custom_params=params_seoul)
    print(f"서울 재고: {count}대")
    
    # 예시 3: 전북 전체 (시군구 지정 안함)
    print("\n[예시 3] 전북 전체 - 캐스퍼 일렉트릭")
    print("-"*70)
    
    params_jeonbuk = {
        "carCode": "AX03",                    # 캐스퍼 일렉트릭
        "subsidyRegion": "2800",
        "exhbNo": "R0003",
        "sortCode": "10",
        "deliveryAreaCode": "J",              # 전북
        "deliveryLocalAreaCode": "J1",        # 군산시 (예시)
        "carBodyCode": "",
        "carEngineCode": "",
        "carTrimCode": "",
        "exteriorColorCode": "",
        "interiorColorCode": [],
        "deliveryCenterCode": "",
        "wpaScnCd": "",
        "optionFilter": "",
        "minSalePrice": "32060670",
        "maxSalePrice": "32060670",
        "choiceOptYn": "Y",
        "pageNo": 1,
        "pageSize": 18
    }
    
    count = checker.get_car_count(custom_params=params_jeonbuk)
    print(f"전북 군산시 재고: {count}대")


def region_code_mapping():
    """지역 코드 매핑 정보"""
    
    print("\n" + "="*70)
    print("📋 주요 지역 코드 매핑")
    print("="*70)
    
    regions = [
        ("서울", "B", "B0", "서울특별시"),
        ("인천", "D", "D0", "인천광역시"),
        ("경기", "E", "E0", "경기도"),
        ("강원", "F", "F0", "강원특별자치도"),
        ("세종", "W", "W0", "세종특별자치시"),
        ("충남", "I", "I0", "충청남도"),
        ("대전", "H", "H0", "대전광역시"),
        ("충북", "G", "G0", "충청북도"),
        ("대구", "M", "M0", "대구광역시"),
        ("경북", "N", "N0~NL", "경북 21개 시군구"),
        ("부산", "P", "P0", "부산광역시"),
        ("경남", "S", "S0", "경상남도"),
        ("울산", "U", "U0", "울산광역시"),
        ("전북", "J", "J0~J?", "전북특별자치도"),
        ("전남", "L", "L0", "전라남도"),
        ("광주", "K", "K0", "광주광역시"),
        ("제주", "T", "T0", "제주특별자치도"),
    ]
    
    print(f"\n{'지역':<8} {'시도코드':<10} {'시군구코드':<12} {'비고'}")
    print("-"*70)
    for name, sido, sigun, note in regions:
        print(f"{name:<8} {sido:<10} {sigun:<12} {note}")
    
    print("\n💡 시군구 코드는 fetch_regions.py를 실행하여 확인하세요!")


def create_region_search_helper():
    """지역 검색 헬퍼 함수 생성 가이드"""
    
    print("\n" + "="*70)
    print("🛠️  지역 검색 헬퍼 함수 사용법")
    print("="*70)
    
    guide = """
1. fetch_regions.py 실행:
   python fetch_regions.py
   
2. region_constants.py 파일이 생성됨

3. 헬퍼 함수 사용:
   from region_constants import SIDO_CODES, SIGUN_CODES
   
   # 경북 포항 코드 가져오기
   sido_code = SIDO_CODES["경북"]          # "N"
   sigun_code = SIGUN_CODES["경북"]["포항시"]  # "NL"
   
4. casper_checker와 연동:
   checker = CasperChecker()
   
   params = {
       "carCode": "AX05",
       "deliveryAreaCode": sido_code,
       "deliveryLocalAreaCode": sigun_code,
       # ... 기타 파라미터
   }
   
   cars = checker.get_car_list(custom_params=params)
"""
    
    print(guide)


if __name__ == "__main__":
    # 1. 지역별 검색 예시
    search_by_region_example()
    
    # 2. 지역 코드 매핑표
    region_code_mapping()
    
    # 3. 사용 가이드
    create_region_search_helper()
    
    print("\n" + "="*70)
    print("✅ 완료!")
    print("="*70)
    print("\n💡 팁:")
    print("  1. fetch_regions.py를 먼저 실행하여 전체 지역 데이터를 수집하세요")
    print("  2. 생성된 region_constants.py를 import하여 사용하세요")
    print("  3. deliveryAreaCode와 deliveryLocalAreaCode를 정확히 설정하세요")
