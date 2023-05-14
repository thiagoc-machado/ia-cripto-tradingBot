import ccxt
import pandas as pd
import pandas_ta as ta
from ta.trend import MACD
from config import (
    SYMBOL,
    TIMEFRAME,
    START_DATE,
    END_DATE,
    RSI_PERIOD,
    MACD_FAST_PERIOD,
    MACD_SLOW_PERIOD,
    MACD_SIGNAL_PERIOD,
    SMA_PERIODS,
)

# Inicializar o objeto ccxt para a Binance
exchange = ccxt.binance({
    "rateLimit": 1200,
    "enableRateLimit": True,
})

# Função para baixar dados históricos
def fetch_historical_data(symbol, timeframe, start_date, end_date):
    data = []
    since = exchange.parse8601(start_date + "T00:00:00Z") - 86400000  # Subtrai 1 dia em milissegundos
    end_timestamp = exchange.parse8601(end_date + "T23:59:59Z")

    print("Baixando dados históricos...")
    while since < end_timestamp:
        candles = exchange.fetch_ohlcv(symbol, timeframe, since)
        print(f"Baixados {len(candles)} dados históricos.", end="\r")
        print(f"processando {(since / end_timestamp) * 100:.2f}% - {since} até {end_timestamp}", end="\r")

        if not candles:
            break
        data.extend(candles)
        since = candles[-1][0] + 1

    print("\nDados históricos baixados.")
    return data

# Baixar os dados históricos
historical_data = fetch_historical_data(SYMBOL, TIMEFRAME, START_DATE, END_DATE)

# Verificar se há dados histéricos

if not historical_data:
    print("Nenhum dado histérico encontrado.")
    exit()

print("Preparando os dados...")
# Converter para DataFrame do Pandas
columns = ["timestamp", "open", "high", "low", "close", "volume"]
df = pd.DataFrame(historical_data, columns=columns)

# Converter timestamp para data e hora
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

# Definir timestamp como índice
df.set_index("timestamp", inplace=True)


print("Calculando indicadores técnicos...")
# Calcular os indicadores técnicos
df["rsi"] = ta.rsi(df["close"], length=RSI_PERIOD)
for period in SMA_PERIODS:
    df[f"sma_{period}"] = ta.sma(df["close"], length=period)
    
macd_indicator = MACD(df['close'], window_slow=MACD_SLOW_PERIOD, window_fast=MACD_FAST_PERIOD, window_sign=MACD_SIGNAL_PERIOD)
df['macd'] = macd_indicator.macd()
df['macd_signal'] = macd_indicator.macd_signal()
df['macd_histogram'] = macd_indicator.macd_diff()

# Remover o primeiro dia de dados
start_timestamp = exchange.parse8601(START_DATE + "T00:00:00Z")
df = df[df.index >= pd.to_datetime(start_timestamp, unit="ms")]
numeric_columns = [col for col in df.columns if col not in ['timestamp', 'date', 'time']]

print(df.head())

df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric)


print("Salvando dados e indicadores em um arquivo CSV...")
# Salvar o DataFrame com dados e indicadores em um arquivo CSV
df.to_csv("historical_data_with_indicators.csv")
print("Arquivo CSV gerado com sucesso.")