# -*- coding: utf-8 -*-
"""
현대 캐스퍼 배송지 코드 상수

자동 생성된 파일입니다.
"""

# 시도 코드
SIDO_CODES = {
    "서울": "B",
    "인천": "D",
    "경기": "E",
    "강원": "F",
    "세종": "W",
    "충남": "I",
    "대전": "H",
    "충북": "G",
    "대구": "M",
    "경북": "N",
    "부산": "P",
    "경남": "S",
    "울산": "U",
    "전북": "J",
    "전남": "L",
    "광주": "K",
    "제주": "T",
}

# 시군구 코드
SIGUN_CODES = {
    "서울": {
        "서울특별시": "B0",
    },
    "인천": {
        "인천광역시": "D1",
        "강화군": "D2",
        "영종도(운서동)": "D3",
    },
    "경기": {
        "가평군": "E0",
        "고양시": "E1",
        "과천시": "E2",
        "광명시": "E3",
        "광주시": "E4",
        "구리시": "E5",
        "군포시": "E6",
        "김포시": "E7",
        "남양주시": "E8",
        "동두천시": "E9",
        "부천시": "EA",
        "성남시": "EB",
        "수원시": "EC",
        "시흥시": "ED",
        "안산시": "EE",
        "안성시": "EF",
        "안양시": "EG",
        "양주시": "EH",
        "양평군": "EI",
        "여주시": "EJ",
        "연천군": "EK",
        "오산시": "EL",
        "용인시": "EM",
        "의왕시": "EN",
        "의정부시": "EP",
        "이천시": "EQ",
        "파주시": "ER",
        "평택시": "ES",
        "포천시": "ET",
        "하남시": "EU",
        "화성시": "EV",
    },
    "강원": {
        "강릉시": "F0",
        "고성군": "F1",
        "동해시": "F2",
        "삼척시": "F3",
        "속초시": "F4",
        "양구군": "F5",
        "양양군": "F6",
        "영월군": "F7",
        "원주시": "F8",
        "인제군": "F9",
        "정선군": "FA",
        "철원군": "FB",
        "춘천시": "FC",
        "태백시": "FD",
        "평창군": "FE",
        "홍천군": "FF",
        "화천군": "FG",
        "횡성군": "FH",
    },
    "세종": {
        "세종특별자치시": "I9",
    },
    "충남": {
        "공주시": "I0",
        "금산군": "I1",
        "논산시": "I2",
        "당진시": "I3",
        "보령시": "I4",
        "부여군": "I5",
        "서산시": "I6",
        "서천군": "I7",
        "아산시": "I8",
        "세종특별자치시": "I9",
        "예산군": "IA",
        "천안시": "IB",
        "청양군": "IC",
        "태안군": "ID",
        "홍성군": "IE",
        "계룡시": "IF",
    },
    "대전": {
        "대전광역시": "H0",
    },
    "충북": {
        "괴산군": "G0",
        "단양군": "G1",
        "보은군": "G2",
        "영동군": "G3",
        "옥천군": "G4",
        "음성군": "G5",
        "제천시": "G6",
        "진천군": "G7",
        "청주시": "G9",
        "충주시": "GA",
        "증평군": "GB",
    },
    "대구": {
        "대구광역시": "M0",
        "군위군": "M1",
    },
    "경북": {
        "경산시": "N0",
        "경주시": "N1",
        "고령군": "N2",
        "구미시": "N3",
        "김천시": "N5",
        "문경시": "N6",
        "봉화군": "N7",
        "상주시": "N8",
        "성주군": "N9",
        "안동시": "NA",
        "영덕군": "NB",
        "영양군": "NC",
        "영주시": "ND",
        "영천시": "NE",
        "예천군": "NF",
        "울진군": "NG",
        "의성군": "NH",
        "청도군": "NI",
        "청송군": "NJ",
        "칠곡군": "NK",
        "포항시": "NL",
    },
    "부산": {
        "부산광역시": "P0",
    },
    "경남": {
        "거제시": "S0",
        "거창군": "S1",
        "고성군": "S2",
        "김해시": "S3",
        "남해군": "S4",
        "창원시(마산)": "S5",
        "밀양시": "S6",
        "사천시": "S7",
        "산청군": "S8",
        "양산시": "S9",
        "의령군": "SA",
        "진주시": "SB",
        "창원시(진해)": "SC",
        "창녕군": "SD",
        "창원시": "SE",
        "통영시": "SF",
        "하동군": "SG",
        "함안군": "SH",
        "함양군": "SI",
        "합천군": "SJ",
    },
    "울산": {
        "울산광역시": "U0",
        "울주군": "U1",
    },
    "전북": {
        "고창군": "J0",
        "군산시": "J1",
        "김제시": "J2",
        "남원시": "J3",
        "무주군": "J4",
        "부안군": "J5",
        "순창군": "J6",
        "완주군": "J7",
        "익산시": "J8",
        "임실군": "J9",
        "장수군": "JA",
        "전주시": "JB",
        "정읍시": "JC",
        "진안군": "JD",
    },
    "전남": {
        "강진군": "L0",
        "고흥군": "L1",
        "곡성군": "L2",
        "광양시": "L3",
        "구례군": "L4",
        "나주시": "L5",
        "담양군": "L6",
        "목포시": "L7",
        "무안군": "L8",
        "보성군": "L9",
        "순천시": "LA",
        "여수시": "LB",
        "영광군": "LC",
        "영암군": "LD",
        "완도군": "LE",
        "장성군": "LF",
        "장흥군": "LG",
        "진도군": "LH",
        "함평군": "LI",
        "해남군": "LJ",
        "화순군": "LK",
    },
    "광주": {
        "광주광역시": "K0",
    },
    "제주": {
        "제주항": "T0",
        "제주시": "T1",
        "서귀포시": "T2",
    },
}

