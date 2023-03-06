import numpy as np
import pandas as pd
import yfinance as yf
from keras.layers import Bidirectional
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM, Lambda, Reshape
from keras.callbacks import EarlyStopping
from sklearn.metrics import confusion_matrix, accuracy_score
# Obtém dados históricos do preço do Bitcoin com as colunas Open, High, Low, Close e Volume
df_price = yf.download('BTC-USD', start='2023-01-01', end='2023-03-05'
                                                          '', interval='1h', group_by='ticker')

# Calcula a variação percentual do preço do Bitcoin
df_price['Variation'] = df_price['Close'].pct_change() * 100

date = pd.to_datetime(df_price.index)

df_price['Hour'] = df_price.index.hour
df_price['Day'] = df_price.index.day
df_price['Month'] = df_price.index.month
df_price['Year'] = df_price.index.year
# Remove a primeira linha que contém valores NaN
df_price = df_price.iloc[1:]

# Define a nova data de início para o conjunto de dados de teste
test_start_date = '2023-02-05'

# Cria um conjunto de dados de treinamento e teste
train_data = df_price.loc[df_price.index < test_start_date][['Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close', 'Variation', 'Hour', 'Day','Month', 'Year']].values
test_data = df_price.loc[df_price.index >= test_start_date][['Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close', 'Variation', 'Hour', 'Day','Month', 'Year']].values
# Normaliza os dados de treinamento e teste
scaler = MinMaxScaler(feature_range=(0, 1))
train_data_normalized = scaler.fit_transform(train_data)
test_data_normalized = scaler.transform(test_data)

# Define o número de amostras a serem utilizadas para a predição. 70 é muito bom loss: 0.0019 - val_loss: 0.0012. Testar com 68.
timesteps = 70

# Cria os dados de treinamento com a janela deslizante
X_train = []
y_train = []
for i in range(timesteps, len(train_data_normalized)):
    X_train.append(train_data_normalized[i-timesteps:i, :])
    y_train.append(train_data_normalized[i, :])
X_train, y_train = np.array(X_train), np.array(y_train)

# Cria os dados de teste com a janela deslizante
X_test = []
y_test = []
for i in range(timesteps, len(test_data_normalized)):
    X_test.append(test_data_normalized[i-timesteps:i, :])
    y_test.append(test_data_normalized[i, :])
X_test, y_test = np.array(X_test), np.array(y_test)

# Reshape dos dados de treinamento e teste
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], X_train.shape[2])
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], X_test.shape[2])

model = Sequential()
model.add(Bidirectional(LSTM(units=50, activation='tanh', return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2]))))
model.add(Bidirectional(LSTM(units=50, activation='tanh')))
model.add(Dense(units=11, activation='tanh'))
model.compile(optimizer='nadam', loss='mse')
early_stop = EarlyStopping(monitor='val_loss', patience=3, verbose=1, restore_best_weights=True)
history = model.fit(X_train, y_train, epochs=100, batch_size=32, validation_split=0.2, callbacks=[early_stop], verbose=1)

last_data = test_data_normalized[-1:]

last_data = np.expand_dims(last_data, axis=0)
prediction = model.predict(last_data)
prediction = scaler.inverse_transform(prediction)

y_test = scaler.inverse_transform(y_test)

print("Previsão das seis próximas observações:")
print(prediction[0])
