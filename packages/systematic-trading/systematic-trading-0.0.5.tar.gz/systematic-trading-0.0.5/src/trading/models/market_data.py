"""
Market data access.
"""
from datetime import date, timedelta

from methodtools import lru_cache
import numpy as np
from pandas_market_calendars import get_calendar

from .contract import Contract
from ..data.client import Client
from ..data.constants import FUTURES
from ..utils.dates import is_weekend


LIBOR_BEFORE_2001 = 6.65125
MAXIMUM_NUMBER_OF_DAYS_BEFORE_EXPIRY = 40


class MarketData:
    """
    Market data access.
    """

    def __init__(self):
        self._client = Client()

    def bardata(self, day: date, ric: str = None):
        """
        Get bar data.

        Parameters
        ----------
            ric: str
                RIC of the instrument.

            day: date
                Day collect data for.

        Returns
        -------
            DataFrame
                Collected bar data.
        """
        data, err = self.get_future_ohlcv_for_day(day=day, ric=ric)
        if err:
            raise Exception(err["message"])
        data = data.fillna(value=np.nan)
        if (
            np.isnan(data.Close[0])
            and not np.isnan(data.Volume[0])
            and not np.all(np.isnan(data[["Open", "High", "Low"]].values[0]))
        ):
            data.Close = np.nanmedian(data[["Open", "High", "Low"]].values[0])
        return data

    @lru_cache()
    def __get_future_ohlcv(self, ric, start_date, end_date):
        """
        Get OHLCV data for a future.

        Parameters
        ----------
            ric: str
                RIC of the instrument.

            start_date: date
                Start date of the period to collect data from.

            end_date: date
                End date of the period to collect data from.

        Returns
        -------
            DataFrame
                Future data.
            str
                Error message.
        """
        dfm, error = self._client.get_daily_ohlcv(ric, start_date, end_date)
        if dfm is None:
            return None, error
        dfm.reset_index(drop=False, inplace=True)
        dfm.Date = dfm.Date.apply(lambda x: x[:10])
        dfm.drop(columns=["RIC"], inplace=True)
        dfm.set_index("Date", drop=True, inplace=True)
        return dfm, error

    def get_future_ohlcv_for_day(self, day: date, ric=None):
        """
        Get OHLCV data for a future and for a specific day.

        Parameters
        ----------
            ric: str
                RIC of the instrument.

            day: date
                Day to collect data from.

        Returns
        -------
            DataFrame
                Future data.
            str
                Error message.
        """
        first_trade_date = Contract(ric=ric).first_trade_date
        last_trade_date = Contract(ric=ric).last_trade_date
        if (
            first_trade_date is None
            or day < first_trade_date
            or last_trade_date is None
            or day > last_trade_date
        ):
            message = f"No OHLCV for {ric} on {day.isoformat()}"
            return None, {"message": message}
        dfm, _ = self.__get_future_ohlcv(ric, first_trade_date, last_trade_date)
        if dfm is not None:
            index = dfm.index == day.isoformat()
            current_day_exists = np.any(index)
            if current_day_exists:
                return dfm.loc[index, :], None
        message = f"No OHLCV for {ric} on {day.isoformat()}"
        return None, {"message": message}

    def get_start_day(self, first_trading_day: date, window: int):
        """
        Get the start day of the strategy.

        Parameters
        ----------
            first_trading_day: date
                First day we have data for.

            window: int
                Number of trading days the strategy need.

        Returns
        -------
            date
                First day the strategy should be started to be traded.
        """
        i = 0
        number_of_business_days = 0
        while number_of_business_days < window:
            day = first_trading_day + timedelta(days=-i)
            is_trading_day = len(get_calendar("NYSE").valid_days(day, day)) == 1
            if is_trading_day and i > 0:
                number_of_business_days += 1
            i += 1
        return day

    def is_trading_day(self, day: date, ric=None):
        """
        Check is the day is a trading day for this instrument.

        Parameters
        ----------
            ric: str
                RIC of the instrument.

            day: date
                Day to check.

        Returns
        -------
            bool
                True is the day is a trading day. Folse otherwise.
        """
        if ric is None:
            return False
        try:
            row = self.bardata(day=day, ric=ric)
        except Exception as exception:
            message = str(exception)
            if "No OHLCV for" in message:
                return False
            if "[not-started]" in message:
                return False
            raise exception
        return not np.isnan(row.Close[0])

    def should_roll_today(self, day: date, ticker: str):
        """
        Check is the future needs to be rolled or not.

        Parameters
        ----------
            ticker: str
                Ticker of the instrument.

            day: date
                Day to check.

        Returns
        -------
            bool
                True is the future needs to be rolled.
        """
        front_ltd, front_ric = Contract(day=day, ticker=ticker).front_contract
        if day + timedelta(days=MAXIMUM_NUMBER_OF_DAYS_BEFORE_EXPIRY) < front_ltd:
            return False
        future = FUTURES.get(ticker, {})
        roll_offset_from_reference = timedelta(
            days=future.get("RollOffsetFromReference", -31)
        )

        def is_good_day_to_roll(day):
            return (
                not is_weekend(day)
                and self.is_trading_day(day=day, ric=front_ric)
                and self.is_trading_day(day=day, ric=next_ric)
            )

        delta = front_ltd - day + roll_offset_from_reference
        _, next_ric = Contract(day=day, ticker=ticker).front_contract
        day_to_roll = None
        for i in range(delta.days, -1, -1):
            _day = day + timedelta(days=i)
            if is_good_day_to_roll(_day):
                return day == _day
        return False
