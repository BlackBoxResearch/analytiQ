import streamlit as st
from metaapi_cloud_sdk import MetaApi
import asyncio
from datetime import datetime, timezone

TOKEN = 'eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiIxNzM2NDVlM2U5MThkZjE2NjQzZmFjZDI0NTBlMGVmMiIsImFjY2Vzc1J1bGVzIjpbeyJpZCI6InRyYWRpbmctYWNjb3VudC1tYW5hZ2VtZW50LWFwaSIsIm1ldGhvZHMiOlsidHJhZGluZy1hY2NvdW50LW1hbmFnZW1lbnQtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVzdC1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcnBjLWFwaSIsIm1ldGhvZHMiOlsibWV0YWFwaS1hcGk6d3M6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6Im1ldGFhcGktcmVhbC10aW1lLXN0cmVhbWluZy1hcGkiLCJtZXRob2RzIjpbIm1ldGFhcGktYXBpOndzOnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJtZXRhc3RhdHMtYXBpIiwibWV0aG9kcyI6WyJtZXRhc3RhdHMtYXBpOnJlc3Q6cHVibGljOio6KiJdLCJyb2xlcyI6WyJyZWFkZXIiLCJ3cml0ZXIiXSwicmVzb3VyY2VzIjpbIio6JFVTRVJfSUQkOioiXX0seyJpZCI6InJpc2stbWFuYWdlbWVudC1hcGkiLCJtZXRob2RzIjpbInJpc2stbWFuYWdlbWVudC1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoiY29weWZhY3RvcnktYXBpIiwibWV0aG9kcyI6WyJjb3B5ZmFjdG9yeS1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciIsIndyaXRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfSx7ImlkIjoibXQtbWFuYWdlci1hcGkiLCJtZXRob2RzIjpbIm10LW1hbmFnZXItYXBpOnJlc3Q6ZGVhbGluZzoqOioiLCJtdC1tYW5hZ2VyLWFwaTpyZXN0OnB1YmxpYzoqOioiXSwicm9sZXMiOlsicmVhZGVyIiwid3JpdGVyIl0sInJlc291cmNlcyI6WyIqOiRVU0VSX0lEJDoqIl19LHsiaWQiOiJiaWxsaW5nLWFwaSIsIm1ldGhvZHMiOlsiYmlsbGluZy1hcGk6cmVzdDpwdWJsaWM6KjoqIl0sInJvbGVzIjpbInJlYWRlciJdLCJyZXNvdXJjZXMiOlsiKjokVVNFUl9JRCQ6KiJdfV0sImlnbm9yZVJhdGVMaW1pdHMiOmZhbHNlLCJ0b2tlbklkIjoiMjAyMTAyMTMiLCJpbXBlcnNvbmF0ZWQiOmZhbHNlLCJyZWFsVXNlcklkIjoiMTczNjQ1ZTNlOTE4ZGYxNjY0M2ZhY2QyNDUwZTBlZjIiLCJpYXQiOjE3NjY4ODQwMzh9.TxlTccBIbkoaxc39Ud1QbAuIeyi9YMcKxQaAMolJCjjptHRoMWy1DMzDhYo5wd5RtNbv3jrG2Y81Qx2mDC5C0UIjHIwRMADZuLtWtiFSPTPdfeqQBhk2tR12tzDrr8TZSMNH-lLTYx_MDTTDQkvJi2iDNy4U1V9kJxJ2qhgHPFhJYUN635r3A4M_hS2SvygUA6-zpiBlmEBiEk7CCxNe8l2ERVdMcYUwpFdfp_8rLKT94mVKAG6CspZYOgtAAbqEjcryZ9TStQ4_adhGU3UQt0n_AjNgPxwdxErKFEDI4UpJIeOfVZgbnSW_47W0sufRfTwz99RJNBHJvwNTCzsMeOR3FPMNiEtEnVD2lC4QzKg9ag_aOZ79hlGJ_NXLA_RnYD5rCnoRzxeiERdVgr2_29_ZZguGqaBXrUp8D7DKFsAMH_cyo7AbwHOi8tLRR5XxhzjtmDCJuhRyWT8ILEcl6Pety9ZN99Ekjx1C4SKfpsjmRmGu46J3yskdPD-0f0DyDqA3PZ2_VPtPQZbC7OVmwQAYHxchJLST7TH1GUNt_xZCImWYpVLO0u1NY4WnwFUVjRA4loDimEqiZ-t_iXdWojjRhB6fppcLMh7a2OmJkS_wZv6rZGiF1uUAcuhtWizh6ZwuTJ1GMgm9KAOc6vgfP71q-y1BDOlJpNbwRGT0JOs'
login = "140276"
password = "Q!8qWiMh"
server = "SeacrestMarkets-MT5"

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

        # Update the account's active status in the database
        update_query = "UPDATE accounts SET active = TRUE WHERE account_id = %s"
        #execute_query(update_query, (account.id,), fetch_results=False)

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
    #save_account(user_id, account.id, account_info, name)
    print("Account added to database.")

    # Fetch and process historical deals
    print('Fetching historical deals...')
    start_time = datetime(2020, 1, 1, tzinfo=timezone.utc)
    end_time = datetime.now(timezone.utc)
    deals_response = await connection.get_deals_by_time_range(start_time, end_time)

    deals = deals_response.get('deals', [])
    #positions, balance_operations = process_deals(deals, account.id)

    # Save historical data to the database
    #save_positions(account.id, positions)
    #save_balance_operations(account.id, balance_operations)

    print("Historical data saved successfully.")
    return account

async def undeploy_account(account_id):
    """
    Undeploys an account, making it dormant but available for redeployment.
    Updates the account's active status to FALSE in the database.

    Args:
        account_id (str): The unique ID of the account to be undeployed.

    Returns:
        bool: True if the account was successfully undeployed and database updated, False otherwise.
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

        # Update the account's active status in the database
        update_query = "UPDATE accounts SET active = FALSE WHERE account_id = %s"
        #execute_query(update_query, (account_id,), fetch_results=False)

        print(f"Account with ID {account_id} has been undeployed and marked as inactive.")
        return True

    except Exception as e:
        print(f"An error occurred while undeploying the account: {e}")
        return False

asyncio.run(deploy_account(123, "test-account", login, password, server, "mt5"))
