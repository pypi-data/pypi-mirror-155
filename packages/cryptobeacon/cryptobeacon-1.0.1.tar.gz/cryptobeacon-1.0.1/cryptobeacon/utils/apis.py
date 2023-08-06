"Manage the connection with the employed APIs."

from typing import Dict, Mapping

import requests
from requests.adapters import HTTPAdapter, Retry

_URL_API = "https://api.coingecko.com/api/v3/"
_ENDPOINT_SIMPLE = "simple/"


class API:
    def __init__(self, url_base: str = _URL_API) -> None:
        """Initiate the request session and set retry configurations.

        Args:
            url_base (str, optional): Base URL of the API. Defaults to _URL_API.
        """

        self.url_base = url_base
        self.timeout = 10

        self.session = requests.Session()
        retries = Retry(total=3, backoff_factor=0.25, status_forcelist=[502, 503, 504])
        self.session.mount(self.url_base, HTTPAdapter(max_retries=retries))

    def __request(
        self, url: str, headers: Mapping[str, str], params: Mapping[str, str]
    ) -> Dict[str, Dict[str, str]]:
        """Send an request to the API.

        Args:
            url (str): URL of the API.
            headers (Mapping[str, str]): HTTP headers.
            params (Mapping[str, str]): Request parameters.

        Returns:
            Dict[str, Dict[str, str]]: JSON HTTP response.
        """

        response = self.session.get(
            url,
            headers=headers,
            params=params,
            timeout=self.timeout,
        )

        response.raise_for_status()

        return response.json()

    def get_price(
        self,
        ids: str,
        vs_currencies: str = "usd",
        include_market_cap: bool = False,
        include_24hr_vol: bool = False,
        include_24hr_change: bool = False,
        include_last_updated_at: bool = False,
    ) -> Dict[str, Dict[str, str]]:
        """The the price related information for a list o coins.

        Args:
            ids (str): List of coin IDs.
            vs_currencies (str, optional): Fiat currency pair. Defaults to "usd".
            include_market_cap (bool, optional): Include market cap. Defaults to False.
            include_24hr_vol (bool, optional): Include 24h trading volume. Defaults to False.
            include_24hr_change (bool, optional): Include 24 price change. Defaults to False.
            include_last_updated_at (bool, optional): Include last update time. Defaults to False.

        Returns:
            Dict[str, Dict[str, str]]: Dictionary with the information by coin ID.
        """

        url = f"{_URL_API}{_ENDPOINT_SIMPLE}price"
        headers = {"accept": "application/json"}
        params = {
            "ids": ids,
            "vs_currencies": vs_currencies,
            "include_market_cap": str(include_market_cap).lower(),
            "include_24hr_vol": str(include_24hr_vol).lower(),
            "include_24hr_change": str(include_24hr_change).lower(),
            "include_last_updated_at": str(include_last_updated_at).lower(),
        }

        return self.__request(url, headers, params)

    def get_coin(
        self,
        id: str,
        localization: bool = False,
        tickers: bool = False,
        market_data: bool = False,
        community_data: bool = False,
        developer_data: bool = False,
        sparkline: bool = False,
    ) -> Dict[str, Dict[str, str]]:
        """Get all the information available for a coin.

        Args:
            id (str): Coin ID.
            localization (bool, optional): Add the description in other languages. Defaults to False.
            tickers (bool, optional): Add coin ticker price information. Defaults to False.
            market_data (bool, optional): Add global market information for the coin. Defaults to False.
            community_data (bool, optional): Add community information. Defaults to False.
            developer_data (bool, optional): Add development information. Defaults to False.
            sparkline (bool, optional): ?. Defaults to False.

        Returns:
            Dict[str, Dict[str, str]]: Dictionary containing all the request information.
        """

        url = f"{_URL_API}coins/{id}"
        headers = {"accept": "application/json"}
        params = {
            "localization": str(localization).lower(),
            "tickers": str(tickers).lower(),
            "market_data": str(market_data).lower(),
            "community_data": str(community_data).lower(),
            "developer_data": str(developer_data).lower(),
            "sparkline": str(sparkline).lower(),
        }

        return self.__request(url, headers, params)
