#!/usr/bin/env python3
"""
지역 검색 빠른 시작 가이드

실제 수집된 167개 시군구 데이터를 활용한 예시입니다.
"""

from region_aware_checker import RegionAwareCasperChecker
from casper_checker import CarModel


def example_basic():
    """기본 사용법"""
    print("\n" + "="*70)
    print("📌 기본 사용법")
    print("="*70)
    
    checker = RegionAwareCasperChecker()
    
    # 지역명으로 간단 검색
    cars = checker.search_by_region(
        CarModel.CASPER_ELECTRIC_2026,
        "경북",
        "포항시"
    )
    
    print(f"\n경북 포항시 - 2026 캐스퍼 일렉트릭: {len(cars)}대")


def example_all_gyeongbuk_cities():
    """경북 모든 시군구 검색"""
    print("\n" + "="*70)
    print("📌 경북 전체 시군구 재고 현황")
    print("="*70)
    
    checker = RegionAwareCasperChecker()
    
    # 경북의 모든 시군구
    siguns = checker.list_available_siguns("경북")
    
    print(f"\n경북 시군구: {len(siguns)}개")
    print(f"목록: {', '.join(siguns)}")
    
    print(f"\n{'시군구':<10} {'재고':<10}")
    print("-"*30)
    
    for sigun in siguns[:10]:  # 처음 10개만
        count = checker.get_region_count(
            CarModel.CASPER_ELECTRIC_2026,
            "경북",
            sigun
        )
        if count > 0:
            print(f"{sigun:<10} {count:<10}")


def example_nationwide():
    """전국 재고 현황"""
    print("\n" + "="*70)
    print("📌 2026 캐스퍼 일렉트릭 - 전국 현황")
    print("="*70)
    
    checker = RegionAwareCasperChecker()
    
    results = checker.search_all_regions_for_model(CarModel.CASPER_ELECTRIC_2026)
    
    print(f"\n재고가 있는 지역: {len(results)}곳")
    print(f"\n{'지역':<10} {'재고':<10}")
    print("-"*30)
    
    for region, count in sorted(results.items(), key=lambda x: x[1], reverse=True):
        print(f"{region:<10} {count:<10}")


def example_color_filter():
    """색상 필터링"""
    print("\n" + "="*70)
    print("📌 특정 색상만 검색")
    print("="*70)
    
    checker = RegionAwareCasperChecker()
    
    # 아틀라스 화이트만
    white_cars = checker.search_by_region(
        CarModel.CASPER_ELECTRIC_2026,
        "경북",
        "포항시",
        exteriorColorCode="SAW"
    )
    
    print(f"\n경북 포항시 - 아틀라스 화이트: {len(white_cars)}대")
    
    if white_cars:
        for car in white_cars:
            print(f"  • {car['carTrimName']} - {int(car['finalAmount']):,}원")


def example_compare_models():
    """같은 지역에서 모델 비교"""
    print("\n" + "="*70)
    print("📌 서울 - 모델별 재고 비교")
    print("="*70)
    
    checker = RegionAwareCasperChecker()
    
    models = [
        (CarModel.CASPER_ELECTRIC_2026, "2026 캐스퍼 일렉트릭"),
        (CarModel.CASPER_2026, "2026 캐스퍼"),
        (CarModel.CASPER_ELECTRIC, "캐스퍼 일렉트릭"),
        (CarModel.CASPER_NEW, "더 뉴 캐스퍼"),
    ]
    
    print(f"\n{'모델':<25} {'재고':<10}")
    print("-"*40)
    
    for model, name in models:
        count = checker.get_region_count(model, "서울")
        print(f"{name:<25} {count:<10}")


def example_major_cities():
    """주요 도시 재고 비교"""
    print("\n" + "="*70)
    print("📌 주요 도시 - 2026 캐스퍼 일렉트릭 재고")
    print("="*70)
    
    checker = RegionAwareCasperChecker()
    
    cities = [
        ("서울", None),
        ("부산", None),
        ("대구", None),
        ("인천", "인천광역시"),
        ("광주", None),
        ("대전", None),
        ("울산", "울산광역시"),
        ("경기", "수원시"),
        ("경기", "성남시"),
        ("경북", "포항시"),
    ]
    
    print(f"\n{'지역':<15} {'재고':<10}")
    print("-"*30)
    
    for sido, sigun in cities:
        display_name = f"{sido} {sigun}" if sigun else sido
        count = checker.get_region_count(
            CarModel.CASPER_ELECTRIC_2026,
            sido,
            sigun
        )
        print(f"{display_name:<15} {count:<10}")


