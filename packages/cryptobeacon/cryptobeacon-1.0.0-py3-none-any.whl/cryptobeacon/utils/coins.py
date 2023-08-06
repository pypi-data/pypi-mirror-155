"Manage the coin information."

import os
from dataclasses import dataclass
from importlib import resources
from typing import Dict, List, Mapping, Set

import typer
from rich import box
from rich.table import Table

_FILE_ICON = "beacon.ico"


@dataclass
class Coin:
    id: str
    name: str
    symbol: str

    price_current: float
    price_previous: float

    alarms_down: Set[float]
    alarms_up: Set[float]

    def __post_init__(self) -> None:
        """Clean invalid alarms."""

        list_remove = []

        for alarm in self.alarms_down:
            if alarm > self.price_current:
                list_remove.append(alarm)

        for alarm in list_remove:
            self.alarms_down.remove(alarm)

        list_remove = []

        for alarm in self.alarms_up:
            if alarm < self.price_current:
                list_remove.append(alarm)

        for alarm in list_remove:
            self.alarms_up.remove(alarm)

    def update_price(self, value) -> None:
        """Update the current and previous prices for the coin.

        Args:
            value (_type_): Current value.
        """

        self.price_previous = self.price_current
        self.price_current = value

    def set_alarm(self, value: float) -> None:
        """Set an alarm for the coin.

        Args:
            value (float): Target price for the alarm.

        Raises:
            ValueError: Invalid target value.
        """

        if value > self.price_current:
            self.alarms_up.add(value)

        elif value < self.price_current:
            self.alarms_down.add(value)

        else:
            raise ValueError

    def remove_alarm(self, value: float) -> None:
        """Remove an alarm.

        Args:
            value (float): Target price of the alarm.
        """

        if value > self.price_current:
            self.alarms_up.remove(value)

        else:
            self.alarms_down.remove(value)

    def check_alarms(self) -> None:
        """Check the alarms against the current price, sending a notification if a target is reached."""

        list_remove = []

        if self.price_current > self.price_previous:

            for alarm in self.alarms_up:
                if alarm <= self.price_current:
                    list_remove.append(alarm)

            for alarm in list_remove:
                self.alarms_up.remove(alarm)
                self.ring_alarm()

        else:

            for alarm in self.alarms_down:
                if alarm > self.price_current:
                    list_remove.append(alarm)

            for alarm in list_remove:
                self.alarms_down.remove(alarm)
                self.ring_alarm()

    def ring_alarm(self) -> None:
        """Send a desktop notification including the coin name and the current price."""

        os.system(
            f'notify-send "The price of {self.name} has reached {self.price_current}" -i "{resources.path("assets", _FILE_ICON)}"'
        )


def string_2_set(alarms: str) -> Set[float]:
    """Converts a comma-separated string to a set.

    Args:
        alarms (str): Comma-separated alarm string.

    Returns:
        Set[float]: Set of alarms.
    """

    values = []

    if alarms:
        values = alarms.split(" ")
        values = [float(value) for value in values]

    return set(values)


def set_to_string(alarms: Set[float]) -> str:
    """Convert a set to a comma-separated alarm string.

    Args:
        alarms (Set[float]): Set of alarms.

    Returns:
        str: Comma-separated alarm string.
    """

    values = [str(value) for value in alarms]

    return " ".join(values)


def load_coins(ctx: typer.Context, coins: str) -> Dict[str, Coin]:
    """Load the coins from the configuration file.

    Args:
        ctx (typer.Context): Typer context manager.
        coins (str): Comma-separated list of coins.

    Returns:
        Dict[str, Coin]: Dictionary of Coin objects.
    """

    coin_dict = {}
    prices = ctx.obj["API"].get_price(coins)

    if coins:
        for coin_id in coins.split(","):

            coin_info = ctx.obj["PARSER"][coin_id]
            price_previous = float(coin_info["price_current"])
            price_current = float(prices[coin_id]["usd"])

            coin_dict[coin_id] = Coin(
                id=coin_info["id"],
                name=coin_info["name"],
                symbol=coin_info["symbol"],
                price_current=price_current,
                price_previous=price_previous,
                alarms_down=string_2_set(coin_info["alarms_down"]),
                alarms_up=string_2_set(coin_info["alarms_up"]),
            )

    return coin_dict


def save_coins(ctx: typer.Context, coin_list: List[Coin]) -> None:
    """Save the coin watchlist to the configuration file.

    Args:
        ctx (typer.Context): Typer context manager.
        coin_list (List[Coin]): List of Coin objects.
    """

    for coin in coin_list:

        ctx.obj["PARSER"][coin.id] = {
            "id": coin.id,
            "name": coin.name,
            "symbol": coin.symbol,
            "price_current": str(coin.price_current),
            "price_previous": str(coin.price_previous),
            "alarms_down": set_to_string(coin.alarms_down),
            "alarms_up": set_to_string(coin.alarms_up),
        }

    with ctx.obj["FILE"].open("w") as f:
        ctx.obj["PARSER"].write(f)


def list_coins(ctx: typer.Context, coin_list: Mapping[str, Coin]) -> None:
    """Show the coin watchlist, including name, symbol, price and active alarms for each coin.

    Args:
        ctx (typer.Context): Typer context manager.
        coin_list (Mapping[str, Coin]): Dictionary of Coin objects.
    """

    list_table = Table(
        title="\n🔎 [underline]WATCHLIST",
        show_header=True,
        title_style="bold",
        header_style="bold",
        show_lines=True,
        box=box.ROUNDED,
    )
    list_table.add_column("#", justify="center")
    list_table.add_column("[blue]Coin", justify="center")
    list_table.add_column("[magenta]Symbol", justify="center")
    list_table.add_column("[yellow]$ Price", justify="center")
    list_table.add_column("[green]▲ Up", justify="center")
    list_table.add_column("[red]▼ Down", justify="center")

    for index, key in enumerate(coin_list):

        coin = coin_list[key]
        list_table.add_row(
            str(index + 1),
            coin.name,
            coin.symbol.upper(),
            str(coin.price_current),
            set_to_string(coin.alarms_up),
            set_to_string(coin.alarms_down),
        )

    ctx.obj["CONSOLE"].print(list_table)
