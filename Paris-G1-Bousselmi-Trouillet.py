#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 16:36:55 2023

@author: evantrouillet
"""
import tkinter as tk
import os


#Les consignes pour ce projet sont assez simples : nous avons carte blanche tant que nous travaillons sur quelque chose de "financier". Après réflexion, nous avons décidé de nous concentrer sur les données on-chain de Bitcoin. 
 # Notre projet est composé de trois parties chacune representant un investissement different. 
 # 1- Investissement sur BTC avec une simulation d'achat et de vente grace aux EMA
 # 2- Un investissement sur un protocole de finance decentralisé (Curve) qui nous permet d'avoir des rendements.Etant donné que les rendements sont distribués tous les jous, nous pouvons utiliser une méthode d'interets cumulés.
 # 3- Un investissement moins risqué de manière a securisé une partie de notre fond. Nous allons donc investir sur du PaxGold un stablecoin indexé sur le cours de l'Or. 


#Cette partie du projet permet d'avoir une interface pour faire tourner les simulations. 
# il est plus interressant de l'ouvrir et le faire tourner via Visual studio code. 

def run_btc():
    os.system('python strategy/BTC.py')

def run_defi():
    os.system('python strategy/defi.py')

def run_paxg():
    os.system('python strategy/paxg.py')

def run_recap():
    os.system('python strategy/recap.py')

root = tk.Tk()
root.title("Invest Project")
root.geometry("1200x520")
root.configure(bg='#444444')

title_label = tk.Label(root, text="Invest Project", font=("Arial Bold", 50), fg='white', bg='#444444')
title_label.place(relx=0.5, rely=0.1, anchor='center')

btc_button = tk.Button(root, text="BTC", font=("Arial", 30), bg='#666666', fg='white', command=run_btc)
btc_button.place(relx=0.3, rely=0.4, anchor='center', width=200, height=100)

defi_button = tk.Button(root, text="DEFI", font=("Arial", 30), bg='#666666', fg='white', command=run_defi)
defi_button.place(relx=0.5, rely=0.4, anchor='center', width=200, height=100)

paxg_button = tk.Button(root, text="PAXG", font=("Arial", 30), bg='#666666', fg='white', command=run_paxg)
paxg_button.place(relx=0.7, rely=0.4, anchor='center', width=200, height=100)

recap_button = tk.Button(root, text="Strategy summary", font=("Arial", 30), bg='#666666', fg='white', command=run_recap)
recap_button.place(relx=0.5, rely=0.7, anchor='center', width=600, height=100)

cash_label = tk.Label(root, text="CASH Invest = 10000 (per invest strategy)", font=("Arial", 16), fg='white', bg='#444444')
cash_label.place(relx=0.95, rely=0.95, anchor='se')

root.mainloop()



###################################

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

########################################BTC#######################################

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


