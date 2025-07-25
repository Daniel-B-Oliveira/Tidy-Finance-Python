import pandas as pd
import tidyfinance as tf

'''
To facilitate the computation of the annualization factor,
write a function that takes a vector of return dates as
input and determines the frequency before returning the
appropriate annualization factor.
'''

def get_frequency_from_dates(dates: list) -> str:
    """
    Determines the frequency (daily, weekly, monthly, quarterly, yearly)
    of a series of dates.

    Args:
        dates: A list or Pandas Series of datetime objects.

    Returns:
        A string representing the estimated frequency:
        'B' (Business Day), 'W' (Weekly), 'M' (Monthly),
        'Q' (Quarterly), 'Y' (Yearly).
        Returns 'Unknown' if the frequency cannot be determined.
    """

    date_series = pd.to_datetime(dates)

    time_diffs = date_series.diff().dropna()

    if time_diffs.empty:
        return "Unknown"

    mean_diff = time_diffs.mean()

    tolerance = pd.Timedelta(hours=12)

    frequency_mapping = {
        "B": pd.Timedelta(days=1),                     # Business Day
        "W": pd.Timedelta(weeks=1),                    # Weekly
        "M": pd.Timedelta(days=365.25 / 12),           # Monthly (approximate)
        "Q": pd.Timedelta(days=365.25 / 4),            # Quarterly (approximate)
        "Y": pd.Timedelta(days=365.25)                 # Yearly (approximate)
    }

    for freq_code, avg_delta in frequency_mapping.items():
        if abs(mean_diff - avg_delta) < tolerance:
            return freq_code

    return "Unknown"

if __name__ == "__main__":
    prices = tf.download_data(
        domain="stock_prices", 
        symbols="AAPL",
        start_date="2000-01-01", 
        end_date="2000-01-31"
    )

    dates = prices["date"].sort_values().reset_index(drop=True)
    
    print(get_frequency_from_dates(dates))


