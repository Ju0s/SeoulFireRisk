# -*- coding:utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from utils.data_loader import load_data
from utils.ui_helpers import setup_sidebar_links


# 페이지 설정
st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_icon="🔥")

setup_sidebar_links()

# 데이터 로드
df = load_data("data/18_23_서울시_화재.csv")
dong = load_data("data/동별_화재발생_장소_2021_2022.csv")

seoul_total = dong.drop(['자치구', '동'], axis=1).sum().rename('서울시 전체')
seoul_total['자치구'] = '서울시 전체'
seoul_total['동'] = '전체'

dong = pd.concat([dong, pd.DataFrame([seoul_total])], ignore_index=True)
dong = dong.drop(columns=["Unnamed: 0"])

# 시각화 함수 정의
def visualize_trend_by_district_with_tabs(df):
    columns = ['화재건수', '사망', '부상', '인명피해 계', '부동산피해(천원)', '동산피해(천원)', '재산피해(천원)', '재산피해/건당(천원)']
    years = [f'{year}' for year in range(18, 24)]
    selected_districts = []

    with st.container(border=True, height=650):
        option = st.radio("**화재 추세 분석**", ("서울시 전체", "각 구별로 비교하기"), horizontal=True)

        if option == "서울시 전체":
            df = df[df['자치구'] == '서울시']
        else:
            districts_options = df['자치구'].unique().tolist()
            if '서울시' in districts_options:
                districts_options.remove('서울시')
            default_districts = [district for district in ['강북구', '송파구', '영등포구'] if district in districts_options]
            selected_districts = st.multiselect('**자치구 선택**', options=districts_options, default=default_districts)
            if not selected_districts:
                st.error('적어도 하나 이상의 자치구를 선택해야 합니다.', icon="🚨")
                return
            df = df[df['자치구'].isin(selected_districts)]

        if selected_districts or option == "서울시 전체":
            tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(columns)
            tabs = [tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8]

            for tab, column in zip(tabs, columns):
                with tab:
                    data_list = []
                    for year in years:
                        for index, row in df.iterrows():
                            data_list.append({'자치구': row['자치구'], '연도': f'20{year}', column: row[f'{year}_{column}']})

                    new_df = pd.DataFrame(data_list)
                    if option == "서울시 전체" and column == "화재건수":
                        title = f'서울시 전체 {column} 추세 (2018-2023)'
                        fig = px.line(new_df, x='연도', y=column, color='자치구', title=title)
                        fig.update_layout(height=350)
                        col1, col2 = st.columns([4,5])
                        with col1:
                            st.plotly_chart(fig, use_container_width=True)
                        with col2:
                            st.markdown('**2024년 서울시 월별 화재건수 예측**')
                            st.image('data/사진/2024_서울시_월별화재건수_예측.png')
                    else:
                        title = f'{("서울시 전체 " if option == "서울시 전체" else "")}{column} 추세 (2018-2023)'
                        fig = px.line(new_df, x='연도', y=column, color='자치구', title=title)
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)

def display_treemap(df):
    col1, col2 = st.columns(2)
    with col1:
        selected_gu = st.selectbox('자치구 선택', options=df['자치구'].unique(), key='자치구_select')
        df_filtered_by_gu = df[df['자치구'] == selected_gu]
    with col2:
        selected_dong = st.selectbox('동 선택', options=df_filtered_by_gu['동'].unique(), key='동_select_dong')
        df_filtered_by_dong = df_filtered_by_gu[df_filtered_by_gu['동'] == selected_dong]

    df_agg = df_filtered_by_dong.melt(id_vars=['자치구', '동'], value_vars=df.columns[3:], var_name='장소 유형', value_name='건수')
    df_agg = df_agg.groupby(['자치구', '동', '장소 유형']).sum().reset_index()
    df_agg = df_agg[df_agg['건수'] > 0]

    colors = ['#F25E6B', '#F2C744', '#A1BF34', '#EEDFE2', '#FCE77C', '#E2D0F8', '#DCE2F0', '#F2EFBB', '#D5D971', '#6779A1', '#9B7776','#1BBFBF', '#D94B2B', '#D98F89', '#FFDEDC', '#ACC7B4']

    fig = px.treemap(df_agg, path=['자치구', '동', '장소 유형'], values='건수', color='장소 유형', hover_data=['건수'], color_discrete_sequence=colors)
    fig.update_layout(title='동별 화재 장소유형 트리맵', font=dict(family="Arial, sans-serif", size=14, color="black"))
    st.plotly_chart(fig, use_container_width=True)

def visualize_facilities(df_selected):
    fig = go.Figure()
    colors = ['#F25E6B', '#F2C744', '#A1BF34', '#EEDFE2', '#FCE77C', '#E2D0F8', '#DCE2F0', '#F2EFBB', '#D5D971', '#6779A1', '#9B7776','#1BBFBF', '#D94B2B', '#D98F89', '#FFDEDC', '#ACC7B4']
    facility_types = ['단독주택', '공동주택', '기타주택', '학교', '일반업무', '판매시설', '숙박시설', '종교시설', '의료시설', '공장 및 창고', '작업장', '위락오락시설', '음식점', '일상서비스시설', '기타']
    color_map = dict(zip(facility_types, colors))

    for column in df_selected.columns[2:]:
        total = df_selected[column].sum()
        fig.add_trace(go.Bar(x=[column], y=[total], marker_color=color_map.get(column), showlegend=False))

    fig.update_layout(title="시설 유형별 총계", xaxis_title="시설 유형", yaxis_title="총계")
    st.plotly_chart(fig, use_container_width=True)


# 메인
def main():
    st.header('서울시 화재사고 현황', help='이 페이지에서는 서울시에서 발생한 최근 화재 사고에 대한 통계와 지역 및 장소 유형별 분석을 제공합니다.', divider='gray')
    st.button("**기간: 2024-02-24~2024-03-25**", disabled=True)

    col1, col2, col3, col4 = st.columns([1,1,1,1])
    with col1:
        with st.container(height=130, border=True):
            st.metric(label="**화재 건수 🔥**", value='465건', delta='- 64건', delta_color="inverse", help = '전년동기: 529건')
    with col2:
        with st.container(height=130, border=True):
            st.metric(label="**인명피해 🚑**", value='21명', delta='+ 9명', delta_color="inverse", help='사망자 수 2명, 부상자 수 19명 | 전년동기: 인명피해 12명, 사망자 수 2명, 부상자 수 10명')
    with col3:
        with st.container(height=130, border=True):
            st.metric(label="**총 재산피해 💸**", value='36.79억', delta='+ 17.79억', delta_color="inverse", help = '부동산피해 567,425 천원, 동산피해 3,111,368 천원 | 전년동기: 총 재산피해 1,899,163 천원, 부동산피해 511,694 천원, 동산피해 1,387,469 천원')
    with col4:
        with st.container(height=130, border=True):
            st.metric(label="**재산 피해/건당 💰**", value='7,911 천원', delta='+ 4,321 천원', delta_color="inverse", help = '전년동기: 3,590 천원')

    visualize_trend_by_district_with_tabs(df)

    with st.container(border=True, height=700):
        st.markdown('<h4>화재 장소 유형 분석</h4>', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["트리맵으로 보기", "막대 그래프로 보기"])
        with tab1:
            display_treemap(dong)
        with tab2:
            selected_gu = st.selectbox("자치구 선택", options=dong['자치구'].unique())
            df_selected = dong[dong['자치구'] == selected_gu]
            visualize_facilities(df_selected)

if __name__ == "__main__":
    main()
