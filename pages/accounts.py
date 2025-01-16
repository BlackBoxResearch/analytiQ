import streamlit as st
import time
import nest_asyncio
import asyncio
import pandas as pd
from utils.account_management import deploy_account, undeploy_account
from utils.database_management import execute_query
from static.elements import tile, metric_tile

@st.dialog("Pricing", width="large")
def pricing_table():
    st.components.v1.html(
        html='''<script async src="https://js.stripe.com/v3/pricing-table.js"></script>
        <stripe-pricing-table pricing-table-id="prctbl_1QhhzHDjNID2hO5KdY8PhrUJ"
        publishable-key="pk_test_51QK6BRDjNID2hO5KX6S5w4J0oO3PFEL6TRZ9fkJzXdGPlgTwWk56DoDX6RZvVL8eWy2EMEugQ2ojG3AsQBST6IHH00T2LJFAU3">
        </stripe-pricing-table>
        ''', height=500, scrolling=True)

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

def accounts_page():
    st.subheader(f'My Accounts', anchor=False)
    user_id = st.session_state["user_id"]
    
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

    select_account_column, add_account_column = st.columns(2, vertical_alignment="bottom")

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

        confirm_add_account_button = st.button(label="Add Account", key="confirm_add_account_button", icon=":material/check:", type="primary", use_container_width=True)

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
                    loop.run_until_complete(deploy_account(
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

        with tab1:
            open_pricing = st.button("Open Pricing")
            if open_pricing:
                pricing_table()

            st.dataframe(pd.DataFrame(get_trades(selected_account_id)), hide_index=True, use_container_width=True)
            st.dataframe(pd.DataFrame(get_balances(selected_account_id)), hide_index=True, use_container_width=True)

        with tab2:
            delete_account_button = st.button("Delete Account")

            if delete_account_button:
                with st.spinner("Deleting account..."):
                    try:
                        # Ensure there is an event loop in the current thread
                        try:
                            loop = asyncio.get_event_loop()
                        except RuntimeError:
                            # No event loop in the current thread; create a new one
                            loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(loop)
                        
                        # Run the async function in the current thread's event loop
                        loop.run_until_complete(undeploy_account(
                            account_id=selected_account_id
                        ))
                        st.success("Account successfully deleted!")
                        time.sleep(2)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to delete account: {e}")

if __name__ == "__main__":
    accounts_page()
 