# crypto_trading_env.py

import numpy as np
import pandas as pd
import gym
from gym import spaces
from config import TRADE_PENALTY, INITIAL_BALANCE

class CryptoTradingEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, df):
        super(CryptoTradingEnv, self).__init__()
        self.df = df
        self.action_space = spaces.Discrete(3)  # Comprar, vender ou manter
        self.observation_space = spaces.Box(low=0, high=np.finfo(np.float32).max, shape=(len(self.df.columns) - 1,), dtype=np.float32)
        self.reset()
        if 'MACD_5_13_4' in df.columns:
            df = df.drop('MACD_5_13_4', axis=1)

    def reset(self):
        self.current_step = 0
        self.balance = INITIAL_BALANCE
        self.held_crypto = 0
        
        return self._get_observation()
    
    @staticmethod
    def load_data():
        file_path = 'historical_data_with_indicators.csv'
        column_names = ['open', 'high', 'low', 'close', 'volume', 'rsi', 'sma_10', 'sma_20', 'sma_50', 'macd', 'macd_signal', 'macd_histogram']  # Substitua isso pelos nomes de coluna corretos
        df = pd.read_csv(file_path, header=None, names=column_names, skiprows=1)
        df.reset_index(drop=True, inplace=True)
        return df


    def _get_observation(self):
        return self.df.iloc[self.current_step].values[1:].astype('float64')


    def step(self, action):
        self.current_step += 1
        current_price = self.df.loc[self.current_step, 'close']
        reward = 0
        done = False

        if action == 0:  # Comprar
            self.held_crypto += self.balance / current_price
            self.balance = 0
        elif action == 1:  # Vender
            self.balance += self.held_crypto * current_price
            self.held_crypto = 0
        elif action == 2:  # Manter
            pass

        if self.current_step >= len(self.df) - 1:
            done = True

        reward += self.held_crypto * current_price - self.balance * TRADE_PENALTY

        return self._get_observation(), reward, done, {}

    def render(self, mode='human', close=False):
        pass
