import streamlit as st
import time
import pandas as pd
from utils.account_management import deploy_account, undeploy_account, run_async_function
from utils.database_management import execute_query
from static.elements import tile, metric_tile, gradient_tile, line_chart, button
from streamlit_extras import stylable_container
from streamlit_extras.switch_page_button import switch_page

def summary_tiles(height, stat_1, stat_2, stat_3, stat_4):
    
    summary_tile_1, summary_tile_2, summary_tile_3, summary_tile_4 = st.columns(4, vertical_alignment="bottom")

    with summary_tile_1:
        metric_tile(key="summary_tile_1", 
                    stat="Gain", 
                    value=stat_1, 
                    height=height, 
                    border=False, 
                    tooltip=None
                    )
    
    with summary_tile_2:
        metric_tile(key="summary_tile_2", 
                    stat="Win Rate", 
                    value=stat_2, 
                    height=height, 
                    border=False, 
                    tooltip=None
                    )
    
    with summary_tile_3:
        metric_tile(key="summary_tile_3", 
                    stat="Profit Factor", 
                    value=stat_3, 
                    height=height, 
                    border=False, 
                    tooltip=None
                    )
    
    with summary_tile_4:
        gradient_tile(
            key="summary_tile_4", 
            content=f"""
                <div style="line-height: 1.5;">
                    <p style="margin: 0; font-size: 0.9em; color: #878884;">AnalytiQ Score</p>
                    <p style="margin: 0; font-size: 1.4em; font-weight: bold; color: #E8E8E8;">{stat_4}</p>
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

@st.dialog("Delete Account")
def delete_account_dialog(selected_account_id):
    st.write("Are you sure you want delete this account?")
    col1, col2 = st.columns(2)

    with col1:
        proceed_button = st.button("Yes", type="secondary", use_container_width=True)

    with col2:
        if button("No", "cancel_delete", '#ca4747', None, False):
            switch_page("Dashboard")
            #st.rerun()

    if proceed_button:
        with st.spinner("Deleting account..."):
            try:
                run_async_function(undeploy_account, account_id=selected_account_id)
                st.success("Account successfully deleted!")
                time.sleep(2)
                st.rerun()
            except Exception as e:
                st.error(f"Failed to delete account: {e}")
        st.rerun()

def dashboard_page():
    user_id = st.session_state["user_id"]
    first_name = st.session_state["first_name"]
    
    st.subheader(f'Welcome, {first_name}!', anchor=False)
    st.info("This is your **Dashboard** where you can connect your trading accounts, and analyse your performance.")
    
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
    
    with select_account_column:
        account_selection = st.selectbox("Select Account", account_options, disabled=select_disabled)

    with add_account_column:
        # Check the number of active accounts for the current user
        query = "SELECT COUNT(*) AS active_account_count FROM accounts WHERE user_id = %s AND active = TRUE"
        result = execute_query(query, (user_id,))

        if result and len(result) > 0:
            active_account_count = result[0]["active_account_count"]
        else:
            active_account_count = 0  # Fallback if no result found

        if active_account_count >= 3:
            add_account_disabled = True
        else:
            add_account_disabled = False

        with st.popover("Add Account", 
                        icon=":material/add_circle:", 
                        use_container_width=True, 
                        disabled=add_account_disabled):
            
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
            disabled = False
        else:
            disabled = True

        if button(label="Delete Account",
                  key="delete-account-button",
                  color='#ca4747',
                  icon=":material/delete:",
                  disabled=disabled,
            ):
            delete_account_dialog(selected_account_id)

    if account_selection != "No accounts available":
        selected_account_id = account_map[account_selection]
        st.divider()

        st.subheader(f'{selected_account_id['name']}')

        summary_tiles(
            height=55, 
            stat_1=f"55%",
            stat_2=f"64%",
            stat_3=f"1.32",
            stat_4=f"75",
        )

        data = pd.DataFrame({
            "Date": [
                "2024-01-31", "2024-02-29", "2024-03-31", "2024-04-30", 
                "2024-05-31", "2024-06-30", "2024-07-31", "2024-08-31", 
                "2024-09-30", "2024-10-31", "2024-11-30", "2024-12-31"
            ],
            "Portfolio Returns": [
                -0.094091, -0.126721, -0.095698, -0.071110, 
                -0.103823, 0.067332, 0.205205, 0.217096, 
                0.157245, 0.236674, 0.488432, 0.440673
            ]
        })

        col1, col2 = st.columns([3,1], vertical_alignment="top")

        with col1:
            with tile("performance_overview_chart", 300, border=False):
                st.markdown("**Performance**")
                line_chart(
                    data=data,
                    x="Date",
                    y="Portfolio Returns",
                    x_label="Date",
                    y_label="Cumulative Returns",
                    height=250,
                    show_labels=False,
                    line_color='#3952f5',
                    fill_color='#3952f5',
                )

        with col2:
            tile("stats", height=300, border=False)       

if __name__ == "__main__":
    dashboard_page()
 
