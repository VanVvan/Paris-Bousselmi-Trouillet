import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

symbol = "PAXG-USD"
start_date = "2020-01-01"
end_date = "2023-03-27"

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
        print("Acheter PAXG à", price)

    elif sell_price == 0.0 and price > paxg_data['MA50'][i] * (1 - sell_threshold):
        cash = shares * price
        shares = 0
        sell_price = price
        print("Vendre PAXG à", price)

    if shares == 0:
        buy_price = 0.0
    if cash == 0.0:
        sell_price = 0.0

if shares == 0:
    pct_gain = (cash - cash_ini) / cash_ini * 100
    print("Cash : " + str(cash))
    print("Gain :", pct_gain, "%")
else:
    pct_gain = (cash - cash_ini) / cash_ini * 100
    print("Cash : " + str(cash))
    print("Loss :" + str(pct_gain) + "%")

plt.plot(paxg_data['Close'])
plt.plot(paxg_data['MA50'])
plt.show()