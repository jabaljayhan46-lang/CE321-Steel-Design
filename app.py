import streamlit as st
import base64

st.set_page_config(page_title="CE 321 - Steel Design", layout="wide")

def get_base64(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return ""

campus_base64 = get_base64("campus.jpg") 

st.markdown(f"""
<style>
.stApp {{
    background-image: url("data:image/jpg;base64,{campus_base64}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}
.block-container {{
    background-color: rgba(255, 255, 255, 0.92); 
    padding: 3rem !important;
    border-radius: 15px;
    box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);
    margin-top: 2rem;
}}
div[data-testid="stSidebar"] {{ background-color: #F8F9FA; color: black; }}
div[data-testid="stSidebar"] h1, div[data-testid="stSidebar"] p {{ color: #000000 !important; }}
h1 {{ color: #000000; border-bottom: 3px solid #FFCC00; padding-bottom: 10px; margin-bottom: 20px; }}
h2, h3 {{ color: #000000; }}
div[data-testid="stPageLink-NavLink"] {{ background-color: #FFFFFF; padding: 15px; border-radius: 8px; border: 2px solid #FFCC00; margin-bottom: 10px; font-size: 1.1rem; font-weight: 600; color: #000000; }}
div[data-testid="stPageLink-NavLink"]:hover {{ background-color: #FFCC00; color: #000000; }}
</style>
""", unsafe_allow_html=True)

try:
    st.sidebar.image("logo.png", use_container_width=True) 
except Exception:
    pass 

st.title("Principles of Steel Design (CE 321)")
st.subheader("Analysis & Design Software Suite")

st.markdown("Welcome to the Steel Design Suite. This application automates the calculations for the analysis and design of structural steel members according to standard specifications (NSCP 2015 / AISC 360).")

st.write("### Please select a module below to begin calculations:")

col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/1_Tension.py", label="Axial Tension")
    st.page_link("pages/3_Bending.py", label="Bending Members")
    st.page_link("pages/5_Combined.py", label="Combined Loading")

with col2:
    st.page_link("pages/2_Compression.py", label="Axial Compression")
    st.page_link("pages/4_Shear.py", label="Shear Strength")
    st.page_link("pages/6_Connections.py", label="Bolted Connections")

st.divider()
st.caption("Developed for CE 321 - University of Santo Tomas - Legazpi")