from trade_management import process_deals, save_positions
from utils.database_management import execute_query
from metaapi_cloud_sdk import MetaApi
import asyncio
import streamlit as st
from datetime import datetime, timezone

TOKEN = st.secrets['META_API_TOKEN']

def save_account(user_id, account_id, account_info, account_name):
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
    api = MetaApi(TOKEN)

    accounts = await api.metatrader_account_api.get_accounts_with_infinite_scroll_pagination()
    account = next((item for item in accounts if item.login == login and item.type.startswith('cloud')), None)

    if account:
        print(f"Account already exists on MetaApi with ID: {account.id}")
        return account

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

    # Connect to MetaApi API
    connection = account.get_rpc_connection()
    await connection.connect()

    # Wait until the terminal state is synchronized
    print('Waiting for SDK to synchronize to terminal state (may take some time depending on your history size)...')
    await connection.wait_synchronized(600)

    # Access account information using appropriate SDK methods
    print('Testing terminal state access...')
    account_info = await connection.get_account_information()
    print('Account information:', account_info)

    save_account(user_id, account.id, account_info, name)
    print("Account added to database")

    # Ensure start_time and end_time are datetime objects
    start_time = datetime(2020, 1, 1, tzinfo=timezone.utc)
    end_time = datetime.now(timezone.utc)

    deals_response = await connection.get_deals_by_time_range(start_time, end_time)

    deals = deals_response.get('deals', [])

    positions, balance_operations = process_deals(deals, account.id)

    save_positions(account.id, positions)
    save_balance_operations(account.id, balance_operations)
