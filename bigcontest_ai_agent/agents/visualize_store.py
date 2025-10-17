"""
Store 데이터 시각화 스크립트
Usage: python visualize_store.py <json_file_path>
"""
import json
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

# 한글 폰트 설정
try:
    plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows
except:
    try:
        plt.rcParams['font.family'] = 'AppleGothic'  # Mac
    except:
        plt.rcParams['font.family'] = 'DejaVu Sans'  # Fallback
plt.rcParams['axes.unicode_minus'] = False


def load_data(json_path: str) -> dict:
    """JSON 파일 로드"""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def visualize_all(data: dict, output_dir: Path):
    """전체 시각화"""
    store_name = data['store_overview']['name']
    store_code = data['store_overview']['code']
    
    output_dir.mkdir(exist_ok=True)
    
    # 1. 매장 개요
    plot_store_overview(data['store_overview'], output_dir)
    
    # 2. 성별 분포
    plot_gender_distribution(data['customer_analysis']['gender_distribution'], store_name, output_dir)
    
    # 3. 연령대별 분포
    plot_age_distribution(data['customer_analysis']['age_group_distribution'], store_name, output_dir)
    
    # 4. 상세 고객 비율 (Top 10)
    plot_detailed_customers(data['customer_analysis']['detailed_customer_ratios'], store_name, output_dir)
    
    # 5. 신규/재방문 고객
    plot_customer_types(data['customer_analysis']['customer_type_analysis'], store_name, output_dir)
    
    # 6. 고객 분포 (주거/직장/유동)
    plot_customer_distribution(
        data['customer_analysis']['customer_type_analysis']['customer_distribution'], 
        store_name, output_dir
    )
    
    # 7. 업종/상권 순위
    plot_rankings(data['sales_analysis']['rankings'], store_name, output_dir)
    
    # 8. 취소율 분석
    if 'cancellation_analysis' in data['sales_analysis']:
        plot_cancellation(data['sales_analysis']['cancellation_analysis'], store_name, output_dir)
    
    print(f"\n✅ 시각화 완료! 📊")
    print(f"📂 저장 위치: {output_dir}/")
    print(f"   생성된 그래프: 8개")


