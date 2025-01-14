import streamlit as st
import time
from utils.account_management import deploy_account
from utils.database_management import execute_query

def accounts_page():
    st.write("accounts")

    @st.dialog("Add Account")
    def add_account_dialog():
        # Check the number of active accounts for the current user
        user_id = st.session_state["user_id"]
        query = "SELECT COUNT(*) AS active_account_count FROM accounts WHERE user_id = %s AND active = TRUE"
        result = execute_query(query, (user_id,))
        
        if result:
            active_account_count = result[0]["active_account_count"]
        else:
            st.error("Could not retrieve account information. Please try again later.")
            return

        if active_account_count >= 3:
            st.warning("You have reached the maximum limit of 3 connected accounts.")
            return

        # User input for adding a new account
        account_name = st.text_input("Account Name", placeholder="e.g., Main Account")
        login = st.text_input("Account Number", placeholder="Account Number")
        password = st.text_input("Investor Password", placeholder="Investor Password", type="password")
        server = st.text_input("Server", placeholder="Server")
        platform = st.selectbox("Platform", ("mt4", "mt5"), placeholder="Platform")

        confirm_add_account_button = st.button("Add Account", key="confirm_add_account_button", icon=":material/check:", type="secondary", use_container_width=True)

        if confirm_add_account_button:
            with st.spinner("Adding your account..."):
                if deploy_account(
                    user_id=user_id,
                    name=account_name,
                    login=login,
                    password=password,
                    server_name=server,
                    platform=platform,
                ):
                    st.success("Account successfully added!")
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("Failed to add account.")

    open_add_account_dialog = st.button(label="Add Account", key="open_add_account_dialog", icon=":material/add_circle:", type="secondary", use_container_width=True)

    if open_add_account_dialog: add_account_dialog()
    
if __name__ == "__main__":
    accounts_page()
