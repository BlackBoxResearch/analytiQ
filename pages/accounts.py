import streamlit as st
import time
import nest_asyncio
import asyncio
from utils.account_management import deploy_account
from utils.database_management import execute_query
from static.elements import tile, metric_tile

def summary_tiles(height, gain_value, win_rate_value, profit_factor_value, analytiq_score_value):
    summary_tile_1, summary_tile_2, summary_tile_3, summary_tile_4 = st.columns(4, vertical_alignment="bottom")

    with summary_tile_1:
        metric_tile(key="summary_tile_1", 
                    stat="Gain", 
                    value=gain_value, 
                    height=height, 
                    border=True, 
                    tooltip=None
                    )
    
    with summary_tile_2:
        metric_tile(key="summary_tile_2", 
                    stat="Win Rate", 
                    value=win_rate_value, 
                    height=height, 
                    border=True, 
                    tooltip=None
                    )
    
    with summary_tile_3:
        metric_tile(key="summary_tile_3", 
                    stat="Profit Factor", 
                    value=profit_factor_value, 
                    height=height, 
                    border=True, 
                    tooltip=None
                    )
    
    with summary_tile_4:
        metric_tile(key="summary_tile_4", 
                    stat="AnalytiQ Score", 
                    value=analytiq_score_value, 
                    height=height, 
                    border=True, 
                    tooltip=None
                    )










def accounts_page():
    user_id = st.session_state["user_id"]

    st.subheader(f'My Accounts', anchor=False)

    @st.dialog("Add Account")
    def add_account_dialog():
        # Check the number of active accounts for the current user
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
            with st.spinner("Deploying account..."):
                time.sleep(3)
            with st.spinner("Fetching trade history..."):
                try:
                    # Ensure there is an event loop in the current thread
                    try:
                        loop = asyncio.get_event_loop()
                    except RuntimeError:
                        # No event loop in the current thread; create a new one
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                    
                    # Run the async function in the current thread's event loop
                    account = loop.run_until_complete(deploy_account(
                        user_id=user_id,
                        name=account_name,
                        login=login,
                        password=password,
                        server_name=server,
                        platform=platform,
                    ))
                    st.success("Account successfully added!")
                    time.sleep(2)
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to add account: {e}")
    
    # Execute the query
    query = "SELECT account_id, name, login FROM accounts WHERE user_id = %s AND active = TRUE"
    user_accounts = execute_query(query, (user_id,))

    # Extract name and login values to display in the desired format
    if user_accounts:
        account_options = [f"{account['name']} ({account['login']})" for account in user_accounts]  # Format as "name (login)"
        select_disabled = False
    else:
        account_options = ["No accounts available"]
        select_disabled = True

    select_account_column, add_account_column = st.columns(2, vertical_alignment="bottom")

    account_selection = select_account_column.selectbox("Select Account", account_options, disabled=select_disabled)

    if add_account_column.button(label="Add Account", key="open_add_account_dialog", icon=":material/add_circle:", type="secondary", use_container_width=True):
         add_account_dialog()

    if account_selection != "No accounts available":
        gain = 55
        win_rate = 64
        profit_factor = 1.32
        analytiq_score = 75
        summary_tiles(
            55, 
            f"{gain}%",
            f"{win_rate}%",
            f"{profit_factor}",
            f"{analytiq_score}",
        )

if __name__ == "__main__":
    accounts_page()