# 전체 지역 데이터
REGION_DATA = {
    "서울": {
        "code": "B",
        "has_sigun": False,
        "sigun_list": [
            {
                "code": "B0",
                "codeName": "서울특별시",
                "repnCarInfos": []
            }
        ],
        "count": 1
    },
    "인천": {
        "code": "D",
        "has_sigun": True,
        "sigun_list": [
            {
                "code": "D1",
                "codeName": "인천광역시",
                "repnCarInfos": []
            },
            {
                "code": "D2",
                "codeName": "강화군",
                "repnCarInfos": []
            },
            {
                "code": "D3",
                "codeName": "영종도(운서동)",
                "repnCarInfos": []
            }
        ],
        "count": 3
    },
    "경기": {
        "code": "E",
        "has_sigun": True,
        "sigun_list": [
            {
                "code": "E0",
                "codeName": "가평군",
                "repnCarInfos": []
            },
            {
                "code": "E1",
                "codeName": "고양시",
                "repnCarInfos": []
            },
            {
                "code": "E2",
                "codeName": "과천시",
                "repnCarInfos": []
            },
            {
                "code": "E3",
                "codeName": "광명시",
                "repnCarInfos": []
            },
            {
                "code": "E4",
                "codeName": "광주시",
                "repnCarInfos": []
            },
            {
                "code": "E5",
                "codeName": "구리시",
                "repnCarInfos": []
            },
            {
                "code": "E6",
                "codeName": "군포시",
                "repnCarInfos": []
            },
            {
                "code": "E7",
                "codeName": "김포시",
                "repnCarInfos": []
            },
            {
                "code": "E8",
                "codeName": "남양주시",
                "repnCarInfos": []
            },
            {
                "code": "E9",
                "codeName": "동두천시",
                "repnCarInfos": []
            },
            {
                "code": "EA",
                "codeName": "부천시",
                "repnCarInfos": []
            },
            {
                "code": "EB",
                "codeName": "성남시",
                "repnCarInfos": []
            },
            {
                "code": "EC",
                "codeName": "수원시",
                "repnCarInfos": []
            },
            {
                "code": "ED",
                "codeName": "시흥시",
                "repnCarInfos": []
            },
            {
                "code": "EE",
                "codeName": "안산시",
                "repnCarInfos": []
            },
            {
                "code": "EF",
                "codeName": "안성시",
                "repnCarInfos": []
            },
            {
                "code": "EG",
                "codeName": "안양시",
                "repnCarInfos": []
            },
            {
                "code": "EH",
                "codeName": "양주시",
                "repnCarInfos": []
            },
            {
                "code": "EI",
                "codeName": "양평군",
                "repnCarInfos": []
            },
            {
                "code": "EJ",
                "codeName": "여주시",
                "repnCarInfos": []
            },
            {
                "code": "EK",
                "codeName": "연천군",
                "repnCarInfos": []
            },
            {
                "code": "EL",
                "codeName": "오산시",
                "repnCarInfos": []
            },
            {
                "code": "EM",
                "codeName": "용인시",
                "repnCarInfos": []
            },
            {
                "code": "EN",
                "codeName": "의왕시",
                "repnCarInfos": []
            },
            {
                "code": "EP",
                "codeName": "의정부시",
                "repnCarInfos": []
            },
            {
                "code": "EQ",
                "codeName": "이천시",
                "repnCarInfos": []
            },
            {
                "code": "ER",
                "codeName": "파주시",
                "repnCarInfos": []
            },
            {
                "code": "ES",
                "codeName": "평택시",
                "repnCarInfos": []
            },
            {
                "code": "ET",
                "codeName": "포천시",
                "repnCarInfos": []
            },
            {
                "code": "EU",
                "codeName": "하남시",
                "repnCarInfos": []
            },
            {
                "code": "EV",
                "codeName": "화성시",
                "repnCarInfos": []
            }
        ],
        "count": 31
    },
    "강원": {
        "code": "F",
        "has_sigun": True,
        "sigun_list": [
            {
                "code": "F0",
                "codeName": "강릉시",
                "repnCarInfos": []
            },
            {
                "code": "F1",
                "codeName": "고성군",
                "repnCarInfos": []
            },
            {
                "code": "F2",
                "codeName": "동해시",
                "repnCarInfos": []
            },
            {
                "code": "F3",
                "codeName": "삼척시",
                "repnCarInfos": []
            },
            {
                "code": "F4",
                "codeName": "속초시",
                "repnCarInfos": []
            },
            {
                "code": "F5",
                "codeName": "양구군",
                "repnCarInfos": []
            },
            {
                "code": "F6",
                "codeName": "양양군",
                "repnCarInfos": []
            },
            {
                "code": "F7",
                "codeName": "영월군",
                "repnCarInfos": []
            },
            {
                "code": "F8",
                "codeName": "원주시",
                "repnCarInfos": []
            },
            {
                "code": "F9",
                "codeName": "인제군",
                "repnCarInfos": []
            },
            {
                "code": "FA",
                "codeName": "정선군",
                "repnCarInfos": []
            },
            {
                "code": "FB",
                "codeName": "철원군",
                "repnCarInfos": []
            },
            {
                "code": "FC",
                "codeName": "춘천시",
                "repnCarInfos": []
            },
            {
                "code": "FD",
                "codeName": "태백시",
                "repnCarInfos": []
            },
            {
                "code": "FE",
                "codeName": "평창군",
                "repnCarInfos": []
            },
            {
                "code": "FF",
                "codeName": "홍천군",
                "repnCarInfos": []
            },
            {
                "code": "FG",
                "codeName": "화천군",
                "repnCarInfos": []
            },
            {
                "code": "FH",
                "codeName": "횡성군",
                "repnCarInfos": []
            }
        ],
        "count": 18
    },
    "세종": {
        "code": "W",
        "has_sigun": False,
        "sigun_list": [
            {
                "code": "I9",
                "codeName": "세종특별자치시",
                "repnCarInfos": []
            }
        ],
        "count": 1
    },
    "충남": {
        "code": "I",
        "has_sigun": True,
        "sigun_list": [
            {
                "code": "I0",
                "codeName": "공주시",
                "repnCarInfos": []
            },
            {
                "code": "I1",
                "codeName": "금산군",
                "repnCarInfos": []
            },
            {
                "code": "I2",
                "codeName": "논산시",
                "repnCarInfos": []
            },
            {
                "code": "I3",
                "codeName": "당진시",
                "repnCarInfos": []
            },
            {
                "code": "I4",
                "codeName": "보령시",
                "repnCarInfos": []
            },
            {
                "code": "I5",
                "codeName": "부여군",
                "repnCarInfos": []
            },
            {
                "code": "I6",
                "codeName": "서산시",
                "repnCarInfos": []
            },
            {
                "code": "I7",
                "codeName": "서천군",
                "repnCarInfos": []
            },
            {
                "code": "I8",
                "codeName": "아산시",
                "repnCarInfos": []
            },
            {
                "code": "I9",
                "codeName": "세종특별자치시",
                "repnCarInfos": []
            },
            {
                "code": "IA",
                "codeName": "예산군",
                "repnCarInfos": []
            },
            {
                "code": "IB",
                "codeName": "천안시",
                "repnCarInfos": []
            },
            {
                "code": "IC",
                "codeName": "청양군",
                "repnCarInfos": []
            },
            {
                "code": "ID",
                "codeName": "태안군",
                "repnCarInfos": []
            },
            {
                "code": "IE",
                "codeName": "홍성군",
                "repnCarInfos": []
            },
            {
                "code": "IF",
                "codeName": "계룡시",
                "repnCarInfos": []
            }
        ],
        "count": 16
    },
    "대전": {
        "code": "H",
        "has_sigun": False,
        "sigun_list": [
            {
                "code": "H0",
                "codeName": "대전광역시",
                "repnCarInfos": []
            }
        ],
        "count": 1
    },
    "충북": {
        "code": "G",
        "has_sigun": True,
        "sigun_list": [
            {
                "code": "G0",
                "codeName": "괴산군",
                "repnCarInfos": []
            },
            {
                "code": "G1",
                "codeName": "단양군",
                "repnCarInfos": []
            },
            {
                "code": "G2",
                "codeName": "보은군",
                "repnCarInfos": []
            },
            {
                "code": "G3",
                "codeName": "영동군",
                "repnCarInfos": []
            },
            {
                "code": "G4",
                "codeName": "옥천군",
                "repnCarInfos": []
            },
            {
                "code": "G5",
                "codeName": "음성군",
                "repnCarInfos": []
            },
            {
                "code": "G6",
                "codeName": "제천시",
                "repnCarInfos": []
            },
            {
                "code": "G7",
                "codeName": "진천군",
                "repnCarInfos": []
            },
            {
                "code": "G9",
                "codeName": "청주시",
                "repnCarInfos": []
            },
            {
                "code": "GA",
                "codeName": "충주시",
                "repnCarInfos": []
            },
            {
                "code": "GB",
                "codeName": "증평군",
                "repnCarInfos": []
            }
        ],
        "count": 11
    },
    "대구": {
        "code": "M",
        "has_sigun": True,
        "sigun_list": [
            {
                "code": "M0",
                "codeName": "대구광역시",
                "repnCarInfos": []
            },
            {
                "code": "M1",
                "codeName": "군위군",
                "repnCarInfos": []
            }
        ],
        "count": 2
    },
    "경북": {
        "code": "N",
        "has_sigun": True,
        "sigun_list": [
            {
                "code": "N0",
                "codeName": "경산시",
                "repnCarInfos": []
            },
            {
                "code": "N1",
                "codeName": "경주시",
                "repnCarInfos": []
            },
            {
                "code": "N2",
                "codeName": "고령군",
                "repnCarInfos": []
            },
            {
                "code": "N3",
                "codeName": "구미시",
                "repnCarInfos": []
            },
            {
                "code": "N5",
                "codeName": "김천시",
                "repnCarInfos": []
            },
            {
                "code": "N6",
                "codeName": "문경시",
                "repnCarInfos": []
            },
            {
                "code": "N7",
                "codeName": "봉화군",
                "repnCarInfos": []
            },
            {
                "code": "N8",
                "codeName": "상주시",
                "repnCarInfos": []
            },
            {
                "code": "N9",
                "codeName": "성주군",
                "repnCarInfos": []
            },
            {
                "code": "NA",
                "codeName": "안동시",
                "repnCarInfos": []
            },
            {
                "code": "NB",
                "codeName": "영덕군",
                "repnCarInfos": []
            },
            {
                "code": "NC",
                "codeName": "영양군",
                "repnCarInfos": []
            },
            {
                "code": "ND",
                "codeName": "영주시",
                "repnCarInfos": []
            },
            {
                "code": "NE",
                "codeName": "영천시",
                "repnCarInfos": []
            },
            {
                "code": "NF",
                "codeName": "예천군",
                "repnCarInfos": []
            },
            {
                "code": "NG",
                "codeName": "울진군",
                "repnCarInfos": []
            },
            {
                "code": "NH",
                "codeName": "의성군",
                "repnCarInfos": []
            },
            {
                "code": "NI",
                "codeName": "청도군",
                "repnCarInfos": []
            },
            {
                "code": "NJ",
                "codeName": "청송군",
                "repnCarInfos": []
            },
            {
                "code": "NK",
                "codeName": "칠곡군",
                "repnCarInfos": []
            },
            {
                "code": "NL",
                "codeName": "포항시",
                "repnCarInfos": []
            }
        ],
        "count": 21
    },
    "부산": {
        "code": "P",
        "has_sigun": False,
        "sigun_list": [
            {
                "code": "P0",
                "codeName": "부산광역시",
                "repnCarInfos": []
            }
        ],
        "count": 1
    },
    "경남": {
        "code": "S",
        "has_sigun": True,
        "sigun_list": [
            {
                "code": "S0",
                "codeName": "거제시",
                "repnCarInfos": []
            },
            {
                "code": "S1",
                "codeName": "거창군",
                "repnCarInfos": []
            },
            {
                "code": "S2",
                "codeName": "고성군",
                "repnCarInfos": []
            },
            {
                "code": "S3",
                "codeName": "김해시",
                "repnCarInfos": []
            },
            {
                "code": "S4",
                "codeName": "남해군",
                "repnCarInfos": []
            },
            {
                "code": "S5",
                "codeName": "창원시(마산)",
                "repnCarInfos": []
            },
            {
                "code": "S6",
                "codeName": "밀양시",
                "repnCarInfos": []
            },
            {
                "code": "S7",
                "codeName": "사천시",
                "repnCarInfos": []
            },
            {
                "code": "S8",
                "codeName": "산청군",
                "repnCarInfos": []
            },
            {
                "code": "S9",
                "codeName": "양산시",
                "repnCarInfos": []
            },
            {
                "code": "SA",
                "codeName": "의령군",
                "repnCarInfos": []
            },
            {
                "code": "SB",
                "codeName": "진주시",
                "repnCarInfos": []
            },
            {
                "code": "SC",
                "codeName": "창원시(진해)",
                "repnCarInfos": []
            },
            {
                "code": "SD",
                "codeName": "창녕군",
                "repnCarInfos": []
            },
            {
                "code": "SE",
                "codeName": "창원시",
                "repnCarInfos": []
            },
            {
                "code": "SF",
                "codeName": "통영시",
                "repnCarInfos": []
            },
            {
                "code": "SG",
                "codeName": "하동군",
                "repnCarInfos": []
            },
            {
                "code": "SH",
                "codeName": "함안군",
                "repnCarInfos": []
            },
            {
                "code": "SI",
                "codeName": "함양군",
                "repnCarInfos": []
            },
            {
                "code": "SJ",
                "codeName": "합천군",
                "repnCarInfos": []
            }
        ],
        "count": 20
    },
    "울산": {
        "code": "U",
        "has_sigun": True,
        "sigun_list": [
            {
                "code": "U0",
                "codeName": "울산광역시",
                "repnCarInfos": []
            },
            {
                "code": "U1",
                "codeName": "울주군",
                "repnCarInfos": []
            }
        ],
        "count": 2
    },
    "전북": {
        "code": "J",
        "has_sigun": True,
        "sigun_list": [
            {
                "code": "J0",
                "codeName": "고창군",
                "repnCarInfos": []
            },
            {
                "code": "J1",
                "codeName": "군산시",
                "repnCarInfos": []
            },
            {
                "code": "J2",
                "codeName": "김제시",
                "repnCarInfos": []
            },
            {
                "code": "J3",
                "codeName": "남원시",
                "repnCarInfos": []
            },
            {
                "code": "J4",
                "codeName": "무주군",
                "repnCarInfos": []
            },
            {
                "code": "J5",
                "codeName": "부안군",
                "repnCarInfos": []
            },
            {
                "code": "J6",
                "codeName": "순창군",
                "repnCarInfos": []
            },
            {
                "code": "J7",
                "codeName": "완주군",
                "repnCarInfos": []
            },
            {
                "code": "J8",
                "codeName": "익산시",
                "repnCarInfos": []
            },
            {
                "code": "J9",
                "codeName": "임실군",
                "repnCarInfos": []
            },
            {
                "code": "JA",
                "codeName": "장수군",
                "repnCarInfos": []
            },
            {
                "code": "JB",
                "codeName": "전주시",
                "repnCarInfos": []
            },
            {
                "code": "JC",
                "codeName": "정읍시",
                "repnCarInfos": []
            },
            {
                "code": "JD",
                "codeName": "진안군",
                "repnCarInfos": []
            }
        ],
        "count": 14
    },
    "전남": {
        "code": "L",
        "has_sigun": True,
        "sigun_list": [
            {
                "code": "L0",
                "codeName": "강진군",
                "repnCarInfos": []
            },
            {
                "code": "L1",
                "codeName": "고흥군",
                "repnCarInfos": []
            },
            {
                "code": "L2",
                "codeName": "곡성군",
                "repnCarInfos": []
            },
            {
                "code": "L3",
                "codeName": "광양시",
                "repnCarInfos": []
            },
            {
                "code": "L4",
                "codeName": "구례군",
                "repnCarInfos": []
            },
            {
                "code": "L5",
                "codeName": "나주시",
                "repnCarInfos": []
            },
            {
                "code": "L6",
                "codeName": "담양군",
                "repnCarInfos": []
            },
            {
                "code": "L7",
                "codeName": "목포시",
                "repnCarInfos": []
            },
            {
                "code": "L8",
                "codeName": "무안군",
                "repnCarInfos": []
            },
            {
                "code": "L9",
                "codeName": "보성군",
                "repnCarInfos": []
            },
            {
                "code": "LA",
                "codeName": "순천시",
                "repnCarInfos": []
            },
            {
                "code": "LB",
                "codeName": "여수시",
                "repnCarInfos": []
            },
            {
                "code": "LC",
                "codeName": "영광군",
                "repnCarInfos": []
            },
            {
                "code": "LD",
                "codeName": "영암군",
                "repnCarInfos": []
            },
            {
                "code": "LE",
                "codeName": "완도군",
                "repnCarInfos": []
            },
            {
                "code": "LF",
                "codeName": "장성군",
                "repnCarInfos": []
            },
            {
                "code": "LG",
                "codeName": "장흥군",
                "repnCarInfos": []
            },
            {
                "code": "LH",
                "codeName": "진도군",
                "repnCarInfos": []
            },
            {
                "code": "LI",
                "codeName": "함평군",
                "repnCarInfos": []
            },
            {
                "code": "LJ",
                "codeName": "해남군",
                "repnCarInfos": []
            },
            {
                "code": "LK",
                "codeName": "화순군",
                "repnCarInfos": []
            }
        ],
        "count": 21
    },
    "광주": {
        "code": "K",
        "has_sigun": False,
        "sigun_list": [
            {
                "code": "K0",
                "codeName": "광주광역시",
                "repnCarInfos": []
            }
        ],
        "count": 1
    },
    "제주": {
        "code": "T",
        "has_sigun": True,
        "sigun_list": [
            {
                "code": "T0",
                "codeName": "제주항",
                "repnCarInfos": []
            },
            {
                "code": "T1",
                "codeName": "제주시",
                "repnCarInfos": []
            },
            {
                "code": "T2",
                "codeName": "서귀포시",
                "repnCarInfos": []
            }
        ],
        "count": 3
    }
}
