import pandas as pd
import influxdb
from influxdb import DataFrameClient
import datetime as dt


# Read the csv into a dataframe
df = pd.read_json("../resources/jsons/PayPal.json")


# create a timestamp out of the four columns
# print(dt.date(1900,1,1))
df['TimeStamp'] = df[['Date']].apply(lambda s: (s - 25569) * 86400)

print(df)

new_df = df.drop(['Date'],axis=1)
new_df = new_df.dropna()
new_df.set_index(pd.DatetimeIndex(df['TimeStamp']*10**9), inplace = True)
# new_df.set_index(pd.DatetimeIndex(new_df['TimeStamp']))

print(new_df)

Fields = ['Open','High','Low','Close','Adj_Close','Volume']
client = DataFrameClient('localhost', 8086, 'admin', 'admin', 'fintech_stocks')
client.write_points(new_df,'PayPal',database='fintech_stocks',protocol='line')


# # print(df['TimeStamp'])