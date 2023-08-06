"""
Client for the API https://marketdata.edarchimbaud.com
"""
from datetime import date
import os

import pandas as pd
import requests

from .constants import LAST_MODIFIED


class Client:
    """
    Client for the API https://marketdata.edarchimbaud.com
    """

    def __init__(self):
        self.api_url = "https://" + os.getenv("DATA_DOMAIN")
        self.headers = {"Authorization": os.getenv("DATA_SECRET_KEY")}

    def patch_bucket(self, bucket_name: str, action: str = LAST_MODIFIED):
        """
        Send a patch query to modify a bucket.

        Parameters
        ----------
            bucket_name: str
                Bucket name.

            action: str
                Action name, either empty or last-modified.

        Returns
        -------
        """
        requests.patch(
            f"{self.api_url}/private/bucket",
            headers=self.headers,
            params={"bucket_name": bucket_name, "action": action},
        )

    def get_daily_borrowing_rates(self, day: date):
        """
        Get daily borrowing rates.

        Parameters
        ----------
            day: date
                Day of the rates to query.

        Returns
        -------
            DataFrame
                Borrowing rates.

            str
                Error message.
        """
        response = requests.get(
            f"{self.api_url}/private/daily/borrowing-rates",
            headers=self.headers,
            params={
                "day": day.isoformat(),
            },
        )
        response_json = response.json()
        error = response_json["error"]
        data = response_json["data"]
        if data is None:
            return None, error
        dfm = pd.DataFrame.from_dict(data)
        dfm = dfm.set_index(["Date", "RIC"])
        return dfm, error

    def get_daily_factor(
        self, name: str, ticker: str, start_date: date, end_date: date
    ):
        """
        Get daily factor.

        Parameters
        ----------
            name: str
                Name of the factor to get. Either:
                    carry/bond
                    carry/commodity
                    carry/currency
                    carry/equity
                    cot
                    currency
                    nav/long
                    nav/short
                    news/headlines
                    news/stories
                    roll-return
                    splits

            ticker: str
                Instrument ticker.

            start_date: date
                Start date.

            end_date: date
                End date.

        Returns
        -------
            DataFrame
                Factor data.

            str
                Error message.
        """
        response = requests.get(
            f"{self.api_url}/private/daily/factor/{name}",
            headers=self.headers,
            params={
                "ticker": ticker,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
            },
        )
        response_json = response.json()
        error = response_json["error"]
        data = response_json["data"]
        if data is None:
            return None, error
        dfm = pd.DataFrame.from_dict(data)
        dfm = dfm.set_index(["Date", "Stem"])
        return dfm, error

    def get_daily_ohlcv(self, ric: str, start_date: date, end_date: date):
        """
        Get daily Open High Low Close Volume.

        Parameters
        ----------
            ric: str
                Instrument RIC.

            start_date: date
                Start date.

            end_date: date
                End date.

        Returns
        -------
            DataFrame
                Open High Low Close Volume data.

            str
                Error message.
        """
        response = requests.get(
            f"{self.api_url}/private/daily/ohlcv",
            headers=self.headers,
            params={
                "ric": ric,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
            },
        )
        response_json = response.json()
        error = response_json["error"]
        data = response_json["data"]
        if data is None:
            return None, error
        dfm = pd.DataFrame.from_dict(data)
        dfm = dfm.set_index(["Date", "RIC"])
        return dfm, error

    def get_daily_risk_free_rate(self, ric: str, start_date: date, end_date: date):
        """
        Get daily risk free rate.

        Parameters
        ----------
            ric: str
                Instrument RIC.

            start_date: date
                Start date.

            end_date: date
                End date.

        Returns
        -------
            DataFrame
                Risk free rate data.

            str
                Error message.
        """
        response = requests.get(
            f"{self.api_url}/private/daily/risk-free-rate",
            headers=self.headers,
            params={
                "ric": ric,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
            },
        )
        response_json = response.json()
        error = response_json["error"]
        data = response_json["data"]
        if data is None:
            return None, error
        dfm = pd.DataFrame.from_dict(data)
        dfm = dfm.set_index(["Date", "RIC"])
        return dfm, error

    def get_dataset(self, ticker: str, start_date: date, end_date: date):
        """
        Get dataset of market features and targets.

        Parameters
        ----------
            ticker: str
                Instrument ticker.

            start_date: date
                Start date.

            end_date: date
                End date.

        Returns
        -------
            DataFrame
                Dataset data.

            str
                Error message.
        """
        is_authenticated = bool(os.getenv("DATA_SECRET_KEY"))
        url = (
            f"{self.api_url}/private/dataset"
            if is_authenticated
            else f"{self.api_url}/public/dataset"
        )
        response = requests.get(
            url,
            headers=self.headers,
            params={
                "ticker": ticker,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
            },
        )
        response_json = response.json()
        error = response_json["error"]
        data = response_json["data"]
        if data is None:
            return None, error
        dfm = pd.DataFrame.from_dict(data)
        return dfm, error

    def get_expiry_calendar(self, ticker: str, download: bool = False):
        """
        Get expiry calendar.

        Parameters
        ----------
            ticker: str
                Instrument ticker.

            download: bool
                For download if True. Otherwise uses cache if possible.

        Returns
        -------
            DataFrame
                Expiry calendar data.

            str
                Error message.
        """
        response = requests.get(
            f"{self.api_url}/private/expiry-calendar",
            headers=self.headers,
            params={"ticker": ticker, "download": download},
        )
        response_json = response.json()
        error = response_json["error"]
        data = response_json["data"]
        if data is None:
            return None, error
        dfm = pd.DataFrame.from_dict(data)
        return dfm, error

    def get_health_ric(self, ric: str):
        """
        Check if RIC is still live or not.

        Parameters
        ----------
            ric: str
                Instrument RIC.

        Returns
        -------
            bool
                Either True if the RIC is live or False if not.

            str
                Error message.
        """
        response = requests.get(
            f"{self.api_url}/private/health/ric",
            headers=self.headers,
            params={
                "ric": ric,
            },
        )
        response_json = response.json()
        data = response_json["data"]
        error = response_json["error"]
        return data, error

    def get_tickers(self):
        """
        Get the list of instruments of the perimeter and their parameters.

        Parameters
        ----------

        Returns
        -------
            object
                List of instruments and their parameters.

            str
                Error message.
        """
        response = requests.get(f"{self.api_url}/private/tickers", headers=self.headers)
        response_json = response.json()
        data = response_json.get("data", [])
        error = response_json["error"]
        return data, error
