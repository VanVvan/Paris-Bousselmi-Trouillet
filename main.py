import tkinter as tk
import os

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