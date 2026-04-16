import streamlit as st
import math

st.set_page_config(page_title="Axial Compression", layout="wide")

# Embedded CSS
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

st.title("⬇️ Analysis of Axial Compression Members")

# Inputs
col1, col2 = st.columns(2)

with col1:
    st.subheader("Material Properties")
    fy = st.number_input("Yield Strength, Fy (MPa)", value=248.0)
    E = st.number_input("Modulus of Elasticity, E (MPa)", value=200000.0)
    method = st.radio("Design Philosophy", ["LRFD", "ASD"])

with col2:
    st.subheader("Geometric Properties")
    k = st.number_input("Effective Length Factor, K", value=1.0)
    l_m = st.number_input("Unbraced Length, L (meters)", value=3.0)
    r = st.number_input("Radius of Gyration, r (mm)", value=50.0)
    ag = st.number_input("Gross Area, Ag (mm²)", value=6000.0)

# --- MATHEMATICAL SAFEGUARDS ---
fy_safe = max(fy, 0.001)
E_safe = max(E, 0.001)
r_safe = max(r, 0.001)

# Calculations
L_mm = l_m * 1000
slenderness = (k * L_mm) / r_safe
slenderness_safe = max(slenderness, 0.001)
fe = (math.pi**2 * E_safe) / (slenderness_safe**2)
fe_safe = max(fe, 0.001)

# Determine Fcr (AISC 360 Section E3)
limit = 4.71 * math.sqrt(E_safe / fy_safe)

if slenderness <= limit:
    try:
        ratio = fy_safe / fe_safe
        ratio = min(max(ratio, -50), 50) 
        fcr = (0.658**ratio) * fy_safe
    except Exception:
        fcr = 0.0
    buckling_type = "Inelastic Buckling"
else:
    fcr = 0.877 * fe_safe
    buckling_type = "Elastic Buckling"

pn = fcr * ag / 1000 # Convert to kN

if method == "LRFD":
    capacity = 0.90 * pn
else:
    capacity = pn / 1.67

# Results Display
st.divider()
st.subheader("Design Capacity")
c1, c2, c3 = st.columns(3)
c1.metric("Slenderness Ratio (KL/r)", f"{slenderness:.2f}")
c2.metric("Critical Stress (Fcr)", f"{fcr:.2f} MPa")
c3.metric(f"Design Strength ({method})", f"{capacity:.2f} kN")

st.info(f"**Failure Mode:** {buckling_type}")

with st.expander("📝 View Detailed Step-by-Step Calculations"):
    st.markdown("### 1. Slenderness Ratio")
    st.latex(r"\frac{KL}{r}")
    st.write(f"KL/r = ({k} * {L_mm}) / {r} = {slenderness:.2f}")
    
    st.markdown("### 2. Elastic Buckling Stress (Fe)")
    st.latex(r"F_e = \frac{\pi^2 E}{(KL/r)^2}")
    st.write(f"Fe = {fe:.2f} MPa")
    
    st.markdown("### 3. Critical Stress (Fcr)")
    st.latex(r"4.71 \sqrt{\frac{E}{F_y}} = " + str(round(limit, 2)))
    if slenderness <= limit:
        st.latex(r"F_{cr} = \left[ 0.658^{\frac{F_y}{F_e}} \right] F_y")
    else:
        st.latex(r"F_{cr} = 0.877 F_e")
    st.write(f"Fcr = {fcr:.2f} MPa")