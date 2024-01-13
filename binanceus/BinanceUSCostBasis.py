import urllib.parse
import hashlib
import hmac
import requests
import time
import json
from decimal import Decimal

api_url = "https://api.binance.us"

### Enter your desired settings below - START

api_key='mmTrwnhpKEcTyh8PnGtXpfnwKiok57WJkGpdmEF7NwQju3hVEOWV9IGj8y4PReZ1' # Enter your BinanceUS API public key here
api_secret='Q1YMgnpMCm9nJ1qGgS2C2Ethj0azJVs4pyNKckoLGpybIlgTHmDZ3Ncdq7ARBlgO' # Enter your BinanceUS API private key here

# Set the start time to, example: November 1, 2023 (00:00:00 UTC) # Use the line below to set the date you wish to start tracking your trades.
start_time_utc = time.mktime(time.strptime('2023-11-01 00:00:00', '%Y-%m-%d %H:%M:%S')) * 1000

### Enter your desired settings above - END


uri_path = "/api/v3/myTrades"
server_time = int(requests.get(f'{api_url}/api/v3/time').json()['serverTime'])

def get_server_timestamp():
    response = requests.get('https://api.binance.us/api/v3/time').json()
    timestamp = response['serverTime']
    # rint(f'get_server_timestamp {timestamp}')
    return timestamp

def get_binanceus_signature_trades(data, secret):
    postdata = urllib.parse.urlencode(data)
    message = postdata.encode()
    byte_key = bytes(secret, 'UTF-8')
    mac = hmac.new(byte_key, message, hashlib.sha256).hexdigest()
    return mac

def get_binanceus_signature_account(api_secret, timestamp):
    message = f'timestamp={timestamp}'
    # print(f'timestamp in siggen {timestamp}')
    byte_key = bytes(api_secret, 'UTF-8')
    signature = hmac.new(byte_key, message.encode('utf-8'), hashlib.sha256).hexdigest()
    return signature

def get_account_info():
    timestamp = get_server_timestamp()
    signature = get_binanceus_signature_account(api_secret, timestamp)
    params = {'timestamp': timestamp, 'signature': signature}
    headers = {'X-MBX-APIKEY': api_key}
    response = requests.get('https://api.binance.us/api/v3/account', params=params, headers=headers)
    # print("GAI: ", timestamp, " ", signature)
    # print("GAI: ", response.json())

    return response.json()

def get_trade_history(uri_path, data, api_key, api_secret):
    headers = {}
    headers['X-MBX-APIKEY'] = api_key
    signature = get_binanceus_signature_trades(data, api_secret)
    params={
        **data,
        "signature": signature
        }
    req = requests.get((api_url + uri_path), params=params, headers=headers)

    return req.text

def calculate_average_prices(trades):
    trades_dict = json.loads(trades)
    total_buy_quantity = 0
    total_buy_value = 0
    total_sell_quantity = 0
    total_sell_value = 0

    for trade in trades_dict:
        qty = Decimal(trade['qty'])
        quote_qty = Decimal(trade['quoteQty'])
        is_buyer = trade['isBuyer']

        if is_buyer:
            total_buy_quantity += qty
            total_buy_value += quote_qty
        else:
            total_sell_quantity += qty
            total_sell_value += quote_qty

    average_buy_price = total_buy_value / total_buy_quantity if total_buy_quantity != 0 else Decimal(0)
    average_sell_price = total_sell_value / total_sell_quantity if total_sell_quantity != 0 else Decimal(0)

    return average_buy_price, average_sell_price

def calculate_total_usdt(trades):
    trades_dict = json.loads(trades)
    total_buy_value = 0
    total_sell_value = 0
    buys = []
    sells = []

    for trade in trades_dict:
        quote_qty = Decimal(trade['quoteQty'])
        is_buyer = trade['isBuyer']

        if is_buyer:
            total_buy_value += quote_qty
            buys.append(quote_qty)
        else:
            total_sell_value += quote_qty
            sells.append(quote_qty)

    return total_buy_value, total_sell_value, buys, sells

def calculate_personal_money(trades):
    trades_dict = json.loads(trades)
    personal_investment = 0

    for trade in trades_dict:
        qty = Decimal(trade['qty'])
        quote_qty = Decimal(trade['quoteQty'])
        is_buyer = trade['isBuyer']

        if is_buyer:
            # Buy trade
            personal_investment += quote_qty

    remaining_personal_money = personal_investment

    for trade in trades_dict:
        qty = Decimal(trade['qty'])
        quote_qty = Decimal(trade['quoteQty'])
        is_buyer = trade['isBuyer']

        if not is_buyer:
            # Sell trade
            remaining_personal_money -= quote_qty

    if remaining_personal_money < 0:
        remaining_personal_money = 0

    return remaining_personal_money

# Fetch account information to get a list of coins in the wallet
account_info = get_account_info()
coins_in_wallet = [asset['asset'] for asset in account_info['balances'] if float(asset['free']) > 0]
print(f'Coins in wallet: {coins_in_wallet}')

# List to store coin data
coin_data_list = []

# Loop through each coin and calculate average buy and sell prices
for coin_symbol in coins_in_wallet:
    if coin_symbol.startswith('USD'):
        continue
    symbol = coin_symbol + 'USDT'

    server_time = requests.get('https://api.binance.us/api/v3/time').json()['serverTime']
    local_time = int(time.time() * 1000)
    timestamp_diff = abs(server_time - local_time)
    if timestamp_diff > 60000:
        server_time = int(requests.get(f'{api_url}/api/v3/time').json()['serverTime'])

    data = {
        "timestamp": server_time,
        "symbol": symbol,
        'recvWindow': 60000,
        'startTime': int(start_time_utc)
    }

    price_response = requests.get(f'https://api.binance.us/api/v3/ticker/price?symbol={symbol}')
    price_data = price_response.json()
    price = float(price_data['price'])

    trade_history = get_trade_history(uri_path, data, api_key, api_secret)
    average_buy_price, average_sell_price = calculate_average_prices(trade_history)
    total_buy_value, total_sell_value, buys, sells = calculate_total_usdt(trade_history)
    personal_money_left = calculate_personal_money(trade_history)

    coin_data = {
        "pair": symbol,
        "price": price,
        "average_buy_price": average_buy_price,
        "average_sell_price": average_sell_price,
        "total_amount_spent": total_buy_value,
        "total_amount_sold": total_sell_value,
        "personal_money_left": personal_money_left
    }

    # Add data to the list
    coin_data_list.append(coin_data)

    print(f"Pair: {symbol}")
    print(f"The current price of {symbol} is: {price:.8f} USDT")
    print(f"Average Buy Price: {average_buy_price:.8f} USDT")
    print(f"Average Sell Price: {average_sell_price:.8f} USDT")
    print(f"Total Amount Spent: {total_buy_value:.8f} USDT")
    print(f"Total Amount Sold: {total_sell_value:.8f} USDT")
    print(f"Personal Money Left: {personal_money_left:.2f} USDT")
    print()
