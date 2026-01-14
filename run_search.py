#!/usr/bin/env python3
"""
캐스퍼 전국 재고 검색 - 올인원

한 번 실행으로 전국 모든 지역의 재고를 확인합니다.
"""

import time
from datetime import datetime
from casper_checker import CasperChecker, CarModel
from region_helper import RegionHelper
from typing import Dict, List


def check_all_regions(model: CarModel) -> Dict[str, List]:
    """
    전국 모든 지역의 재고를 검색합니다.
    
    Args:
        model: 검색할 차량 모델
    
    Returns:
        지역별 재고 딕셔너리
    """
    helper = RegionHelper()
    checker = CasperChecker()
    
    if not helper.is_available():
        print("❌ 지역 데이터가 없습니다.")
        print("먼저 실행: python fetch_regions.py")
        return {}
    
    results = {}
    total_cars = 0
    
    print(f"\n🔍 전국 재고 검색 중... (모델: {model.value['name']})")
    print("="*80)
    
    sidos = helper.list_sidos()
    
    for i, sido in enumerate(sidos, 1):
        print(f"\n[{i:2d}/17] {sido} ", end="")
        print("-"*70)
        
        # 시군구가 있는 경우 각각 검색
        siguns = helper.list_siguns(sido)
        
        sido_total = 0
        sido_results = {}
        
        if len(siguns) > 1:
            # 시군구별로 검색
            for sigun in siguns:
                try:
                    cars = checker.search_by_region(model, sido, sigun)
                    if cars:
                        sido_results[sigun] = cars
                        sido_total += len(cars)
                        print(f"  ✅ {sigun:<20} {len(cars):>3}대")
                except Exception as e:
                    pass
                time.sleep(0.1)  # API 부담 줄이기
            
            if sido_total == 0:
                print(f"  ❌ 재고 없음")
        else:
            # 시도 전체 검색
            try:
                cars = checker.search_by_region(model, sido)
                if cars:
                    sido_results[sido] = cars
                    sido_total = len(cars)
                    print(f"  ✅ {sido:<20} {sido_total:>3}대")
                else:
                    print(f"  ❌ 재고 없음")
            except Exception as e:
                print(f"  ❌ 오류")
        
        results[sido] = sido_results
        total_cars += sido_total
        
        if sido_total > 0:
            print(f"  {'─'*70}")
            print(f"  📍 {sido} 합계: {sido_total}대")
        
        time.sleep(0.2)  # 요청 간 지연
    
    print("\n" + "="*80)
    print(f"✅ 검색 완료! 전국 총 재고: {total_cars}대\n")
    
    return results


def print_summary(results: Dict[str, Dict[str, List]], model: CarModel):
    """검색 결과 요약 출력"""
    if not results:
        print("검색 결과가 없습니다.")
        return
    
    print("\n" + "="*80)
    print(f"📊 전국 재고 요약 - {model.value['name']}")
    print("="*80)
    
    # 재고가 있는 지역만 추출
    regions_with_stock = []
    for sido, sigun_dict in results.items():
        if sigun_dict:
            for sigun, cars in sigun_dict.items():
                if cars:
                    regions_with_stock.append((sido, sigun, cars))
    
    if not regions_with_stock:
        print("\n❌ 전국에 재고가 없습니다.")
        return
    
    # 재고 많은 순으로 정렬
    regions_with_stock.sort(key=lambda x: len(x[2]), reverse=True)
    
    print(f"\n{'시도':<8} {'시군구':<20} {'재고':<8} {'최저가':<15} {'최고가':<15}")
    print("-"*80)
    
    sido_totals = {}
    
    for sido, sigun, cars in regions_with_stock:
        count = len(cars)
        min_price = min(int(float(car['finalAmount'])) for car in cars)
        max_price = max(int(float(car['finalAmount'])) for car in cars)
        
        print(f"{sido:<8} {sigun:<20} {count:<8} {min_price:>12,}원 {max_price:>12,}원")
        
        # 시도별 합계 계산
        if sido not in sido_totals:
            sido_totals[sido] = 0
        sido_totals[sido] += count
    
    # 시도별 합계
    print("-"*80)
    print("\n📍 시도별 합계:")
    print("-"*80)
    for sido, total in sorted(sido_totals.items(), key=lambda x: x[1], reverse=True):
        if total > 0:
            print(f"  {sido:<10} {total:>3}대")
    
    total = sum(sido_totals.values())
    print("-"*80)
    print(f"  {'전국 합계':<10} {total:>3}대")
    print("="*80)


