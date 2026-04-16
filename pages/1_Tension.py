import streamlit as st

st.set_page_config(page_title="Axial Tension", layout="wide")

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

st.title("🔗 Analysis of Axial Tension Members")

# Input Section
st.sidebar.header("Material & Section Properties")
method = st.sidebar.radio("Design Philosophy", ["LRFD", "ASD"])

fy = st.sidebar.number_input("Yield Strength, Fy (MPa)", value=248.0, step=10.0)
fu = st.sidebar.number_input("Tensile Strength, Fu (MPa)", value=400.0, step=10.0)
ag = st.sidebar.number_input("Gross Area, Ag (mm²)", value=5000.0, step=100.0)
ae = st.sidebar.number_input("Effective Net Area, Ae (mm²)", value=4200.0, step=100.0)

# Calculations
# 1. Gross Section Yielding
pn_yield = fy * ag / 1000  # Convert to kN
if method == "LRFD":
    capacity_yield = 0.90 * pn_yield
else:
    capacity_yield = pn_yield / 1.67

# 2. Net Section Rupture
pn_rupture = fu * ae / 1000 # Convert to kN
if method == "LRFD":
    capacity_rupture = 0.75 * pn_rupture
else:
    capacity_rupture = pn_rupture / 2.00

# Controlling Capacity
controlling_capacity = min(capacity_yield, capacity_rupture)
controlling_limit = "Yielding" if capacity_yield < capacity_rupture else "Rupture"

# UI Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Capacity Results")
    st.metric(f"Gross Yielding Capacity ({method})", f"{capacity_yield:.2f} kN")
    st.metric(f"Net Rupture Capacity ({method})", f"{capacity_rupture:.2f} kN")
    
with col2:
    st.subheader("Final Design Strength")
    st.success(f"**Governing Capacity:** {controlling_capacity:.2f} kN")
    st.info(f"**Failure Mode:** {controlling_limit}")

st.divider()

# Professional Calculations Output using LaTeX
with st.expander("📝 View Detailed Step-by-Step Calculations"):
    st.markdown("### 1. Tensile Yielding in the Gross Section")
    st.latex(r"P_n = F_y A_g")
    st.write(f"$P_n = {fy} \\times {ag} = {pn_yield:.2f}$ kN")
    
    if method == "LRFD":
        st.latex(r"\phi P_n = 0.90 \times P_n")
    else:
        st.latex(r"\frac{P_n}{\Omega} = \frac{P_n}{1.67}")
        
    st.markdown("### 2. Tensile Rupture in the Net Section")
    st.latex(r"P_n = F_u A_e")
    st.write(f"$P_n = {fu} \\times {ae} = {pn_rupture:.2f}$ kN")
    
    if method == "LRFD":
        st.latex(r"\phi P_n = 0.75 \times P_n")
    else:
        st.latex(r"\frac{P_n}{\Omega} = \frac{P_n}{2.00}")