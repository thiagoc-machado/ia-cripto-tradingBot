from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from config import LEARNING_RATE, DISCOUNT_FACTOR, EXPLORATION_RATE, SHORT, MARKET, MODE
from crypto_trading_env import CryptoTradingEnv

# Carregar os dados com indicadores técnicos
df = CryptoTradingEnv.load_data()

# Criar o ambiente de negociação de criptomoedas
#env = CryptoTradingEnv(df)
env = CryptoTradingEnv(df)


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