import streamlit as st
from translation_ui import init_translation, render_translation_sidebar, t

init_translation()

with st.sidebar:
    render_translation_sidebar()

# ================= PAGE CONTENT =================

st.title(t("Terms & Conditions"))

st.markdown(t("""
These Terms & Conditions govern your use of DGP Finance. By accessing or using the platform, 
you agree to comply with and be bound by these terms.
"""))

# ===== USE OF PLATFORM =====
st.header(t("1. Use of the Platform"))

st.markdown(t("""
DGP Finance provides financial tools, analytics, and reporting features designed to assist users 
in understanding financial data.

You agree to use the platform only for lawful purposes and in a manner that does not disrupt 
or interfere with the system or other users.
"""))

# ===== NO FINANCIAL ADVICE =====
st.header(t("2. No Financial Advice"))

st.markdown(t("""
All information provided by DGP Finance is for **informational and educational purposes only**.

We do **not** provide investment, financial, legal, or tax advice. 
Any decisions you make based on the platform are made entirely at your own risk.
"""))

# ===== DATA ACCURACY =====
st.header(t("3. Data Accuracy and Reliability"))

st.markdown(t("""
While we aim to provide accurate and up-to-date information, we make **no guarantees** regarding 
the completeness, reliability, or accuracy of any data displayed.

Market data, financial calculations, and outputs may contain errors or delays.
"""))

# ===== USER ACCOUNTS =====
st.header(t("4. User Accounts and Security"))

st.markdown(t("""
You are responsible for:

- Maintaining the confidentiality of your account credentials  
- All activities conducted under your account  
- Ensuring the accuracy of information you provide  

We are not liable for unauthorized access resulting from your failure to secure your account.
"""))

# ===== DATA USAGE =====
st.header(t("5. Data Usage"))

st.markdown(t("""
By using the platform, you grant DGP Finance the right to store and process your data 
for the purpose of providing its services.

For more details, refer to our Privacy Policy.
"""))

# ===== LIMITATION OF LIABILITY =====
st.header(t("6. Limitation of Liability"))

st.markdown(t("""
To the fullest extent permitted by law, DGP Finance shall not be liable for:

- Financial losses or investment decisions  
- Data inaccuracies or system errors  
- Service interruptions or downtime  
- Any indirect, incidental, or consequential damages  

Use of the platform is entirely at your own risk.
"""))

# ===== SERVICE AVAILABILITY =====
st.header(t("7. Service Availability"))

st.markdown(t("""
We reserve the right to modify, suspend, or discontinue any part of the platform at any time 
without prior notice.

We do not guarantee uninterrupted or error-free operation.
"""))

# ===== TERMINATION =====
st.header(t("8. Termination"))

st.markdown(t("""
We reserve the right to suspend or terminate access to the platform if you violate these terms 
or engage in harmful or abusive behavior.

You may stop using the platform at any time.
"""))

# ===== CHANGES TO TERMS =====
st.header(t("9. Changes to Terms"))

st.markdown(t("""
These Terms & Conditions may be updated periodically. Continued use of the platform after changes 
constitutes acceptance of the updated terms.
"""))

# ===== GOVERNING PRINCIPLE =====
st.header(t("10. Governing Principle"))

st.markdown(t("""
These terms are intended to ensure fair use, transparency, and protection for both the user 
and the platform.
"""))

# ===== CONTACT =====
st.header(t("11. Contact"))

st.markdown(t("""
If you have any questions regarding these Terms & Conditions, please contact:

📧 csaha@mun.ca
"""))

st.info(t("By using DGP Finance, you acknowledge that you have read, understood, and agreed to these Terms & Conditions."))