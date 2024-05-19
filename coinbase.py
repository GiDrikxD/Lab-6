import cbpro
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

public_client = cbpro.PublicClient()

products = public_client.get_products()
products_df = pd.DataFrame(products)

selected_products = ['BTC-USD', 'ETH-USD', 'LTC-USD']

periods = {
    '1день': {'granularity': 3600, 'start': datetime.now() - timedelta(days=1)},  
    '1місяць': {'granularity': 21600, 'start': datetime.now() - timedelta(days=30)},  
    '1рік': {'granularity': 86400, 'start': datetime.now() - timedelta(days=365)},  
}

data_frames = {}

for product in selected_products:
    data_frames[product] = {}
    for period, params in periods.items():
        historical_data = []
        start_time = params['start']
        end_time = datetime.now()
        granularity = params['granularity']
        
        while start_time < end_time:
            batch_end_time = start_time + timedelta(seconds=granularity*300)
            if batch_end_time > end_time:
                batch_end_time = end_time
            data = public_client.get_product_historic_rates(product, 
                                                            granularity=granularity, 
                                                            start=start_time.isoformat(), 
                                                            end=batch_end_time.isoformat())
            historical_data.extend(data)
            start_time = batch_end_time
        
        historical_data.sort(key=lambda x: x[0])
        
        df = pd.DataFrame(historical_data, columns=['time', 'low', 'high', 'open', 'close', 'volume'])
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.set_index('time', inplace=True)
        data_frames[product][period] = df

fig, axs = plt.subplots(len(selected_products), len(periods), figsize=(20, 15))
for i, product in enumerate(selected_products):
    for j, period in enumerate(periods):
        ax = axs[i, j]
        data_frames[product][period]['close'].plot(ax=ax)
        ax.set_title(f'{product} - {period}')
plt.tight_layout()
plt.show()

for product in selected_products:
    for period in periods:
        df = data_frames[product][period]
        print(f'{product} - {period}:')
        print(f'Середнє значення: {df["close"].mean()}')
        print(f'Девіація: {df["close"].std()}')
        print(f'RSA за 10 днів: {df["close"].rolling(window=10).mean()}')
        print(f'RSA за 20 днів: {df["close"].rolling(window=20).mean()}')
        print(f'RSA за 50 днів: {df["close"].rolling(window=50).mean()}')
        print('\n')
