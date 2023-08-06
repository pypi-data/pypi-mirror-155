"""
Broker simulator
"""
import numpy as np

from .contract import Contract
from .forex import Forex
from .margin import Margin
from .market_data import MarketData
from .market_impact import MarketImpact
from ..data.constants import FUTURES, FUTURE_TYPE


COMMISSION_INTERACTIVE_BROKERS_USD = (
    1.05  # Source: https://www.interactivebrokers.com/en/index.php?f=1590&p=futures2
)


# pylint: disable=too-many-instance-attributes
class Broker:
    """
    Broker. Compute the executions and maintains the positions registry.
    """

    def __init__(
        self,
        cash,
        live,
        no_check=False,
    ):
        self.positions = {
            "Cash": {
                "USD": cash,
            },
            FUTURE_TYPE: {},
        }
        self.previous_close = {}
        self.day = None
        self.executions = []
        self.forex = Forex()
        self.has_execution = False
        self.live = live
        self.margin = Margin()
        self.market_data = MarketData()
        self.market_impact = MarketImpact()
        self.no_check = no_check

    def apply_adjustment(self, adjustment_ratio: float):
        """
        Apply adjustment to position size based on the actual cash on the broker account.

        Parameters
        ----------
            adjustment_ratio: float
                Cash adjustment ratio.

        Returns
        -------
        """
        for key, value in self.positions.items():
            self.positions[key] = {k: v * adjustment_ratio for k, v in value.items()}

    def _apply_commission(self, contract_number: int):
        commission = -np.abs(contract_number) * COMMISSION_INTERACTIVE_BROKERS_USD
        self.positions["Cash"]["USD"] += commission
        return commission

    def _apply_market_impact(self, ric, contract_number, execution_price):
        relative_market_impact = self.market_impact.get(ric=ric)
        ticker = Contract(ric=ric).ticker
        full_point_value = FUTURES[ticker]["FullPointValue"]
        currency = FUTURES[ticker]["Currency"]
        full_point_value_usd = full_point_value * self.forex.to_usd(currency, self.day)
        market_impact = (
            -np.abs(contract_number)
            * relative_market_impact
            * execution_price
            * full_point_value_usd
        )
        self.positions["Cash"][currency] += market_impact
        return market_impact

    def buy_future(self, contract: Contract, contract_number: int):
        """
        Buy future contracts.

        Parameters
        ----------
            contract: Contract
                Instrument Contract.

            contract_number: int
                Number of contracts to buy.

        Returns
        -------
        """
        if not self.live:
            contract_number = np.round(contract_number)
        if contract_number == 0:
            return
        currency = FUTURES[contract.ticker]["Currency"]
        if currency not in self.positions["Cash"]:
            self.positions["Cash"][currency] = 0
        if np.isnan(self.positions["Cash"][currency]):
            raise ValueError("Cash is nan.", ric, self.day)

        row = self.market_data.bardata(contract=contract, day=self.day)
        if np.isnan(row.Close[0]):
            raise ValueError("Close is nan.", contract.ric, self.day)
        execution_price = row.Close[0]
        self.positions[FUTURE_TYPE][contract.ric] = (
            self.positions[FUTURE_TYPE].get(contract.ric, 0) + contract_number
        )
        self.positions["Cash"][currency] -= (
            contract_number
            * execution_price
            * FUTURES[contract.ticker]["FullPointValue"]
        )
        commission = self._apply_commission(contract_number)
        market_impact = self._apply_market_impact(
            contract.ric, contract_number, execution_price
        )
        self._check_initial_margin(contract.ric, contract_number)
        self.executions.append(
            {
                **{
                    "Date": self.day.isoformat(),
                    "Ric": contract.ric,
                    "Ticker": contract.ticker,
                    "Type": "Buy" if contract_number > 0 else "Sell",
                    "ContractNumber": contract_number,
                    "Currency": currency,
                    "ExecutionPrice": execution_price,
                    "FullPointValue": FUTURES[contract.ticker]["FullPointValue"],
                    "Commission": commission,
                    "MarketImpact": market_impact,
                },
                **{f"CashAfter{k}": v for k, v in self.positions["Cash"].items()},
            }
        )
        self.has_execution = True

    def _check_initial_margin(self, ric: str, contract_number: int):
        if self.no_check:
            return
        total_required_margin = 0
        for _ric, _contract_number in self.positions[FUTURE_TYPE].items():
            if _ric == ric:
                _contract_number += contract_number
            ticker = Contract(ric=_ric).ticker
            margin = (
                self.margin.overnight_maintenance_future(ticker, self.day)
                if _ric != ric
                else self.margin.overnight_initial_future(ticker, self.day)
            )
            total_required_margin += np.abs(_contract_number) * margin
        if total_required_margin > self.nav:
            raise Exception(
                f"Initial margin exceeded {self.day.isoformat()} {ric}"
                + f" {contract_number} {total_required_margin} {self.nav}"
            )

    def _check_maintenance_margin(self):
        if self.no_check:
            return
        total_required_margin = 0
        for _ric, _contract_number in self.positions[FUTURE_TYPE].items():
            ticker = Contract(ric=_ric).ticker
            margin = self.margin.overnight_maintenance_future(ticker, self.day)
            if np.isnan(margin):
                continue
            total_required_margin += np.abs(_contract_number) * margin
        if total_required_margin > self.nav:
            raise Exception(f"Maintenance margin exceeded {self.day.isoformat()}")

    def expire_future(self, contract: Contract):
        """
        Force future expiration closing all positions.

        Parameters
        ----------
            ric: str
                Instrument RIC.

        Returns
        -------
        """
        dfm, _ = self.market_data.get_future_ohlcv_for_day(
            contract=contract, day=self.day
        )
        execution_price = (
            dfm.Close[0]
            if not np.isnan(dfm.Close[0])
            else np.nanmedian(dfm[["Open", "High", "Low"]])
        )
        return self.close_future(contract=contract, execution_price=execution_price)

    def close_future(self, contract: Contract, execution_price=None):
        """
        Close future positions.

        Parameters
        ----------
            contract: Contract
                Instrument Contract.

            execution_price: float | None
                Execution price of the position closing.

        Returns
        -------
        """
        currency = FUTURES[contract.ticker]["Currency"]
        if currency not in self.positions["Cash"]:
            self.positions["Cash"][currency] = 0
        if np.isnan(self.positions["Cash"][currency]):
            raise ValueError("Cash is nan.", contract.ric, self.day)
        if execution_price is None:
            row = self.market_data.bardata(contract=contract, day=self.day)
            if np.isnan(row.Close[0]):
                raise ValueError("Close is nan.", contract.ric, self.day)
            execution_price = row.Close[0]
        contract_number = self.positions[FUTURE_TYPE].get(contract.ric, 0)
        self.positions[FUTURE_TYPE][contract.ric] = (
            self.positions[FUTURE_TYPE].get(contract.ric, 0) - contract_number
        )
        self.positions["Cash"][currency] += (
            contract_number
            * execution_price
            * FUTURES[contract.ticker]["FullPointValue"]
        )
        commission = self._apply_commission(contract_number)
        market_impact = self._apply_market_impact(
            contract.ric, contract_number, execution_price
        )
        self.executions.append(
            {
                **{
                    "Date": self.day.isoformat(),
                    "Ric": contract.ric,
                    "Ticker": contract.ticker,
                    "Type": "Close",
                    "ContractNumber": contract_number,
                    "Currency": currency,
                    "ExecutionPrice": execution_price,
                    "FullPointValue": FUTURES[contract.ticker]["FullPointValue"],
                    "Commission": commission,
                    "MarketImpact": market_impact,
                },
                **{f"CashAfter{k}": v for k, v in self.positions["Cash"].items()},
            }
        )
        self.has_execution = True
        return contract_number

    @property
    def nav(self):
        """
        Compute the current Net Asset Value.

        Parameters
        ----------

        Returns
        -------
            float
                NAV
        """
        if np.any([np.isnan(cash) for cash in self.positions["Cash"].values()]):
            raise ValueError("Cash is nan.", self.day)
        cash_in_usd = np.sum(
            [
                value * self.forex.to_usd(currency, self.day)
                for currency, value in self.positions["Cash"].items()
            ]
        )
        nav = cash_in_usd
        for ric, contract_number in self.positions[FUTURE_TYPE].items():
            if contract_number == 0:
                continue
            contract = Contract(ric=ric)
            if self.market_data.is_trading_day(contract=contract, day=self.day):
                row = self.market_data.bardata(contract=contract, day=self.day)
                close = row.Close[0]
                self.previous_close[contract.ric] = close
            else:
                close = self.previous_close.get(ric, np.NaN)
            ticker = Contract(ric=ric).ticker
            full_point_value = FUTURES[ticker]["FullPointValue"]
            currency = FUTURES[ticker]["Currency"]
            full_point_value_usd = full_point_value * self.forex.to_usd(
                currency, self.day
            )
            nav += contract_number * close * full_point_value_usd
        return nav

    def next(self, day):
        """
        Go to next day and set it.

        Parameters
        ----------
            day: date
                Next day.

        Returns
        -------
        """
        self.day = day
        self._check_maintenance_margin()
        self.has_execution = False

    def roll_front_contract(self, ticker):
        """
        For front contract to the next one.

        Parameters
        ----------
            ticker: str
                Instrument ticker.

        Returns
        -------
        """
        front_contract, _ = Contract(day=self.day, ticker=ticker).front_contract
        next_contract, _ = Contract(day=self.day, ticker=ticker).next_contract
        if not self.market_data.is_trading_day(
            contract=front_contract, day=self.day
        ) or not self.market_data.is_trading_day(contract=next_contract, day=self.day):
            return None
        closed_contract_number = 0
        if self.positions[FUTURE_TYPE].get(front_contract.ric, 0) != 0:
            closed_contract_number += self.close_future(contract=front_contract)

        if closed_contract_number != 0:
            self.buy_future(
                contract=next_contract, contract_number=closed_contract_number
            )
        return next_contract.ric

    def sell_future(self, contract: Contract, contract_number: int):
        """
        Sell future contracts.

        Parameters
        ----------
            ric: str
                Instrument RIC.

            contract_number: int
                Number of contracts to buy.

        Returns
        -------
        """
        return self.buy_future(contract, -contract_number)
