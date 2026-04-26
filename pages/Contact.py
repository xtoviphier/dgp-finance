import streamlit as st
from translation_ui import init_translation, render_translation_sidebar, t

init_translation()

with st.sidebar:
    render_translation_sidebar()

# ================= PAGE CONTENT =================

st.title(t("Contact"))

st.markdown(t("""
We’d love to hear from you. Whether you have questions, feedback, or collaboration inquiries, 
feel free to reach out through the channels below.
"""))

# ===== CONTACT DETAILS =====
st.header(t("Get in Touch"))

st.markdown(t(f"""
📧 **Email:** csaha@mun.ca  
🔗 **LinkedIn:** [Christopher Wambua](https://www.linkedin.com/in/christopher-wambua-654081214/)  

⏱ **Response Time:** Within 24–48 hours
"""))

# ===== SUPPORT TYPES =====
st.header(t("What You Can Contact Us For"))

st.markdown(t("""
- General inquiries about DGP Finance  
- Technical support or bug reports  
- Feedback and feature suggestions  
- Business or collaboration opportunities  
"""))

# ===== NOTE =====
st.info(t("We aim to respond to all messages as quickly as possible. Thank you for your patience."))