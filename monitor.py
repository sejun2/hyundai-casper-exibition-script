#!/usr/bin/env python3
"""
캐스퍼 재고 간단 모니터링 스크립트

주기적으로 재고를 확인하고 재고가 있으면 알림을 줍니다.
"""

import time
from casper_checker import CasperChecker, CarModel
from typing import Optional, Dict, List


def monitor_stock(
    interval: int = 60, 
    models: Optional[List[CarModel]] = None,
    custom_params: dict = None
):
    """
    재고를 주기적으로 모니터링합니다.
    
    Args:
        interval: 확인 주기 (초 단위, 기본 60초)
        models: 모니터링할 모델 리스트 (None이면 전체)
        custom_params: 커스텀 파라미터
    """
    checker = CasperChecker()
    
    if models is None:
        models = list(CarModel)
        print(f"🔍 전체 캐스퍼 모델 재고 모니터링 시작")
    else:
        model_names = [m.value['name'] for m in models]
        print(f"🔍 캐스퍼 재고 모니터링 시작")
        print(f"대상 모델: {', '.join(model_names)}")
    
    print(f"확인 주기: {interval}초")
    print("중단하려면 Ctrl+C를 누르세요\n")
    
    last_counts = {model: 0 for model in models}
    check_count = 0
    
    try:
        while True:
            check_count += 1
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"\n{'='*70}")
            print(f"[확인 #{check_count}] {current_time}")
            print(f"{'='*70}")
            
            for model in models:
                if custom_params:
                    count = checker.get_car_count(custom_params=custom_params)
                else:
                    count = checker.get_car_count(model)
                
                model_name = model.value['name']
                status = "✅" if count > 0 else "❌"
                
                print(f"{status} {model_name:<25} | 재고: {count:>3}대", end="")
                
                # 재고 변동 감지
                last_count = last_counts[model]
                if count != last_count:
                    if count > last_count:
                        print(f" 🎉 +{count - last_count}대 증가!")
                        
                        # 새로 들어온 차량 정보 간단히 출력
                        cars = checker.get_car_list(model) if not custom_params else checker.get_car_list(custom_params=custom_params)
                        if cars:
                            print(f"  └─ 새 차량:")
                            for i, car in enumerate(cars[:3], 1):
                                print(f"     {i}. {car['exteriorColorName']} - {int(car['finalAmount']):,}원")
                    elif count < last_count:
                        print(f" 📉 -{last_count - count}대 감소")
                    
                    last_counts[model] = count
                else:
                    print()
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n\n✋ 모니터링을 종료합니다.")
        print(f"총 {check_count}번 확인했습니다.")


def monitor_specific_model(model: CarModel, interval: int = 60):
    """
    특정 모델만 모니터링합니다.
    
    Args:
        model: 모니터링할 CarModel
        interval: 확인 주기 (초)
    """
    monitor_stock(interval=interval, models=[model])


if __name__ == "__main__":
    # 사용 예시 선택
    print("캐스퍼 재고 모니터링")
    print("="*70)
    print("1. 전체 모델 모니터링")
    print("2. 2026 캐스퍼 일렉트릭만")
    print("3. 2026 캐스퍼만")
    print("4. 캐스퍼 일렉트릭만")
    print("5. 더 뉴 캐스퍼만")
    print("6. 전기차 모델만 (2026 일렉트릭 + 일렉트릭)")
    
    try:
        choice = input("\n선택 (1-6, Enter=전체): ").strip()
        
        if choice == "2":
            monitor_specific_model(CarModel.CASPER_ELECTRIC_2026)
        elif choice == "3":
            monitor_specific_model(CarModel.CASPER_2026)
        elif choice == "4":
            monitor_specific_model(CarModel.CASPER_ELECTRIC)
        elif choice == "5":
            monitor_specific_model(CarModel.CASPER_NEW)
        elif choice == "6":
            monitor_stock(
                models=[CarModel.CASPER_ELECTRIC_2026, CarModel.CASPER_ELECTRIC]
            )
        else:
            # 기본: 전체 모델
            monitor_stock(interval=60)
            
    except KeyboardInterrupt:
        print("\n종료합니다.")
