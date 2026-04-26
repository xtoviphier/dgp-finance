import streamlit as st
from translation_ui import init_translation, render_translation_sidebar, t

init_translation()

with st.sidebar:
    render_translation_sidebar()

# ================= PAGE CONTENT =================

st.title(t("Privacy Policy"))

st.markdown(t("""
This Privacy Policy explains how DGP Finance collects, uses, and protects your information when you use the platform.
"""))

# ===== DATA COLLECTION =====
st.header(t("1. Information We Collect"))

st.markdown(t("""
We may collect the following types of information:

- **Account Information:** Email address used for authentication  
- **Financial Data:** Information you input to generate reports  
- **Usage Data:** Basic interaction data to improve functionality  

We do not collect unnecessary personal data beyond what is required to operate the platform.
"""))

# ===== DATA USAGE =====
st.header(t("2. How We Use Your Information"))

st.markdown(t("""
Your data is used strictly to:

- Provide and maintain application functionality  
- Generate and store financial reports  
- Improve performance and user experience  
- Respond to support inquiries  

We do not use your data for advertising or profiling.
"""))

# ===== DATA STORAGE =====
st.header(t("3. Data Storage and Security"))

st.markdown(t("""
All data is securely stored using Supabase infrastructure.

We implement reasonable security measures to protect your information from unauthorized access, 
loss, or misuse. However, no system is completely secure, and users should exercise caution 
when sharing sensitive information.
"""))

# ===== DATA SHARING =====
st.header(t("4. Data Sharing"))

st.markdown(t("""
We do **not** sell, rent, or trade your personal data.

Your information may only be shared if required by law or to protect the integrity and security 
of the platform.
"""))

# ===== USER RIGHTS =====
st.header(t("5. Your Rights"))

st.markdown(t("""
You have the right to:

- Access the data we store about you  
- Request correction of inaccurate data  
- Request deletion of your data  
- Stop using the platform at any time  

To exercise these rights, please contact us directly.
"""))

# ===== DATA RETENTION =====
st.header(t("6. Data Retention"))

st.markdown(t("""
We retain your data only for as long as necessary to provide our services. 
If you request deletion, your data will be permanently removed within a reasonable timeframe.
"""))

# ===== THIRD-PARTY SERVICES =====
st.header(t("7. Third-Party Services"))

st.markdown(t("""
DGP Finance relies on third-party services such as Supabase for backend infrastructure. 
These services may process your data in accordance with their own privacy policies.
"""))

# ===== POLICY UPDATES =====
st.header(t("8. Updates to This Policy"))

st.markdown(t("""
We may update this Privacy Policy from time to time. 
Any changes will be reflected on this page with immediate effect.
"""))

# ===== CONTACT =====
st.header(t("9. Contact"))

st.markdown(t("""
If you have any questions about this Privacy Policy or your data, please contact:

📧 csaha@mun.ca
"""))

st.info(t("By using DGP Finance, you agree to this Privacy Policy."))