import streamlit as st
import time
import nest_asyncio
import asyncio
import pandas as pd
from utils.account_management import deploy_account, undeploy_account, run_async_function
from utils.database_management import execute_query
from static.elements import tile, metric_tile, gradient_tile

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
        gradient_tile(
            key="summary_tile_4", 
            content=f"""
                <div style="line-height: 1.5;">
                    <p style="margin: 0; font-size: 0.9em; color: #878884;">AnalytiQ Score</p>
                    <p style="margin: 0; font-size: 1.4em; font-weight: bold; color: #E8E8E8;">{analytiq_score_value}</p>
                </div>
                """
            )
    
def get_trades(account_id):
    """
    Retrieves all trades for a given account ID.

    Args:
        account_id (int): The ID of the account to retrieve trades for.

    Returns:
        list or None: A list of trades for the specified account ID, or None if an error occurs.
    """
    trades_query = "SELECT * FROM trades WHERE account_id = %s"
    trades = execute_query(trades_query, (account_id,))
    if trades is None:
        print(f"Failed to retrieve trades for account_id: {account_id}")
    return trades

def get_balances(account_id):
    """
    Retrieves all balance operations for a given account ID.

    Args:
        account_id (int): The ID of the account to retrieve balance operations for.

    Returns:
        list or None: A list of balance operations for the specified account ID, or None if an error occurs.
    """
    balances_query = "SELECT * FROM balance_operations WHERE account_id = %s"
    balances = execute_query(balances_query, (account_id,))
    if balances is None:
        print(f"Failed to retrieve balances for account_id: {account_id}")
    return balances

def dashboard_page():
    user_id = st.session_state["user_id"]
    first_name = st.session_state["first_name"]
    
    st.subheader(f'Welcome {first_name}', anchor=False)

    
    # Execute the query to fetch user accounts
    query = "SELECT account_id, name, login FROM accounts WHERE user_id = %s AND active = TRUE"
    user_accounts = execute_query(query, (user_id,))

    # Extract options and map them to account IDs
    if user_accounts:
        account_map = {f"{account['name']} ({account['login']})": account['account_id'] for account in user_accounts}
        account_options = list(account_map.keys())
        select_disabled = False
    else:
        account_map = {}
        account_options = ["No accounts available"]
        select_disabled = True

    select_account_column, add_account_column, delete_account_column = st.columns([2,1,1], vertical_alignment="bottom")
    account_selection = select_account_column.selectbox("Select Account", account_options, disabled=select_disabled)

    with add_account_column.popover("Add Account", icon=":material/add_circle:", use_container_width=True):
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

        confirm_add_account_button = st.button(label="Add Account", key="confirm_add_account_button", icon=":material/check:", type="secondary", use_container_width=True)

        if confirm_add_account_button:
            with st.spinner("Deploying account..."):
                time.sleep(3)
            with st.spinner("Fetching trade history..."):
                try:
                    run_async_function(
                        deploy_account,
                        user_id=user_id,
                        name=account_name,
                        login=login,
                        password=password,
                        server_name=server,
                        platform=platform,
                    )
                    st.success("Account successfully added!")
                    time.sleep(2)
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to add account: {e}")

    with delete_account_column:

        if account_selection != "No accounts available":
            disabled = True
        else:
            disabled = False

        delete_account_button = st.button("Delete Account", icon=":material/delete:", use_container_width=True, disabled=disabled)

        if delete_account_button:

            @st.dialog("Delete Account")
            def delete_account_dialog():
                st.write("Are you sure you want delete this account?")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Yes", type="secondary", use_container_width=True):
                        with st.spinner("Deleting account..."):
                            try:
                                run_async_function(undeploy_account, account_id=selected_account_id)
                                st.success("Account successfully deleted!")
                                time.sleep(2)
                                st.rerun()
                            except Exception as e:
                                st.error(f"Failed to delete account: {e}")
                        st.rerun()
                with col2:
                    if st.button("No", type="primary", use_container_width=True):
                        st.rerun()
            
            delete_account_dialog()


    if account_selection != "No accounts available":
        selected_account_id = account_map[account_selection]

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

        tab1, tab2 = st.tabs(["Deal History", "Settings"])
           

if __name__ == "__main__":
    dashboard_page()
 