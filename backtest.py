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
    fig, ax = plt.subplots()
    trade_data = pd.DataFrame(trades)

    ax.plot(df.index, df['close'], label='Preço de fechamento')

    for _, trade in trade_data.iterrows():
        color = 'g' if trade['profit'] > 0 else 'r'
        ax.plot([trade['open_time'], trade['close_time']], [trade['entry_price'], trade['exit_price']], color=color, linestyle='-', marker='o')
        ax.annotate(f"{trade['profit']:.2f}", (trade['close_time'], trade['exit_price']), textcoords="offset points", xytext=(-15,7), fontsize=8, color=color, ha='center')

    ax.set_title(f'{SYMBOL} - Trades de backtesting')
    ax.set_xlabel('Data e Hora')
    ax.set_ylabel('Preço')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    # Carregar o modelo treinado e fazer backtesting
    # Carregar os dados históricos
    df = CryptoTradingEnv.load_data()
    print("Dados históricos carregados")
    # Define the model file
    model_dir = 'crypto_trading_agent'
    model_file = "crypto_trading_agent.zip"

    # Carrega o modelo
    model = PPO.load(model_file)
    print("Modelo carregado")

    # Create the trading environment
    env = CryptoTradingEnv(df, mode=MODE, short=SHORT, market=MARKET)
    print("Ambiente criado")

    # Realizar backtesting
    trades = backtest(model, env)

    # Analisar os trades
    analyze_trades(trades)

    # Plotar os trades e resultados
    plot_trades(trades, df)
