import streamlit as st

st.set_page_config(page_title="Combined Loading", layout="wide")

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

st.title("🌀 Combined Axial and Flexural Loading")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Required Strength (Demands)")
    pr = st.number_input("Required Axial Load, Pr (kN)", value=500.0)
    mr = st.number_input("Required Flexural Moment, Mr (kN-m)", value=150.0)

with col2:
    st.subheader("Available Strength (Capacities)")
    pc = st.number_input("Available Axial Capacity, Pc (kN)", value=2000.0)
    mc = st.number_input("Available Moment Capacity, Mc (kN-m)", value=300.0)

# Mathematical Safeguards to prevent ZeroDivisionError
pc_safe = max(pc, 0.001)
mc_safe = max(mc, 0.001)

# Calculations
pr_pc = pr / pc_safe
mr_mc = mr / mc_safe

if pr_pc >= 0.2:
    interaction_ratio = pr_pc + (8/9) * mr_mc
    eq_used = "H1-1a"
else:
    interaction_ratio = (pr_pc / 2) + mr_mc
    eq_used = "H1-1b"

# Results
st.divider()
st.subheader("Interaction Result")

status = "PASS" if interaction_ratio <= 1.0 else "FAIL"
color = "normal" if interaction_ratio <= 1.0 else "inverse"

c1, c2, c3 = st.columns(3)
c1.metric("Axial Ratio (Pr/Pc)", f"{pr_pc:.3f}")
c2.metric("Moment Ratio (Mr/Mc)", f"{mr_mc:.3f}")
c3.metric("Interaction Value", f"{interaction_ratio:.3f}", f"Must be ≤ 1.0 ({status})", delta_color=color)

with st.expander("📝 View Detailed Step-by-Step Calculations"):
    st.markdown("### AISC Chapter H Interaction Equations")
    st.write(f"Check ratio: $P_r / P_c = {pr} / {pc} = {pr_pc:.3f}$")
    
    if pr_pc >= 0.2:
        st.markdown("**Since $P_r/P_c \ge 0.2$, use Equation H1-1a:**")
        st.latex(r"\frac{P_r}{P_c} + \frac{8}{9} \left( \frac{M_r}{M_c} \right) \le 1.0")
        st.write(f"${pr_pc:.3f} + (8/9)({mr_mc:.3f}) = {interaction_ratio:.3f}$")
    else:
        st.markdown("**Since $P_r/P_c < 0.2$, use Equation H1-1b:**")
        st.latex(r"\frac{P_r}{2P_c} + \left( \frac{M_r}{M_c} \right) \le 1.0")
        st.write(f"${pr_pc:.3f}/2 + {mr_mc:.3f} = {interaction_ratio:.3f}$")