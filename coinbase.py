import cbpro
import pandas as pd
import matplotlib.pyplot as plt

public_client = cbpro.PublicClient()

products = public_client.get_products()
products_df = pd.DataFrame(products)

selected_products = ['BTC-USD', 'ETH-USD', 'LTC-USD']

data_frames = {}
for product in selected_products:
    data_frames[product] = {}
    for period in ['1day', '1month', '1year']:
        historical_data = public_client.get_product_historic_rates(product, granularity=3600, start=None, end=None)
        df = pd.DataFrame(historical_data, columns=['time', 'low', 'high', 'open', 'close', 'volume'])
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.set_index('time', inplace=True)
        data_frames[product][period] = df

fig, axs = plt.subplots(len(selected_products), len(data_frames[selected_products[0]]), figsize=(20, 15))
for i, product in enumerate(selected_products):
    for j, period in enumerate(data_frames[product]):
        ax = axs[i, j]
        data_frames[product][period]['close'].plot(ax=ax)
        ax.set_title(f'{product} - {period}')
plt.tight_layout()
plt.show()
    
for product in selected_products:
    for period in data_frames[product]:
        df = data_frames[product][period]
        print(f'{product} - {period}:')
        print(f'Середнє значення: {df["close"].mean()}')
        print(f'Девіація: {df["close"].std()}')
        print(f'RSA за 10 днів: {df["close"].rolling(window=10).mean()}')
        print(f'RSA за 20 днів: {df["close"].rolling(window=20).mean()}')
        print(f'RSA за 50 днів: {df["close"].rolling(window=50).mean()}')
        print('\n')
