#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


Created on Sun Mar  5 19:31:18 2023

@author: evantrouillet
"""

#Les consignes pour ce projet sont assez simples : nous avons carte blanche tant que nous travaillons sur quelque chose de "financier". Après réflexion, nous avons décidé de nous concentrer sur les données on-chain de Bitcoin. 
 # Notre projet est composé de trois parties chacune representant un investissement different. 
 # 1- Investissement sur BTC avec une simulation d'achat et de vente grace aux EMA
 # 2- Un investissement sur un protocole de finance decentralisé (Curve) qui nous permet d'avoir des rendements.Etant donné que les rendements sont distribués tous les jous, nous pouvons utiliser une méthode d'interets cumulés.
 # 3- Un investissement moins risqué de manière a securisé une partie de notre fond. Nous allons donc investir sur du PaxGold un stablecoin indexé sur le cours de l'Or. 
 


import pandas as pd
import numpy as np
import pandas_datareader.data as pdr
import yfinance as yf
import matplotlib.pyplot as plt

from datetime import datetime, timedelta
import time 

yf.pdr_override()

end_date = datetime.now().strftime('%Y-%m-%d')
start_date = (datetime.now() - timedelta(days=5*365)).strftime('%Y-%m-%d')

# btc = yf.Ticker("BTC-USD")
# hist = btc.history(period="10d")
# print(hist.head())

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
        print(f' ---- Achat à {price} ---- ')

    elif buy_price is not None and price < buy_price * (1 - SELL_THRESHOLD):
        cash = coins * price
        coins = 0
        buy_price = None
        print(f' ---- Vente à {price} ---- ')

    else:
        pass

for i in range(len(hist)):
    price = hist['Close'][i]
    trade(price)
    time.sleep(1)
    print('Loading : ' + str(i) + ' on ' + str(len(hist)))

if coins > 0:
    message = ('\U0001F525 \U0001F525 ==== Solde final : {coins * hist["Close"].iloc[-1]:.2f} BTC ==== \U0001F525 \U0001F525')
    frame = len(message) + 15
    print("╒" + "═" * frame + "╕")
    for i in range(3):
        print("│" + " " * frame + "│")
    print(f'\U0001F525 \U0001F525 ==== Solde final : {coins * hist["Close"].iloc[-1]:.2f} BTC ==== \U0001F525 \U0001F525'.center(frame))

    for i in range(3):
        print("│" + " " * frame + "│")
    print("╘" + "═" * frame + "╛")


else:
    print(f' ==== Solde final : ${cash:.2f} ====')


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

print('Evolution de l\'investissement : ' + str(pct_gain) + '%')

plt.plot(date_column['Date'], portfolio_series, label='Portfolio Value')

plt.plot(hist['Close'], label='BTC Price')
plt.plot(hist['EMA_SHORT'], label='EMA_SHORT')
plt.plot(hist['EMA_LONG'], label='EMA_LONG')

plt.legend()
plt.xlabel('Date')
plt.ylabel('Price')
plt.xticks(rotation=90)
plt.show()