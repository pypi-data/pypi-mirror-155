"Manage the alarms for a coin in the watchlist."

import typer
from cryptobeacon.utils.coins import load_coins, save_coins
from requests import RequestException

app = typer.Typer()


@app.command()
def add(
    ctx: typer.Context,
    id_coin: str = typer.Argument(..., help="ID of the coin in the watchlist."),
    value: float = typer.Argument(..., help="Target price for the alarm."),
) -> None:
    """Set an alarm for a coin in the watchlist, sending a desktop notification when the price is reached."""

    try:

        coin = load_coins(ctx, id_coin)[id_coin]

        try:

            coin.set_alarm(value)
            save_coins(ctx, [coin])

            ctx.obj["CONSOLE"].print(
                f"The [green]{value}[/green] alarm was set to [blue]{id_coin.capitalize()}[/blue]",
                style="bold",
            )

        except ValueError:
            ctx.obj["CONSOLE"].print(
                f"The [magenta]{value}[/magenta] alarm is the current price of [blue]{id_coin.capitalize()}[/blue]",
                style="bold",
            )

    except KeyError:
        ctx.obj["CONSOLE"].print(
            f"[magenta]{id_coin.capitalize()}[/magenta] is not on the watchlist",
            style="bold",
        )

    except FileNotFoundError:
        ctx.obj["CONSOLE"].print(
            "Missing the [red]configurations[/red] file", style="bold"
        )

    except RequestException as e:

        if e.response.status_code == 404:
            ctx.obj["CONSOLE"].print(
                f"Unable to find the coin with id [red]{id_coin}[/red]",
                style="bold",
            )

        else:
            ctx.obj["CONSOLE"].print(
                f"Request error: [red]{e}[/red]",
                style="bold",
            )


@app.command()
def remove(
    ctx: typer.Context,
    id_coin: str = typer.Argument(..., help="ID of the coin in the watchlist."),
    value: float = typer.Argument(..., help="Target price for the alarm."),
) -> None:
    """Remove an alarm for a coin in the watchlist."""

    try:

        coin = load_coins(ctx, id_coin)[id_coin]

        try:

            coin.remove_alarm(value)
            save_coins(ctx, [coin])

            ctx.obj["CONSOLE"].print(
                f"The [green]{value}[/green] alarm was removed from [blue]{id_coin.capitalize()}[/blue]",
                style="bold",
            )

        except KeyError:
            ctx.obj["CONSOLE"].print(
                f"There is no [magenta]{value}[/magenta] alarm on [blue]{id_coin.capitalize()}[/blue]",
                style="bold",
            )

    except KeyError:
        ctx.obj["CONSOLE"].print(
            f"There is no coin with ID [red]{id_coin}[/red] on the watchlist",
            style="bold",
        )

    except FileNotFoundError:
        ctx.obj["CONSOLE"].print(
            "Missing the [red]configurations[/red] file", style="bold"
        )

    except RequestException as e:

        if e.response.status_code == 404:
            ctx.obj["CONSOLE"].print(
                f"Unable to find the coin with ID [red]{id_coin}[/red]",
                style="bold",
            )

        else:
            ctx.obj["CONSOLE"].print(
                f"Request error: [red]{e}[/red]",
                style="bold",
            )
