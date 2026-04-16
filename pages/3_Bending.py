import streamlit as st

st.set_page_config(page_title="Bending Members", layout="wide")

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

st.title("🛹 Analysis of Bending Members")

# Inputs
st.sidebar.header("Section & Material Properties")
method = st.sidebar.radio("Design Philosophy", ["LRFD", "ASD"])

fy = st.sidebar.number_input("Yield Strength, Fy (MPa)", value=248.0)
zx = st.sidebar.number_input("Plastic Section Modulus, Zx (10³ mm³)", value=1200.0) * 1000
sx = st.sidebar.number_input("Elastic Section Modulus, Sx (10³ mm³)", value=1050.0) * 1000

# Calculations (Assuming fully supported beam for Yielding limit state)
mn_yield = (fy * zx) / 10**6 # Converted to kN-m

if method == "LRFD":
    capacity = 0.90 * mn_yield
else:
    capacity = mn_yield / 1.67

# Results
col1, col2 = st.columns(2)
with col1:
    st.subheader("Nominal Flexural Strength")
    st.metric("Moment Capacity (Mn)", f"{mn_yield:.2f} kN-m")

with col2:
    st.subheader("Design Flexural Strength")
    st.success(f"**Available Moment ({method}):** {capacity:.2f} kN-m")

st.divider()

with st.expander("📝 View Detailed Step-by-Step Calculations"):
    st.markdown("### 1. Nominal Moment Capacity (Yielding Limit State)")
    st.markdown("Assuming the beam is continuously supported ($L_b \le L_p$):")
    st.latex(r"M_n = F_y Z_x")
    st.write(f"$M_n = ({fy} \\text{{ MPa}}) \\times ({zx} \\text{{ mm}}^3) / 10^6$")
    st.write(f"$M_n = {mn_yield:.2f}$ kN-m")
    
    st.markdown("### 2. Available Strength")
    if method == "LRFD":
        st.latex(r"\phi_b M_n = 0.90 \times M_n")
    else:
        st.latex(r"\frac{M_n}{\Omega_b} = \frac{M_n}{1.67}")