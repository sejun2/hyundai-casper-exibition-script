#!/usr/bin/env python3
"""
지역 검색 기능이 통합된 캐스퍼 재고 확인 도구

region_constants.py의 데이터를 활용하여 편리하게 지역별 검색을 수행합니다.
"""

from casper_checker import CasperChecker, CarModel
from typing import Optional, List, Dict, Any
import json


class RegionAwareCasperChecker(CasperChecker):
    """지역 검색 기능이 추가된 CasperChecker"""
    
    def __init__(self):
        super().__init__()
        self.region_data = self._load_region_data()
    
    def _load_region_data(self) -> Dict[str, Any]:
        """region_data.json 파일을 로드합니다."""
        try:
            with open('region_data.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("⚠️  region_data.json 파일이 없습니다.")
            print("   먼저 'python fetch_regions.py'를 실행하세요.")
            return {}
    
    def get_region_code(self, sido_name: str) -> Optional[str]:
        """시도명으로 코드를 반환합니다."""
        region = self.region_data.get(sido_name)
        return region['code'] if region else None
    
    def get_sigun_code(self, sido_name: str, sigun_name: str) -> Optional[str]:
        """시군구명으로 코드를 반환합니다."""
        region = self.region_data.get(sido_name)
        if not region:
            return None
        
        for sigun in region.get('sigun_list', []):
            if sigun['codeName'] == sigun_name:
                return sigun['code']
        
        return None
    
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
            sido_name: 시도명 (예: "경북")
            sigun_name: 시군구명 (예: "포항시"), 선택사항
            **kwargs: 추가 필터 (exteriorColorCode 등)
        
        Returns:
            차량 리스트
        
        Examples:
            >>> checker.search_by_region(CarModel.CASPER_ELECTRIC_2026, "경북", "포항시")
            >>> checker.search_by_region(CarModel.CASPER_2026, "서울")
        """
        # 시도 코드 가져오기
        sido_code = self.get_region_code(sido_name)
        if not sido_code:
            print(f"❌ '{sido_name}' 시도를 찾을 수 없습니다.")
            return []
        
        # 시군구 코드 가져오기
        if sigun_name:
            sigun_code = self.get_sigun_code(sido_name, sigun_name)
            if not sigun_code:
                print(f"❌ '{sido_name}'에서 '{sigun_name}' 시군구를 찾을 수 없습니다.")
                return []
        else:
            # 시군구가 없으면 첫 번째 시군구 사용
            region = self.region_data.get(sido_name)
            sigun_list = region.get('sigun_list', [])
            if sigun_list:
                sigun_code = sigun_list[0]['code']
            else:
                sigun_code = f"{sido_code}0"
        
        # 파라미터 구성
        model_data = model.value
        params = {
            "carCode": model_data["carCode"],
            "subsidyRegion": model_data["subsidyRegion"],
            "exhbNo": "R0003",
            "sortCode": "10",
            "deliveryAreaCode": sido_code,
            "deliveryLocalAreaCode": sigun_code,
            "carBodyCode": "",
            "carEngineCode": "",
            "carTrimCode": "",
            "exteriorColorCode": kwargs.get("exteriorColorCode", ""),
            "interiorColorCode": kwargs.get("interiorColorCode", []),
            "deliveryCenterCode": kwargs.get("deliveryCenterCode", ""),
            "wpaScnCd": "",
            "optionFilter": "",
            "minSalePrice": model_data["minSalePrice"],
            "maxSalePrice": model_data["maxSalePrice"],
            "choiceOptYn": "Y",
            "pageNo": 1,
            "pageSize": 18
        }
        
        return self.get_car_list(custom_params=params)
    
    def get_region_count(
        self,
        model: CarModel,
        sido_name: str,
        sigun_name: Optional[str] = None,
        **kwargs
    ) -> int:
        """지역별 재고 개수를 반환합니다."""
        cars = self.search_by_region(model, sido_name, sigun_name, **kwargs)
        return len(cars)
    
    def list_available_siguns(self, sido_name: str) -> List[str]:
        """특정 시도의 시군구 목록을 반환합니다."""
        region = self.region_data.get(sido_name)
        if not region:
            return []
        
        return [sigun['codeName'] for sigun in region.get('sigun_list', [])]
    
    def search_all_regions_for_model(
        self,
        model: CarModel,
        **kwargs
    ) -> Dict[str, int]:
        """
        모든 지역의 특정 모델 재고를 검색합니다.
        
        Returns:
            {지역명: 재고개수} 딕셔너리
        """
        results = {}
        
        for sido_name in self.region_data.keys():
            count = self.get_region_count(model, sido_name, **kwargs)
            if count > 0:
                results[sido_name] = count
        
        return results
    
    def find_nearest_stock(
        self,
        model: CarModel,
        my_sido: str,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        내 지역과 인근 지역의 재고를 검색합니다.
        
        Args:
            model: 차량 모델
            my_sido: 내 시도 (예: "경북")
            **kwargs: 추가 필터
        
        Returns:
            지역별 재고 정보 리스트
        """
        # 내 지역부터 검색
        my_count = self.get_region_count(model, my_sido, **kwargs)
        
        results = []
        
        if my_count > 0:
            results.append({
                "sido": my_sido,
                "count": my_count,
                "distance": "내 지역"
            })
        
        # 다른 지역 검색
        for sido_name in self.region_data.keys():
            if sido_name == my_sido:
                continue
            
            count = self.get_region_count(model, sido_name, **kwargs)
            if count > 0:
                results.append({
                    "sido": sido_name,
                    "count": count,
                    "distance": "타 지역"
                })
        
        return results


def main():
    """사용 예시"""
    checker = RegionAwareCasperChecker()
    
    if not checker.region_data:
        print("\n❌ 지역 데이터가 로드되지 않았습니다.")
        print("먼저 'python fetch_regions.py'를 실행하세요.")
        return
    
    print("="*70)
    print("🗺️  지역 검색 기능 통합 캐스퍼 재고 확인")
    print("="*70)
    
    # 예시 1: 경북 포항시 검색
    print("\n[예시 1] 경북 포항시 - 2026 캐스퍼 일렉트릭")
    print("-"*70)
    
    cars = checker.search_by_region(
        CarModel.CASPER_ELECTRIC_2026,
        "경북",
        "포항시"
    )
    
    print(f"재고: {len(cars)}대")
    if cars:
        for i, car in enumerate(cars[:3], 1):
            print(f"  {i}. {car['exteriorColorName']} - {int(car['finalAmount']):,}원")
    
    # 예시 2: 서울 전체 검색
    print("\n[예시 2] 서울 - 2026 캐스퍼")
    print("-"*70)
    
    count = checker.get_region_count(CarModel.CASPER_2026, "서울")
    print(f"재고: {count}대")
    
    # 예시 3: 경북의 시군구 목록
    print("\n[예시 3] 경북 시군구 목록")
    print("-"*70)
    
    siguns = checker.list_available_siguns("경북")
    print(f"총 {len(siguns)}개: {', '.join(siguns[:5])}... 등")
    
    # 예시 4: 전국 검색
    print("\n[예시 4] 2026 캐스퍼 일렉트릭 - 전국 재고 현황")
    print("-"*70)
    
    all_regions = checker.search_all_regions_for_model(CarModel.CASPER_ELECTRIC_2026)
    
    if all_regions:
        print("\n재고가 있는 지역:")
        for region, count in sorted(all_regions.items(), key=lambda x: x[1], reverse=True):
            print(f"  {region}: {count}대")
    else:
        print("전국에 재고가 없습니다.")
    
    # 예시 5: 인근 지역 재고 찾기
    print("\n[예시 5] 경북 및 인근 지역 재고")
    print("-"*70)
    
    nearby = checker.find_nearest_stock(CarModel.CASPER_ELECTRIC_2026, "경북")
    
    if nearby:
        for info in nearby[:5]:
            print(f"  {info['sido']}: {info['count']}대 ({info['distance']})")
    
    # 예시 6: 특정 색상으로 검색
    print("\n[예시 6] 경북 포항시 - 아틀라스 화이트만")
    print("-"*70)
    
    white_cars = checker.search_by_region(
        CarModel.CASPER_ELECTRIC_2026,
        "경북",
        "포항시",
        exteriorColorCode="SAW"
    )
    
    print(f"아틀라스 화이트 재고: {len(white_cars)}대")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n중단됨")
    except Exception as e:
        print(f"\n오류: {e}")
        import traceback
        traceback.print_exc()
