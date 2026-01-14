#!/usr/bin/env python3
"""
Hyundai Casper 재고 확인 스크립트
"""

import requests
import json
from typing import Optional, Dict, Any, List
from enum import Enum


class CarModel(Enum):
    """캐스퍼 차량 모델"""
    CASPER_ELECTRIC_2026 = {
        "name": "2026 캐스퍼 일렉트릭",
        "carCode": "AX05",
        "subsidyRegion": "2800",
        "minSalePrice": "35877000",
        "maxSalePrice": "37306000"
    }
    CASPER_2026 = {
        "name": "2026 캐스퍼",
        "carCode": "AX06",
        "subsidyRegion": "",
        "minSalePrice": "",
        "maxSalePrice": ""
    }
    CASPER_ELECTRIC = {
        "name": "캐스퍼 일렉트릭",
        "carCode": "AX03",
        "subsidyRegion": "2800",
        "minSalePrice": "32060670",
        "maxSalePrice": "32060670"
    }
    CASPER_NEW = {
        "name": "더 뉴 캐스퍼",
        "carCode": "AX04",
        "subsidyRegion": "",
        "minSalePrice": "",
        "maxSalePrice": ""
    }


class CasperChecker:
    def __init__(self):
        self.base_url = "https://casper.hyundai.com/gw/wp/product/v2/product/exhibition/cars/R0003"
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "ko,en-US;q=0.9,en;q=0.8,ja;q=0.7",
            "content-type": "application/json;charset=UTF-8",
            "origin": "https://casper.hyundai.com",
            "referer": "https://casper.hyundai.com/vehicles/car-list/promotion?exhbNo=R0003",
            "sec-ch-ua": '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            "ep-channel": "wpc",
            "service-type": "product"
        }
    
    def check_inventory(
        self, 
        model: Optional[CarModel] = None,
        custom_params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        재고를 확인합니다.
        
        Args:
            model: CarModel enum (없으면 2026 캐스퍼 일렉트릭)
            custom_params: 추가 커스텀 파라미터 (딕셔너리)
        
        Returns:
            API 응답 데이터
        """
        # 기본 모델 설정
        if model is None and custom_params is None:
            model = CarModel.CASPER_ELECTRIC_2026
        
        # 기본 파라미터 구성
        if custom_params is None:
            if model:
                model_data = model.value
                params = {
                    "carCode": model_data["carCode"],
                    "subsidyRegion": model_data["subsidyRegion"],
                    "exhbNo": "R0003",
                    "sortCode": "10",
                    "deliveryAreaCode": "J",
                    "deliveryLocalAreaCode": "J1",
                    "carBodyCode": "",
                    "carEngineCode": "",
                    "carTrimCode": "",
                    "exteriorColorCode": "",
                    "interiorColorCode": [],
                    "deliveryCenterCode": "",
                    "wpaScnCd": "",
                    "optionFilter": "",
                    "minSalePrice": model_data["minSalePrice"],
                    "maxSalePrice": model_data["maxSalePrice"],
                    "choiceOptYn": "Y",
                    "pageNo": 1,
                    "pageSize": 18
                }
            else:
                # 완전 기본값 (모든 모델 검색)
                params = {
                    "carCode": "",
                    "subsidyRegion": "",
                    "exhbNo": "R0003",
                    "sortCode": "10",
                    "deliveryAreaCode": "J",
                    "deliveryLocalAreaCode": "J1",
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
        else:
            params = custom_params
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=params,
                timeout=10
            )
            response.raise_for_status()
            
            return {
                "success": True,
                "status_code": response.status_code,
                "data": response.json(),
                "model": model.value["name"] if model else "전체"
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "status_code": getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None,
                "model": model.value["name"] if model else "전체"
            }
    
    def check_availability(
        self, 
        model: Optional[CarModel] = None,
        custom_params: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        차량 재고가 있는지 확인합니다.
        
        Returns:
            재고가 있으면 True, 없으면 False
        """
        result = self.check_inventory(model, custom_params)
        
        if result["success"]:
            response_data = result["data"]
            # 실제 응답 구조 확인
            if "data" in response_data and "totalCount" in response_data["data"]:
                return response_data["data"]["totalCount"] > 0
        
        return False
    
    def get_car_count(
        self, 
        model: Optional[CarModel] = None,
        custom_params: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        재고 개수를 반환합니다.
        
        Returns:
            재고 개수
        """
        result = self.check_inventory(model, custom_params)
        
        if result["success"]:
            response_data = result["data"]
            if "data" in response_data and "totalCount" in response_data["data"]:
                return response_data["data"]["totalCount"]
        
        return 0
    
    def get_car_list(
        self, 
        model: Optional[CarModel] = None,
        custom_params: Optional[Dict[str, Any]] = None
    ) -> list:
        """
        재고 차량 리스트를 반환합니다.
        
        Returns:
            차량 정보 리스트
        """
        result = self.check_inventory(model, custom_params)
        
        if result["success"]:
            response_data = result["data"]
            if "data" in response_data and "discountsearchcars" in response_data["data"]:
                return response_data["data"]["discountsearchcars"]
        
        return []
    
    def check_all_models(self) -> Dict[str, Any]:
        """
        모든 모델의 재고를 한번에 확인합니다.
        
        Returns:
            모델별 재고 정보 딕셔너리
        """
        results = {}
        
        for model in CarModel:
            count = self.get_car_count(model)
            results[model.value["name"]] = {
                "count": count,
                "carCode": model.value["carCode"],
                "available": count > 0
            }
        
        return results
    
    def search_by_region(
        self,
        model: CarModel,
        sido_name: str,
        sigun_name: Optional[str] = None,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        지역명으로 재고를 검색합니다.
        
        Args:
            model: 차량 모델
            sido_name: 시도명 (예: "경북", "서울")
            sigun_name: 시군구명 (예: "포항시", 선택사항)
            **kwargs: 추가 필터 옵션 (exteriorColorCode 등)
        
        Returns:
            해당 지역의 차량 리스트
        
        Examples:
            >>> checker = CasperChecker()
            >>> cars = checker.search_by_region(
            ...     CarModel.CASPER_ELECTRIC_2026,
            ...     "경북",
            ...     "포항시"
            ... )
        """
        try:
            from region_helper import get_codes
            area_code, local_code = get_codes(sido_name, sigun_name)
        except (ImportError, ValueError) as e:
            print(f"❌ 지역 코드 조회 실패: {e}")
            print("fetch_regions.py를 먼저 실행하세요.")
            return []
        
        model_data = model.value
        
        # 기본 파라미터 생성
        params = {
            "carCode": model_data["carCode"],
            "subsidyRegion": model_data["subsidyRegion"],
            "exhbNo": "R0003",
            "sortCode": "10",
            "deliveryAreaCode": area_code,
            "deliveryLocalAreaCode": local_code,
            "carBodyCode": "",
            "carEngineCode": "",
            "carTrimCode": "",
            "exteriorColorCode": "",
            "interiorColorCode": [],
            "deliveryCenterCode": "",
            "wpaScnCd": "",
            "optionFilter": "",
            "minSalePrice": model_data["minSalePrice"],
            "maxSalePrice": model_data["maxSalePrice"],
            "choiceOptYn": "Y",
            "pageNo": 1,
            "pageSize": 18
        }
        
        # 추가 옵션 적용
        params.update(kwargs)
        
        return self.get_car_list(custom_params=params)
    
    def get_region_count(
        self,
        model: CarModel,
        sido_name: str,
        sigun_name: Optional[str] = None
    ) -> int:
        """
        특정 지역의 재고 개수를 반환합니다.
        
        Args:
            model: 차량 모델
            sido_name: 시도명
            sigun_name: 시군구명 (선택)
        
        Returns:
            재고 개수
        """
        cars = self.search_by_region(model, sido_name, sigun_name)
        return len(cars)
    
    def print_car_info(self, car: Dict[str, Any]) -> None:
        """
        차량 정보를 보기 좋게 출력합니다.
        """
        print(f"\n{'='*60}")
        print(f"🚗 {car['carName']} - {car['saleModelName']}")
        print(f"{'='*60}")
        print(f"트림: {car['carTrimName']}")
        print(f"외장색: {car['exteriorColorName']}")
        print(f"내장색: {car['interiorColorName']}")
        print(f"미션: {car['carMissionName']}")
        print(f"\n💰 가격 정보:")
        print(f"  차량 가격: {int(float(car['carPrice'])):,}원")
        print(f"  할인 금액: {int(float(car['discountPrice'])):,}원 ({car['discountRate']}%)")
        print(f"  최종 금액: {int(float(car['finalAmount'])):,}원")
        print(f"  배송비: {int(float(car['totalDeiveryPrice'])):,}원")
        print(f"\n📦 옵션:")
        if car.get('carChoiceOption'):
            for option in car['carChoiceOption']:
                print(f"  - {option['choiceOptionName']}: {int(float(option['choiceOptionPrice'])):,}원")
        else:
            print(f"  {car.get('optionSummary', '없음')}")
        print(f"\n📍 출고 정보:")
        print(f"  출고센터: {car['deliveryCenterName']}")
        print(f"  생산일: {car['prdnDt'][:4]}-{car['prdnDt'][4:6]}-{car['prdnDt'][6:]}")
        print(f"  차대번호: {car['carProductionNumber']}")
        print(f"\n💡 할인 사유: {car['discountReasonSubstance']}")
        print(f"{'='*60}\n")


def main():
    """메인 실행 함수"""
    checker = CasperChecker()
    
    print("="*70)
    print("🚗 현대 캐스퍼 재고 확인 시스템")
    print("="*70)
    
    # 모든 모델 재고 확인
    print("\n📊 전체 모델 재고 현황:")
    print("-"*70)
    all_models = checker.check_all_models()
    
    for model_name, info in all_models.items():
        status = "✅" if info["available"] else "❌"
        print(f"{status} {model_name:<25} | 재고: {info['count']:>3}대 | 코드: {info['carCode']}")
    
    # 재고가 있는 모델 상세 정보
    print("\n" + "="*70)
    print("📦 재고 상세 정보")
    print("="*70)
    
    for model in CarModel:
        count = checker.get_car_count(model)
        
        if count > 0:
            print(f"\n[{model.value['name']}] - 총 {count}대")
            print("-"*70)
            
            cars = checker.get_car_list(model)
            for i, car in enumerate(cars[:3], 1):  # 처음 3대만 표시
                print(f"\n  [{i}] {car['exteriorColorName']} | {car['carTrimName']}")
                print(f"      가격: {int(float(car['finalAmount'])):,}원 (할인 {int(float(car['discountPrice'])):,}원)")
                print(f"      출고: {car['deliveryCenterName']}")
            
            if count > 3:
                print(f"\n  ... 외 {count - 3}대 더 있음")
    
    # 특정 모델만 상세 조회 예시
    print("\n\n" + "="*70)
    print("💡 특정 모델 상세 조회 예시")
    print("="*70)
    
    # 2026 캐스퍼 일렉트릭만 조회
    print("\n[2026 캐스퍼 일렉트릭 상세 정보]")
    cars = checker.get_car_list(CarModel.CASPER_ELECTRIC_2026)
    
    if cars:
        for car in cars[:2]:  # 처음 2대만
            checker.print_car_info(car)
    else:
        print("현재 재고가 없습니다.")


if __name__ == "__main__":
    main()
