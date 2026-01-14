#!/usr/bin/env python3
"""
캐스퍼 재고 확인 고급 예제

다양한 필터링 및 검색 조건 사용 예시
"""

from casper_checker import CasperChecker, CarModel


def example_1_all_models():
    """예제 1: 모든 모델 한번에 확인"""
    print("\n" + "="*60)
    print("예제 1: 모든 모델 재고 한번에 확인")
    print("="*60)
    
    checker = CasperChecker()
    results = checker.check_all_models()
    
    print("\n전체 모델 재고 현황:")
    for model_name, info in results.items():
        status = "✅" if info["available"] else "❌"
        print(f"{status} {model_name:<25} | {info['count']:>3}대")


def example_2_specific_model():
    """예제 2: 특정 모델만 조회"""
    print("\n" + "="*60)
    print("예제 2: 2026 캐스퍼 일렉트릭만 조회")
    print("="*60)
    
    checker = CasperChecker()
    
    # 2026 캐스퍼 일렉트릭
    count = checker.get_car_count(CarModel.CASPER_ELECTRIC_2026)
    print(f"\n2026 캐스퍼 일렉트릭 재고: {count}대")
    
    if count > 0:
        cars = checker.get_car_list(CarModel.CASPER_ELECTRIC_2026)
        for i, car in enumerate(cars[:3], 1):
            print(f"\n[{i}]")
            print(f"  트림: {car['carTrimName']}")
            print(f"  색상: {car['exteriorColorName']}")
            print(f"  가격: {int(car['finalAmount']):,}원")


def example_3_compare_models():
    """예제 3: 모델별 비교"""
    print("\n" + "="*60)
    print("예제 3: 전기차 vs 일반 모델 비교")
    print("="*60)
    
    checker = CasperChecker()
    
    electric_models = [CarModel.CASPER_ELECTRIC_2026, CarModel.CASPER_ELECTRIC]
    gas_models = [CarModel.CASPER_2026, CarModel.CASPER_NEW]
    
    print("\n⚡ 전기차 모델:")
    for model in electric_models:
        count = checker.get_car_count(model)
        print(f"  {model.value['name']}: {count}대")
    
    print("\n⛽ 일반 모델:")
    for model in gas_models:
        count = checker.get_car_count(model)
        print(f"  {model.value['name']}: {count}대")


def example_4_color_filter():
    """예제 4: 색상별 필터링"""
    print("\n" + "="*60)
    print("예제 4: 색상별 재고 확인")
    print("="*60)
    
    checker = CasperChecker()
    
    # 커스텀 파라미터로 색상 필터링
    params = {
        "carCode": "AX05",  # 2026 캐스퍼 일렉트릭
        "subsidyRegion": "2800",
        "exhbNo": "R0003",
        "sortCode": "10",
        "deliveryAreaCode": "J",
        "deliveryLocalAreaCode": "J1",
        "carBodyCode": "",
        "carEngineCode": "",
        "carTrimCode": "",
        "exteriorColorCode": "SAW",  # 아틀라스 화이트
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
    
    count = checker.get_car_count(custom_params=params)
    print(f"\n아틀라스 화이트 2026 캐스퍼 일렉트릭: {count}대")


def example_5_price_comparison():
    """예제 5: 모델별 최저가 비교"""
    print("\n" + "="*60)
    print("예제 5: 모델별 최저가 비교")
    print("="*60)
    
    checker = CasperChecker()
    
    print(f"\n{'모델':<25} {'재고':<10} {'최저가':<15}")
    print("-" * 60)
    
    for model in CarModel:
        cars = checker.get_car_list(model)
        if cars:
            min_price = min(int(car['finalAmount']) for car in cars)
            print(f"{model.value['name']:<25} {len(cars):<10} {min_price:>12,}원")
        else:
            print(f"{model.value['name']:<25} {'0':<10} {'재고없음':<15}")


def example_6_best_discount():
    """예제 6: 전체 모델 중 최대 할인 차량"""
    print("\n" + "="*60)
    print("예제 6: 전체 중 최대 할인 차량 찾기")
    print("="*60)
    
    checker = CasperChecker()
    
    all_cars = []
    for model in CarModel:
        cars = checker.get_car_list(model)
        all_cars.extend(cars)
    
    if not all_cars:
        print("\n현재 재고가 없습니다.")
        return
    
    # 할인율 기준 정렬
    all_cars.sort(key=lambda x: float(x['discountRate']), reverse=True)
    
    print("\n🏆 TOP 3 할인 차량:")
    for i, car in enumerate(all_cars[:3], 1):
        print(f"\n[{i}위]")
        print(f"  모델: {car['carName']}")
        print(f"  색상: {car['exteriorColorName']}")
        print(f"  할인: {int(car['discountPrice']):,}원 ({car['discountRate']}%)")
        print(f"  최종: {int(car['finalAmount']):,}원")


def example_7_delivery_center():
    """예제 7: 출고센터별 재고"""
    print("\n" + "="*60)
    print("예제 7: 출고센터별 재고 현황")
    print("="*60)
    
    checker = CasperChecker()
    
    all_cars = []
    for model in CarModel:
        cars = checker.get_car_list(model)
        all_cars.extend(cars)
    
    if not all_cars:
        print("\n현재 재고가 없습니다.")
        return
    
    # 출고센터별 그룹화
    centers = {}
    for car in all_cars:
        center = car['deliveryCenterName']
        if center not in centers:
            centers[center] = []
        centers[center].append(car)
    
    print(f"\n{'출고센터':<15} {'재고':<10}")
    print("-" * 30)
    for center, cars in sorted(centers.items()):
        print(f"{center:<15} {len(cars):<10}")


def main():
    """모든 예제 실행"""
    examples = [
        ("모든 모델 확인", example_1_all_models),
        ("특정 모델 조회", example_2_specific_model),
        ("모델 비교", example_3_compare_models),
        ("색상 필터링", example_4_color_filter),
        ("가격 비교", example_5_price_comparison),
        ("최대 할인 차량", example_6_best_discount),
        ("출고센터별 재고", example_7_delivery_center),
    ]
    
    print("\n" + "="*60)
    print("캐스퍼 재고 확인 고급 예제")
    print("="*60)
    print("\n실행할 예제를 선택하세요:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"{i}. {name}")
    print("0. 모두 실행")
    
    try:
        choice = input("\n선택 (0-7): ").strip()
        
        if choice == "0":
            for _, func in examples:
                func()
                input("\n계속하려면 Enter를 누르세요...")
        elif choice.isdigit() and 1 <= int(choice) <= len(examples):
            examples[int(choice) - 1][1]()
        else:
            print("잘못된 선택입니다.")
    except KeyboardInterrupt:
        print("\n종료합니다.")


if __name__ == "__main__":
    main()
