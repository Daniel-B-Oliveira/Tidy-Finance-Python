import pandas as pd
import tidyfinance as tf
from plotnine import *

'''
Are days with high aggregate trading volume often
also days with large absolute returns? Find an
appropriate visualization to analyze the question
using the symbol AAPL.
'''

prices = tf.download_data_stock_prices(
    symbols="AAPL",
    start_date="2000-01-01",
    end_date="2025-07-25"
)

print(prices.head(5))

ret_and_trad_vol = (prices
    .sort_values("date")          
    .assign(ret=lambda x: x["adjusted_close"].pct_change())
    .dropna()
    .assign(trading_volume=lambda x: (x["volume"]*x["adjusted_close"])/1e9)
    .get(["date","symbol","ret","trading_volume"])
)

print(ret_and_trad_vol.head(7))

ret_and_vol_figure = (
    ggplot(ret_and_trad_vol, aes(x="ret", y="trading_volume"))
    + geom_point()
    + geom_vline(xintercept=0, linetype="dashed")
)

ret_and_vol_figure.show()