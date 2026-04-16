import streamlit as st
import math

st.set_page_config(page_title="Connections", layout="wide")

st.markdown("""
<style>
div[data-testid="stSidebar"] { background-color: #1E293B; color: white; }
div[data-testid="stSidebar"] h1, div[data-testid="stSidebar"] p { color: #F8FAFC !important; }
div[data-testid="stMetricValue"] { font-size: 2rem !important; color: #0F172A; font-weight: 700; }
div[data-testid="stMetricLabel"] { font-size: 1rem !important; color: #64748B; font-weight: 600; }
h1 { color: #0F172A; border-bottom: 3px solid #3B82F6; padding-bottom: 10px; margin-bottom: 20px; }
h2, h3 { color: #1E293B; }
.streamlit-expanderHeader { background-color: #F1F5F9; border-radius: 5px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("🔩 Bolted Connections (Shear)")

st.sidebar.header("Bolt Properties")
method = st.sidebar.radio("Design Philosophy", ["LRFD", "ASD"])

bolt_dia = st.sidebar.number_input("Bolt Diameter, db (mm)", value=20.0)
fnv = st.sidebar.number_input("Nominal Shear Stress of Bolt, Fnv (MPa)", value=372.0, help="E.g., A325 with threads included = 372 MPa")
n_bolts = st.sidebar.number_input("Number of Bolts, n", value=4, step=1)
shear_planes = st.sidebar.radio("Shear Planes", [1, 2], format_func=lambda x: "Single Shear" if x==1 else "Double Shear")

# Calculations
ab = (math.pi * bolt_dia**2) / 4
rn_single = fnv * ab / 1000 # kN per bolt per plane
rn_total = rn_single * n_bolts * shear_planes

if method == "LRFD":
    capacity = 0.75 * rn_total
else:
    capacity = rn_total / 2.00

# Results
col1, col2 = st.columns(2)
with col1:
    st.subheader("Bolt Data")
    st.metric("Area per Bolt (Ab)", f"{ab:.2f} mm²")
    st.metric("Nominal Strength (Rn)", f"{rn_total:.2f} kN")

with col2:
    st.subheader("Design Connection Strength")
    st.success(f"**Available Strength ({method}):** {capacity:.2f} kN")

st.divider()

with st.expander("📝 View Detailed Step-by-Step Calculations"):
    st.markdown("### 1. Area of One Bolt")
    st.latex(r"A_b = \frac{\pi d_b^2}{4}")
    st.write(f"$A_b = \pi ({bolt_dia})^2 / 4 = {ab:.2f}$ mm²")
    
    st.markdown("### 2. Total Nominal Shear Strength")
    st.latex(r"R_n = F_{nv} A_b \times n \times \text{planes}")
    st.write(f"$R_n = {fnv} \times {ab:.2f} \times {n_bolts} \times {shear_planes} / 1000$")
    st.write(f"$R_n = {rn_total:.2f}$ kN")
    
    st.markdown("### 3. Available Strength")
    if method == "LRFD":
        st.latex(r"\phi R_n = 0.75 \times R_n")
    else:
        st.latex(r"\frac{R_n}{\Omega} = \frac{R_n}{2.00}")