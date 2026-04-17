import streamlit as st

st.set_page_config(page_title="Shear Strength", layout="wide")
st.markdown("""<style>div[data-testid="stSidebar"]{background-color:#F8F9FA;} h1{color:#000000; border-bottom:3px solid #FFCC00;} .streamlit-expanderHeader{background-color:#F8F9FA; color:black; font-weight:bold;}</style>""", unsafe_allow_html=True)

st.title("Analysis of Shear Strength")

st.sidebar.header("Section Properties")
method = st.sidebar.radio("Design Philosophy", ["LRFD", "ASD"])

fy = st.sidebar.number_input("Yield Strength, Fy (MPa)", value=248.0)
d = st.sidebar.number_input("Overall Depth, d (mm)", value=400.0)
tw = st.sidebar.number_input("Web Thickness, tw (mm)", value=10.0)
cv = st.sidebar.number_input("Web Shear Coefficient, Cv1", value=1.0)

aw = d * tw
vn = 0.6 * fy * aw * cv / 1000 

if method == "LRFD":
    capacity = 1.00 * vn
else:
    capacity = vn / 1.50

col1, col2 = st.columns(2)
with col1:
    st.subheader("Section Properties")
    st.metric("Area of Web (Aw)", f"{aw:.2f} mm²")
    st.metric("Nominal Shear (Vn)", f"{vn:.2f} kN")

with col2:
    st.subheader("Design Shear Strength")
    st.success(f"**Available Shear ({method}):** {capacity:.2f} kN")

st.divider()

with st.expander("📝 View Detailed Step-by-Step Calculations"):
    st.markdown("### 1. Area of Web")
    st.latex(r"A_w = d \times t_w")
    st.write(f"Aw = {d} * {tw} = {aw:.2f} mm²")
    
    st.markdown("### 2. Nominal Shear Strength")
    st.latex(r"V_n = 0.6 F_y A_w C_{v1}")
    st.write(f"Vn = 0.6 * {fy} * {aw} * {cv} / 1000")
    st.write(f"Vn = {vn:.2f} kN")