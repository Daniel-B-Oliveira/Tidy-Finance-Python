import pandas as pd
import numpy as np
import tidyfinance as tf
from plotnine import *
from mizani.formatters import percent_format
from mizani.breaks import date_breaks
from mizani.formatters import date_format

symbols = tf.download_data(
    domain="constituents",
    index="Dow Jones Industrial Average"
)

selected_symbols = ["AAPL", "MSFT", "AMZN", "JPM", "PG"]

prices_daily = tf.download_data(
    domain="stock_prices",
    symbols=symbols[symbols["symbol"].isin(selected_symbols)]["symbol"].tolist(),
    start_date="2001-01-01",
    end_date="2025-07-21"
)

# print(prices_daily.head(15))

prices_figure = (
    ggplot (prices_daily, aes(y="adjusted_close", x="date", color="symbol"))
    + geom_line()
    + scale_x_datetime(date_breaks="5 years", date_labels="%Y")
    + labs(x="", y="", color="", title="Stocks prices of DOW index constituents")
    + theme(legend_position="none")
)

# prices_figure.show()

returns_daily = (prices_daily
    .assign(ret=lambda x: x.groupby("symbol")["adjusted_close"].pct_change())
    .get(["symbol", "date", "ret"])
    .dropna(subset="ret")                 
)

# print(
#     (returns_daily
#     .groupby("symbol")["ret"]
#     .describe()
#     .round(3)
#     )
# )

# Different Frequencies

returns_monthly = (returns_daily
    .assign(date=returns_daily["date"].dt.to_period("M").dt.to_timestamp())
    .groupby(["symbol", "date"], as_index=False)
    .agg(ret=("ret", lambda x: np.prod(1+x)-1))
)

# print(returns_monthly)

apple_daily = (returns_daily
    .query("symbol == 'AAPL'")
    .assign(frequency="Daily")               
)

apple_monthly = (returns_monthly
    .query("symbol == 'AAPL'")
    .assign(frequency="Monthly")                 
)

apple_retuns = pd.concat([apple_daily, apple_monthly], ignore_index=True)

apple_retuns_figure = (
    ggplot(apple_retuns, aes(x="ret", fill="frequency"))
    + geom_histogram(position="identity", bins=50)
    + labs(
        x="", y="", fill="frequency",
        title="Distribution of Apple retuns across different frequencies"
    )
    + scale_x_continuous(labels=percent_format())
    + facet_wrap("frequency", scales="free")
    + theme(legend_position="none")
)

# apple_retuns_figure.show()

# Other Forms of Data Aggregation

trading_volume = (prices_daily
    .assign(trading_volume=lambda x: (x["volume"]*x["adjusted_close"])/1e9)
    .groupby("date")["trading_volume"]
    .sum()
    .reset_index()
    .assign(trading_volume_lag=lambda x: x["trading_volume"].shift(periods=1))
)

# print(trading_volume)

trading_volume_figure = (
    ggplot(trading_volume, aes(x="date", y="trading_volume"))
    + geom_line()
    + scale_x_datetime(date_breaks="5 years", date_labels="%Y")
    + labs(
        x="", y="",
        title="Aggregate daily trading volume of DOW index constituents in billion USD"
    )
)

# trading_volume_figure.show()

persitence_figure = (
    ggplot(trading_volume, aes(x="trading_volume_lag", y="trading_volume"))
    + geom_point()
    + geom_abline(aes(intercept=0, slope=1), linetype="dashed")
    + labs(
        x="Previous day aggregate trading volume",
        y="Aggregate trading volume",
        title="Persistence in daily trading volume of DOW constituents in billion USD"
    )
)

persitence_figure.show()