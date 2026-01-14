#!/usr/bin/env python3
"""
현대 캐스퍼 배송지 정보 수집 스크립트

전국의 모든 시도 및 시군구 정보를 수집합니다.
"""

import requests
import json
from typing import Dict, List, Any
import time


class RegionFetcher:
    """배송지 정보를 수집하는 클래스"""
    
    # 시도 정보 (순서대로)
    REGIONS = [
        {"name": "서울", "code": "B"},
        {"name": "인천", "code": "D"},
        {"name": "경기", "code": "E"},
        {"name": "강원", "code": "F"},
        {"name": "세종", "code": "W"},
        {"name": "충남", "code": "I"},
        {"name": "대전", "code": "H"},
        {"name": "충북", "code": "G"},
        {"name": "대구", "code": "M"},
        {"name": "경북", "code": "N"},
        {"name": "부산", "code": "P"},
        {"name": "경남", "code": "S"},
        {"name": "울산", "code": "U"},
        {"name": "전북", "code": "J"},
        {"name": "전남", "code": "L"},
        {"name": "광주", "code": "K"},
        {"name": "제주", "code": "T"},
    ]
    
    def __init__(self):
        self.base_url = "https://casper.hyundai.com/gw/wp/common/v2/common/address/si-gun"
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "ko,en-US;q=0.9,en;q=0.8,ja;q=0.7",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
            "referer": "https://casper.hyundai.com/",
            "sec-ch-ua": '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
        }
        self.region_data = {}
    
    def fetch_sigun(self, region_code: str) -> List[Dict[str, Any]]:
        """
        특정 시도의 시군구 정보를 가져옵니다.
        
        Args:
            region_code: 시도 코드 (예: 'B', 'N')
        
        Returns:
            시군구 리스트
        """
        params = {"commonCode": region_code}
        
        try:
            response = requests.get(
                self.base_url,
                headers=self.headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            if data.get("rspStatus", {}).get("rspCode") == "0000":
                return data.get("data", [])
            else:
                print(f"⚠️  {region_code} 응답 오류: {data.get('rspStatus', {}).get('rspMessage')}")
                return []
                
        except Exception as e:
            print(f"❌ {region_code} 요청 실패: {e}")
            return []
    
    def fetch_all_regions(self, delay: float = 0.5) -> Dict[str, Any]:
        """
        모든 시도의 시군구 정보를 수집합니다.
        
        Args:
            delay: 각 요청 사이의 지연 시간 (초)
        
        Returns:
            전체 지역 데이터 딕셔너리
        """
        print("🔍 전국 배송지 정보 수집 중...\n")
        print("="*70)
        
        for i, region in enumerate(self.REGIONS, 1):
            region_name = region["name"]
            region_code = region["code"]
            
            print(f"[{i:2d}/17] {region_name:<6} (코드: {region_code}) ", end="", flush=True)
            
            sigun_list = self.fetch_sigun(region_code)
            
            if len(sigun_list) > 1:
                # 시군구가 여러 개 있음
                print(f"✅ {len(sigun_list)}개 시군구")
                self.region_data[region_name] = {
                    "code": region_code,
                    "has_sigun": True,
                    "sigun_list": sigun_list,
                    "count": len(sigun_list)
                }
            elif len(sigun_list) == 1:
                # 시군구 구분 없음 (시도 단위만)
                print(f"ℹ️  시군구 구분 없음")
                self.region_data[region_name] = {
                    "code": region_code,
                    "has_sigun": False,
                    "sigun_list": sigun_list,
                    "count": 1
                }
            else:
                print(f"❌ 데이터 없음")
                self.region_data[region_name] = {
                    "code": region_code,
                    "has_sigun": False,
                    "sigun_list": [],
                    "count": 0
                }
            
            # 요청 간 지연
            if i < len(self.REGIONS):
                time.sleep(delay)
        
        print("="*70)
        print("\n✅ 수집 완료!\n")
        
        return self.region_data
    
    def print_summary(self):
        """수집 결과 요약 출력"""
        if not self.region_data:
            print("데이터가 없습니다.")
            return
        
        print("\n" + "="*70)
        print("📊 수집 결과 요약")
        print("="*70)
        
        total_siguns = sum(r["count"] for r in self.region_data.values())
        regions_with_sigun = sum(1 for r in self.region_data.values() if r["has_sigun"])
        
        print(f"\n전체 시도: {len(self.region_data)}개")
        print(f"시군구 세분화된 지역: {regions_with_sigun}개")
        print(f"전체 시군구 개수: {total_siguns}개\n")
    
    def print_detail(self):
        """상세 정보 출력"""
        if not self.region_data:
            print("데이터가 없습니다.")
            return
        
        print("\n" + "="*70)
        print("📋 상세 정보")
        print("="*70)
        
        for region_name, info in self.region_data.items():
            print(f"\n[{region_name}] (코드: {info['code']})")
            
            if info["has_sigun"]:
                print(f"  시군구 {info['count']}개:")
                for sigun in info["sigun_list"]:
                    print(f"    • {sigun['code']}: {sigun['codeName']}")
            else:
                if info["sigun_list"]:
                    sigun = info["sigun_list"][0]
                    print(f"  시군구 구분 없음 - {sigun['code']}: {sigun['codeName']}")
                else:
                    print(f"  데이터 없음")
    
    def save_to_json(self, filename: str = "region_data.json"):
        """JSON 파일로 저장"""
        if not self.region_data:
            print("저장할 데이터가 없습니다.")
            return
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.region_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 데이터 저장 완료: {filename}")
    
    def save_to_python(self, filename: str = "region_constants.py"):
        """Python 상수로 저장"""
        if not self.region_data:
            print("저장할 데이터가 없습니다.")
            return
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# -*- coding: utf-8 -*-\n")
            f.write('"""\n현대 캐스퍼 배송지 코드 상수\n\n')
            f.write("자동 생성된 파일입니다.\n")
            f.write('"""\n\n')
            
            # 시도 코드 딕셔너리
            f.write("# 시도 코드\n")
            f.write("SIDO_CODES = {\n")
            for region_name, info in self.region_data.items():
                f.write(f'    "{region_name}": "{info["code"]}",\n')
            f.write("}\n\n")
            
            # 시군구 코드 딕셔너리
            f.write("# 시군구 코드\n")
            f.write("SIGUN_CODES = {\n")
            for region_name, info in self.region_data.items():
                if info["sigun_list"]:
                    f.write(f'    "{region_name}": {{\n')
                    for sigun in info["sigun_list"]:
                        f.write(f'        "{sigun["codeName"]}": "{sigun["code"]}",\n')
                    f.write('    },\n')
            f.write("}\n\n")
            
            # 전체 데이터
            f.write("# 전체 지역 데이터\n")
            f.write("REGION_DATA = ")
            # JSON을 문자열로 변환 후 true/false를 True/False로 변경
            json_str = json.dumps(self.region_data, ensure_ascii=False, indent=4)
            json_str = json_str.replace(': true', ': True').replace(': false', ': False')
            f.write(json_str)
            f.write("\n")
        
        print(f"\n💾 Python 상수 저장 완료: {filename}")
    
    def get_region_by_name(self, region_name: str) -> Dict[str, Any]:
        """지역명으로 정보 조회"""
        return self.region_data.get(region_name, {})
    
    def search_sigun(self, sigun_name: str) -> List[Dict[str, Any]]:
        """시군구명으로 검색"""
        results = []
        for region_name, info in self.region_data.items():
            for sigun in info.get("sigun_list", []):
                if sigun_name in sigun["codeName"]:
                    results.append({
                        "sido": region_name,
                        "sido_code": info["code"],
                        "sigun": sigun["codeName"],
                        "sigun_code": sigun["code"]
                    })
        return results


def main():
    """메인 실행 함수"""
    fetcher = RegionFetcher()
    
    # 1. 데이터 수집
    fetcher.fetch_all_regions(delay=0.3)
    
    # 2. 요약 출력
    fetcher.print_summary()
    
    # 3. 상세 정보 출력
    print("\n상세 정보를 보시겠습니까? (y/n): ", end="")
    try:
        choice = input().strip().lower()
        if choice == 'y':
            fetcher.print_detail()
    except:
        pass
    
    # 4. 파일 저장
    fetcher.save_to_json("region_data.json")
    fetcher.save_to_python("region_constants.py")
    
    # 5. 검색 예시
    print("\n" + "="*70)
    print("🔍 검색 예시")
    print("="*70)
    
    # 경북 정보
    print("\n[경북 시군구 정보]")
    gyeongbuk = fetcher.get_region_by_name("경북")
    if gyeongbuk:
        print(f"코드: {gyeongbuk['code']}")
        print(f"시군구 개수: {gyeongbuk['count']}")
        if gyeongbuk['count'] > 0:
            print("시군구 목록:")
            for sigun in gyeongbuk['sigun_list'][:5]:  # 처음 5개만
                print(f"  • {sigun['code']}: {sigun['codeName']}")
            if gyeongbuk['count'] > 5:
                print(f"  ... 외 {gyeongbuk['count'] - 5}개")
    
    # 포항 검색
    print("\n['포항' 검색 결과]")
    results = fetcher.search_sigun("포항")
    for result in results:
        print(f"  {result['sido']} ({result['sido_code']}) > "
              f"{result['sigun']} ({result['sigun_code']})")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n중단됨")
    except Exception as e:
        print(f"\n오류 발생: {e}")
