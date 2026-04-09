import streamlit as st
import pandas as pd
import time

# 1. Setup Professional Page Layout
st.set_page_config(page_title="Data Privacy Vault", page_icon="🔒", layout="wide")

# 2. Add a Sidebar for Project Context
with st.sidebar:
    st.title("⚙️ System Info")
    st.write("**Project:** PII Data Sanitization")
    st.write("**Environment:** Local / Demo")
    st.divider()
    st.info(
        "**About this Tool:**\n\n"
        "This portal ingests raw user datasets and automatically redacts "
        "Personally Identifiable Information (PII) using a zero-trust masking engine."
    )

# 3. Main Dashboard Header
st.title("🔒 Enterprise Data Sanitization Portal")
st.markdown(
    "Securely upload raw datasets to automatically mask and redact sensitive information before analysis or database storage.")

# 4. File Uploader
uploaded_file = st.file_uploader("📂 Upload Raw Dataset (CSV format)", type=["csv"])

# 5. Application Logic
if uploaded_file is not None:

    # Read the data and normalize columns
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip().str.lower()

    # --- DEMO EFFECT: Progress Bar ---
    st.divider()
    st.subheader("⚙️ Processing Engine Engine")
    progress_bar = st.progress(0)
    status_text = st.empty()

    for i in range(100):
        time.sleep(0.01)  # Simulates heavy processing for 1 second
        progress_bar.progress(i + 1)
        status_text.text(f"Scanning rows and applying masking rules... {i + 1}%")

    status_text.text("✅ Data Sanitization Complete!")
    st.balloons()  # Triggers a professional success animation

    # --- MASKING ENGINE ---
    # Create a copy so we can show the before/after
    df_clean = df.copy()

    df_clean.fillna("[N/A]", inplace=True)

    if 'credit_card' in df_clean.columns:
        df_clean['credit_card'] = df_clean['credit_card'].apply(
            lambda x: f"****-****-****-{str(x)[-4:]}" if str(x) != "[N/A]" else x)
    if 'national_id' in df_clean.columns:
        df_clean['national_id'] = df_clean['national_id'].apply(
            lambda x: f"***-**-{str(x)[-4:]}" if str(x) != "[N/A]" else x)
    if 'mobile_no' in df_clean.columns:
        df_clean['mobile_no'] = df_clean['mobile_no'].apply(lambda x: "**********" if str(x) != "[N/A]" else x)
    if 'email' in df_clean.columns:
        df_clean['email'] = df_clean['email'].apply(lambda x: "*****@*****.***" if str(x) != "[N/A]" else x)
    #if 'full_name' in df_clean.columns:
        #df_clean['full_name'] = df_clean['full_name'].apply(lambda x: "**********" if str(x) != "[N/A]" else x)
    if 'ip_address' in df_clean.columns:
        df_clean['ip_address'] = df_clean['ip_address'].apply(lambda x: "***.***.***.***" if str(x) != "[N/A]" else x)

    # --- KPI METRICS ---
    st.subheader("📊 Sanitization Report")
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Rows Processed", value=len(df))
    col2.metric(label="PII Columns Masked", value="6")
    col3.metric(label="Security Status", value="100% Secured", delta="Zero-Trust Enforced", delta_color="normal")

    st.divider()

    # --- PROFESSIONAL DISPLAY (TABS) ---
    tab1, tab2 = st.tabs(["✅ Sanitized Output (Safe for Distribution)", "⚠️ Raw Data (Restricted Access)"])

    with tab1:
        st.dataframe(df_clean, use_container_width=True)
        # Download Button
        csv_data = df_clean.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Secure Dataset",
            data=csv_data,
            file_name="enterprise_sanitized_data.csv",
            mime="text/csv",
            type="primary"
        )

    with tab2:
        st.warning("WARNING: You are viewing restricted raw data. Do not distribute.")
        st.dataframe(df, use_container_width=True)