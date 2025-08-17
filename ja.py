# streamlit_app.py
# --------------------------------------
# 1. 필요한 모듈 설치
# Streamlit Cloud에서는 requirements.txt에 아래 추가:
# pyvis
# networkx
# streamlit

import streamlit as st
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import os

# --------------------------------------
# 2. 페이지 설정
st.set_page_config(page_title="죽음과 화학적 순환 시뮬레이션", layout="wide")
st.title("죽음에서 생태계로: 생명체 분해와 인간 기술 시뮬레이션")

# --------------------------------------
# 3. 네트워크 생성
G = nx.DiGraph()

# 노드 정의 (단계 + 화학 반응 + 인간 기술)
nodes = {
    "생물학적 죽음": {"type":"stage", "info":"세포와 장기 기능 상실"},
    "단백질 분해": {"type":"reaction", "info":"Protein + H2O → Amino acids → NH3 → NO3-"},
    "지방 분해": {"type":"reaction", "info":"Lipid + H2O → Glycerol + Fatty acids → CH4 + CO2"},
    "탄수화물 분해": {"type":"reaction", "info":"Carbohydrates + O2 → CO2 + H2O"},
    "원소 순환": {"type":"stage", "info":"C, N, P 등 원소가 토양과 환경으로 순환"},
    "바이오연료": {"type":"tech", "info":"Methane, Ethanol, Butanol 생산 → 에너지 활용"},
    "바이오소재": {"type":"tech", "info":"PLA, PHA 생분해성 고분자 개발"},
    "그린 장례": {"type":"tech", "info":"알칼리 가수분해(Resomation)로 시신 분해"},
}

# 노드 추가
for node, attr in nodes.items():
    G.add_node(node, **attr)

# 에지 추가 (흐름)
edges = [
    ("생물학적 죽음", "단백질 분해"),
    ("생물학적 죽음", "지방 분해"),
    ("생물학적 죽음", "탄수화물 분해"),
    ("단백질 분해", "원소 순환"),
    ("지방 분해", "원소 순환"),
    ("탄수화물 분해", "원소 순환"),
    ("원소 순환", "바이오연료"),
    ("원소 순환", "바이오소재"),
    ("원소 순환", "그린 장례"),
]
G.add_edges_from(edges)

# --------------------------------------
# 4. Pyvis 네트워크 생성
net = Network(height="700px", width="100%", directed=True, notebook=False)

# 노드/에지 Pyvis로 변환
net.from_nx(G)

# 노드 색상과 툴팁
for node in net.nodes:
    node["title"] = G.nodes[node["id"]]["info"]  # 클릭 시 정보 표시
    if G.nodes[node["id"]]["type"] == "reaction":
        node["color"] = "orange"
    elif G.nodes[node["id"]]["type]()
