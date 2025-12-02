import geopandas as gpd
import pandas as pd
import os

# 1. 파일 경로 설정
# 이전 단계에서 생성된 GeoJSON 파일사용
input_geojson_file = "korea_major_roads_filtered.geojson"
output_csv_file = "korea_roads_with_residential_features.csv" # 파일명 변경

# 2. GeoJSON 파일 로드
try:
    major_roads_gpd = gpd.read_file(input_geojson_file)
    print(f"{input_geojson_file}' 파일 로드 완료. (총 {len(major_roads_gpd)}개 도로 구간)")
except FileNotFoundError:
    print(f"오류: {input_geojson_file} 파일을 찾을 수 없습니다.")
    exit()

# 3. GeoPandas를 이용한 명시적 재필터링
# 프로젝트 목표에 따라 포함할 모든 highway=도로/경로타입 등급을 정의
major_road_types_with_res = [
    "motorway",     #고속도로(고속도로 전용) — 제한된 진입/고속 주행
    "trunk",        #고속도로급(주도로)
    "primary",      #주요 간선도로
    "secondary",    #이차 간선도로
    "tertiary",     #삼차도로(작은 도시/마을 연결로)
    "unclassified", #분류되지 않은 작은 연결 도로
    "residential",   #주거지역 도로
    "construction",  #공사중
    "proposed"       #공사예정       
]

# 'highway' 컬럼의 값이 major_road_types_with_res 리스트에 포함된 행만 선택
filtered_roads = major_roads_gpd[
    major_roads_gpd['highway'].isin(major_road_types_with_res)
].copy()

print(f"'motorway'부터 'residential'까지 명시적 재필터링 완료.")
print(f"최종 {len(filtered_roads)}개 도로 구간 선택.")


# 4. Pandas DataFrame으로 변환 및 컬럼 준비
# Geometry를 WKT(Well-Known Text) 텍스트로 변환하여 CSV에 지리정보를 보존합니다.
filtered_roads['geometry_wkt'] = filtered_roads['geometry'].apply(lambda geom: geom.wkt)

# DataFrame으로 변환 (geometry 객체 컬럼 삭제)
final_df = filtered_roads.drop(columns=['geometry'])

# GAT 모델 Features로 사용할 핵심 속성 컬럼 선택
columns_to_save = [
    'id',
    'name', 
    'highway', 
    'length', 
    'lanes', 
    'maxspeed', 
    'oneway', 
    'geometry_wkt' # 각 노드의 지리정보(위도/경도)
]

# 선택한 컬럼만 남깁니다.
final_df = final_df[columns_to_save]


# 5. CSV 파일로 저장
try:
    final_df.to_csv(output_csv_file, index=False, encoding="utf-8-sig")
    
    print(f"\n--- 최종 저장 완료 ---")
    print(f"필터링된 도로 특징 데이터가 '{output_csv_file}' CSV 파일로 저장되었습니다.")
    
except Exception as e:
    print(f"CSV 저장 중 오류 발생: {e}")