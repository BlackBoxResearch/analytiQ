from metaapi_cloud_sdk import MetaApi, SynchronizationListener
from asyncio import Queue
import asyncio

class MySynchronizationListener(SynchronizationListener):
    """A listener that prints new deal events after synchronization is complete."""

    def __init__(self, account_id):
        super().__init__()
        self.account_id = account_id
        self.synchronized = False  # Flag to indicate synchronization status

    async def on_deal_added(self, instance_index, deal):

        # Correctly check the entryType
        if deal['entryType'] == "DEAL_ENTRY_OUT":
            print(f"[Account {self.account_id}] #{deal['positionId']} Closed for ${deal['profit'] + deal['commission'] + deal['swap']}")
            # Optional: Uncomment the line below to see full deal details
            #print(f"[Account {self.account_id}] New deal added: {deal}")

async def add_account_to_stream(account_id, api, connections):
    """Dynamically adds an account to the streaming system."""
    try:
        # Retrieve the MetaTrader account
        account = await api.metatrader_account_api.get_account(account_id)
        connection = account.get_streaming_connection()
        
        # Instantiate and attach the synchronization listener
        listener = MySynchronizationListener(account_id)
        connection.add_synchronization_listener(listener)

        # Connect and synchronize
        await connection.connect()
        print(f"[Account {account_id}] Connecting and synchronizing...")
        await connection.wait_synchronized({"timeoutInSeconds": 60})
        print(f"[Account {account_id}] Connected and synchronized.")

        # Store the connection for cleanup
        connections[account_id] = connection
    except Exception as e:
        print(f"Failed to add account {account_id}: {e}")

async def monitor_queue(account_queue, api, connections):
    """Monitors the queue for new accounts and adds them dynamically."""
    while True:
        account_id = await account_queue.get()
        print(f"Adding new account {account_id} to monitoring...")
        await add_account_to_stream(account_id, api, connections)
        account_queue.task_done()

async def remove_account(account_id, connections):
    """Removes an account from the streaming system."""
    if account_id in connections:
        print(f"Removing account {account_id}...")
        await connections[account_id].close()
        del connections[account_id]
        print(f"Account {account_id} removed.")

