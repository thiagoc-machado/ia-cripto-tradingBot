import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from stable_baselines3 import PPO
from config import CryptoTradingEnvConfig
from crypto_trading_env import CryptoTradingEnv
from config import SHORT, MARKET, MODE, START_DATE, END_DATE, TIMEFRAME, SYMBOL

def load_test_data(csv_file):
    df = pd.read_csv(csv_file)
    # Certifique-se de que as colunas sejam as mesmas que você usou durante o treinamento
    return df

def plot_trades(df, trades, title):
    fig, ax = plt.subplots()

    # Plote o gráfico de velas
    df['date'] = pd.to_datetime(df.index, unit='s')
    df.set_index('date', inplace=True)
    df[['open', 'high', 'low', 'close']].plot(ax=ax, lw=1, figsize=(14, 7))

    # Plote os pontos de entrada e saída
    for trade in trades:
        entry_date, entry_price, exit_date, exit_price, profit = trade
        color = 'g' if profit > 0 else 'r'
        ax.scatter(entry_date, entry_price, marker='^', c=color, s=100)
        ax.scatter(exit_date, exit_price, marker='v', c=color, s=100)
        ax.text(exit_date, exit_price, f'{profit * 100:.2f}%', fontsize=12)

    ax.set_title(title)
    ax.set_ylabel('Price')
    fig.tight_layout()
    plt.show()
    fig.savefig('trades.png')

model = PPO.load("trained_model.zip")
test_data = load_test_data("test_data.csv")

env_config = CryptoTradingEnvConfig(
    df=test_data,
    short=SHORT,
    market=MARKET,
    mode=MODE,
    start_date = START_DATE,
    end_date = END_DATE,
    timeframe = TIMEFRAME,
    symbol = SYMBOL
    # Defina outros parâmetros de configuração, se necessário
)

test_env = CryptoTradingEnv(config=env_config)

obs = test_env.reset()
done = False
trades = []

while not done:
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, info = test_env.step(action)

    if 'trade' in info:
        trades.append(info['trade'])

print("Total profit:", test_env.total_profit)
print("Total trades:", test_env.total_trades)

# Cálculo da duração média dos trades
trade_durations = [(trade[2] - trade[0]).total_seconds() for trade in trades]
average_trade_duration = np.mean(trade_durations)
print("Average trade duration (seconds):", average_trade_duration)

# Valorização da moeda no período
initial_value = test_data.iloc[0]['close']
final_value = test_data.iloc[-1]['close']
currency_valuation = (final_value - initial_value) / initial_value
print("Currency valuation:", currency_valuation)

# Plote o gráfico de trades
plot_trades(test_data, trades, "Trades Visualization")
