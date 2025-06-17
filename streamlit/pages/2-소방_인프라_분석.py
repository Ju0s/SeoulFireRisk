# -*- coding:utf-8 -*-
import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
from shapely import wkt
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
from folium.features import DivIcon
from utils.data_loader import load_data
from utils.ui_helpers import setup_sidebar_links, display_season_colors, create_html_button


# 페이지 설정
st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_icon='🚒')
setup_sidebar_links()


# 데이터 로드
data = load_data("data/서울시_비상소화장치_좌표_구동.csv")
grid = load_data("data/seoul_500_grid_water.csv", encoding='euc-kr')
df = load_data("data/서울시_소방시설_좌표_구동.csv")
time = load_data("data/화재출동_골든타임.csv")

data['geometry'] = data['geometry'].apply(wkt.loads)  
_gdf = gpd.GeoDataFrame(data, geometry='geometry')


# 시각화 함수
@st.cache_data
def create_folium_map(df):
    m = folium.Map(location=[37.5642135, 127.0016985], zoom_start=11)
    colors = {
        '소방서': 'red',
        '안전센터': 'blue',
        '구조대': 'orange',
        '소방항공대': 'black',
        '특수대응단': 'yellow'
    }
    for index, row in df.iterrows():
        popup_content = f"<b>서ㆍ센터명:</b> {row['서ㆍ센터명']}<br><b>유형구분명:</b> {row['유형구분명']}"
        folium.CircleMarker(
            location=[row['위도'], row['경도']],
            radius=8,
            color=colors[row['유형구분명']],
            fill=True,
            fill_color=colors[row['유형구분명']],
            fill_opacity=0.5,
            popup=folium.Popup(popup_content, max_width=300)
        ).add_to(m)
    folium_static(m)

