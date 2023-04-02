import requests
import matplotlib.pyplot as plt
from datetime import datetime

# URL de l'API DefiLlama pour les pools Ethereum
api_url = "https://yields.llama.fi/chart/57d30b9c-fc66-4ac2-b666-69ad5f410cce"

# investissement initial
initial_investment = 10000

response = requests.get(api_url)

response_json = response.json()

data_json = response_json['data']

timestamps = [datetime.strptime(data['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ") for data in data_json]
apy_values = [float(data['apy']) for data in data_json]

daily_growth = [(1 + apy/36500) for apy in apy_values]

daily_gains = [initial_investment * (growth_factor - 1) for growth_factor in daily_growth]

total_gain = sum(daily_gains)

dates = [date.date() for date in timestamps]

plt.plot(dates, daily_gains)

plt.xlabel("Date")
plt.ylabel("Gain quotidien ($)")
plt.title("Gains quotidiens")
plt.xticks(rotation=90)
plt.show()

print(f"Gain total : {total_gain:.2f}$")