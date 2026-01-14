#!/usr/bin/env python3
"""
지역별 캐스퍼 재고 검색 CLI

간단하게 지역명으로 재고를 검색할 수 있습니다.
"""

import sys
from casper_checker import CasperChecker, CarModel
from region_helper import RegionHelper


def main():
    helper = RegionHelper()
    checker = CasperChecker()
    
    if not helper.is_available():
        print("❌ 지역 데이터가 없습니다.")
        print("먼저 다음 명령을 실행하세요: python fetch_regions.py")
        sys.exit(1)
    
    print("="*70)
    print("🗺️  지역별 캐스퍼 재고 검색")
    print("="*70)
    
    # 1. 시도 선택
    print("\n[1단계] 시도 선택")
    print("-"*70)
    sidos = helper.list_sidos()
    for i, sido in enumerate(sidos, 1):
        print(f"{i:2}. {sido}")
    
    try:
        choice = input("\n시도 번호 선택 (1-17): ").strip()
        sido_idx = int(choice) - 1
        
        if sido_idx < 0 or sido_idx >= len(sidos):
            print("잘못된 선택입니다.")
            sys.exit(1)
        
        sido_name = sidos[sido_idx]
        
    except (ValueError, KeyboardInterrupt):
        print("\n중단됨")
        sys.exit(0)
    
    # 2. 시군구 선택 (있는 경우)
    sigun_name = None
    siguns = helper.list_siguns(sido_name)
    
    if len(siguns) > 1:
        print(f"\n[2단계] {sido_name} 시군구 선택")
        print("-"*70)
        print("0. 전체")
        for i, sigun in enumerate(siguns, 1):
            print(f"{i:2}. {sigun}")
        
        try:
            choice = input(f"\n시군구 번호 선택 (0-{len(siguns)}): ").strip()
            sigun_idx = int(choice)
            
            if sigun_idx < 0 or sigun_idx > len(siguns):
                print("잘못된 선택입니다.")
                sys.exit(1)
            
            if sigun_idx > 0:
                sigun_name = siguns[sigun_idx - 1]
        
        except (ValueError, KeyboardInterrupt):
            print("\n중단됨")
            sys.exit(0)
    
    # 3. 모델 선택
    print("\n[3단계] 모델 선택")
    print("-"*70)
    models = list(CarModel)
    for i, model in enumerate(models, 1):
        print(f"{i}. {model.value['name']}")
    
    try:
        choice = input("\n모델 번호 선택 (1-4): ").strip()
        model_idx = int(choice) - 1
        
        if model_idx < 0 or model_idx >= len(models):
            print("잘못된 선택입니다.")
            sys.exit(1)
        
        selected_model = models[model_idx]
        
    except (ValueError, KeyboardInterrupt):
        print("\n중단됨")
        sys.exit(0)
    
    # 4. 검색 실행
    print("\n" + "="*70)
    print("🔍 검색 중...")
    print("="*70)
    
    location = f"{sido_name} {sigun_name}" if sigun_name else sido_name
    print(f"\n지역: {location}")
    print(f"모델: {selected_model.value['name']}")
    print("-"*70)
    
    try:
        cars = checker.search_by_region(selected_model, sido_name, sigun_name)
        count = len(cars)
        
        print(f"\n📊 검색 결과: {count}대\n")
        
        if count > 0:
            for i, car in enumerate(cars, 1):
                print(f"[{i}]")
                print(f"  색상: {car['exteriorColorName']} / {car['interiorColorName']}")
                print(f"  가격: {int(float(car['finalAmount'])):,}원 (할인 {int(float(car['discountPrice'])):,}원)")
                print(f"  트림: {car['carTrimName']}")
                print(f"  출고: {car['deliveryCenterName']}")
                print()
        else:
            print("현재 해당 지역에 재고가 없습니다.")
    
    except Exception as e:
        print(f"❌ 검색 실패: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n중단됨")
        sys.exit(0)
