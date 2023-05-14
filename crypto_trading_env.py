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

        self.df = CryptoTradingEnv.load_data()
        self.df = df
        self.action_space = spaces.Discrete(3)  # Comprar, vender ou manter
        self.observation_space = spaces.Box(low=0, high=np.finfo(np.float32).max, shape=(len(df.columns) - 1,), dtype=np.float32)

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
        df = pd.read_csv('historical_data_with_indicators.csv', index_col=0, parse_dates=True)
        df = df.dropna()
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
