# -*- coding:utf-8 -*-
import streamlit as st
import pandas as pd
import os
from utils.ui_helpers import setup_sidebar_links


# 페이지 설정
st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_icon='💬')
setup_sidebar_links()


# 메인 
def main():
    st.header('건의사항 페이지', divider='gray')
    st.markdown("""
    대시보드를 개선해 나갈 수 있도록 **건의사항을 남겨주세요🙇‍♂️**
    - 🛠 **기능 개선이 필요한 부분**
    - ✨ **추가되었으면 하는 새로운 기능**
    - 🐞 **사용 중 발견한 버그나 오류**
    """)

    file_path = 'recommendations/건의사항.csv'  

    with st.container(border=True):
        anonymous = st.checkbox('익명으로 제출하기')
        if anonymous:
            username = "익명"
            email = "익명"
        else:
            username = st.text_input('이름', key='username')  
            email = st.text_input('이메일', key='email')

        category = st.selectbox('카테고리', ['기능 개선', '새 기능 제안', '버그 신고', '기타'], key='category')
        suggestion = st.text_area('건의사항', key='suggestion')
        file = st.file_uploader("문제를 보여줄 스크린샷이나 문서 첨부", type=['png', 'jpg', 'jpeg', 'pdf'], key='file')

        if file is not None:
            specific_file_path = f'recommendations/{file.name}'
            with open(specific_file_path, "wb") as f:
                f.write(file.getbuffer())
            st.success('파일이 성공적으로 업로드되었습니다.')
            file_info = specific_file_path
        else:
            file_info = "첨부파일 없음"

        submit_button = st.button('제출')

    if submit_button:
        new_data = {'이름': username, '이메일': email, '카테고리': category, '건의사항': suggestion, '파일': file_info}
        df = pd.DataFrame([new_data])
        if os.path.exists(file_path):
            df.to_csv(file_path, mode='a', header=False, index=False)
        else:
            df.to_csv(file_path, mode='w', header=True, index=False)
        st.success('건의사항이 성공적으로 제출되었습니다.')

    if os.path.exists(file_path):
        df_건의사항 = pd.read_csv(file_path)
        st.divider()
        if '건의사항' in df_건의사항.columns:
            selected_indices = st.multiselect(
                '해결된 건의사항을 선택하세요.', 
                df_건의사항.index, 
                format_func=lambda x: df_건의사항.loc[x, '건의사항']
            )
            if st.button('선택 항목 삭제'):
                df_건의사항 = df_건의사항.drop(index=selected_indices)
                df_건의사항.to_csv(file_path, index=False)
                st.success('선택한 항목이 삭제되었습니다.')
            st.dataframe(df_건의사항, width=800, height=300)

if __name__ == "__main__":
    main()