def plot_store_overview(data: dict, output_dir: Path):
    """1. 매장 개요"""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('off')
    
    # 제목
    title_text = f"📊 {data['name']} ({data['code']})"
    ax.text(0.5, 0.95, title_text, fontsize=24, fontweight='bold', 
            ha='center', va='top', transform=ax.transAxes)
    
    # 정보 테이블
    info = [
        ['항목', '내용'],
        ['상호명', data['name']],
        ['업종', data['industry']],
        ['브랜드', data['brand']],
        ['상권', data['commercial_area']],
        ['주소', data['address']],
        ['영업 개월 수', f"{data['operating_months']:.1f}개월"],
        ['데이터 기록', f"{data['record_months']}개월"],
        ['매장 상태', data['store_age']],
    ]
    
    # 표 그리기
    table = ax.table(cellText=info, cellLoc='left', loc='center',
                     colWidths=[0.25, 0.65],
                     bbox=[0.1, 0.1, 0.8, 0.75])
    
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 2.5)
    
    # 헤더 스타일
    for i in range(2):
        table[(0, i)].set_facecolor('#4ECDC4')
        table[(0, i)].set_text_props(weight='bold', color='white', fontsize=14)
    
    # 행 색상
    for i in range(1, len(info)):
        for j in range(2):
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#F0F0F0')
    
    plt.tight_layout()
    plt.savefig(output_dir / '1_매장개요.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ 1_매장개요.png")


def plot_gender_distribution(data: dict, store_name: str, output_dir: Path):
    """2. 성별 분포"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    labels = ['남성', '여성']
    values = [data['male_ratio'], data['female_ratio']]
    colors = ['#4A90E2', '#E94B3C']
    
    # 파이 차트
    wedges, texts, autotexts = ax1.pie(values, labels=labels, autopct='%1.1f%%',
                                         colors=colors, startangle=90,
                                         textprops={'fontsize': 14, 'fontweight': 'bold'})
    for autotext in autotexts:
        autotext.set_color('white')
    
    ax1.set_title('성별 비율', fontsize=16, fontweight='bold', pad=20)
    
    # 막대 그래프
    bars = ax2.bar(labels, values, color=colors, alpha=0.8, edgecolor='black', linewidth=2)
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom', fontsize=14, fontweight='bold')
    
    ax2.set_ylabel('비율 (%)', fontsize=12)
    ax2.set_ylim(0, max(values) + 10)
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    ax2.set_title('성별 비교', fontsize=16, fontweight='bold', pad=20)
    
    fig.suptitle(f'👥 {store_name} - 고객 성별 분포', fontsize=18, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(output_dir / '2_성별분포.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ 2_성별분포.png")


def plot_age_distribution(data: dict, store_name: str, output_dir: Path):
    """3. 연령대별 분포"""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    labels = list(data.keys())
    values = list(data.values())
    
    colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(labels)))
    bars = ax.bar(labels, values, color=colors, alpha=0.8, edgecolor='black', linewidth=2)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax.set_title(f'👥 {store_name} - 연령대별 고객 분포', fontsize=18, fontweight='bold', pad=20)
    ax.set_ylabel('비율 (%)', fontsize=14)
    ax.set_ylim(0, max(values) + 5)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(output_dir / '3_연령대별분포.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ 3_연령대별분포.png")


def plot_detailed_customers(data: dict, store_name: str, output_dir: Path):
    """4. 상세 고객 비율 (Top 10)"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # 정렬
    sorted_data = dict(sorted(data.items(), key=lambda x: x[1], reverse=True)[:10])
    labels = list(sorted_data.keys())
    values = list(sorted_data.values())
    
    # 성별에 따른 색상
    colors = ['#4A90E2' if '남' in label else '#E94B3C' for label in labels]
    
    bars = ax.barh(labels, values, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.3, bar.get_y() + bar.get_height()/2.,
                f'{width:.1f}%',
                ha='left', va='center', fontsize=11, fontweight='bold')
    
    ax.set_title(f'🎯 {store_name} - 상세 고객 세그먼트 (Top 10)', 
                 fontsize=18, fontweight='bold', pad=20)
    ax.set_xlabel('비율 (%)', fontsize=14)
    ax.set_xlim(0, max(values) + 3)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    # 범례
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#4A90E2', label='남성'),
        Patch(facecolor='#E94B3C', label='여성')
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(output_dir / '4_상세고객비율.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ 4_상세고객비율.png")


def plot_customer_types(data: dict, store_name: str, output_dir: Path):
    """5. 신규/재방문 고객"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # 비율 비교
    labels = ['신규 고객', '재방문 고객']
    values = [data['new_customers']['ratio'], data['returning_customers']['ratio']]
    trends = [data['new_customers']['trend'], data['returning_customers']['trend']]
    colors = ['#4ECDC4', '#FF6B6B']
    
    bars = ax1.bar(labels, values, color=colors, alpha=0.8, edgecolor='black', linewidth=2)
    
    for bar, trend in zip(bars, trends):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%\n({trend})',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax1.set_ylabel('비율 (%)', fontsize=12)
    ax1.set_ylim(0, max(values) + 3)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    ax1.set_title('신규 vs 재방문', fontsize=14, fontweight='bold', pad=15)
    
    # 파이 차트
    ax2.pie(values, labels=labels, autopct='%1.1f%%', colors=colors,
            startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'})
    ax2.set_title('고객 유형 비율', fontsize=14, fontweight='bold', pad=15)
    
    fig.suptitle(f'🔄 {store_name} - 고객 유형 분석', fontsize=18, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(output_dir / '5_고객유형.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ 5_고객유형.png")


def plot_customer_distribution(data: dict, store_name: str, output_dir: Path):
    """6. 고객 분포 (주거/직장/유동)"""
    fig, ax = plt.subplots(figsize=(10, 7))
    
    labels = ['주거지', '직장지', '유동인구']
    values = [data['residential'], data['workplace'], data['floating']]
    colors = ['#FF6B6B', '#4ECDC4', '#FFA07A']
    
    # 도넛 차트
    wedges, texts, autotexts = ax.pie(values, labels=labels, autopct='%1.1f%%',
                                        colors=colors, startangle=90,
                                        wedgeprops=dict(width=0.5, edgecolor='white', linewidth=3),
                                        textprops={'fontsize': 14, 'fontweight': 'bold'})
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(16)
    
    # 중앙 텍스트
    ax.text(0, 0, '고객\n분포', ha='center', va='center', 
            fontsize=18, fontweight='bold')
    
    ax.set_title(f'📍 {store_name} - 고객 분포 (주거/직장/유동)', 
                 fontsize=18, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(output_dir / '6_고객분포.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ 6_고객분포.png")


def plot_rankings(data: dict, store_name: str, output_dir: Path):
    """7. 업종/상권 순위"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    labels = ['업종 내 순위', '상권 내 순위']
    values = [data['industry_rank']['average'], data['commercial_rank']['average']]
    trends = [data['industry_rank']['trend'], data['commercial_rank']['trend']]
    
    # 순위는 낮을수록 좋으므로 색상 반전
    colors = ['#4ECDC4' if '개선' in trend or '상승' in trend else '#FF6B6B' for trend in trends]
    
    bars = ax.barh(labels, values, color=colors, alpha=0.8, edgecolor='black', linewidth=2)
    
    for bar, trend in zip(bars, trends):
        width = bar.get_width()
        ax.text(width + 2, bar.get_y() + bar.get_height()/2.,
                f'{width:.1f}위\n({trend})',
                ha='left', va='center', fontsize=12, fontweight='bold')
    
    ax.set_xlabel('평균 순위', fontsize=12)
    ax.set_xlim(0, max(values) + 20)
    ax.invert_xaxis()  # 순위 반전 (낮은 순위가 오른쪽)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_title(f'🏆 {store_name} - 순위 분석 (낮을수록 우수)', 
                 fontsize=18, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(output_dir / '7_순위분석.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ 7_순위분석.png")


def plot_cancellation(data: dict, store_name: str, output_dir: Path):
    """8. 취소율 분석"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # 취소율 등급
    avg_grade = data['average_grade']
    grade_color = '#4ECDC4' if avg_grade < 3 else '#FFA07A' if avg_grade < 5 else '#FF6B6B'
    
    ax1.bar(['취소율 등급'], [avg_grade], color=grade_color, alpha=0.8, 
            edgecolor='black', linewidth=2, width=0.5)
    ax1.text(0, avg_grade, f'{avg_grade:.1f}',
            ha='center', va='bottom', fontsize=20, fontweight='bold')
    ax1.set_ylim(0, 10)
    ax1.set_ylabel('등급 (낮을수록 우수)', fontsize=12)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    ax1.set_title('평균 취소율 등급', fontsize=14, fontweight='bold')
    
    # 등급 분포
    grades = list(data['grade_distribution'].keys())
    counts = list(data['grade_distribution'].values())
    colors_dist = ['#4ECDC4' if float(g) < 3 else '#FFA07A' if float(g) < 5 else '#FF6B6B' 
                   for g in grades]
    
    bars = ax2.bar(grades, counts, color=colors_dist, alpha=0.8, edgecolor='black', linewidth=2)
    
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}개월',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax2.set_xlabel('취소율 등급', fontsize=12)
    ax2.set_ylabel('개월 수', fontsize=12)
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    ax2.set_title('등급별 분포', fontsize=14, fontweight='bold')
    
    # 추천사항
    fig.text(0.5, 0.02, f"💡 {data['recommendation']}", 
             ha='center', fontsize=12, style='italic',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    fig.suptitle(f'📊 {store_name} - 취소율 분석', fontsize=18, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.1)
    plt.savefig(output_dir / '8_취소율분석.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ 8_취소율분석.png")


def visualize_latest_from_folder(folder_path: str = "test_output") -> bool:
    """
    test_output 폴더에서 최신 store_*.json 파일을 찾아 시각화
    
    Returns:
        성공 여부
    """
    from glob import glob
    
    folder = Path(folder_path)
    store_files = sorted(glob(str(folder / "store_*.json")))
    
    if not store_files:
        print("[Store Viz] store_*.json 파일 없음")
        return False
    
    json_path = Path(store_files[-1])  # 최신 파일
    
    try:
        # 데이터 로드
        data = load_data(json_path)
        store_code = data['store_overview']['code']
        
        # 출력 디렉토리
        output_dir = json_path.parent / f"store_viz_{store_code}"
        
        # 시각화
        visualize_all(data, output_dir)
        return True
    except Exception as e:
        print(f"[Store Viz] Error: {e}")
        return False


def main():
    """메인 실행"""
    if len(sys.argv) < 2:
        # 인자 없으면 test_output에서 자동 찾기
        print("[Store] test_output에서 최신 파일 찾는 중...")
        success = visualize_latest_from_folder("test_output")
        if success:
            print("[Store] 시각화 완료!")
        return
    
    json_path = sys.argv[1]
    
    # 와일드카드 처리
    if '*' in json_path:
        from glob import glob
        files = glob(json_path)
        if not files:
            print(f"파일을 찾을 수 없습니다: {json_path}")
            return
        json_path = sorted(files)[-1]
        print(f"최신 파일 선택: {json_path}")
    
    json_path = Path(json_path)
    
    if not json_path.exists():
        print(f"파일이 없습니다: {json_path}")
        return
    
    # 데이터 로드
    data = load_data(json_path)
    store_code = data['store_overview']['code']
    
    # 출력 디렉토리
    output_dir = json_path.parent / f"store_viz_{store_code}"
    
    # 시각화
    visualize_all(data, output_dir)
    print("[Store] 완료!")


if __name__ == "__main__":
    main()

