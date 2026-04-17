import streamlit as st
import math

st.set_page_config(page_title="Connections", layout="wide")
st.markdown("""<style>div[data-testid="stSidebar"]{background-color:#F8F9FA;} h1{color:#000000; border-bottom:3px solid #FFCC00;} .streamlit-expanderHeader{background-color:#F8F9FA; color:black; font-weight:bold;}</style>""", unsafe_allow_html=True)

st.title("Bolted Connections (Shear)")

st.sidebar.header("Bolt Properties")
method = st.sidebar.radio("Design Philosophy", ["LRFD", "ASD"])

bolt_dia = st.sidebar.number_input("Bolt Diameter (mm)", value=20.0)
fnv = st.sidebar.number_input("Nominal Shear Stress, Fnv (MPa)", value=372.0)
n_bolts = st.sidebar.number_input("Number of Bolts", value=4, step=1)
shear_planes = st.sidebar.radio("Shear Planes", [1, 2], format_func=lambda x: "Single Shear (1)" if x==1 else "Double Shear (2)")

ab = (math.pi * bolt_dia**2) / 4
rn_total = (fnv * ab * n_bolts * shear_planes) / 1000

if method == "LRFD":
    capacity = 0.75 * rn_total
else:
    capacity = rn_total / 2.00

col1, col2 = st.columns(2)
with col1:
    st.subheader("Strength per Group")
    st.metric("Total Nominal Strength (Rn)", f"{rn_total:.2f} kN")

with col2:
    st.subheader("Design Strength")
    st.success(f"**Available Strength ({method}):** {capacity:.2f} kN")

st.divider()

with st.expander("📝 View Detailed Step-by-Step Calculations"):
    st.markdown("### 1. Area of One Bolt")
    st.latex(r"A_b = \frac{\pi d^2}{4}")
    st.write(f"Ab = (\pi * {bolt_dia}^2) / 4 = {ab:.2f} mm²")
    
    st.markdown("### 2. Nominal Shear Strength")
    st.latex(r"R_n = F_{nv} A_b \times n \times planes")
    st.write(f"Rn = {fnv} * {ab:.2f} * {n_bolts} * {shear_planes} / 1000")
    st.write(f"Rn = {rn_total:.2f} kN")