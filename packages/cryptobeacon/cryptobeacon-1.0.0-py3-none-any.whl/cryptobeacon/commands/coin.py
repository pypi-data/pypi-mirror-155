"Manage the coins tracked by the watchlist."

import typer
from cryptobeacon.utils.coins import Coin, save_coins
from requests.exceptions import RequestException

app = typer.Typer()


@app.command()
def add(
    ctx: typer.Context, id_coin: str = typer.Argument(..., help="ID of the coin.")
) -> None:
    """Add a coin to be tracked in the watchlist."""

    if id_coin in ctx.obj["PARSER"].sections():
        ctx.obj["CONSOLE"].print(
            f"[red]{id_coin.capitalize()}[/red] is already on the watchlist",
            style="bold",
        )

    else:

        try:

            response = ctx.obj["API"].get_coin(id_coin, market_data=True)

            save_coins(
                ctx,
                [
                    Coin(
                        id=response["id"],
                        name=response["name"],
                        symbol=response["symbol"],
                        price_current=float(
                            response["market_data"]["current_price"]["usd"]
                        ),
                        price_previous=0.0,
                        alarms_down=set(),
                        alarms_up=set(),
                    )
                ],
            )

            ctx.obj["CONSOLE"].print(
                f"[green]{id_coin.capitalize()}[/green] was added to the watchlist",
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
    ctx: typer.Context, id_coin: str = typer.Argument(..., help="ID of the coin.")
) -> None:
    """Remove a coin from the watchlist."""

    try:

        del ctx.obj["PARSER"][id_coin]

        with ctx.obj["FILE"].open("w") as f:
            ctx.obj["PARSER"].write(f)

        ctx.obj["CONSOLE"].print(
            f"[green]{id_coin.capitalize()}[/green] was removed from the watchlist",
            style="bold",
        )

    except FileNotFoundError:
        ctx.obj["CONSOLE"].print(
            "Missing the [red]configurations[/red] file", style="bold"
        )

    except KeyError:
        ctx.obj["CONSOLE"].print(
            f"[magenta]{id_coin.capitalize()}[/magenta] is not on the watchlist",
            style="bold",
        )
