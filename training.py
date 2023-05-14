import pandas as pd
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from config import LEARNING_RATE, DISCOUNT_FACTOR, EXPLORATION_RATE
from crypto_trading_env import CryptoTradingEnv

# Carregar os dados com indicadores técnicos
df = pd.read_csv("historical_data_with_indicators.csv", index_col=0, parse_dates=True)

# Criar o ambiente de negociação de criptomoedas
env = CryptoTradingEnv(df)
env = DummyVecEnv([lambda: env])

# Definir os hiperparâmetros do modelo
model_params = {
    "policy": "MlpPolicy",
    "env": env,
    "learning_rate": LEARNING_RATE,
    "gamma": DISCOUNT_FACTOR,
    "ent_coef": EXPLORATION_RATE,
    "verbose": 1,
}

# Criar e treinar o modelo PPO
model = PPO(**model_params)
print("Iniciando o treinamento do modelo...")
model.learn(total_timesteps=200000)
print("Treinamento concluído.")

# Salvar o modelo treinado
model.save("crypto_trading_agent")

print("Modelo salvo com sucesso.")