def print_detail(results: Dict[str, Dict[str, List]], max_per_region: int = 3):
    """상세 정보 출력"""
    print("\n" + "="*80)
    print(f"📋 지역별 상세 정보 (각 시군구 최대 {max_per_region}대)")
    print("="*80)
    
    for sido, sigun_dict in results.items():
        if not sigun_dict:
            continue
        
        sido_total = sum(len(cars) for cars in sigun_dict.values())
        if sido_total == 0:
            continue
        
        print(f"\n{'='*80}")
        print(f"📍 {sido} - 총 {sido_total}대")
        print(f"{'='*80}")
        
        for sigun, cars in sigun_dict.items():
            if not cars:
                continue
            
            print(f"\n  [{sigun}] - {len(cars)}대")
            print("  " + "-"*76)
            
            for i, car in enumerate(cars[:max_per_region], 1):
                print(f"  {i}. {car['exteriorColorName']:<15} | "
                      f"{car['carTrimName']:<12} | "
                      f"{int(float(car['finalAmount'])):>12,}원 | "
                      f"할인 {int(float(car['discountPrice'])):>10,}원")
                print(f"     출고: {car['deliveryCenterName']}")
            
            if len(cars) > max_per_region:
                print(f"     ... 외 {len(cars) - max_per_region}대")


def save_results(results: Dict[str, Dict[str, List]], model: CarModel, filename: str = None):
    """결과를 JSON 파일로 저장"""
    import json
    
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"casper_stock_{model.value['carCode']}_{timestamp}.json"
    
    # 총 재고 계산
    total_count = 0
    for sigun_dict in results.values():
        for cars in sigun_dict.values():
            total_count += len(cars)
    
    data = {
        "timestamp": datetime.now().isoformat(),
        "model": model.value['name'],
        "model_code": model.value['carCode'],
        "total_count": total_count,
        "regions": {}
    }
    
    # 시도별로 데이터 구성
    for sido, sigun_dict in results.items():
        if not sigun_dict:
            continue
        
        data["regions"][sido] = {}
        
        for sigun, cars in sigun_dict.items():
            if not cars:
                continue
            
            data["regions"][sido][sigun] = [
                {
                    "color": car['exteriorColorName'],
                    "interior": car['interiorColorName'],
                    "trim": car['carTrimName'],
                    "price": car['finalAmount'],
                    "discount": car['discountPrice'],
                    "discount_rate": car['discountRate'],
                    "center": car['deliveryCenterName'],
                    "production_date": car.get('prdnDt', ''),
                }
                for car in cars
            ]
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 결과 저장: {filename}")


def monitor_mode(model: CarModel, interval: int = 300):
    """
    주기적으로 전국 재고를 모니터링합니다.
    
    Args:
        model: 모니터링할 모델
        interval: 확인 주기 (초 단위, 기본 300초 = 5분)
    """
    print("="*80)
    print(f"🔄 전국 재고 모니터링 시작")
    print(f"모델: {model.value['name']}")
    print(f"주기: {interval}초 ({interval//60}분)")
    print("="*80)
    print("\n중단하려면 Ctrl+C를 누르세요\n")
    
    last_total = 0
    check_count = 0
    
    try:
        while True:
            check_count += 1
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"\n{'='*80}")
            print(f"[확인 #{check_count}] {current_time}")
            print(f"{'='*80}")
            
            # 전국 검색
            results = check_all_regions(model)
            
            # 총 재고 계산
            total = 0
            for sigun_dict in results.values():
                for cars in sigun_dict.values():
                    total += len(cars)
            
            # 변동 감지
            if check_count > 1:
                if total > last_total:
                    print(f"\n🎉 재고 증가! {last_total}대 → {total}대 (+{total - last_total})")
                elif total < last_total:
                    print(f"\n📉 재고 감소! {last_total}대 → {total}대 (-{last_total - total})")
                else:
                    print(f"\n📊 재고 변동 없음 ({total}대)")
            
            last_total = total
            
            # 요약 출력
            print_summary(results, model)
            
            # 결과 저장
            save_results(results, model)
            
            # 다음 확인까지 대기
            print(f"\n⏳ {interval}초 후 다시 확인합니다...")
            time.sleep(interval)
    
    except KeyboardInterrupt:
        print("\n\n✋ 모니터링을 종료합니다.")
        print(f"총 {check_count}번 확인했습니다.")


