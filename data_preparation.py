import ccxt
import pandas as pd
import pandas_ta as ta
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
        if not candles:
            break
        data.extend(candles)
        since = candles[-1][0] + 1

    print("\nDados históricos baixados.")
    return data

# Baixar os dados históricos
historical_data = fetch_historical_data(SYMBOL, TIMEFRAME, START_DATE, END_DATE)


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
df["macd"], df["macd_signal"], df["macd_histogram"] = ta.macd(
    df["close"],
    fast=MACD_FAST_PERIOD,
    slow=MACD_SLOW_PERIOD,
    signal=MACD_SIGNAL_PERIOD,
)

# Remover o primeiro dia de dados
start_timestamp = exchange.parse8601(START_DATE + "T00:00:00Z")
df = df[df.index >= pd.to_datetime(start_timestamp, unit="ms")]
df = df.apply(pd.to_numeric)

print("Salvando dados e indicadores em um arquivo CSV...")
# Salvar o DataFrame com dados e indicadores em um arquivo CSV
df.to_csv("historical_data_with_indicators.csv")
print("Arquivo CSV gerado com sucesso.")