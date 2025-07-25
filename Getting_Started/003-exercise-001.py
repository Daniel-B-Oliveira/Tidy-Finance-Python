import tidyfinance as tf
import pandas as pd
from plotnine import *

'''
Download daily prices for another stock market symbol of your
choice from Yahoo Finance using tf.download_data().
Plot two time series of the symbol’s un-adjusted and adjusted
closing prices. Explain any visible differences.
'''

prices_daily = tf.download_data(
    domain="stock_prices",
    symbols="AMZN",
    start_date="2000-01-01",
    end_date="2025-07-24"
)

# print(prices_daily.head(5))

amzn_close_figure = (
    ggplot(prices_daily, aes(y="close", x="date"))
    + geom_line()
    + labs(x="", y="", title="Amazon stock prices from 2000 to 2025")
)

amzn_adjusted_close_figure = (
    ggplot(prices_daily, aes(y="adjusted_close", x="date"))
    + geom_line()
    + labs(x="", y="", title="Amazon adjusted stock prices from 2000 to 2025")
)

# amzn_close_figure.show()
# amzn_adjusted_close_figure.show()

teste = (prices_daily
    .sort_values("date")
    .assign(diference=lambda x: x["close"]-x["adjusted_close"])
)

amazn_diference_figure = (
    ggplot(teste, aes(y="diference", x="date"))
    + geom_line()
    + labs(x="", y="", title="Diference between close and adjusted_close")
)

amazn_diference_figure.show()