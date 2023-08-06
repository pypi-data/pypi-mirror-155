"""
Backtester
"""

from datetime import timedelta
import os
from pprint import pprint
import uuid

import numpy as np
import pandas as pd
from tqdm import tqdm

from .broker import Broker
from .contract import Contract
from .market_data import MarketData
from ..utils.dates import is_weekend


TWELVE_MONTHS = 250


from dataclasses import dataclass


# pylint: disable=too-many-instance-attributes
@dataclass
class BacktesterParameters:
    """
    Backtester parameters.
    """

    def __init__(self):
        self.cash = 0
        self.custom = {}
        self.end_date = None
        self.leverage = 1
        self.live = False
        self.no_check = False
        self.plot = True
        self.suffix = ""
        self.start_date = None
        self.tickers = []


# pylint:
class Backtester:
    """
    This class implements the backtester.
    The function run() iterates on every day of the backtesting period and
    calls next() and next_iterators() where respectively the decisions and
    indicators computations happen.
    """

    def __init__(
        self,
        params,
    ):
        self.broker = Broker(params.cash, params.live, params.no_check)
        self.market_data = MarketData()
        self.data = []
        self.dates = []
        self.day = None
        self._params = params
        self.nav = params.cash

    def compute_kelly(self):
        """
        Compute the Kelly ratio, an indicator for strategy max leverage.

        Parameters
        ----------

        Returns
        -------
            float
                Kelly ratio.
        """
        dfm = pd.DataFrame(data=self.data, index=self.dates)
        returns = np.diff(np.log(dfm.Nav))
        kelly = np.nanmean(returns) / np.power(np.nanstd(returns), 2)
        return kelly

    def compute_mean(self):
        """
        Compute the mean of daily returns, annualized.

        Parameters
        ----------

        Returns
        -------
            float
                Mean of daily returns, annualized.
        """
        dfm = pd.DataFrame(data=self.data, index=self.dates)
        returns = np.diff(np.log(dfm.Nav))
        mean = np.nanmean(returns) * TWELVE_MONTHS
        return mean

    def _plot_nav(self):
        dfm = pd.DataFrame(data=self.data, index=self.dates)
        fname = ",".join(self._params.tickers)
        if len(fname) > 30:
            fname = str(uuid.uuid3(uuid.NAMESPACE_URL, fname))
        filename = (
            fname
            + f".{self._params.leverage}.{self._params.end_date.isoformat()}"
            + f".{self._params.suffix}.png"
        )
        path = os.path.join(os.getenv("HOME"), "Downloads", filename)
        dfm[["Nav"]].plot(logy=True).get_figure().savefig(path)

    def compute_sharpe_ratio(self):
        """
        Compute the Sharpe ratio.

        Parameters
        ----------

        Returns
        -------
            float
                Sharpe ratio.
        """
        dfm = pd.DataFrame(data=self.data, index=self.dates)
        returns = np.diff(np.log(dfm.Nav))
        sharpe_ratio = np.nanmean(returns) / np.nanstd(returns) * np.sqrt(250)
        return sharpe_ratio

    def compute_std(self):
        """
        Compute the standard deviation of daily returns, annualized (ie. the volatility).

        Parameters
        ----------

        Returns
        -------
            float
                Standard deviation of daily returns, annualized.
        """
        dfm = pd.DataFrame(data=self.data, index=self.dates)
        returns = np.diff(np.log(dfm.Nav))
        std = np.nanstd(returns) * np.sqrt(TWELVE_MONTHS)
        return std

    def _has_not_enough_active_contracts(self):
        for ticker in self._params.tickers:
            active_contracts = Contract.get_chain(ticker=ticker, day=self.day)
            if active_contracts.shape[0] < 2:
                return ticker
        return None

    def run(self):
        """
        This function iterate on the backtest period and call
        the next function where the logic of the strategy is implemented.

        Parameters
        ----------

        Returns
        -------
        """
        delta = self._params.end_date - self._params.start_date
        for i in tqdm(range(delta.days + 1)):
            self.day = self._params.start_date + timedelta(days=i)
            not_enough_active_contracts = self._has_not_enough_active_contracts()
            if not_enough_active_contracts is not None:
                raise Exception(
                    f"Update future-expiry/{not_enough_active_contracts}.csv in Minio"
                )
            if is_weekend(self.day):
                continue
            self.broker.next(self.day)
            self.next()
            self.next_indicators()
            self.dates.append(self.day)
            nav = self.broker.nav
            if not np.isnan(nav):
                self.nav = nav
            data = {}
            data["Nav"] = nav
            self.data.append(data)
        if not self._params.live and self._params.plot:
            self._plot_nav()
        kelly = self.compute_kelly()
        mean = self.compute_mean()
        sharpe = self.compute_sharpe_ratio()
        std = self.compute_std()
        pprint(
            {
                "day": self.day,
                "mean": mean,
                "std": std,
                "kelly": kelly,
                "sharpe": sharpe,
            }
        )

    def next(self):
        """
        This function contains the logic of the strategy: decision, update of positions, etc.
        It is called on every new day.

        Parameters
        ----------

        Returns
        -------
        """
        raise Exception("To be implemented in the child class")

    def next_indicators(self):
        """
        This function contains the logic of the calculation of the indicators.
        It is called on every new day, after next().

        Parameters
        ----------

        Returns
        -------
        """
        raise Exception("To be implemented in the child class")
