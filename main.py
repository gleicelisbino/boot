from neuralprophet import NeuralProphet
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Obtendo os dados históricos do Bitcoin
symbol = "BTC-USD"
start_date = "2022-01-01"
end_date = "2023-03-05"
df = yf.download('BTC-USD', start='2021-04-01', end='2023-03-05', interval='1h', group_by='ticker')
df["Date"] = df.index.astype('datetime64[ns]')
df['Variation'] = df['Close'].pct_change() * 100
df = df.iloc[1:]


data = df.reset_index()[["Date","Variation"]].rename({"Date": "ds", "Variation": "y"}, axis=1)
data = data.dropna()
# Instanciando e treinando o modelo
# Criar um objeto MinMaxScaler
scaler = MinMaxScaler(feature_range=(-1, 1))

# Normalizar os dados
data_norm = scaler.fit_transform(data[['y']])
model = NeuralProphet(batch_size=128)
df_train, df_test = model.split_df(data, freq="H")

metrics = model.fit(df_train, freq="H", validation_df=df_test, progress="plot")

# model = NeuralProphet(batch_size=64)
# model.fit(data, freq="H")

# Fazendo previsões
future = model.make_future_dataframe(data, periods=365*24, n_historic_predictions=len(data))
forecast = model.predict(future)
data_denorm = scaler.inverse_transform(data_norm)
df.to_csv('xxxxadasdasdasd.csv', index=False)

