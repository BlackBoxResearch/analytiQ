import streamlit as st
import time

def accounts_page():
    st.write("accounts")

    @st.dialog("Add Account")
    def add_account_dialog():
        accountaccount_number = st.text_input("Account Number", placeholder="Account Number")
        password = st.text_input("Investor Password", placeholder="Investor Password", type="password")
        server = st.text_input("Server", placeholder="Server")
        platform = st.selectbox("Platform", ("mt4", "mt5"), placeholder="Platform")

        confirm_add_account_button = st.button("Add Account", key="confirm_add_account_button", icon=":material/check:", type="secondary", use_container_width=True)

        if confirm_add_account_button:
            with st.spinner("Adding your account..."):
                time.sleep(2)
            st.success("Account successfully added! (TEST)")
            time.sleep(2)
            st.rerun()

    open_add_account_dialog = st.button(label="Add Account", key="open_add_account_dialog", icon=":material/add_circle:", type="secondary", use_container_width=True)

    if open_add_account_dialog: add_account_dialog()
    
if __name__ == "__main__":
    accounts_page()
