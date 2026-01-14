#!/usr/bin/env python3
"""
지역 검색 헬퍼 모듈

region_constants.py의 데이터를 쉽게 사용할 수 있도록 도와줍니다.
"""

import os
import json
from typing import Dict, List, Optional, Tuple


class RegionHelper:
    """지역 코드 검색을 도와주는 헬퍼 클래스"""
    
    def __init__(self):
        self.sido_codes = {}
        self.sigun_codes = {}
        self.region_data = {}
        self._load_region_data()
    
    def _load_region_data(self):
        """지역 데이터를 로드합니다."""
        try:
            # region_constants.py에서 로드 시도
            from region_constants import SIDO_CODES, SIGUN_CODES, REGION_DATA
            self.sido_codes = SIDO_CODES
            self.sigun_codes = SIGUN_CODES
            self.region_data = REGION_DATA
        except ImportError:
            # region_data.json에서 로드 시도
            try:
                if os.path.exists('region_data.json'):
                    with open('region_data.json', 'r', encoding='utf-8') as f:
                        self.region_data = json.load(f)
                        self._build_codes_from_json()
                else:
                    print("⚠️  지역 데이터가 없습니다. fetch_regions.py를 먼저 실행하세요.")
            except Exception as e:
                print(f"❌ 지역 데이터 로드 실패: {e}")
    
    def _build_codes_from_json(self):
        """JSON 데이터로부터 코드 딕셔너리 생성"""
        for region_name, info in self.region_data.items():
            self.sido_codes[region_name] = info['code']
            
            if info.get('sigun_list'):
                self.sigun_codes[region_name] = {}
                for sigun in info['sigun_list']:
                    self.sigun_codes[region_name][sigun['codeName']] = sigun['code']
    
    def get_codes(self, sido_name: str, sigun_name: Optional[str] = None) -> Tuple[str, str]:
        """
        지역명으로 코드를 조회합니다.
        
        Args:
            sido_name: 시도명 (예: "경북", "서울")
            sigun_name: 시군구명 (예: "포항시", "강화군")
        
        Returns:
            (deliveryAreaCode, deliveryLocalAreaCode) 튜플
        
        Examples:
            >>> helper = RegionHelper()
            >>> helper.get_codes("경북", "포항시")
            ('N', 'NL')
            
            >>> helper.get_codes("서울")
            ('B', 'B0')
        """
        if not self.sido_codes:
            raise ValueError("지역 데이터가 로드되지 않았습니다. fetch_regions.py를 먼저 실행하세요.")
        
        # 시도 코드 조회
        sido_code = self.sido_codes.get(sido_name)
        if not sido_code:
            available = ', '.join(self.sido_codes.keys())
            raise ValueError(f"알 수 없는 시도명: {sido_name}\n사용 가능: {available}")
        
        # 시군구 코드 조회
        if sigun_name:
            region_siguns = self.sigun_codes.get(sido_name, {})
            sigun_code = region_siguns.get(sigun_name)
            
            if not sigun_code:
                available = ', '.join(region_siguns.keys()) if region_siguns else "시군구 구분 없음"
                raise ValueError(f"{sido_name}에서 '{sigun_name}'을(를) 찾을 수 없습니다.\n사용 가능: {available}")
            
            return sido_code, sigun_code
        else:
            # 시군구가 없으면 첫 번째 시군구 사용
            region_info = self.region_data.get(sido_name, {})
            sigun_list = region_info.get('sigun_list', [])
            
            if sigun_list:
                return sido_code, sigun_list[0]['code']
            else:
                # 데이터가 없으면 시도코드 + "0" 사용
                return sido_code, f"{sido_code}0"
    
    def search_sigun(self, query: str) -> List[Dict[str, str]]:
        """
        시군구명으로 검색합니다.
        
        Args:
            query: 검색어 (예: "포항", "강화")
        
        Returns:
            검색 결과 리스트
        """
        results = []
        
        for sido_name, siguns in self.sigun_codes.items():
            for sigun_name, sigun_code in siguns.items():
                if query in sigun_name:
                    results.append({
                        'sido': sido_name,
                        'sido_code': self.sido_codes[sido_name],
                        'sigun': sigun_name,
                        'sigun_code': sigun_code
                    })
        
        return results
    
    def list_siguns(self, sido_name: str) -> List[str]:
        """
        특정 시도의 모든 시군구 목록을 반환합니다.
        
        Args:
            sido_name: 시도명
        
        Returns:
            시군구명 리스트
        """
        return list(self.sigun_codes.get(sido_name, {}).keys())
    
    def list_sidos(self) -> List[str]:
        """모든 시도 목록을 반환합니다."""
        return list(self.sido_codes.keys())
    
    def is_available(self) -> bool:
        """지역 데이터가 사용 가능한지 확인합니다."""
        return bool(self.sido_codes)
    
    def print_summary(self):
        """지역 정보 요약을 출력합니다."""
        if not self.is_available():
            print("❌ 지역 데이터가 없습니다. fetch_regions.py를 먼저 실행하세요.")
            return
        
        print("📍 사용 가능한 시도:")
        for sido in self.list_sidos():
            siguns = self.list_siguns(sido)
            count = len(siguns)
            if count > 0:
                print(f"  • {sido:4} ({self.sido_codes[sido]}) - {count:2}개 시군구")
            else:
                print(f"  • {sido:4} ({self.sido_codes[sido]}) - 시군구 구분 없음")


# 전역 인스턴스
_region_helper = None


def get_region_helper() -> RegionHelper:
    """RegionHelper 싱글톤 인스턴스를 반환합니다."""
    global _region_helper
    if _region_helper is None:
        _region_helper = RegionHelper()
    return _region_helper


# 편의 함수들
def get_codes(sido_name: str, sigun_name: Optional[str] = None) -> Tuple[str, str]:
    """지역명으로 배송지 코드를 조회합니다."""
    return get_region_helper().get_codes(sido_name, sigun_name)


def search_sigun(query: str) -> List[Dict[str, str]]:
    """시군구명으로 검색합니다."""
    return get_region_helper().search_sigun(query)


def list_siguns(sido_name: str) -> List[str]:
    """특정 시도의 시군구 목록을 반환합니다."""
    return get_region_helper().list_siguns(sido_name)


def list_sidos() -> List[str]:
    """모든 시도 목록을 반환합니다."""
    return get_region_helper().list_sidos()


if __name__ == "__main__":
    helper = RegionHelper()
    
    if helper.is_available():
        print("✅ 지역 데이터 로드 성공!\n")
        
        # 요약 출력
        helper.print_summary()
        
        # 예시
        print("\n" + "="*70)
        print("🔍 사용 예시")
        print("="*70)
        
        # 경북 포항
        try:
            area, local = helper.get_codes("경북", "포항시")
            print(f"\n경북 포항시: deliveryAreaCode={area}, deliveryLocalAreaCode={local}")
        except ValueError as e:
            print(f"오류: {e}")
        
        # 서울
        try:
            area, local = helper.get_codes("서울")
            print(f"서울: deliveryAreaCode={area}, deliveryLocalAreaCode={local}")
        except ValueError as e:
            print(f"오류: {e}")
        
        # 검색
        print("\n'포항' 검색 결과:")
        results = helper.search_sigun("포항")
        for r in results:
            print(f"  {r['sido']} > {r['sigun']} (코드: {r['sido_code']}-{r['sigun_code']})")
    else:
        print("❌ 지역 데이터를 찾을 수 없습니다.")
        print("fetch_regions.py를 먼저 실행하세요.")
