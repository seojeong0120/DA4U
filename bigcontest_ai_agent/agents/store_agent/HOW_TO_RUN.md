# Store Agent Module 실행 가이드

## 🚀 실행 방법

### 방법 1: Python 스크립트로 실행 (권장)

```bash
# 프로젝트 루트 디렉토리에서 실행
python run_test.py
```

### 방법 2: Python 인터랙티브 쉘

```python
import asyncio
from report_builder.store_agent_module import StoreAgentModule, StoreAgentState

async def test():
    # 1. 초기화
    agent = StoreAgentModule()
    
    # 2. State 준비
    state: StoreAgentState = {
        "user_query": "000F03E44A 매장 분석해줘",
        "user_id": "test_user",
        "session_id": "test_001",
        "context": {},
        "store_analysis": None,
        "error": None
    }
    
    # 3. 실행
    result = await agent.execute_analysis_with_self_evaluation(state)
    
    # 4. 결과 확인
    if result["error"]:
        print(f"에러: {result['error']}")
    else:
        analysis = result["store_analysis"]
        print(f"분석 완료: {analysis['store_code']}")
        print(f"품질 점수: {analysis['evaluation']['quality_score']:.2%}")
        print(f"리포트: {analysis['output_file_path']}")
    
    return result

# 실행
result = asyncio.run(test())
```

### 방법 3: Jupyter Notebook

```python
# Cell 1: Import
from report_builder.store_agent_module import StoreAgentModule, StoreAgentState

# Cell 2: 초기화
agent = StoreAgentModule()
print(f"데이터 경로: {agent.data_path}")

# Cell 3: State 준비
state: StoreAgentState = {
    "user_query": "000F03E44A 매장 분석해줘",
    "user_id": "test_user",
    "session_id": "test_001",
    "context": {},
    "store_analysis": None,
    "error": None
}

# Cell 4: 실행
result = await agent.execute_analysis_with_self_evaluation(state)

# Cell 5: 결과 확인
if not result["error"]:
    analysis = result["store_analysis"]
    overview = analysis['analysis_result']['store_overview']
    
    print(f"매장명: {overview['name']}")
    print(f"주소: {overview['address']}")
    print(f"업종: {overview['industry']}")
    print(f"품질 점수: {analysis['evaluation']['quality_score']:.2%}")
```

## 📊 예상 출력 결과

```
============================================================
Store Agent Module 테스트
============================================================

✅ 모듈 초기화 완료
   데이터 경로: C:\ㅈ\DA4U\bigcontest_ai_agent\agents\store_agent\store_data\final_merged_data.csv

📊 분석 실행 중...
------------------------------------------------------------
INFO - 매장 분석 시작 - 사용자: test_user, 쿼리: 000F03E44A 매장 분석해줘
INFO - 데이터 로드 완료: 86592 행 - 경로: ...
INFO - 매장 분석 시작
INFO - 매장 분석 완료 - 품질점수: 0.85
INFO - JSON 리포트 저장: ...
------------------------------------------------------------

✅ 분석 완료!

============================================================
📊 분석 결과
============================================================

🏪 매장 정보:
   코드: 000F03E44A
   상호명: 육육**
   주소: 서울 성동구 왕십리로4가길 9
   업종: 중식-딤섬/중식만두
   운영: 82.5개월 (기존 매장)

⭐ 품질 점수:
   종합: 85.0%
   완성도: 100.0%
   정확성: 90.0%

📁 생성된 파일:
   리포트: C:\...\outputs\reports\store_analysis_report_000F03E44A_20251012_xxxxxx.json
   차트: 7개 생성

============================================================
🎉 테스트 완료!
============================================================
```

## 📁 생성되는 파일

### 1. JSON 리포트
**위치**: `outputs/reports/store_analysis_report_000F03E44A_{timestamp}.json`

