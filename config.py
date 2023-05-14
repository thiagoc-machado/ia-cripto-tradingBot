# Parâmetros de mercado e dados históricos
SYMBOL = "BTC/USDT"                # Símbolo da moeda (par de negociação)
TIMEFRAME = "3m"                   # Intervalo de tempo das velas (1 minuto para scalping)
START_DATE = "2023-01-01"          # Data de início para coleta de dados históricos
END_DATE = "2023-05-13"            # Data final para coleta de dados históricos

# Parâmetros dos indicadores técnicos
RSI_PERIOD = 7                     # Período do RSI (menor para reações mais rápidas)
MACD_FAST_PERIOD = 5               # Período da média móvel rápida do MACD
MACD_SLOW_PERIOD = 13              # Período da média móvel lenta do MACD
MACD_SIGNAL_PERIOD = 4             # Período da linha de sinal do MACD
SMA_PERIODS = [10, 20, 50]         # Períodos das médias móveis simples (ajustados para scalping)

# Parâmetros de aprendizado por reforço
LEARNING_RATE = 0.01               # Taxa de aprendizado do algoritmo de aprendizado por reforço
DISCOUNT_FACTOR = 0.99             # Fator de desconto para o algoritmo de aprendizado por reforço
EXPLORATION_RATE = 0.1             # Taxa de exploração para o algoritmo de aprendizado por reforço
REWARD_MULTIPLIER = 100            # Multiplicador de recompensa por trade (ajusta a escala das recompensas)
TRADE_PENALTY = 0.001              # Penalidade por manter posição aberta (incentiva trades rápidos)

# Parâmetros do backtesting
INITIAL_BALANCE = 10000            # Saldo inicial para backtesting
COMMISSION = 0.001                 # Comissão por trade (taxa da corretora)

# Configurações da Binance
BINANCE_API_KEY = "YOUR_BINANCE_API_KEY"        # Chave da API da Binance
BINANCE_SECRET_KEY = "YOUR_BINANCE_SECRET_KEY"  # Chave secreta da API da Binance
