import tidyfinance as tf
import pandas as pd
from plotnine import *
from mizani.formatters import date_format
from mizani.breaks import date_breaks

'''
Take your code from the previous exercises and generalize
it such that you can perform all the computations for an
arbitrary number of symbols (e.g., symbol = ["AAPL", "MMM", "BA"]).
Automate the download, the plot of the price time series, and
create a table of return summary statistics for this arbitrary
number of assets.
'''

symbols = tf.download_data(
    domain="constituents",
    index="Dow Jones Industrial Average"
)

selectd_symbols = ["AAPL", "MMM", "BA"]

# print(symbols)

prices_daily = tf.download_data(
    domain="stock_prices",
    symbols=symbols[symbols["symbol"].isin(selectd_symbols)]["symbol"].tolist(),
    start_date="2000-01-01",
    end_date="2005-07-24"
)

# print(prices_daily.head(5))

prices_daily_figure = (
    ggplot(prices_daily, aes(y="adjusted_close", x="date", color="symbol"))
    + geom_line()
    + scale_x_datetime(date_breaks="5 years", date_labels="%Y")
    + theme(legend_position="none")
)

# prices_daily_figure.show()

returns_daily = (prices_daily
    .assign(ret=lambda x: x.groupby("symbol")["adjusted_close"].pct_change())
    .get(["symbol","date", "ret"])
    .dropna()              
)

print(
    (returns_daily
      .groupby("symbol")["ret"]
      .describe()
      .round(3)
    )
)