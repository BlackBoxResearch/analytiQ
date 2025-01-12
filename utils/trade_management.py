from utils.database_management import execute_query

def process_deals(deals, account_id):
    """
    Processes a list of deals into positions and balance operations.

    Args:
        deals (list): List of deal objects.
        account_id (str): The ID of the account associated with the deals.

    Returns:
        tuple: A tuple containing two lists:
            - positions: Processed positions grouped by positionId.
            - balance_operations: Processed balance operations.
    """
    positions = {}
    balance_operations = []

    for deal in deals:
        deal_type = deal.get('type')
        if deal_type == 'DEAL_TYPE_BALANCE':
            # Process balance operation
            balance_operations.append({
                'account_id': account_id,
                'time': deal.get('time'),
                'type': 'deposit' if deal.get('profit', 0) > 0 else 'withdrawal',
                'amount': deal.get('profit', 0),  # Positive or negative profit
                'comment': deal.get('comment', '')  # Optional, if available
            })
            continue

        # Process positions
        position_id = deal.get('positionId')
        if not position_id:
            continue

        if position_id not in positions:
            positions[position_id] = {
                'position_id': position_id,
                'account_id': account_id,
                'symbol': deal.get('symbol'),
                'volume': deal.get('volume', 0.0),
                'type': 'BUY' if deal.get('type') == 'DEAL_TYPE_BUY' else 'SELL',
                'open_time': None,
                'open_price': None,
                'stop_loss': None,
                'take_profit': None,
                'close_time': None,
                'close_price': None,
                'commission': 0.0,
                'swap': 0.0,
                'profit': 0.0
            }

        # Update trade details based on deal type
        if deal.get('entryType') == 'DEAL_ENTRY_IN':
            positions[position_id]['open_time'] = deal.get('time')
            positions[position_id]['open_price'] = deal.get('price')
        elif deal.get('entryType') == 'DEAL_ENTRY_OUT':
            positions[position_id]['stop_loss'] = deal.get('stopLoss')
            positions[position_id]['take_profit'] = deal.get('takeProfit')
            positions[position_id]['close_time'] = deal.get('time')
            positions[position_id]['close_price'] = deal.get('price')

        # Accumulate financial data
        positions[position_id]['commission'] += deal.get('commission', 0.0)
        positions[position_id]['swap'] += deal.get('swap', 0.0)
        positions[position_id]['profit'] += deal.get('profit', 0.0)

    return list(positions.values()), balance_operations


def save_positions(account_id, positions):
    query = '''
        INSERT INTO trades (
            account_id,
            position_id,
            symbol,
            volume,
            type,
            open_time,
            open_price,
            stop_loss,
            take_profit,
            close_time,
            close_price,
            commission,
            swap,
            profit
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    for position in positions:
        params = (
            account_id,
            position['position_id'],
            position['symbol'],
            position['volume'],
            position['type'],
            position['open_time'],
            position['open_price'],
            position['stop_loss'],
            position['take_profit'],
            position['close_time'],
            position['close_price'],
            position['commission'],
            position['swap'],
            position['profit'],
        )
        execute_query(query, params, fetch_results=False)
