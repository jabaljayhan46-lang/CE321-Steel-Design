import streamlit as st

# 1. Page Configuration (Must be the first command)
st.set_page_config(
    page_title="CE 321 - Steel Design Suite",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Load the Custom CSS
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
# 3. Homepage Content
st.title("🏗️ Principles of Steel Design (CE 321)")
st.subheader("Analysis & Design Software Suite")

st.markdown("""
Welcome to the Steel Design Suite. This application automates the calculations for the analysis and design of structural steel members according to standard specifications (NSCP 2015 / AISC 360).

### **Available Modules:**
* **Topic 4:** Axial Tension Members
* **Topic 5:** Axial Compression Members
* **Topic 6:** Bending Members
* **Topic 7:** Shear Strength
* **Topic 8:** Combined Axial and Flexural Loading
* **Topic 9:** Connections

**Instructor:** Engr. Tomomi Fujimura, RCE, RMP, SO2
""")

st.info("👈 Please select a design module from the sidebar to begin.")