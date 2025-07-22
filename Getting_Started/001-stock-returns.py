import pandas as pd
import numpy as np
import tidyfinance as tf
from plotnine import *
from mizani.formatters import percent_format

prices = tf.download_data(
  domain="stock_prices", 
  symbols="AAPL",
  start_date="2000-01-01", 
  end_date="2025-07-21"
)

# print(prices.head().round(3))

apple_prices_figure = (
  ggplot(prices, aes(y="adjusted_close", x="date"))
  + geom_line()
  + labs(x="", y="", title="Apple stock prices from 2000 to 2025")
)
#apple_prices_figure.show()

# daly retuns: r_t = p_t / p_{t-1} - 1, where p_t: is the adjusted prices at the end of day t

returns = (prices
    .sort_values("date")
    .assign(ret=lambda x: x["adjusted_close"].pct_change())
    .sort_values("date", ascending=False)
    #.get(["symbol", "date", "ret"])
)

# print(returns)

returns = returns.dropna()

quantile_05 = returns["ret"].quantile(0.05)

apple_returns_figure = (
    ggplot(returns, aes(x="ret"))
    + geom_histogram(bins=100)
    + geom_vline(aes(xintercept=quantile_05), linetype="dashed")
    + labs(x="", y="", title="Ditribution of daily Apple stock returns")
    + scale_x_continuous(labels=percent_format())
)

# apple_returns_figure.show()

# print(pd.DataFrame(returns["ret"].describe()).round(3).T)

print(pd.DataFrame(returns["ret"]
                   .groupby(returns["date"].dt.year)
                   .describe())
                   .round(3)
                   )