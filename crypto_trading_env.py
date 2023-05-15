import numpy as np
import pandas as pd
import gym
from gym import spaces
from config import TRADE_PENALTY, INITIAL_BALANCE, SHORT, MARKET, MODE, TAKE_PROFIT, STOP_LOSS, TRAILING_STOP_LOSS, LEVERAGE, DCA, DCA_VALUE, ORDER_TYPE, SLIPPAGE, SCALE_FACTOR

class CryptoTradingEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, df, **kwargs):
        super(CryptoTradingEnv, self).__init__()
        assert MARKET in ['spot', 'futures'], "Invalid market option. Must be 'spot' or 'futures'."
        assert MODE in ['cross', 'isolated'], "Invalid mode option. Must be 'cross' or 'isolated'."
        assert isinstance(SHORT, bool), "Invalid short option. Must be True or False."

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
        self.buy_price = None
        self.highest_price_since_buy = None
        self.dca_active = False
        
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
        current_price = self.df.iloc[self.current_step]['close']

        # Imprimir o progresso do treinamento
        if self.current_step % 1000 == 0:  # Ajuste este número conforme necessário
            progress = self.current_step / len(self.df)
            print(f"{self.current_step} / {len(self.df)} steps - {progress * 100:.2f}%", end="\r")

        previous_balance = self.balance
        if action == 0:  # Comprar
            buy_price = current_price
            if ORDER_TYPE == 'market':
                buy_price += buy_price * SLIPPAGE
            self.held_crypto += self.balance / buy_price
            self.balance = 0
            self.buy_price = buy_price
            self.highest_price_since_buy = buy_price
            self.dca_active = False
        elif action == 1:  # Vender
            sell_price = current_price
            if ORDER_TYPE == 'market':
                sell_price -= sell_price * SLIPPAGE
            self.balance += self.held_crypto * sell_price
            self.held_crypto = 0
            self.buy_price = None
            self.highest_price_since_buy = None
            self.dca_active = False
        elif action == 2:  # Manter
            pass

        if self.buy_price is not None:
            current_profit = (current_price - self.buy_price) / self.buy_price
            if not self.dca_active and DCA and current_profit < -DCA_VALUE:
                self.dca_active = True
                self.buy_price = (self.buy_price + current_price) / 2

            if current_profit >= TAKE_PROFIT or current_profit <= -STOP_LOSS:
                self.balance += self.held_crypto * current_price
                self.held_crypto = 0
                self.buy_price = None
                self.highest_price_since_buy = None
                self.dca_active = False

            if TRAILING_STOP_LOSS is not None:
                if current_price > self.highest_price_since_buy:
                    self.highest_price_since_buy = current_price
                elif (self.highest_price_since_buy - current_price) / self.highest_price_since_buy >= TRAILING_STOP_LOSS:
                    self.balance += self.held_crypto * current_price
                    self.held_crypto = 0
                    self.buy_price = None
                    self.highest_price_since_buy = None
                    self.dca_active = False

        done = False
        if self.current_step >= len(self.df) - 1:
            done = True

        change_in_balance = self.balance - previous_balance
        # Escalar a diferença de saldo para evitar valores extremamente grandes
        scale_factor = SCALE_FACTOR  # Ajuste este valor conforme necessário
        change_in_balance /= scale_factor
        # Aplicar recompensa/punição exponencial
        if change_in_balance > 0:
            reward = np.exp(change_in_balance)
        else:
            reward = -np.exp(-change_in_balance)

        reward -= self.balance * TRADE_PENALTY

        return self._get_observation(), reward, done, {}

    def render(self, mode='human', close=False):
        pass

