"""
Contract management functions.
"""
from datetime import date, datetime, timedelta

from methodtools import lru_cache

from ..data.client import Client
from ..data.constants import FUTURES, START_DATE


class Contract:
    """
    Contract management.
    """

    def __init__(
        self,
        ric: str = None,
        day: date = None,
        ticker: str = None,
        contract_rank: int = 0,
    ):
        if ric is not None or (day is not None and ticker is not None):
            self.contract_rank = contract_rank
            self.day = day
            self.ric = ric
            self._active_ric = None
            self._client = Client()
            self._first_trade_date = None
            self._last_trade_date = None
            self._ticker = ticker
        else:
            raise Exception("Contract parameters not properly specified.")

    def __get_ric_year(self):
        if "^" in self.ric:
            year_3 = self.ric.split("^")[1]
            year_4 = self.ric.split("^")[0][-1]
            year_12 = "19" if year_3 in ["8", "9"] else "20"
            year = int(f"{year_12}{year_3}{year_4}")
            return year
        return None

    @lru_cache()
    @staticmethod
    def __get_ric_exists_today(ric, _day=date.today()):
        ric_exists, _ = Client().get_health_ric(ric)
        return ric_exists

    @property
    def active_ric(self):
        """
        Converts to active RIC.

        Parameters
        ----------

        Returns
        -------
            str
                RIC.
        """
        if self._active_ric is None:
            is_recent_ric = self.is_recent_ric
            ric_exists = self.__get_ric_exists_today(self.ric)
            if is_recent_ric and not ric_exists:
                self._active_ric = self.ric.split("^")[0]
            else:
                self._active_ric = self.ric
        return self._active_ric

    @property
    def is_recent_ric(self):
        """
        Says if a RIC is still active or not.

        Parameters
        ----------

        Returns
        -------
            bool
                True if this is a recent RIC.
        """
        is_recent_ric = False
        year = self.__get_ric_year()
        if year:
            is_recent_ric = year >= (date.today() - timedelta(days=365)).year
        return is_recent_ric

    def __get_contract(self, ticker: str, day: date, contract_rank: int = 0):
        chain = self.get_chain(ticker=ticker, day=day)
        contract = chain.iloc[contract_rank, :]
        ltd = datetime.strptime(contract.LTD, "%Y-%m-%d").date()
        ric = contract.RIC
        ric = Contract(ric=ric).active_ric
        return ltd, ric

    @property
    def front_contract(self):
        """
        Get the front contract characteristics.

        Parameters
        ----------
            ticker: str
                Ticker of the contract.

            day: date
                Date of the contract to be checked.

        Returns
        -------
            date
                Last trading date.

            str
                RIC.
        """
        if self.ticker is None or self.day is None:
            return None, None

        future = FUTURES.get(self.ticker, {})
        roll_offset_from_reference = timedelta(
            days=future.get("RollOffsetFromReference", -31)
        )
        reference_day = self.day - roll_offset_from_reference
        return self.__get_contract(
            ticker=self.ticker, day=reference_day, contract_rank=0
        )

    @property
    def next_contract(self):
        """
        Get the next contract characteristics.

        Parameters
        ----------
            ticker: str
                Ticker of the contract.

            day: date
                Date of the contract to be checked.

        Returns
        -------
            date
                Last trading date.

            str
                RIC.
        """
        future = FUTURES.get(self.ticker, {})
        roll_offset_from_reference = timedelta(
            days=future.get("RollOffsetFromReference", -31)
        )
        reference_day = self.day - roll_offset_from_reference
        return self.__get_contract(
            ticker=self.ticker, day=reference_day, contract_rank=1
        )

    @property
    def ticker(self):
        """
        Convert a RIC to a ticker.

        Parameters
        ----------

        Returns
        -------
            str
                Ticker.
        """
        if self._ticker is None:
            suffix = "^"
            stem_wo_suffix = (
                self.ric.split(suffix)[0] if suffix in self.ric else self.ric
            )
            delayed_data_prefix = "/"
            stem_wo_prefix = (
                stem_wo_suffix.split(delayed_data_prefix)[-1]
                if delayed_data_prefix in stem_wo_suffix
                else stem_wo_suffix
            )
            stem_wo_year = "".join([c for c in stem_wo_prefix if not c.isdigit()])
            stem_wo_month = stem_wo_year[:-1]
            if stem_wo_month in ["SIRT"]:
                return "SI"
            for ticker in FUTURES.keys():
                if stem_wo_month == FUTURES[ticker].get("Stem", {}).get("Reuters"):
                    self._ticker = ticker
        return self._ticker

    @property
    def first_trade_date(self) -> date:
        """
        Get the contract first trade date.

        Parameters
        ----------

        Returns
        -------
            date
                First trade date.
        """
        if self._first_trade_date is None:
            chain = self.get_chain(ticker=self.ticker)
            if "^" in self.ric:
                contracts = chain.loc[chain.RIC == self.ric, "FTD"]
                if contracts.shape[0] == 0:
                    return None
                self._first_trade_date = datetime.strptime(
                    contracts.iloc[0], "%Y-%m-%d"
                ).date()
            else:
                index = chain.RIC.apply(lambda x: x.split("^")[0]) == self.ric
                contracts = chain.loc[index, :]
                if contracts.shape[0] == 0:
                    return None
                ltd = min(
                    contracts.LTD,
                    key=lambda x: abs(
                        datetime.strptime(x, "%Y-%m-%d").date() - date.today()
                    ),
                )
                ftd = contracts.FTD[contracts.LTD == ltd].iloc[0]
                self._first_trade_date = datetime.strptime(ftd, "%Y-%m-%d").date()
        return self._first_trade_date

    @property
    def last_trade_date(self) -> date:
        """
        Get the contract last trade date.

        Parameters
        ----------

        Returns
        -------
            date
                Last trade date.
        """
        if self._last_trade_date is None:
            chain = self.get_chain(ticker=self.ticker)
            if "^" in self.ric:
                contracts = chain.loc[chain.RIC == self.ric, "LTD"]
                if contracts.shape[0] == 0:
                    return None
                self._last_trade_date = datetime.strptime(
                    contracts.iloc[0], "%Y-%m-%d"
                ).date()
            else:
                index = chain.RIC.apply(lambda x: x.split("^")[0]) == self.ric
                contracts = chain.loc[index, :]
                if contracts.shape[0] == 0:
                    return None
                ltd = min(
                    contracts.LTD,
                    key=lambda x: abs(
                        datetime.strptime(x, "%Y-%m-%d").date() - date.today()
                    ),
                )
                self._last_trade_date = datetime.strptime(ltd, "%Y-%m-%d").date()
            return self._last_trade_date

    @lru_cache()
    @staticmethod
    def get_chain(ticker: str, day: date = START_DATE):
        """
        Get the future contract chain for a given ticker, day and minimum time to expiry.

        Parameters
        ----------
            ticker: str
                Ticker of the contract.

            day: date
                Day of the contract

            minimum_time_to_expiry: int
                Minimum time to expiry.

        Returns
        -------
            DataFrame
                Contract chain.
        """
        minimum_time_to_expiry = 0
        dfm, _ = Client().get_expiry_calendar(ticker)
        if datetime.strptime(dfm.LTD.iloc[-1], "%Y-%m-%d").date() - day < timedelta(
            days=minimum_time_to_expiry
        ):
            expiry_calendar = FUTURES.get(ticker, {}).get("ExpiryCalendar", "")
            raise Exception(
                f"Not enough data for {ticker}. Download expiry data from {expiry_calendar}"
            )
        index = (dfm.LTD >= day.isoformat()) & (
            dfm.WeTrd == 1
        )  # pylint: disable=no-member
        return dfm.loc[index, :].reset_index(drop=True)  # pylint: disable=no-member

    @property
    def will_expire_soon(self):
        """
        Get the future contract chain for a given ticker, day and minimum time to expiry.

        Parameters
        ----------

        Returns
        -------
            bool
                True if the contract expires soon. False otherwise.
        """
        return self.day > self.last_trade_date - timedelta(days=10)


def stem_to_ticker(stem: str):
    """
    Convert a stem to a ticker.

    Parameters
    ----------
        stem: str
            Stem of the contract.

    Returns
    -------
        str
            Ticker.
    """
    tickers = [
        k for k, v in FUTURES.items() if v.get("Stem", {}).get("Reuters") == stem
    ]
    if len(tickers) != 1:
        raise Exception(
            f"No future with Stem.Reuters {stem}. Double check file database-futures.json"
        )
    ticker = tickers[0]
    return ticker