**내용 구조**:
```json
{
  "report_metadata": {
    "store_code": "000F03E44A",
    "analysis_date": "2025-10-12 14:30:00",
    "quality_score": 0.85
  },
  "store_overview": {
    "name": "육육**",
    "address": "서울 성동구 왕십리로4가길 9",
    "industry": "중식-딤섬/중식만두",
    "operating_months": 82.5,
    "store_age": "기존 매장"
  },
  "sales_analysis": {
    "trends": {
      "sales_amount": {
        "trend": "안정 추세",
        "stability": "안정적"
      }
    }
  },
  "customer_analysis": {
    "gender_distribution": {
      "male_ratio": 36.0,
      "female_ratio": 64.0
    }
  },
  "summary": {
    "key_insights": [
      "매출 트렌드: 안정 추세",
      "업종 내 순위: 순위 안정",
      "주 고객층: 여성 고객 중심"
    ],
    "recommendations": [...]
  }
}
```

### 2. 시각화 차트 (7개)
**위치**: `outputs/charts/`

1. `000F03E44A_sales_trend_{timestamp}.png` - 매출 추세 (4개 지표)
2. `000F03E44A_gender_pie_{timestamp}.png` - 성별 분포
3. `000F03E44A_age_pie_{timestamp}.png` - 연령대 분포  
4. `000F03E44A_detailed_pie_{timestamp}.png` - 세부 고객층
5. `000F03E44A_ranking_trend_{timestamp}.png` - 순위 변화
6. `000F03E44A_customer_trends_{timestamp}.png` - 고객층별 트렌드
7. `000F03E44A_new_returning_trends_{timestamp}.png` - 신규/재방문 고객

## 🔍 분석 내용

### 1. 점포 개요
- 매장 기본 정보 (코드, 상호명, 주소)
- 업종 분류 (대/중/소분류)
- 브랜드 정보
- 상권 정보
- 운영 기간 및 매장 연령 분류

### 2. 매출 분석
- 매출금액, 매출건수, 고객수, 객단가 트렌드
- 동일 업종 대비 성과
- 업종 내/상권 내 순위 변화
- 취소율 분석
- 배달 매출 비율

### 3. 고객층 분석
- 성별 분포
- 연령대 분포 (5개 그룹)
- 세부 고객층 (10개 카테고리)
- 신규/재방문 고객 비율
- 거주지/직장/유동인구 고객 분포

### 4. 상권 분석
- 동일 상권 내 매장 수
- 상권 평균 매출 트렌드
- 상권 해지가맹점 비율
- 상권 건강도 평가

### 5. 업종 분석
- 동일 업종 내 매장 수
- 업종 평균 매출 트렌드
- 업종 해지가맹점 비율
- 업종 건강도 평가
- 업종 평균 배달 비율

### 6. 권고사항
- 마케팅 전략 (타겟 고객층 기반)
- 운영 개선 (취소율, 배달)
- 경쟁력 강화 (순위 개선)
- 상권/업종 대응 전략

## 🐛 문제 해결

### "데이터 로드 실패"
```python
# 해결: 경로 확인
import pandas as pd
data_path = "store_data/final_merged_data.csv"
df = pd.read_csv(data_path)
print(f"데이터 로드 성공: {len(df)} 행")
```

### "매장 코드를 찾을 수 없습니다"
```python
# 해결: CSV에서 사용 가능한 매장 코드 확인
import pandas as pd
df = pd.read_csv("store_data/final_merged_data.csv")
codes = df['코드'].unique()
print(f"총 {len(codes)}개 매장")
print(f"예시: {codes[:5]}")
```

### "모듈을 찾을 수 없습니다"
```python
# 해결: 경로 추가
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

from report_builder.store_agent_module import StoreAgentModule
```

## 💡 팁

1. **데이터 캐싱**: 동일 인스턴스로 여러 매장 분석 시 데이터 재사용
2. **비동기 실행**: `await` 키워드 사용 필수
3. **에러 확인**: 항상 `result["error"]` 체크
4. **경로 설정**: 커스텀 데이터 경로 지정 가능

```python
# 커스텀 데이터 경로
agent = StoreAgentModule(data_path="/custom/path/data.csv")
```

## 📚 참고 문서

- **README.md**: 프로젝트 개요
- **USAGE_EXAMPLE.md**: 상세 사용 예제
- **CHANGELOG.md**: 변경 이력
- **test_store_agent.py**: 전체 테스트 코드

---

**버전**: 2.0.0  
**마지막 업데이트**: 2025-10-12