def example_by_province():
    """도별 재고 현황"""
    print("\n" + "="*70)
    print("📌 도별 재고 현황 (2026 캐스퍼 일렉트릭)")
    print("="*70)
    
    checker = RegionAwareCasperChecker()
    
    provinces = [
        "경기", "경북", "경남", "전북", "전남", 
        "충북", "충남", "강원", "제주"
    ]
    
    print(f"\n{'도':<10} {'재고':<10} {'시군구 수':<10}")
    print("-"*40)
    
    for province in provinces:
        count = checker.get_region_count(CarModel.CASPER_ELECTRIC_2026, province)
        siguns = checker.list_available_siguns(province)
        print(f"{province:<10} {count:<10} {len(siguns):<10}")


def interactive_search():
    """대화형 검색"""
    print("\n" + "="*70)
    print("🔍 대화형 지역 검색")
    print("="*70)
    
    checker = RegionAwareCasperChecker()
    
    # 사용 가능한 시도 목록
    available_sidos = list(checker.region_data.keys())
    
    print(f"\n사용 가능한 시도: {', '.join(available_sidos)}")
    
    try:
        sido = input("\n시도를 입력하세요 (예: 경북): ").strip()
        
        if sido not in available_sidos:
            print(f"'{sido}'는 사용할 수 없습니다.")
            return
        
        # 시군구 목록 표시
        siguns = checker.list_available_siguns(sido)
        
        if len(siguns) > 1:
            print(f"\n{sido}의 시군구: {', '.join(siguns)}")
            sigun = input(f"시군구를 입력하세요 (Enter=전체): ").strip()
            sigun = sigun if sigun else None
        else:
            sigun = None
        
        # 모델 선택
        print("\n모델:")
        print("1. 2026 캐스퍼 일렉트릭")
        print("2. 2026 캐스퍼")
        print("3. 캐스퍼 일렉트릭")
        print("4. 더 뉴 캐스퍼")
        
        choice = input("\n선택 (1-4): ").strip()
        
        models = {
            "1": CarModel.CASPER_ELECTRIC_2026,
            "2": CarModel.CASPER_2026,
            "3": CarModel.CASPER_ELECTRIC,
            "4": CarModel.CASPER_NEW
        }
        
        model = models.get(choice, CarModel.CASPER_ELECTRIC_2026)
        
        # 검색
        print("\n검색 중...")
        cars = checker.search_by_region(model, sido, sigun)
        
        print(f"\n결과: {len(cars)}대")
        
        if cars:
            print("\n상위 5대:")
            for i, car in enumerate(cars[:5], 1):
                print(f"{i}. {car['carName']} - {car['exteriorColorName']}")
                print(f"   가격: {int(car['finalAmount']):,}원 (할인 {int(car['discountPrice']):,}원)")
                print(f"   출고: {car['deliveryCenterName']}")
                print()
        
    except KeyboardInterrupt:
        print("\n\n취소됨")


def main():
    """메인 메뉴"""
    examples = [
        ("기본 사용법", example_basic),
        ("경북 전체 시군구", example_all_gyeongbuk_cities),
        ("전국 현황", example_nationwide),
        ("색상 필터링", example_color_filter),
        ("모델 비교", example_compare_models),
        ("주요 도시", example_major_cities),
        ("도별 현황", example_by_province),
        ("대화형 검색", interactive_search),
    ]
    
    print("\n" + "="*70)
    print("🗺️  캐스퍼 지역 검색 예제 모음")
    print("="*70)
    print("\n실행할 예제를 선택하세요:")
    
    for i, (name, _) in enumerate(examples, 1):
        print(f"{i}. {name}")
    print("0. 모두 실행")
    print("q. 종료")
    
    while True:
        try:
            choice = input("\n선택: ").strip()
            
            if choice == 'q':
                break
            elif choice == "0":
                for _, func in examples:
                    func()
                    input("\n계속하려면 Enter를 누르세요...")
                break
            elif choice.isdigit() and 1 <= int(choice) <= len(examples):
                examples[int(choice) - 1][1]()
                input("\n계속하려면 Enter를 누르세요...")
            else:
                print("잘못된 선택입니다.")
                
        except KeyboardInterrupt:
            print("\n\n종료")
            break


if __name__ == "__main__":
    main()
