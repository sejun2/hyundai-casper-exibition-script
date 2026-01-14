#!/usr/bin/env python3
"""
지역별 재고 검색 빠른 예제

fetch_regions.py 실행 후 사용 가능합니다.
"""

from casper_checker import CasperChecker, CarModel
from region_helper import RegionHelper


def example_1_basic_region_search():
    """예제 1: 기본 지역 검색"""
    print("\n" + "="*70)
    print("예제 1: 경북 포항시 - 2026 캐스퍼 일렉트릭")
    print("="*70)
    
    checker = CasperChecker()
    
    # 지역명으로 직접 검색
    cars = checker.search_by_region(
        CarModel.CASPER_ELECTRIC_2026,
        "경북",
        "포항시"
    )
    
    print(f"\n검색 결과: {len(cars)}대")
    for i, car in enumerate(cars[:3], 1):
        print(f"{i}. {car['exteriorColorName']} - {int(float(car['finalAmount'])):,}원")


def example_2_search_multiple_regions():
    """예제 2: 여러 지역 비교"""
    print("\n" + "="*70)
    print("예제 2: 여러 지역 재고 비교")
    print("="*70)
    
    checker = CasperChecker()
    regions = [
        ("경북", "포항시"),
        ("경북", "경주시"),
        ("경북", "구미시"),
        ("부산", None),
        ("대구", None),
    ]
    
    print(f"\n모델: 2026 캐스퍼 일렉트릭")
    print("-"*70)
    
    for sido, sigun in regions:
        location = f"{sido} {sigun}" if sigun else sido
        count = checker.get_region_count(
            CarModel.CASPER_ELECTRIC_2026,
            sido,
            sigun
        )
        print(f"{location:<15}: {count:>3}대")


def example_3_all_models_in_region():
    """예제 3: 특정 지역의 모든 모델 재고"""
    print("\n" + "="*70)
    print("예제 3: 서울 - 모든 모델 재고")
    print("="*70)
    
    checker = CasperChecker()
    
    print("\n서울 재고 현황:")
    print("-"*70)
    
    for model in CarModel:
        count = checker.get_region_count(model, "서울")
        status = "✅" if count > 0 else "❌"
        print(f"{status} {model.value['name']:<25}: {count:>3}대")


def example_4_color_filter_by_region():
    """예제 4: 지역 + 색상 필터"""
    print("\n" + "="*70)
    print("예제 4: 경북 - 아틀라스 화이트만 검색")
    print("="*70)
    
    checker = CasperChecker()
    
    # 색상 필터 추가
    cars = checker.search_by_region(
        CarModel.CASPER_ELECTRIC_2026,
        "경북",
        exteriorColorCode="SAW"  # 아틀라스 화이트
    )
    
    print(f"\n아틀라스 화이트 재고: {len(cars)}대")
    for car in cars[:5]:
        print(f"  • {car['carTrimName']} - {int(float(car['finalAmount'])):,}원 - {car['deliveryCenterName']}")


def example_5_region_helper():
    """예제 5: RegionHelper 직접 사용"""
    print("\n" + "="*70)
    print("예제 5: RegionHelper 활용")
    print("="*70)
    
    helper = RegionHelper()
    
    # 1. 모든 시도 출력
    print("\n[전국 시도 목록]")
    for sido in helper.list_sidos():
        print(f"  • {sido}")
    
    # 2. 경북 시군구 출력
    print("\n[경북 시군구]")
    for sigun in helper.list_siguns("경북")[:5]:
        print(f"  • {sigun}")
    print("  ... 등")
    
    # 3. 검색
    print("\n['창원' 검색 결과]")
    results = helper.search_sigun("창원")
    for r in results:
        print(f"  {r['sido']} > {r['sigun']} (코드: {r['sido_code']}-{r['sigun_code']})")


def example_6_region_statistics():
    """예제 6: 지역별 재고 통계"""
    print("\n" + "="*70)
    print("예제 6: 경상권 재고 분석")
    print("="*70)
    
    checker = CasperChecker()
    helper = RegionHelper()
    
    # 경상권 지역
    gyeongsang_regions = ["경북", "경남", "대구", "부산", "울산"]
    
    print(f"\n2026 캐스퍼 일렉트릭 - 경상권 재고:")
    print("-"*70)
    
    total = 0
    for sido in gyeongsang_regions:
        count = checker.get_region_count(
            CarModel.CASPER_ELECTRIC_2026,
            sido
        )
        total += count
        print(f"{sido:<10}: {count:>3}대")
    
    print("-"*70)
    print(f"{'합계':<10}: {total:>3}대")


def main():
    """모든 예제 실행"""
    helper = RegionHelper()
    
    if not helper.is_available():
        print("❌ 지역 데이터가 없습니다.")
        print("\n다음 명령을 먼저 실행하세요:")
        print("  python fetch_regions.py")
        return
    
    print("="*70)
    print("🗺️  지역별 재고 검색 예제")
    print("="*70)
    
    examples = [
        ("기본 지역 검색", example_1_basic_region_search),
        ("여러 지역 비교", example_2_search_multiple_regions),
        ("특정 지역 전체 모델", example_3_all_models_in_region),
        ("지역 + 색상 필터", example_4_color_filter_by_region),
        ("RegionHelper 활용", example_5_region_helper),
        ("지역별 통계", example_6_region_statistics),
    ]
    
    print("\n실행할 예제를 선택하세요:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"{i}. {name}")
    print("0. 모두 실행")
    
    try:
        choice = input("\n선택 (0-6): ").strip()
        
        if choice == "0":
            for _, func in examples:
                func()
                input("\n계속하려면 Enter를 누르세요...")
        elif choice.isdigit() and 1 <= int(choice) <= len(examples):
            examples[int(choice) - 1][1]()
        else:
            print("잘못된 선택입니다.")
    
    except KeyboardInterrupt:
        print("\n\n종료합니다.")


if __name__ == "__main__":
    main()
