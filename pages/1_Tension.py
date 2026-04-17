import streamlit as st

st.set_page_config(page_title="Axial Tension", layout="wide")
st.markdown("""<style>div[data-testid="stSidebar"]{background-color:#F8F9FA;} h1{color:#000000; border-bottom:3px solid #FFCC00;} .streamlit-expanderHeader{background-color:#F8F9FA; color:black; font-weight:bold;}</style>""", unsafe_allow_html=True)

st.title("Analysis of Axial Tension Members")

st.sidebar.header("Section & Material Properties")
method = st.sidebar.radio("Design Philosophy", ["LRFD", "ASD"])

fy = st.sidebar.number_input("Yield Strength, Fy (MPa)", value=248.0)
fu = st.sidebar.number_input("Tensile Strength, Fu (MPa)", value=400.0)
ag = st.sidebar.number_input("Gross Area, Ag (mm²)", value=5000.0)
ae = st.sidebar.number_input("Effective Net Area, Ae (mm²)", value=4000.0)

pn_yield = fy * ag / 1000
pn_rupture = fu * ae / 1000

if method == "LRFD":
    capacity_yield = 0.90 * pn_yield
    capacity_rupture = 0.75 * pn_rupture
else:
    capacity_yield = pn_yield / 1.67
    capacity_rupture = pn_rupture / 2.00

controlling_capacity = min(capacity_yield, capacity_rupture)
controlling_limit = "Yielding" if capacity_yield < capacity_rupture else "Rupture"

col1, col2 = st.columns(2)
with col1:
    st.subheader("Capacity Results")
    st.metric(f"Gross Yielding ({method})", f"{capacity_yield:.2f} kN")
    st.metric(f"Net Rupture ({method})", f"{capacity_rupture:.2f} kN")

with col2:
    st.subheader("Final Design Strength")
    st.success(f"**Governing Capacity:** {controlling_capacity:.2f} kN")
    st.info(f"**Failure Mode:** {controlling_limit}")

st.divider()

with st.expander("📝 View Detailed Step-by-Step Calculations"):
    st.markdown("### 1. Gross Section Yielding")
    st.latex(r"P_n = F_y A_g")
    st.write(f"Pn = {fy} * {ag} / 1000 = {pn_yield:.2f} kN")
    if method == "LRFD":
        st.write(f"Capacity = 0.90 * {pn_yield:.2f} = {capacity_yield:.2f} kN")
    else:
        st.write(f"Capacity = {pn_yield:.2f} / 1.67 = {capacity_yield:.2f} kN")
    
    st.markdown("### 2. Net Section Rupture")
    st.latex(r"P_n = F_u A_e")
    st.write(f"Pn = {fu} * {ae} / 1000 = {pn_rupture:.2f} kN")
    if method == "LRFD":
        st.write(f"Capacity = 0.75 * {pn_rupture:.2f} = {capacity_rupture:.2f} kN")
    else:
        st.write(f"Capacity = {pn_rupture:.2f} / 2.00 = {capacity_rupture:.2f} kN")