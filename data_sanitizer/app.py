import streamlit as st
import pandas as pd

# --- 1. SETUP PAGE CONFIGURATION ---
st.set_page_config(page_title="Data Masking Studio", layout="wide", page_icon="🔐")

st.title("🔐 Enterprise Data Masking Studio")
st.markdown("Securely manage and sanitize datasets for different clients using Role-Based Access Control.")

# --- 2. INITIALIZE SESSION STATE (APP MEMORY) ---
# This keeps track of different clients and their specific masking rules even when the page refreshes.
if "clients" not in st.session_state:
    st.session_state.clients = {"Admin": {}}

if "selected_client" not in st.session_state:
    st.session_state.selected_client = "Admin"

# --- 3. FILE UPLOAD (SECURE INGESTION) ---
uploaded_file = st.file_uploader("📂 Upload Raw Dataset (CSV format)", type=["csv"])

if uploaded_file:
    # Read data into memory and clean column names
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()

    # --- 4. SIDEBAR: CLIENT MANAGEMENT ---
    st.sidebar.title("👥 Client Management")
    client_names = list(st.session_state.clients.keys())

    # Failsafe: Ensure selected client is valid
    if st.session_state.selected_client not in client_names:
        st.session_state.selected_client = "Admin"

    # Dropdown to switch between active clients
    selected_client = st.sidebar.selectbox(
        "Select Active Client Profile",
        client_names,
        index=client_names.index(st.session_state.selected_client)
    )
    st.session_state.selected_client = selected_client
    st.sidebar.markdown("---")

    # Add a New Client Profile
    st.sidebar.subheader("➕ Add New Client")
    new_client = st.sidebar.text_input("Enter Client Name")
    if st.sidebar.button("Add Client"):
        if new_client and new_client not in st.session_state.clients:
            st.session_state.clients[new_client] = {}
            st.session_state.selected_client = new_client
            st.rerun()  # Refresh UI to show new client
        elif new_client in st.session_state.clients:
            st.sidebar.error("Client name already exists!")
        else:
            st.sidebar.error("Please enter a valid name.")

    # Remove an Existing Client Profile
    st.sidebar.subheader("❌ Remove Client")
    remove_client = st.sidebar.selectbox(
        "Select Client to Remove",
        client_names,
        key="remove_select"
    )
    if st.sidebar.button("Remove Client"):
        if remove_client == "Admin":
            st.sidebar.error("The Admin profile cannot be removed.")
        else:
            del st.session_state.clients[remove_client]
            remaining = list(st.session_state.clients.keys())
            st.session_state.selected_client = remaining[0]
            st.rerun()  # Refresh UI after deletion

    st.sidebar.success(f"Currently Configuring: {st.session_state.selected_client}")

    # --- 5. MAIN LAYOUT (SPLIT SCREEN) ---
    left_col, right_col = st.columns([2, 1])

    # Left Column: Raw Data Preview
    with left_col:
        st.subheader("📊 Raw Dataset Preview (Top 20 Rows)")
        # Show only first 20 rows to prevent crashing the browser on large files
        st.dataframe(df.head(20), use_container_width=True)

    # Right Column: Dynamic Masking Controls
    with right_col:
        st.subheader(f"⚙️ Mask Controls → {selected_client}")
        client_rules = st.session_state.clients[selected_client]

        # Generate a dropdown rule selector for every column in the dataset
        for col in df.columns:
            client_rules[col] = st.selectbox(
                f"Rule for '{col}'",
                ["No Mask", "Partial Mask", "Full Mask"],
                index=["No Mask", "Partial Mask", "Full Mask"].index(
                    client_rules.get(col, "No Mask")  # Default to No Mask
                ),
                key=f"{selected_client}_{col}"  # Unique key per client per column
            )

    st.divider()

    # --- 6. SANITIZATION EXECUTION ---
    run_sanitization = st.button("🚀 Perform Sanitization", use_container_width=True, type="primary")


    # Core Masking Logic Engine
    def apply_mask(val, method):
        # Handle missing/empty values gracefully to prevent crashes
        if pd.isna(val) or str(val).strip() == "":
            return "[N/A]"

        val_str = str(val)

        if method == "No Mask":
            return val_str
        elif method == "Full Mask":
            return "*" * len(val_str)  # Complete blackout
        elif method == "Partial Mask":
            if len(val_str) <= 4:
                return "***"  # Too short to partial mask safely
            # Keep first 2 and last 2 characters, mask the middle
            return val_str[:2] + "*" * (len(val_str) - 4) + val_str[-2:]
