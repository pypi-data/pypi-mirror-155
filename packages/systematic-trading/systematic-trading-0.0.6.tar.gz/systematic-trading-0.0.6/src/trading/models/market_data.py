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
        pass

    def bardata(self, contract: Contract, day: date):
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
        data, err = self.get_future_ohlcv_for_day(contract=contract, day=day)
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
    @staticmethod
    def __get_future_ohlcv(ric, start_date, end_date):
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
        dfm, error = Client().get_daily_ohlcv(ric, start_date, end_date)
        if dfm is None:
            return None, error
        dfm.reset_index(drop=False, inplace=True)
        dfm.Date = dfm.Date.apply(lambda x: x[:10])
        dfm.drop(columns=["RIC"], inplace=True)
        dfm.set_index("Date", drop=True, inplace=True)
        return dfm, error

    def get_future_ohlcv_for_day(self, contract: Contract, day: date):
        """
        Get OHLCV data for a future and for a specific day.

        Parameters
        ----------
            contract: Contract
                Contract of the instrument.

            day: date
                Day to collect data from.

        Returns
        -------
            DataFrame
                Future data.
            str
                Error message.
        """
        first_trade_date = contract.first_trade_date
        last_trade_date = contract.last_trade_date
        if (
            first_trade_date is None
            or day < first_trade_date
            or last_trade_date is None
            or day > last_trade_date
        ):
            message = f"No OHLCV for {contract.ric} on {day.isoformat()}"
            return None, {"message": message}
        dfm, _ = MarketData.__get_future_ohlcv(
            contract.ric, first_trade_date, last_trade_date
        )
        if dfm is not None:
            index = dfm.index == day.isoformat()
            current_day_exists = np.any(index)
            if current_day_exists:
                return dfm.loc[index, :], None
        message = f"No OHLCV for {contract.ric} on {day.isoformat()}"
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
        trading_days = get_calendar("NYSE").valid_days(
            first_trading_day, first_trading_day + timedelta(days=2 * window)
        )
        assert len(trading_days) > window
        return trading_days[window].date()

    def is_trading_day(self, contract: Contract, day: date):
        """
        Check is the day is a trading day for this instrument.

        Parameters
        ----------
            contract: Contract
                Contract object of the instrument.

            day: date
                Day to check.

        Returns
        -------
            bool
                True is the day is a trading day. Folse otherwise.
        """
        try:
            row = self.bardata(contract=contract, day=day)
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
        front_contract, front_ltd = Contract(day=day, ticker=ticker).front_contract
        if day + timedelta(days=MAXIMUM_NUMBER_OF_DAYS_BEFORE_EXPIRY) < front_ltd:
            return False
        future = FUTURES.get(ticker, {})
        roll_offset_from_reference = timedelta(
            days=future.get("RollOffsetFromReference", -31)
        )

        def is_good_day_to_roll(day, front_contract, next_contract):
            return (
                not is_weekend(day)
                and self.is_trading_day(contract=front_contract, day=day)
                and self.is_trading_day(contract=next_contract, day=day)
            )

        delta = front_ltd - day + roll_offset_from_reference
        next_contract, _ = Contract(day=day, ticker=ticker).front_contract
        for i in range(delta.days, -1, -1):
            _day = day + timedelta(days=i)
            if is_good_day_to_roll(_day, front_contract, next_contract):
                return day == _day
        return False
