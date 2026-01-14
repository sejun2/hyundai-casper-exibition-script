#!/usr/bin/env python3
"""
캐스퍼 재고 확인 CLI 도구

간단한 명령줄 인터페이스로 빠르게 재고를 확인할 수 있습니다.
"""

import sys
import argparse
from casper_checker import CasperChecker, CarModel


def main():
    parser = argparse.ArgumentParser(
        description='현대 캐스퍼 재고 확인 도구',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  %(prog)s                          # 전체 모델 재고 확인
  %(prog)s --model AX05             # 2026 캐스퍼 일렉트릭만
  %(prog)s --all                    # 모든 모델 상세 정보
  %(prog)s --color SAW              # 아틀라스 화이트만
  %(prog)s --model AX05 --detail    # 상세 정보 포함

모델 코드:
  AX05: 2026 캐스퍼 일렉트릭
  AX06: 2026 캐스퍼
  AX03: 캐스퍼 일렉트릭
  AX04: 더 뉴 캐스퍼
"""
    )
    
    parser.add_argument(
        '--model', '-m',
        choices=['AX05', 'AX06', 'AX03', 'AX04'],
        help='특정 모델만 조회'
    )
    
    parser.add_argument(
        '--all', '-a',
        action='store_true',
        help='모든 모델의 상세 정보 표시'
    )
    
    parser.add_argument(
        '--detail', '-d',
        action='store_true',
        help='차량 상세 정보 표시'
    )
    
    parser.add_argument(
        '--color', '-c',
        help='외장 색상 코드로 필터링 (예: SAW)'
    )
    
    parser.add_argument(
        '--center',
        help='출고센터 코드로 필터링 (예: Z11)'
    )
    
    parser.add_argument(
        '--count', '-n',
        action='store_true',
        help='재고 개수만 표시'
    )
    
    args = parser.parse_args()
    
    checker = CasperChecker()
    
    # 모델 매핑
    model_map = {
        'AX05': CarModel.CASPER_ELECTRIC_2026,
        'AX06': CarModel.CASPER_2026,
        'AX03': CarModel.CASPER_ELECTRIC,
        'AX04': CarModel.CASPER_NEW
    }
    
    # 커스텀 파라미터 생성
    custom_params = None
    if args.color or args.center:
        model_code = args.model if args.model else "AX05"
        model = model_map[model_code]
        model_data = model.value
        
        custom_params = {
            "carCode": model_data["carCode"],
            "subsidyRegion": model_data["subsidyRegion"],
            "exhbNo": "R0003",
            "sortCode": "10",
            "deliveryAreaCode": "J",
            "deliveryLocalAreaCode": "J1",
            "carBodyCode": "",
            "carEngineCode": "",
            "carTrimCode": "",
            "exteriorColorCode": args.color if args.color else "",
            "interiorColorCode": [],
            "deliveryCenterCode": args.center if args.center else "",
            "wpaScnCd": "",
            "optionFilter": "",
            "minSalePrice": model_data["minSalePrice"],
            "maxSalePrice": model_data["maxSalePrice"],
            "choiceOptYn": "Y",
            "pageNo": 1,
            "pageSize": 18
        }
    
    # 실행
    if args.all:
        # 모든 모델 상세 정보
        print("="*70)
        print("🚗 전체 캐스퍼 모델 재고 현황")
        print("="*70)
        
        for model in CarModel:
            count = checker.get_car_count(model)
            print(f"\n[{model.value['name']}] - {count}대")
            
            if count > 0 and args.detail:
                cars = checker.get_car_list(model)
                for car in cars[:3]:
                    print(f"  • {car['exteriorColorName']} | {int(car['finalAmount']):,}원")
    
    elif args.model:
        # 특정 모델 조회
        model = model_map[args.model]
        
        if custom_params:
            count = checker.get_car_count(custom_params=custom_params)
            cars = checker.get_car_list(custom_params=custom_params)
        else:
            count = checker.get_car_count(model)
            cars = checker.get_car_list(model)
        
        if args.count:
            print(count)
        else:
            print(f"[{model.value['name']}] - {count}대")
            
            if count > 0 and args.detail:
                for car in cars:
                    checker.print_car_info(car)
            elif count > 0:
                for i, car in enumerate(cars, 1):
                    print(f"{i}. {car['exteriorColorName']} | {int(car['finalAmount']):,}원 | {car['deliveryCenterName']}")
    
    else:
        # 기본: 전체 모델 요약
        results = checker.check_all_models()
        
        print("="*70)
        print("📊 캐스퍼 재고 현황")
        print("="*70)
        
        for model_name, info in results.items():
            status = "✅" if info["available"] else "❌"
            print(f"{status} {model_name:<25} | {info['count']:>3}대")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n중단됨")
        sys.exit(0)
    except Exception as e:
        print(f"오류 발생: {e}", file=sys.stderr)
        sys.exit(1)
