import numpy as np

from qtp.tools.utils import read_upbit_1h_db
from qtp.tools.preprocessing import shift_data
from qtp.tools.indicator import bollinger_bands

class Sign03:
    '''
     - bollinger_bands
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
        df = bollinger_bands(df, 'close', ma=120, k=2)
        df = shift_data(df, ['pb', 'bbw'], 1, 'before')
        df.dropna(inplace=True)
        return df

    def buy(self, df):
        con1 = (df['pb-1'] > self.params['buy_pb_min'])
        con2 = (df['pb-1'] < self.params['buy_pb_max'])
        con3 = (df['bbw-1'] > self.params['buy_bbw_min'])
        con4 = (df['bbw-1'] < self.params['buy_bbw_max'])
        df['buy_signal'] = np.where(con1 & con2 & con3 & con4, 1, 0)
        return df

    def sell(self, df):
        con1 = (df['pb-1'] > self.params['sell_pb_min'])
        con2 = (df['pb-1'] < self.params['sell_pb_max'])
        con3 = (df['bbw-1'] > self.params['sell_bbw_min'])
        con4 = (df['bbw-1'] < self.params['sell_bbw_max'])
        df['sell_signal'] = np.where(con1 & con2 & con3 & con4, 1, 0)
        return df

    def multi_buy_values(self, df):
        count1 = self.params['buy_count1'] * 2
        count2 = self.params['buy_count2'] * 2

        pb_min = df['pb'].quantile(.05)
        pb_max = df['pb'].quantile(.95)

        bbw_min = df['bbw'].quantile(.05)
        bbw_max = df['bbw'].quantile(.95)

        pb_range = np.linspace(pb_min, pb_max, count1)
        count1_length = int(len(pb_range) / 2)

        bbw_range = np.linspace(bbw_min, bbw_max, count2)
        count2_length = int(len(bbw_range) / 2)

        values = {
            'buy_pb_min' : pb_range[:count1_length],
            'buy_pb_max' : pb_range[count1_length:],
            'buy_bbw_min' : bbw_range[:count2_length],
            'buy_bbw_max' : bbw_range[count2_length:],
        }
        return values


    def multi_sell_values(self, df):
        count1 = self.params['sell_count1'] * 2
        count2 = self.params['sell_count2'] * 2

        pb_min = df['pb'].quantile(.05)
        pb_max = df['pb'].quantile(.95)

        bbw_min = df['bbw'].quantile(.05)
        bbw_max = df['bbw'].quantile(.95)

        pb_range = np.linspace(pb_min, pb_max, count1)
        count1_length = int(len(pb_range) / 2)

        bbw_range = np.linspace(bbw_min, bbw_max, count2)
        count2_length = int(len(bbw_range) / 2)

        values = {
            'sell_pb_min' : pb_range[:count1_length],
            'sell_pb_max' : pb_range[count1_length:],
            'sell_bbw_min' : bbw_range[:count2_length],
            'sell_bbw_max' : bbw_range[count2_length:],
        }
        return values
