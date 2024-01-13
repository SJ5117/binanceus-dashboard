from flask import Flask, render_template
from binanceus.BinanceUSCostBasis import (
    trade_history, 
    average_buy_price, 
    average_sell_price, 
    total_buy_value, 
    total_sell_value, 
    buys, 
    sells, 
    personal_money_left,
    account_info,
    coins_in_wallet,
    coin_data_list)

app = Flask(__name__)

@app.route('/')
def idnex():

    data = coin_data_list

    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