def main():
    """메인 실행 함수"""
    print("="*70)
    print("🚗 캐스퍼 전국 재고 검색")
    print("="*70)
    
    # 모델 선택
    print("\n모델을 선택하세요:")
    models = list(CarModel)
    for i, model in enumerate(models, 1):
        print(f"{i}. {model.value['name']}")
    print("5. 모든 모델 (전체 검색)")
    
    try:
        choice = input("\n모델 번호 (1-5): ").strip()
        
        if choice == "5":
            # 모든 모델 검색
            search_all_models = True
            selected_models = models
        else:
            model_idx = int(choice) - 1
            
            if model_idx < 0 or model_idx >= len(models):
                print("잘못된 선택입니다.")
                return
            
            search_all_models = False
            selected_models = [models[model_idx]]
    
    except (ValueError, KeyboardInterrupt):
        print("\n중단됨")
        return
    
    # 모드 선택
    print("\n실행 모드를 선택하세요:")
    print("1. 한 번만 검색 (기본)")
    print("2. 주기적 모니터링 (5분마다)")
    print("3. 주기적 모니터링 (10분마다)")
    print("4. 주기적 모니터링 (30분마다)")
    
    try:
        mode = input("\n모드 번호 (1-4, Enter=1): ").strip() or "1"
    except KeyboardInterrupt:
        print("\n중단됨")
        return
    
    if mode == "1":
        # 한 번만 검색
        if search_all_models:
            # 모든 모델 검색
            print("\n" + "="*70)
            print("🔍 모든 모델 전국 재고 검색")
            print("="*70)
            
            all_results = {}
            for model in selected_models:
                print(f"\n{'='*70}")
                print(f"모델: {model.value['name']}")
                print(f"{'='*70}")
                
                results = check_all_regions(model)
                all_results[model.value['name']] = results
                print_summary(results, model)
                
                # 모델 간 약간의 지연
                if model != selected_models[-1]:
                    time.sleep(1)
            
            # 전체 요약
            print("\n" + "="*80)
            print("📊 전체 모델 재고 요약")
            print("="*80)
            
            for model_name, results in all_results.items():
                # 총 재고 계산
                total = 0
                regions_count = 0
                for sigun_dict in results.values():
                    if sigun_dict:
                        regions_count += len([s for s in sigun_dict.values() if s])
                        for cars in sigun_dict.values():
                            total += len(cars)
                
                print(f"\n{model_name}")
                print(f"  전국 재고: {total}대")
                print(f"  재고 있는 시군구: {regions_count}개")
            
            # 상세 정보 보기
            detail = input("\n각 모델의 상세 정보를 보시겠습니까? (y/n): ").strip().lower()
            if detail == 'y':
                for model_name, results in all_results.items():
                    print(f"\n{'='*70}")
                    print(f"{model_name} 상세")
                    print(f"{'='*70}")
                    print_detail(results, max_per_region=2)
            
            # 저장
            save = input("\n결과를 저장하시겠습니까? (y/n): ").strip().lower()
            if save == 'y':
                for i, (model_name, results) in enumerate(all_results.items()):
                    model = selected_models[i]
                    save_results(results, model)
        else:
            # 단일 모델 검색
            results = check_all_regions(selected_models[0])
            print_summary(results, selected_models[0])
            
            # 상세 정보 보기
            detail = input("\n상세 정보를 보시겠습니까? (y/n): ").strip().lower()
            if detail == 'y':
                print_detail(results)
            
            # 저장
            save = input("\n결과를 저장하시겠습니까? (y/n): ").strip().lower()
            if save == 'y':
                save_results(results, selected_models[0])
    
    elif mode in ["2", "3", "4"]:
        if search_all_models:
            print("\n⚠️  모니터링 모드는 단일 모델만 지원합니다.")
            print("모델을 하나 선택해주세요:")
            for i, model in enumerate(models, 1):
                print(f"{i}. {model.value['name']}")
            
            try:
                choice = input("\n모델 번호 (1-4): ").strip()
                model_idx = int(choice) - 1
                
                if model_idx < 0 or model_idx >= len(models):
                    print("잘못된 선택입니다.")
                    return
                
                selected_model = models[model_idx]
            except (ValueError, KeyboardInterrupt):
                print("\n중단됨")
                return
        else:
            selected_model = selected_models[0]
        
        # 모니터링 시작
        intervals = {"2": 300, "3": 600, "4": 1800}
        monitor_mode(selected_model, interval=intervals[mode])
    else:
        print("잘못된 선택입니다.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n중단됨")
    except Exception as e:
        print(f"\n오류 발생: {e}")
        import traceback
        traceback.print_exc()
