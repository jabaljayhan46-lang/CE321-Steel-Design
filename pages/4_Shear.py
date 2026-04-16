import streamlit as st

st.set_page_config(page_title="Shear Strength", layout="wide")

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

st.title("✂️ Analysis of Shear Strength")

# Inputs
st.sidebar.header("Section & Material Properties")
method = st.sidebar.radio("Design Philosophy", ["LRFD", "ASD"])

fy = st.sidebar.number_input("Yield Strength, Fy (MPa)", value=248.0)
d = st.sidebar.number_input("Overall Depth, d (mm)", value=400.0)
tw = st.sidebar.number_input("Web Thickness, tw (mm)", value=10.0)
cv = st.sidebar.number_input("Web Shear Coefficient, Cv1", value=1.0)

# Calculations
aw = d * tw
vn = 0.6 * fy * aw * cv / 1000 # Converted to kN

if method == "LRFD":
    capacity = 1.00 * vn # Phi is 1.0 for shear in most W-shapes
else:
    capacity = vn / 1.50

# Results
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
    st.write(f"$A_w = {d} \\times {tw} = {aw:.2f}$ mm²")
    
    st.markdown("### 2. Nominal Shear Strength")
    st.latex(r"V_n = 0.6 F_y A_w C_{v1}")
    st.write(f"$V_n = 0.6 \times {fy} \times {aw} \times {cv} / 1000$")
    st.write(f"$V_n = {vn:.2f}$ kN")