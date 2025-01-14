from utils.trade_management import process_deals, save_positions
from utils.database_management import execute_query
from metaapi_cloud_sdk import MetaApi
import streamlit as st
from datetime import datetime, timezone

TOKEN = st.secrets['META_API_TOKEN']

def save_account(user_id, account_id, account_info, account_name):
    """
    Saves account details to the database.

    Args:
        user_id (int): The ID of the user who owns the account.
        account_id (str): The unique ID of the account in MetaApi.
        account_info (dict): The account's information from MetaApi, including platform, broker, and server details.
        account_name (str): The name assigned to the account by the user.

    Returns:
        None
    """
    query = '''
        INSERT INTO accounts (
            user_id,
            account_id,
            platform,
            type,
            broker,
            currency,
            server,
            leverage,
            margin_mode,
            name,
            login
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    params = (
        user_id,
        account_id,
        account_info['platform'],
        account_info['type'],
        account_info['broker'],
        account_info['currency'],
        account_info['server'],
        account_info['leverage'],
        account_info['marginMode'],
        account_name,
        account_info['login']
    )
    execute_query(query, params, fetch_results=False)
    print("Account information saved to database.")

def save_balance_operations(account_id, balance_operations):
    """
    Saves balance operations related to an account to the database.

    Args:
        account_id (str): The unique ID of the account in MetaApi.
        balance_operations (list): A list of balance operation objects, each containing time, type, amount, and comment.

    Returns:
        None
    """
    query = '''
        INSERT INTO balance_operations (
            account_id,
            time,
            type,
            amount,
            comment
        ) 
        VALUES (%s, %s, %s, %s, %s)
    '''
    for operation in balance_operations:
        params = (
            account_id,
            operation['time'],
            operation['type'],
            operation['amount'],
            operation['comment']
        )
        execute_query(query, params, fetch_results=False)

async def deploy_account(user_id, name, login, password, server_name, platform):
    """
    Deploys or reconnects a MetaTrader account to MetaApi.

    Args:
        user_id (int): The ID of the user deploying the account.
        name (str): The name to assign to the account in MetaApi.
        login (str): The account's login credentials.
        password (str): The account's password.
        server_name (str): The server name of the broker.
        platform (str): The platform type (e.g., "mt4" or "mt5").

    Returns:
        MetaTraderAccount: The deployed MetaApi account object.
    """
    api = MetaApi(TOKEN)

    # Check if account exists on MetaApi
    accounts = await api.metatrader_account_api.get_accounts_with_infinite_scroll_pagination()
    account = next((item for item in accounts if item.login == login and item.type.startswith('cloud')), None)

    if account:
        print(f"Account already exists on MetaApi with ID: {account.id}. Redeploying and reconnecting...")
        await account.deploy()

        print('Waiting for API server to connect to broker (may take a couple of minutes)...')
        await account.wait_connected()

        connection = account.get_rpc_connection()
        await connection.connect()

        print('Waiting for SDK to synchronize to terminal state (may take some time depending on your history size)...')
        await connection.wait_synchronized(600)

        print("Reconnected to account successfully.")
    else:
        # Create a new account if it doesn't exist
        print("Creating a new account...")
        account = await api.metatrader_account_api.create_account({
            'name': name,
            'type': 'cloud',
            'login': login,
            'password': password,
            'server': server_name,
            'platform': platform,
            'application': 'MetaApi',
            'magic': 1000,
        })
        print(f"Account created with ID: {account.id}.")

        print('Deploying account...')
        await account.deploy()

        print('Waiting for API server to connect to broker (may take a couple of minutes)...')
        await account.wait_connected()

        connection = account.get_rpc_connection()
        await connection.connect()

        print('Waiting for SDK to synchronize to terminal state (may take some time depending on your history size)...')
        await connection.wait_synchronized(600)

    # Fetch account information
    print('Fetching account information...')
    account_info = await connection.get_account_information()
    print('Account information:', account_info)

    # Save account to the database
    save_account(user_id, account.id, account_info, name)
    print("Account added to database.")

    # Fetch and process historical deals
    print('Fetching historical deals...')
    start_time = datetime(2020, 1, 1, tzinfo=timezone.utc)
    end_time = datetime.now(timezone.utc)
    deals_response = await connection.get_deals_by_time_range(start_time, end_time)

    deals = deals_response.get('deals', [])
    positions, balance_operations = process_deals(deals, account.id)

    # Save historical data to the database
    save_positions(account.id, positions)
    save_balance_operations(account.id, balance_operations)

    print("Historical data saved successfully.")
    return account

async def undeploy_account(account_id):
    """
    Undeploys an account, making it dormant but available for redeployment.

    Args:
        account_id (str): The unique ID of the account to be undeployed.

    Returns:
        bool: True if the account was successfully undeployed, False otherwise.
    """
    api = MetaApi(TOKEN)

    try:
        # Fetch the account from MetaApi
        account = await api.metatrader_account_api.get_account(account_id)
        if not account:
            print(f"Account with ID {account_id} not found.")
            return False

        # Undeploy the account
        print(f"Undeploying account with ID: {account_id}...")
        await account.undeploy()

        print(f"Account with ID {account_id} has been undeployed and is now dormant.")
        return True

    except Exception as e:
        print(f"An error occurred while undeploying the account: {e}")
        return False

