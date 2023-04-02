import pandas as pd
import requests
import numpy as np
import pandas_datareader.data as pdr
import yfinance as yf

import tkinter as tk
from tkinter import ttk

from datetime import datetime, timedelta
import time 

yf.pdr_override()

end_date = datetime.now().strftime('%Y-%m-%d')
start_date = (datetime.now() - timedelta(days=5*365)).strftime('%Y-%m-%d')

# btc = yf.Ticker("BTC-USD")
# hist = btc.history(period="10d")
# print(hist.head())

########################################DEFI#######################################

print("=====BTC=====")

hist = yf.download("BTC-USD", start=start_date, end=end_date)

SYMBOL = 'BTC-USD'
BUY_THRESHOLD = 0.05
SELL_THRESHOLD = 0.05
EMA_SHORT = 50
EMA_LONG = 100


hist['EMA_SHORT'] = hist['Close'].ewm(span=EMA_SHORT).mean()
hist['EMA_LONG'] = hist['Close'].ewm(span=EMA_LONG).mean()

buy_price = None
cash_ini = 15000
cash = 15000
coins = 0

def trade(price):
    global buy_price, cash, coins

    if price > hist['EMA_LONG'].iloc[-1] * (1 + BUY_THRESHOLD) and buy_price is None:
        coins = cash / price
        cash = 0
        buy_price = price

    elif buy_price is not None and price < buy_price * (1 - SELL_THRESHOLD):
        cash = coins * price
        coins = 0
        buy_price = None

    else:
        pass

for i in range(len(hist)):
    price = hist['Close'][i]
    trade(price)
    time.sleep(1)
    print('Loading : ' + str(i) + ' on ' + str(len(hist)))

if coins > 0:

    btc_cash = coins * hist["Close"].iloc[-1]

else:

    btc_cash = cash


portfolio_series = pd.Series(np.zeros(len(hist)))
for i in range(len(hist)):
    if coins > 0:
        portfolio_series[i] = cash + coins * hist['Close'][i]
    else:
        portfolio_series[i] = cash


date_column = pd.DataFrame({'Date': hist.index})
date_column = date_column.reset_index(drop=True)
portfolio_df = pd.concat([date_column, portfolio_series], axis=1)
portfolio_df.columns = ['Date', 'Portfolio']

pct_gain = (portfolio_df['Portfolio'].iloc[-1] - cash_ini) / cash_ini * 100

gain_btc = btc_cash - cash_ini

print('Total investissement : ' + str(btc_cash) + ' $')
print('Evolution de l\'investissement : ' + str(pct_gain) + '%')
print('Gain total : ' + str(gain_btc) + ' $')


########################################DEFI#######################################

print("=====DEFI=====")

api_url = "https://yields.llama.fi/chart/57d30b9c-fc66-4ac2-b666-69ad5f410cce"

# investissement initial
initial_investment = 15000

response = requests.get(api_url)

response_json = response.json()

data_json = response_json['data']

timestamps = [datetime.strptime(data['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ") for data in data_json]
apy_values = [float(data['apy']) for data in data_json]

daily_growth = [(1 + apy/36500) for apy in apy_values]

daily_gains = [initial_investment * (growth_factor - 1) for growth_factor in daily_growth]

gain_defi = sum(daily_gains)


print(f"Gain total : {gain_defi:.2f}$")


########################################PAXG#######################################

print("=====PAXG=====")

symbol = "PAXG-USD"

paxg_data = yf.download(symbol, start=start_date, end=end_date)
paxg_data['MA50'] = paxg_data['Close'].rolling(window=50).mean()

cash_ini = 15000.0
cash = 15000.0
shares = 0
buy_price = 0.0
sell_price = 0.0
buy_threshold = 0.03
sell_threshold = 0.03

for i in range(len(paxg_data)):
    price = paxg_data['Close'][i]

    if buy_price == 0.0 and price < paxg_data['MA50'][i] * (1 + buy_threshold):
        shares = cash / price
        cash = 0.0
        buy_price = price

    elif sell_price == 0.0 and price > paxg_data['MA50'][i] * (1 - sell_threshold):
        cash = shares * price
        shares = 0
        sell_price = price

    if shares == 0:
        buy_price = 0.0
    if cash == 0.0:
        sell_price = 0.0

if shares == 0:
    gain_paxg = (cash - cash_ini) / cash_ini
    pct_gain =  gain_paxg * 100
    print("Cash : " + str(cash))
    print("Gain :", pct_gain, "%")
else:
    gain_paxg = (cash - cash_ini) / cash_ini
    pct_gain =  gain_paxg * 100
    print("Cash : " + str(cash))
    print("Loss :" + str(pct_gain) + "%")

########################################Summary#######################################

data = [
    ["BTC", cash_ini, gain_btc],
    ["DEFI", cash_ini, gain_defi],
    ["PAXGOLD", cash_ini, gain_paxg]
]

root = tk.Tk()

table = ttk.Treeview(root, columns=("invest", "gain"))

table.heading("#0", text="Strategy")
table.heading("invest", text="Invest Cash")
table.heading("gain", text="Gain")

for i, row in enumerate(data):
    
    table.insert("", "end", text=row[0], values=(row[1], row[2]))
    
    if row[2] >= 0:
        table.tag_configure(str(i), background="#4fe086")
    else:
        table.tag_configure(str(i), background="#b32424")

    table.item(table.get_children()[i], tags=(str(i),))

table.pack()
root.mainloop()