def folium_map_with_clusters(gdf):
    m = folium.Map(location=[37.5665, 126.9780], tiles='OpenStreetMap', zoom_start=11)
    marker_cluster = MarkerCluster().add_to(m)
    for idx, row in gdf.iterrows():
        tooltip = f"{row['구']}, {row['동']}"
        folium.Marker(
            location=[row['geometry'].y, row['geometry'].x],
            tooltip=tooltip,
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(marker_cluster)
    folium_static(m)

@st.cache_data
def visualize_fire_water(grid, column_name='소방용수_수'):
    grid['geometry'] = gpd.GeoSeries.from_wkt(grid['geometry'])
    gdf = gpd.GeoDataFrame(grid, geometry='geometry')
    gdf.crs = "EPSG:4326"

    map_fw = folium.Map(location=[37.564, 126.997], zoom_start=11, tiles='OpenStreetMap')

    def color_scale(amount):
        if amount == 30:
            return '#01579B' 
        elif amount == 20:
            return '#0277BD' 
        elif amount == 10:
            return '#0288D1' 
        elif amount in[8, 9]:
            return '#039BE5'
        elif amount in[6, 7]:
            return '#03A9F4'  
        elif amount == 5:
            return '#29B6F6'  
        elif amount == 4:
            return '#4FC3F7'  
        elif amount == 3:
            return '#81D4FA'  
        elif amount == 2:
            return '#B3E5FC'  
        elif amount == 1:
            return '#E1F5FE' 
        else:
            return '#808080' 

    folium.GeoJson(
        gdf,
        style_function=lambda feature: {
            'fillColor': color_scale(feature['properties'][column_name]),
            'color': 'black',
            'weight': 0.1,
            'fillOpacity': 0.7,
        }
    ).add_to(map_fw)
    folium_static(map_fw)

@st.cache_data
def fire_incidents_map(df):
    df_filtered = df.dropna(subset=['위도', '경도'])
    map_seoul = folium.Map(location=[37.5665, 126.9780], zoom_start=11)

    def create_popup_html(row):
        return f'''
        <html>
            <head><style>
                .popup {{
                    font-family: Arial, sans-serif;
                    font-size: 12px;
                    color: #333333;
                }}
                .title {{
                    font-weight: bold;
                    color: #0078A8;
                    margin-bottom: 5px;
                }}
                .info {{
                    margin-bottom: 2px;
                }}
            </style></head>
            <body>
                <div class="popup">
                    <div class="title">화재 정보</div>
                    <div class="info">사망수: {row['사망수']}, 부상자수: {row['부상자수']}</div>
                    <div class="info">재산피해금액: {row['재산피해금액']}만원</div>
                    <div class="info">출동소요시간: {row['출동소요시간']}초</div>
                    <div class="info">화재진압시간: {row['화재진압시간']}초</div>
                    <div class="info">위치: {row['시군구명']}, {row['읍면동명']}</div>
                    <div class="info">계절: {row['계절']}, 시간대: {row['시간대']}</div>
                    <div class="info">화재발생일시: {row['화재발생일시']}</div>
                </div>
            </body>
        </html>
        '''

    def get_color(season):
        if season == '봄':
            return 'green'
        elif season == '여름':
            return 'red'
        elif season == '가을':
            return 'orange'
        elif season == '겨울':
            return 'blue'
        else:
            return 'gray'  

    for idx, row in df_filtered.iterrows():
        color = get_color(row['계절'])
        tooltip_text = f'출동소요시간: {row["출동소요시간"]}초'
        popup_html = create_popup_html(row)
        popup = folium.Popup(popup_html, max_width=300)

        folium.CircleMarker(
            [row['위도'], row['경도']],
            radius=5,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            tooltip=tooltip_text,
            popup=popup
        ).add_to(map_seoul)

    folium_static(map_seoul, width=800)


# 메인
def main():
    st.header('서울시 소방 인프라 분석', help='이 페이지에서는 서울시에 위치한 소방 관련 시설의 위치 정보와 소방 서비스의 접근성을 확인할 수 있습니다.', divider="gray")
    col1, col2 = st.columns([7, 3])
    
    with col1:
        with st.container(border=True, height=750):
            st.markdown('<h4>서울시 소방 인프라 위치 시각화</h4>', unsafe_allow_html=True) 
            tab1, tab2, tab3 = st.tabs(["소방서 및 안전센터", "비상 소화장치", "소방용수"])

            with tab1:
                gu_options = ['서울시'] + sorted(df['구'].unique().tolist())
                col_gu, col_dong = st.columns(2)
                with col_gu:
                    selected_gu = st.selectbox('자치구 선택', gu_options, index=0)

                if selected_gu == '서울시':
                    filtered_df = df
                else:
                    with col_dong:
                        dong_options = [f'{selected_gu} 전체'] + sorted(df[df['구'] == selected_gu]['동'].unique().tolist())
                        selected_dong = st.selectbox('동 선택', dong_options, index=0)
                        if selected_dong == f'{selected_gu} 전체':
                            filtered_df = df[df['구'] == selected_gu]
                        else:
                            filtered_df = df[(df['구'] == selected_gu) & (df['동'] == selected_dong)]

                create_folium_map(filtered_df)

            with tab2:
                sig_options = ['서울시'] + sorted(_gdf['구'].unique().tolist())
                col1_sig, col2_emd = st.columns([1,1])
                with col1_sig:
                    selected_sig = st.selectbox('자치구 선택:', sig_options, index=0)

                if selected_sig == '서울시':
                    filtered_gdf = _gdf
                else:
                    with col2_emd:
                        emd_options = [f'{selected_sig} 전체'] + sorted(_gdf[_gdf['구'] == selected_sig]['동'].unique().tolist())
                        selected_emd = st.selectbox('동 선택:', emd_options, index=0)
                    if selected_emd == f'{selected_sig} 전체':
                        filtered_gdf = _gdf[_gdf['구'] == selected_sig]
                    else:
                        filtered_gdf = _gdf[(_gdf['구'] == selected_sig) & (_gdf['동'] == selected_emd)]

                folium_map_with_clusters(filtered_gdf)

            with tab3:
                with st.popover("💡 **시각화 기준 설명**"):
                    st.markdown("""
                    - **소방용수의 분포**: 이 지도상의 색상은 소방용수의 분포를 나타냅니다. 색이 **더 진할수록 소방용수의 양이 많음**을 의미합니다.
                    - **소화용수 접근성**: 서울시 내 대부분의 지역에서는 500미터 이내에 최소 한 개 이상의 소화용수 점이 위치하고 있어, 접근성이 높습니다.
                    - **높은 소방용수 밀집 지역**: 일부 지역에서는 소방용수 점의 수가 100개를 넘는 경우도 있으며, 이는 해당 지역의 소방 안전 인프라가 잘 갖추어져 있음을 나타냅니다.
                    """)
                visualize_fire_water(grid, column_name='소방용수_수')
    
    with col2:
        with st.container(border=True, height=750):
            create_html_button("소방 복지 및 정책")
            st.divider()
            st.link_button("일일 화재 현황 📈", "https://www.nfds.go.kr/dashboard/quicklook.do", use_container_width=True)
            st.link_button("화재예방법 🛡️", "https://www.nfds.go.kr/bbs/selectBbsList.do?bbs=B04", use_container_width=True)
            st.link_button("소화기 사용요령 🔥", "https://www.nfds.go.kr/bbs/selectBbsDetail.do?bbs=B06&bbs_no=7753&pageNo=1", use_container_width=True)
            st.link_button("옥내소화전 사용방법 🚒", "https://www.nfds.go.kr/bbs/selectBbsDetail.do?bbs=B06&bbs_no=7756&pageNo=1", use_container_width=True)
            st.link_button("소화기 사용기한 확인 ⏳", "https://bigdata-119.kr/service/frxtInfr#tab04", use_container_width=True)
            st.link_button("주택용 소방시설 설치 🏠", "https://fire.seoul.go.kr/pages/cnts.do?id=4808", use_container_width=True)
            st.link_button("소방시설 불법행위신고 🚫", "https://fire.seoul.go.kr/pages/cnts.do?id=4113", use_container_width=True)
            st.link_button("안전신문고 📢", "https://www.safetyreport.go.kr/#safereport/safereport", use_container_width=True)
            st.link_button("소방기술민원센터 💡", "https://www.safeland.go.kr/safeland/index.do", use_container_width=True)
            st.link_button("칭찬하기 👏", "https://fire.seoul.go.kr/pages/cnts.do?id=184", use_container_width=True)

    with st.container(border=True, height=650):
        st.markdown('<h4>소방 서비스 접근성 분석: 골든타임 초과 건물화재사고</h4>', unsafe_allow_html=True) 
        col1, col2 = st.columns([2, 8])
        with col1:
            with st.popover("⏰ **골든타임**", use_container_width=True):
                st.markdown('소방차 골든타임은 **7분**입니다. 골든타임 내에 소방대원이 도착하여 화재를 진압할 수 있다면, 인명 및 재산 피해를 최소화할 수 있습니다.')
            display_season_colors()
        with col2:
            fire_incidents_map(time)

if __name__ == "__main__":
    main()