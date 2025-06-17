import streamlit as st
import pandas as pd
import geopandas as gpd

import pandas as pd
import geopandas as gpd
import streamlit as st

# 데이터 로드 함수
@st.cache_data
def load_data(file_path, encoding=None):

    # Determine the file type from the file extension
    file_type = file_path.split('.')[-1].lower()

    if file_type == 'csv':
        if encoding:
            return pd.read_csv(file_path, encoding=encoding)
        else:
            return pd.read_csv(file_path)
    elif file_type == 'shp':
        return gpd.read_file(file_path)
    elif file_type in ['xlsx', 'xls']:
        return pd.read_excel(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

@st.cache_data
def get_locations_data():

    locations = [
        (37.5085071, 127.0825862, '잠실동', 'https://github.com/suhyeon0325/SeoulFireDash/blob/main/data/%EC%82%AC%EC%A7%84/01_%EC%A2%8C%ED%91%9C.png?raw=true', 1),
        (37.50511389, 127.0817572, '잠실동', 'https://github.com/suhyeon0325/SeoulFireDash/blob/main/data/%EC%82%AC%EC%A7%84/02_%EC%A2%8C%ED%91%9C.png?raw=true', 1),
        (37.50231025, 127.0901942, '삼전동', 'https://github.com/suhyeon0325/SeoulFireDash/blob/main/data/%EC%82%AC%EC%A7%84/03_%EC%A2%8C%ED%91%9C.png?raw=true', 4),
        (37.50094046, 127.0936817, '삼전동', 'https://github.com/suhyeon0325/SeoulFireDash/blob/main/data/%EC%82%AC%EC%A7%84/04_%EC%A2%8C%ED%91%9C.png?raw=true', 4),
        (37.504103, 127.090679, '삼전동', 'https://github.com/suhyeon0325/SeoulFireDash/blob/main/data/%EC%82%AC%EC%A7%84/05_%EC%A2%8C%ED%91%9C.png?raw=true', 4),
        (37.49991962, 127.0974103, '석촌동', 'https://github.com/suhyeon0325/SeoulFireDash/blob/main/data/%EC%82%AC%EC%A7%84/06_%EC%A2%8C%ED%91%9C.png?raw=true', 4),
        (37.50097974,127.1000492, '석촌동', 'https://github.com/suhyeon0325/SeoulFireDash/blob/main/data/%EC%82%AC%EC%A7%84/07_%EC%A2%8C%ED%91%9C.png?raw=true', 4),
        (37.50884075,127.1087034, '송파동', 'https://github.com/suhyeon0325/SeoulFireDash/blob/main/data/%EC%82%AC%EC%A7%84/08_%EC%A2%8C%ED%91%9C.png?raw=true', 4),
        (37.511740, 127.110053, '방이동', 'https://github.com/suhyeon0325/SeoulFireDash/blob/main/data/%EC%82%AC%EC%A7%84/09_%EC%A2%8C%ED%91%9C.png?raw=true', 4),  
        (37.51299316, 127.1161285, '방이동', 'https://github.com/suhyeon0325/SeoulFireDash/blob/main/data/%EC%82%AC%EC%A7%84/10_%EC%A2%8C%ED%91%9C.png?raw=true', 4),
        (37.499000, 127.120611, '가락본동, 가락1동', 'https://github.com/suhyeon0325/SeoulFireDash/blob/main/data/%EC%82%AC%EC%A7%84/11_%EC%A2%8C%ED%91%9C.png?raw=true', 2),
        (37.496917, 127.120417, '가락본동, 가락1동', 'https://github.com/suhyeon0325/SeoulFireDash/blob/main/data/%EC%82%AC%EC%A7%84/12_%EC%A2%8C%ED%91%9C.png?raw=true', 2),
        (37.500694, 127.112639, '송파2동', 'https://github.com/suhyeon0325/SeoulFireDash/blob/main/data/%EC%82%AC%EC%A7%84/13_%EC%A2%8C%ED%91%9C.png?raw=true', 3),
        (37.492321, 127.154682, '마천1동', 'https://github.com/suhyeon0325/SeoulFireDash/blob/main/data/%EC%82%AC%EC%A7%84/14_%EC%A2%8C%ED%91%9C.png?raw=true', 3),
        (37.499138, 127.149098, '마천2동', 'https://github.com/suhyeon0325/SeoulFireDash/blob/main/data/%EC%82%AC%EC%A7%84/15_%EC%A2%8C%ED%91%9C.png?raw=true', 4),
        (37.493358, 127.142836, '거여1동', 'https://github.com/suhyeon0325/SeoulFireDash/blob/main/data/%EC%82%AC%EC%A7%84/16_%EC%A2%8C%ED%91%9C.png?raw=true', 4),
        (37.497698, 127.143332, '거여1동', 'https://github.com/suhyeon0325/SeoulFireDash/blob/main/data/%EC%82%AC%EC%A7%84/17_%EC%A2%8C%ED%91%9C.png?raw=true', 3),
        (37.503962, 127.140793, '오금동', 'https://github.com/suhyeon0325/SeoulFireDash/blob/main/data/%EC%82%AC%EC%A7%84/18_%EC%A2%8C%ED%91%9C.png?raw=true', 3),
        (37.502313, 127.134786, '오금동', 'https://github.com/suhyeon0325/SeoulFireDash/blob/main/data/%EC%82%AC%EC%A7%84/19_%EC%A2%8C%ED%91%9C.png?raw=true', 4)
    ]
    return locations
