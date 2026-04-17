import streamlit as st

st.set_page_config(page_title="Bending Members", layout="wide")
st.markdown("""<style>div[data-testid="stSidebar"]{background-color:#F8F9FA;} h1{color:#000000; border-bottom:3px solid #FFCC00;} .streamlit-expanderHeader{background-color:#F8F9FA; color:black; font-weight:bold;}</style>""", unsafe_allow_html=True)

st.title("Analysis of Bending Members")

st.sidebar.header("Section & Material Properties")
method = st.sidebar.radio("Design Philosophy", ["LRFD", "ASD"])

fy = st.sidebar.number_input("Yield Strength, Fy (MPa)", value=248.0)
zx = st.sidebar.number_input("Plastic Section Modulus, Zx (x10³ mm³)", value=1200.0)

zx_true = zx * 1000
mn_yield = (fy * zx_true) / 10**6 

if method == "LRFD":
    capacity = 0.90 * mn_yield
else:
    capacity = mn_yield / 1.67

col1, col2 = st.columns(2)
with col1:
    st.subheader("Section Properties")
    st.metric("Nominal Moment (Mn)", f"{mn_yield:.2f} kN-m")

with col2:
    st.subheader("Design Strength")
    st.success(f"**Available Moment ({method}):** {capacity:.2f} kN-m")

st.divider()

with st.expander("📝 View Detailed Step-by-Step Calculations"):
    st.markdown("### 1. Nominal Moment Capacity (Yielding)")
    st.latex(r"M_n = F_y Z_x")
    st.write(f"Mn = ({fy} * {zx_true}) / 10^6")
    st.write(f"Mn = {mn_yield:.2f} kN-m")