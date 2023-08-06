"""
Forex module.
"""
from datetime import date, datetime

from methodtools import lru_cache
import numpy as np
import pandas as pd

from ..data.client import Client
from ..data.constants import FUTURES


class Forex:
    """
    Forex implementation.
    """

    def __init__(self):
        self._client = Client()

    def bar_to_usd(self, bardata, ticker):
        """
        Convert a bar data to USD values.

        Parameters
        ----------
            bardata: str
                The bardata you convert.

            ticker: str
                The ticker of the instrument. Needed to check its currency.

        Returns
        -------
            DataFrame
                The USD bardata.
        """
        currency = FUTURES[ticker]["Currency"]
        if currency != "USD":
            day = bardata.index[0]
            rate = self.to_usd(currency, day)
            columns = ["Open", "High", "Low", "Close"]
            bardata.loc[:, columns] = bardata.loc[:, columns] * rate
            bardata.loc[:, "Volume"] = bardata.loc[:, "Volume"] / rate
        return bardata

    @lru_cache()
    def __get_forex_ohlcv(self, ric: str, start_date: date, end_date: date):
        """
        Get forex OHLCV.

        Parameters
        ----------
            ric: str
                Instrument RIC.

            start_date: date
                Start date of the time range.

            end_date: date
                End date of the time range.

        Returns
        -------
            DataFrame
                Forex daily OHLCV.
        """
        return self._client.get_daily_ohlcv(ric, start_date, end_date)

    def to_usd(self, currency: str, day: date):
        """
        Get the conversion rate to USD.

        Parameters
        ----------
            currency: str
                Currency code.

            day: date
                Day you want to get forex data for.

        Returns
        -------
            float:
                Conversion rate.
        """
        conversion_rate = np.NaN
        if currency == "AUD":
            conversion_rate = self.__get_pair(day, "USDAUD=R", invert=True)
        elif currency == "CAD":
            conversion_rate = self.__get_pair(day, "CADUSD=R")
        elif currency == "CHF":
            conversion_rate = self.__get_pair(day, "CHFUSD=R")
        elif currency == "EUR":
            conversion_rate = self.__get_pair(day, "USDEUR=R", invert=True)
        elif currency == "GBP":
            conversion_rate = self.__get_pair(day, "USDGBP=R", invert=True)
        elif currency == "HKD":
            conversion_rate = self.__get_pair(day, "HKDUSD=R")
        elif currency == "JPY":
            conversion_rate = self.__get_pair(day, "JPYUSD=R")
        elif currency == "USD":
            conversion_rate = 1
        elif currency == "SGD":
            conversion_rate = self.__get_pair(day, "SGDUSD=R")
        return conversion_rate

    def __get_pair(self, day, ric, invert=False):
        start_date = date(day.year, 1, 1)
        end_date = min(date(day.year, 12, 31), date.today())
        dfm, _ = self.__get_forex_ohlcv(ric, start_date, end_date)
        if dfm is None:
            return np.NaN
        _day = datetime.combine(day, datetime.min.time())
        index = pd.to_datetime(
            dfm.index.map(lambda x: x[0]), format="%Y-%m-%d"
        ).get_indexer([_day], method="nearest")[0]
        dfm = dfm.iloc[index, :]
        return 1 / dfm.Close if invert else dfm.Close
