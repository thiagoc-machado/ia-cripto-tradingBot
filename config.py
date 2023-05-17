# Parâmetros de mercado e dados históricos
SYMBOL = "ADA/USDT"                # Símbolo da moeda (par de negociação)
TIMEFRAME = "15m"                   # Intervalo de tempo das velas (1 minuto para scalping)
START_DATE = "2022-04-13"          # Data de início para coleta de dados históricos
END_DATE = "2023-05-13"            # Data final para coleta de dados históricos
SHORT = False                       # Can short
MARKET = 'spot'                    # 'spot' para mercado à vista, 'futures' para mercado de futuros
MODE = 'isolated'                  # 'cross' ou 'isolated'
ORDER_TYPE = 'market'               # Tipo de ordem (MARKET ou LIMIT)
SLIPPAGE = 0.01                    # Taxa de slippage (ajustado para scalping)
SCALE_FACTOR = 1000

# Parâmetros dos indicadores técnicos
RSI_PERIOD = 3                     # Período do RSI (menor para reações mais rápidas)
MACD_FAST_PERIOD = 5               # Período da média móvel rápida do MACD
MACD_SLOW_PERIOD = 13              # Período da média móvel lenta do MACD
MACD_SIGNAL_PERIOD = 4             # Período da linha de sinal do MACD
SMA_PERIODS = [3, 5, 7]            # Períodos das médias móveis simples (ajustados para scalping)

# Parâmetros de aprendizado por reforço
LEARNING_RATE = 0.01               # Taxa de aprendizado do algoritmo de aprendizado por reforço
DISCOUNT_FACTOR = 0.99             # Fator de desconto para o algoritmo de aprendizado por reforço
EXPLORATION_RATE = 0.3             # Taxa de exploração para o algoritmo de aprendizado por reforço (0.1)
REWARD_MULTIPLIER = 100            # Multiplicador de recompensa por trade (ajusta a escala das recompensas)
TRADE_PENALTY = 0.001              # Penalidade por manter posição aberta (incentiva trades rápidos)
TIME_STEPS = 500000                # Número de passos de tempo para o treinamento


# Parâmetros do backtesting
INITIAL_BALANCE = 1000              # Saldo inicial para backtesting
COMMISSION = 0.0017                 # Comissão por trade (taxa da corretora)


# Configurações da Binance
BINANCE_API_KEY = "YOUR_BINANCE_API_KEY"        # Chave da API da Binance
BINANCE_SECRET_KEY = "YOUR_BINANCE_SECRET_KEY"  # Chave secreta da API da Binance

#Parametros de trading
TAKE_PROFIT = 3.00                  # Take profit (ajustado para scalping)
STOP_LOSS = 3.00                    # Stop loss (ajustado para scalping)
TRAILING_STOP_LOSS = 1.00           # Stop loss de trailing (ajustado para scalping)
LEVERAGE = 3                        # Leverage (ajustado para scalping)
DCA = True                          # DCA (ajustado para scalping)
DCA_VALUE = 0.50                    # Valor da DCA (ajustado para scalping)
ORDER_TYPE = 'market'               # Tipo de ordem (MARKET ou LIMIT)
SLIPPAGE = 0.01                    # Taxa de slippage (ajustado para scalping)
 

