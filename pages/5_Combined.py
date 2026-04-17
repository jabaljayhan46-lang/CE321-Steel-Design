import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Combined Loading", layout="wide")
st.markdown("""<style>div[data-testid="stSidebar"]{background-color:#F8F9FA;} h1{color:#000000; border-bottom:3px solid #FFCC00; padding-bottom:10px; margin-bottom:20px;} h2, h3{color:#000000;} .streamlit-expanderHeader{background-color:#F8F9FA; color:black; font-weight:bold;}</style>""", unsafe_allow_html=True)

st.title("Combined Axial and Flexural Loading")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Required Loads (Demand)")
    pr = st.number_input("Required Axial Load, Pr (kN)", value=500.0)
    mr = st.number_input("Required Flexural Moment, Mr (kN-m)", value=150.0)

with col2:
    st.subheader("Available Strength (Capacity)")
    pc = st.number_input("Available Axial Capacity, Pc (kN)", value=2000.0)
    mc = st.number_input("Available Moment Capacity, Mc (kN-m)", value=300.0)

pc_safe = max(pc, 0.001)
mc_safe = max(mc, 0.001)

pr_pc = pr / pc_safe
mr_mc = mr / mc_safe

if pr_pc >= 0.2:
    interaction = pr_pc + (8/9) * mr_mc
    eq_used = "Equation H1-1a"
else:
    interaction = (pr_pc / 2) + mr_mc
    eq_used = "Equation H1-1b"

status = "PASS" if interaction <= 1.0 else "FAIL"
color = "normal" if interaction <= 1.0 else "inverse"

# --- ANIMATED SUCCESS/FAILURE ALERTS ---
if st.button("🔍 Check Design Capacity"):
    if interaction <= 1.0:
        st.success(f"**Design Adequate!** The section successfully carries the combined loads (Ratio: {interaction:.2f}).")
        st.balloons() # Triggers the celebration animation
    else:
        st.error(f"**DESIGN FAILED.** The interaction value ({interaction:.2f}) exceeds 1.0. Increase section size.")

st.divider()

# --- THE INTERACTIVE DIAGRAM SECTION ---
st.subheader("📊 Interaction Diagram (P-M Curve)")

envelope_x = [0, 0.9, 1.0]
envelope_y = [1.0, 0.2, 0.0]

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=envelope_x, y=envelope_y, 
    mode='lines', 
    name='AISC Capacity Limit',
    line=dict(color='#FFCC00', width=4) 
))

fig.add_trace(go.Scatter(
    x=[0, 0.9, 1.0, 0], y=[1.0, 0.2, 0.0, 0],
    fill='toself',
    fillcolor='rgba(255, 204, 0, 0.1)', 
    line=dict(color='rgba(255,255,255,0)'),
    name='Safe Zone',
    showlegend=False,
    hoverinfo='skip'
))

point_color = '#00CC66' if interaction <= 1.0 else '#FF3333' 
fig.add_trace(go.Scatter(
    x=[mr_mc], y=[pr_pc],
    mode='markers+text',
    name='Applied Load',
    marker=dict(color=point_color, size=14, symbol='cross'),
    text=['Demand Point'],
    textposition='top right',
    textfont=dict(color='black', size=12)
))

fig.update_layout(
    xaxis_title="<b>Moment Ratio (Mr / Mc)</b>",
    yaxis_title="<b>Axial Ratio (Pr / Pc)</b>",
    plot_bgcolor='white',
    margin=dict(l=40, r=40, t=40, b=40),
    xaxis=dict(range=[0, max(1.2, mr_mc + 0.1)], showgrid=True, gridcolor='#E2E8F0', zerolinecolor='black'),
    yaxis=dict(range=[0, max(1.2, pr_pc + 0.1)], showgrid=True, gridcolor='#E2E8F0', zerolinecolor='black')
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# --- VISUAL PROGRESS BAR ---
st.write(f"**Capacity Utilization:** {interaction*100:.1f}%")
st.progress(min(interaction, 1.0)) # Caps at 1.0 so the bar doesn't break if it fails

c1, c2, c3 = st.columns(3)
c1.metric("Axial Ratio (Pr/Pc)", f"{pr_pc:.3f}")
c2.metric("Moment Ratio (Mr/Mc)", f"{mr_mc:.3f}")
c3.metric("Interaction Value", f"{interaction:.3f}", f"Must be ≤ 1.0 ({status})", delta_color=color)

st.info(f"**AISC Specification Used:** {eq_used}")

with st.expander("View Detailed Step-by-Step Calculations"):
    st.markdown("### 1. Determine Ratio")
    st.write(f"Pr / Pc = {pr} / {pc} = {pr_pc:.3f}")
    
    st.markdown("### 2. Interaction Equation")
    if pr_pc >= 0.2:
        st.write("Since Pr/Pc ≥ 0.2, use Equation H1-1a:")
        st.latex(r"\frac{P_r}{P_c} + \frac{8}{9} \left( \frac{M_r}{M_c} \right) \le 1.0")
        st.write(f"= {pr_pc:.3f} + (8/9 * {mr_mc:.3f}) = {interaction:.3f}")
    else:
        st.write("Since Pr/Pc < 0.2, use Equation H1-1b:")
        st.latex(r"\frac{P_r}{2P_c} + \left( \frac{M_r}{M_c} \right) \le 1.0")
        st.write(f"= ({pr_pc:.3f} / 2) + {mr_mc:.3f} = {interaction:.3f}")