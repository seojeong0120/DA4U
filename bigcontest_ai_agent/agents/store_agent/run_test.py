"""
Store Agent Module 실행 테스트
"""
import asyncio
import logging
from report_builder.store_agent_module import StoreAgentModule, StoreAgentState

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

async def main():
    print("\n" + "="*60)
    print("Store Agent Module 테스트")
    print("="*60 + "\n")
    
    # 초기화
    agent = StoreAgentModule()
    print(f"✅ 모듈 초기화 완료")
    print(f"   데이터 경로: {agent.data_path}\n")
    
    # State 준비
    state: StoreAgentState = {
        "user_query": "000F03E44A 매장 분석해줘",
        "user_id": "test_user",
        "session_id": "test_001",
        "context": {},
        "store_analysis": None,
        "error": None
    }
    
    print("📊 분석 실행 중...")
    print("-"*60)
    
    # 분석 실행
    result = await agent.execute_analysis_with_self_evaluation(state)
    
    print("-"*60)
    
    if result["error"]:
        print(f"\n❌ 에러: {result['error']}")
        return
    
    # 결과 출력
    analysis = result["store_analysis"]
    overview = analysis['analysis_result']['store_overview']
    evaluation = analysis['evaluation']
    
    print("\n✅ 분석 완료!\n")
    print("="*60)
    print("📊 분석 결과")
    print("="*60)
    print(f"\n🏪 매장 정보:")
    print(f"   코드: {overview['code']}")
    print(f"   상호명: {overview['name']}")
    print(f"   주소: {overview['address']}")
    print(f"   업종: {overview['industry']}")
    print(f"   운영: {overview['operating_months']:.1f}개월 ({overview['store_age']})")
    
    print(f"\n⭐ 품질 점수:")
    print(f"   종합: {evaluation['quality_score']:.1%}")
    print(f"   완성도: {evaluation['completeness']:.1%}")
    print(f"   정확성: {evaluation['accuracy']:.1%}")
    
    print(f"\n📁 생성된 파일:")
    print(f"   리포트: {analysis['output_file_path']}")
    
    charts = analysis['json_output']['visualizations']['chart_files']
    print(f"   차트: {sum(1 for p in charts.values() if p)}개 생성")
    
    print("\n" + "="*60)
    print("🎉 테스트 완료!")
    print("="*60 + "\n")

if __name__ == "__main__":
    asyncio.run(main())

