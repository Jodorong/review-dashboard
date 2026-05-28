import streamlit as st

def apply_custom_css():
    st.markdown("""
    <style>
    .stApp {
        background-color: #F7F9FC;
    }

    h1 {
        color: #1F2937;
        font-weight: 800;
    }

    h2, h3 {
        color: #111827;
        font-weight: 700;
    }

    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E5E7EB;
    }

    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }

    .stButton > button {
        background-color: #2563EB;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.6rem 1rem;
        font-weight: 600;
    }

    .stButton > button:hover {
        background-color: #1D4ED8;
        color: white;
    }

    div[data-baseweb="select"] > div,
    input {
        border-radius: 10px !important;
    }

    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }

    .info-box {
        background-color: #FFFFFF;
        padding: 20px 24px;
        border-radius: 16px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        margin-bottom: 24px;
    }
    </style>
    """, unsafe_allow_html=True)