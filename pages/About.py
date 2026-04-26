import streamlit as st
from translation_ui import init_translation, render_translation_sidebar, t

init_translation()

with st.sidebar:
    render_translation_sidebar()

# ================= PAGE CONTENT =================

st.title(t("About DGP Finance"))

st.markdown(t("""
DGP Finance is a modern AI powered financial platform designed to simplify complex financial processes 
and provide users with clear, structured, and actionable insights.

Whether you are a student, entrepreneur, analyst, or business owner, DGP Finance equips you with the tools 
needed to generate, interpret, and understand financial data with precision and confidence.
"""))

# ===== VISION =====
st.header(t("Vision"))
st.write(t("""
To become a globally trusted platform for financial analysis, empowering individuals and organizations 
with intelligent tools that make financial clarity accessible to everyone.
"""))

# ===== MISSION =====
st.header(t("Mission"))
st.write(t("""
Our mission is to bridge the gap between raw financial data and meaningful decision-making by delivering 
intuitive, accurate, and scalable financial solutions.
"""))

# ===== WHAT WE DO =====
st.header(t("What We Do"))
st.markdown(t("""
- Generate professional financial statements instantly  
- Provide structured financial analysis and insights  
- Simplify complex accounting and reporting workflows  
- Enable users to manage and track financial performance  
- Support decision-making with clear, data-driven outputs  
"""))

# ===== WHO IT'S FOR =====
st.header(t("Our Users"))
st.markdown(t("""
DGP Finance is built for:

- Students learning finance and accounting  
- Entrepreneurs managing their businesses  
- Analysts working with financial data  
- Organizations seeking structured reporting tools  
"""))

# ===== CORE VALUES =====
st.header(t("Core Values"))
st.markdown(t("""
- **Transparency** – Clear, understandable financial outputs  
- **Simplicity** – Complex systems made intuitive  
- **Accuracy** – Reliable and consistent calculations  
- **Efficiency** – Save time through automation  
- **User Empowerment** – Give users control over their financial insights  
"""))

# ===== WHY DGP FINANCE =====
st.header(t("Why DGP Finance"))
st.write(t("""
Traditional financial tools are often complex, fragmented, or difficult to use. 
DGP Finance is designed to remove these barriers by combining usability, automation, 
and intelligent design into a single streamlined platform.
"""))

# ===== FUTURE =====
st.header(t("The Future of DGP Finance"))
st.write(t("""
DGP Finance is continuously evolving, with plans to integrate advanced analytics, 
AI-driven insights, and expanded financial tools to meet the growing needs of users worldwide.
"""))