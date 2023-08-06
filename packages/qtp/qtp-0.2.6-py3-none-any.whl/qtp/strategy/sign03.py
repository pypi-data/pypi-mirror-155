import numpy as np

from qtp.tools.utils import read_upbit_1h_db
from qtp.tools.preprocessing import shift_data
from qtp.tools.indicator import disparity, rsi

class Sign03:
    '''
     - disparity
     - rsi
    '''
    def __init__(self, params):
        self.params = params

    def preprocessing_df(self, days):
        if self.params['exchange'] == 'upbit':
            if days == 'all':
                df = read_upbit_1h_db(self.params['market'])
                df = df[self.params['start']:self.params['end']]
            else:
                df = read_upbit_1h_db(self.params['market'])
                df = df.iloc[-days*24 : ]
        return self.__preprocessing(df)

    def __preprocessing(self, df):
        df = disparity(df, 70)
        df = rsi(df, source='close', length=70)
        df = shift_data(df, ['ma70disparity', 'rsi'], 1, 'before')
        return df

    def buy(self, df):
        con1 = (df['ma70disparity-1'] > self.params['buy_ma70disparity_min'])
        con2 = (df['ma70disparity-1'] < self.params['buy_ma70disparity_max'])
        con3 = (df['rsi-1'] > self.params['buy_rsi_min'])
        con4 = (df['rsi-1'] < self.params['buy_rsi_max'])

        df['buy_signal'] = np.where(con1 & con2 & con3 & con4, 1, 0)
        return df

    def sell(self, df):
        con1 = (df['ma70disparity-1'] > self.params['sell_ma70disparity_min'])
        con2 = (df['ma70disparity-1'] < self.params['sell_ma70disparity_max'])
        con3 = (df['rsi-1'] > self.params['sell_rsi_min'])
        con4 = (df['rsi-1'] < self.params['sell_rsi_max'])

        df['sell_signal'] = np.where(con1 & con2 & con3 & con4, 1, 0)
        return df

    def multi_buy_values(self, df):
        count1 = self.params['buy_count1'] * 2
        count2 = self.params['buy_count2'] * 2

        ma70disparity_q05 = df['ma70disparity'].quantile(.05)
        ma70disparity_q95 = df['ma70disparity'].quantile(.80)

        rsi_q05 = df['rsi'].quantile(.01)
        rsi_q95 = df['rsi'].quantile(.60)

        ma70disparity_sum_range = np.linspace(ma70disparity_q05,
                                               ma70disparity_q95, count1)
        count1_length = int(len(ma70disparity_sum_range) / 2)

        rsi_sum_range = np.linspace(rsi_q05, rsi_q95, count2)
        count2_length = int(len(rsi_sum_range) / 2)

        values = {
            'buy_ma70disparity_min' : ma70disparity_sum_range[:count1_length],
            'buy_ma70disparity_max' : ma70disparity_sum_range[count1_length:],
            'buy_rsi_min' : rsi_sum_range[:count2_length],
            'buy_rsi_max' : rsi_sum_range[count2_length:],
        }
        return values


    def multi_sell_values(self, df):
        count1 = self.params['sell_count1'] * 2
        count2 = self.params['sell_count2'] * 2

        ma70disparity_q05 = df['ma70disparity'].quantile(.50)
        ma70disparity_q95 = df['ma70disparity'].quantile(.90)

        rsi_q05 = df['rsi'].quantile(.20)
        rsi_q95 = df['rsi'].quantile(.90)

        ma70disparity_sum_range = np.linspace(ma70disparity_q05,
                                               ma70disparity_q95, count1)
        count1_length = int(len(ma70disparity_sum_range) / 2)

        rsi_sum_range = np.linspace(rsi_q05, rsi_q95, count2)
        count2_length = int(len(rsi_sum_range) / 2)

        values = {
            'sell_ma70disparity_min' : ma70disparity_sum_range[:count1_length],
            'sell_ma70disparity_max' : ma70disparity_sum_range[count1_length:],
            'sell_rsi_min' : rsi_sum_range[:count2_length],
            'sell_rsi_max' : rsi_sum_range[count2_length:],
        }
        return values
