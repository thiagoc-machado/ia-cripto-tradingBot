import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from stable_baselines3 import PPO
from config import *
from crypto_trading_env import CryptoTradingEnv
from stable_baselines3.common.save_util import load_from_zip_file


def backtest(model, env):
    trades = []
    obs = env.reset()
    done = False

    while not done:
        action, _ = model.predict(obs)
        obs, reward, done, info = env.step(action)

        if "trade" in info:
            trades.append(info["trade"])

    return trades

df = CryptoTradingEnv.load_data()
print("Dados históricos carregados")

# Define the model file
model_file = "crypto_trading_agent"

# Check if the model file exists
if not os.path.isfile(model_file + ".zip"):
    raise Exception(f"Arquivo do modelo {model_file}.zip não encontrado.")

# Load the trained model
model = PPO.load(model_file)
print("Modelo carregado")

# Create the trading environment
env = CryptoTradingEnv(df, mode=MODE, short=SHORT, market=MARKET)
print("Ambiente criado")

# Implementar a análise de trades e exibir os resultados
def analyze_trades(trades):
    gains = []
    losses = []
    trade_durations = []

    for trade in trades:
        pnl = trade['pnl']
        duration = trade['duration']
        trade_durations.append(duration)

        if pnl > 0:
            gains.append(pnl)
        else:
            losses.append(pnl)

    num_trades = len(trades)
    num_gainers = len(gains)
    num_losers = len(losses)
    avg_gain = np.mean(gains) if gains else 0
    avg_loss = np.mean(losses) if losses else 0
    avg_duration = np.mean(trade_durations)

    print(f"Total de trades: {num_trades}")
    print(f"Trades ganhadores: {num_gainers}")
    print(f"Trades perdedores: {num_losers}")
    print(f"Ganho médio: {avg_gain}")
    print(f"Perda média: {avg_loss}")
    print(f"Duração média dos trades: {avg_duration}")


def plot_trades(trades, df):
    # Aqui você pode criar gráficos para visualizar os resultados dos trades,
    # como gráficos de velas e indicadores técnicos usando bibliotecas como
    # matplotlib, plotly, etc.
    pass


if __name__ == "__main__":
    # Carregar o modelo treinado e fazer backtesting
    model_path = "crypto_trading_agent/data"
    model = PPO.load(model_path)

    # Realizar backtesting
    trades = backtest(model, env)

    # Analisar os trades
    analyze_trades(trades)

    # Plotar os trades e resultados
    plot_trades(trades, env.data.df)