'''
Learning Rate (taxa de aprendizado): 
O valor de 0.01 para a taxa de aprendizado é comumente utilizado. 
No entanto, em problemas de trading, pode ser benéfico experimentar diferentes valores de taxa de aprendizado para encontrar a melhor configuração. 
Taxas de aprendizado mais altas podem permitir uma adaptação mais rápida a mudanças nas condições de mercado, mas também podem levar a oscilações ou a uma instabilidade no treinamento. 
Por outro lado, taxas de aprendizado mais baixas podem levar a um treinamento mais estável, mas com um ajuste mais lento às mudanças. 
Sugiro experimentar diferentes valores de taxa de aprendizado para encontrar um equilíbrio adequado entre a velocidade de aprendizado e a estabilidade do modelo.

Discount Factor (fator de desconto): 
O valor de 0.99 para o fator de desconto indica que seu modelo está considerando recompensas futuras com um peso significativo. 
Isso pode ser apropriado para trades de curto prazo, como o scalping, onde o objetivo é maximizar os ganhos imediatos. 
No entanto, dependendo da natureza do mercado de criptomoedas e das estratégias específicas que você está implementando, pode ser útil ajustar o fator de desconto. 
Valores mais altos de desconto podem priorizar ganhos imediatos, enquanto valores mais baixos podem permitir que o modelo leve em consideração recompensas futuras mais distantes.

Exploration Rate (taxa de exploração): 
A taxa de exploração de 0.1 indica que o seu modelo está explorando 10% das ações com base em uma estratégia aleatória. 
Isso é útil para garantir uma exploração contínua do espaço de ações e evitar ficar preso em mínimos locais. 
No entanto, dependendo do estágio de treinamento em que você se encontra, pode ser interessante reduzir gradualmente a taxa de exploração à medida que o modelo progride. 
Isso permitirá que o modelo se concentre mais em ações que parecem mais promissoras com base nas experiências anteriores.

Reward Multiplier (multiplicador de recompensa): 
O multiplicador de recompensa de 100 indica que as recompensas são amplificadas em 100 vezes. 
Isso pode ser útil para dar mais importância às recompensas e incentivar o modelo a buscar ganhos maiores. 
No entanto, é importante ter cuidado ao amplificar as recompensas, pois isso pode levar a resultados instáveis ou extremos. 
Sugiro monitorar o desempenho do modelo e, se necessário, ajustar o multiplicador de recompensa para alcançar um equilíbrio entre incentivar ganhos maiores e manter a estabilidade do treinamento.

Trade Penalty (penalidade de trade): 
A penalidade de trade de 0.001 é aplicada ao modelo para desencorajar trades frequentes e excessivos. 
Isso pode ser útil para evitar uma atividade de negociação excessiva e focar em trades mais significativos


qui estão as explicações e algumas considerações sobre os valores apresentados:

rollout/ep_len_mean: Essa métrica indica o comprimento médio (em número de etapas) de um episódio durante a fase de rollout, que é uma etapa do treinamento em que o modelo é executado interagindo com o ambiente de negociação. O valor de 1.52e+04 indica que, em média, um episódio tem cerca de 15.200 etapas.

rollout/ep_rew_mean: Essa métrica representa a recompensa média obtida por episódio durante o rollout. O valor de 1.34e+08 indica que, em média, um episódio tem uma recompensa de aproximadamente 134 milhões.

time/fps: A taxa de quadros por segundo (frames per second) durante o treinamento. Indica quantas iterações são realizadas em um segundo. Um valor de 370 fps significa que estão sendo realizadas aproximadamente 370 iterações por segundo.

time/iterations: O número de iterações concluídas durante o treinamento até o momento. Cada iteração normalmente envolve a atualização dos pesos do modelo com base em uma amostra de dados.

time_elapsed: O tempo decorrido em segundos desde o início do treinamento.

total_timesteps: O número total de etapas ou passos de treinamento executados até o momento. Essas etapas podem incluir ações tomadas pelo modelo ou transições de estados em um ambiente de simulação.

train/approx_kl: A divergência aproximada de Kullback-Leibler (KL) entre a nova política e a antiga política. Esse valor é monitorado para verificar se as atualizações estão ocorrendo de forma estável.

train/clip_fraction: A proporção de amostras de treinamento que foram limitadas pelo recorte (clipping) durante o treinamento do PPO. O recorte é uma técnica para evitar grandes atualizações de políticas que podem levar a um treinamento instável.

train/clip_range: O limite para o recorte (clipping) das atualizações de políticas. Valores fora desse intervalo são limitados para mantê-los dentro do intervalo especificado.

train/entropy_loss: A perda de entropia da política. A entropia é uma medida da incerteza na distribuição de probabilidade da política atual. Maximizar a entropia pode incentivar exploração em vez de exploração excessiva.

train/explained_variance: A variância explicada pelos retornos preditos em relação aos retornos reais. Um valor próximo de zero indica que o modelo está tendo dificuldades em ajustar os retornos esperados.

train/learning_rate: A taxa de aprendizado usada no treinamento. Ela controla a magnitude das atualizações dos pesos do modelo a cada iteração.

train/loss: O valor da função de perda total do treinamento. É uma medida da discrepância entre as previsões do modelo e os valores reais durante o treinamento.

train/n_updates: O número total de atualizações realizadas no treinamento. Cada atualização normalmente envolve um cálculo do gradiente e uma atualização dos pesos do modelo.

train/policy_gradient_loss: A perda do gradiente da política. Indica a diferença entre a política atual e a nova política estimada durante o treinamento.

train/value_loss: A perda da função de valor. Ela representa a discrepância entre os valores preditos pelo modelo e os valores reais durante o treinamento.

Avaliar se esses valores são bons ou ruins depende do contexto do seu problema e das metas específicas do seu modelo de trading de criptomoedas. Aqui estão algumas considerações gerais:

Rollout Metrics: O comprimento médio do episódio (ep_len_mean) e a recompensa média por episódio (ep_rew_mean) são medidas que podem fornecer uma ideia do desempenho do seu modelo durante a fase de rollout. Valores mais altos para essas métricas indicam uma duração de episódio maior e/ou recompensas mais altas, o que geralmente é desejável para um modelo de trading. No entanto, a avaliação adequada do desempenho depende do contexto do problema e dos objetivos específicos.

Loss e Variância: Uma perda (loss) alta e uma variância explicada (explained_variance) próxima a zero podem indicar que o modelo está tendo dificuldades em ajustar os retornos esperados e em fazer previsões precisas. Idealmente, você deseja uma perda baixa e uma variância explicada mais próxima de 1. No entanto, essas métricas devem ser interpretadas com base nas características do seu problema e nas métricas de desempenho que você está buscando.

Taxa de Aprendizado: A taxa de aprendizado (learning_rate) de 0.01 é comumente usada, mas é importante ajustar a taxa de aprendizado para encontrar um equilíbrio entre velocidade de aprendizado e estabilidade do treinamento. Valores muito altos podem levar a oscilações ou instabilidade, enquanto valores muito baixos podem retardar o aprendizado.
'''