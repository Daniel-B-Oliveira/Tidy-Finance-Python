import tidyfinance as tf
import pandas as pd
from plotnine import *
from mizani.formatters import percent_format

'''
Compute daily net returns for an asset of your choice
and visualize the distribution of daily returns in a
histogram using 100 bins. Also, use geom_vline() to
add a dashed red vertical line that indicates the 5
percent quantile of the daily returns. Compute summary
statistics (mean, standard deviation, minimum,
and maximum) for the daily returns.
'''

daily_prices = tf.download_data(
    domain="stock_prices",
    symbols="AMZN",
    start_date="2000-01-01",
    end_date="2025-07-24"
)

returns = (daily_prices
    .sort_values("date")
    .assign(ret=lambda x: x["adjusted_close"].pct_change())
    # .get(["symbols", "date", "ret"])
)

# print(returns.head(5).round(3))

returns.dropna()

quantile_05 = returns["ret"].quantile(0.05)

amzn_returns_figure = (
    ggplot(returns, aes(x="ret"))
    + geom_histogram(bins=100)
    + geom_vline(aes(xintercept=quantile_05), linetype="dashed")
    + labs(x="", y="", title="Distribution of daily Amazon stock retuns")
    + scale_x_continuous(labels=percent_format())
)

amzn_returns_figure.show()

print(pd.DataFrame(returns["ret"]
                   .groupby(returns["date"].dt.year)
                   .describe()
                   .round(3)
                   ))