import pyrosm
import geopandas as gpd
import os

# motorway	    고속도로(고속도로 전용) — 제한된 진입/고속 주행	예 (포함)
# trunk	        고속도로급(주도로)	예
# primary	    주요 간선도로	예
# secondary	    이차 간선도로	예
# tertiary	    삼차도로(작은 도시/마을 연결로)	예
# unclassified	분류되지 않은 작은 연결 도로	일반적으로 예(지역에 따라)
# residential	주거지역 도로	보통 포함되지만, driving+service 등 필터 정책 따라 다름
# service	    주차장 진입로나 서비스도로 (driveway, parking_aisle 등)	보통 제외(서비스 중 특정 값은 허용)
# motorway_link, trunk_link, primary_link, ...	위 도로들의 진입/출구 연결(램프)	예
# living_street	생활도로(주로 보행우선/저속)	포함(저속도로)
# pedestrian	보행자 전용(광장/쇼핑가)	보통 제외
# cycleway	    자전거 전용로	제외
# footway	    보행자 전용 도로	제외
# track	        임도(농로 등)	제외(비포장/비주류 도로류)
# path	        비특정 경로 (발자국 등)	제외
# busway / bus_guideway	버스 전용 차로/가이드웨이	보통 제외 (특수)
# raceway	    트랙(레이싱)	제외
# road	        이름이 지정되지 않은 ‘도로’ 임시값	경우에 따라 포함/제외
# construction / proposed	공사중/예정	제외

# others (node features) e.g., traffic_signals, bus_stop, crossing, turning_circle, etc.	
# 도로 관련 노드(정류장·신호등 등) — highway key가 node에 사용	일반적으로 edge(ways) 분석과는 별개로 노드로 표현됨

# 1. PBF 파일 경로 및 출력 파일명 설정
pbf_file_path = "south-korea-251201.osm.pbf" 
output_filename = "korea_major_roads_filtered.geojson"

# 2. Pyrosm 객체 초기화
try:
    osm = pyrosm.OSM(pbf_file_path)
    print(f"{pbf_file_path}' 파일 로드 완료.")
except FileNotFoundError:
    print(f"오류: {pbf_file_path} 파일을 찾을 수 없습니다. 파일명을 확인해주세요.")
    exit()

print("주요 도로 네트워크 필터링 및 추출 중... (tags 인수 사용)")

major_roads = osm.get_network(
    network_type="driving",
)

filter_atributes = osm.get_data_by_custom_criteria('highway', ['motorway', 'trunk', 'primary', 'secondary', 'tertiary'])

print(f"\n--- 추출 결과 요약 ---")
print(f"전체 추출된 도로 구간(Edge) 개수: {len(major_roads)}")

# 5. GeoJSON 파일로 저장 (GitHub 공유용)
try:
    # GeoJSON으로 저장하여 파일 크기를 줄입니다.
    major_roads.to_file(output_filename, driver='GeoJSON', encoding="utf-8")
    
    # 6. 저장된 파일 크기 확인
    file_size_bytes = os.path.getsize(output_filename)
    
    print(f"\n--- 최종 저장 완료 ---")
    print(f"저장된 파일명: {output_filename}")

except Exception as e:
    print(f"GeoJSON 저장 중 오류 발생: {e}")

# 7. (선택적) GeoDataFrame 내용 미리보기
print("\n[필터링된 도로 데이터 상위 5개 행]")
print(major_roads[['id', 'name', 'highway', 'lanes', 'maxspeed', 'length']].head().to_string())