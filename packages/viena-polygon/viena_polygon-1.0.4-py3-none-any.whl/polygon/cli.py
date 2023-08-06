"""This module provides the CLI."""
# cli-module/cli.py

from pathlib import Path
from typing import List, Optional
import typer
from polygon import __app_name__, __version__, dataset, container,search
from polygon import rest_connect

# import dataset
# import container

app = typer.Typer()
app.add_typer(dataset.app, name="dataset")
app.add_typer(container.app, name="container")


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()

def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return


@app.command()
def list(
    description: List[str] = typer.Argument(...),
    priority: int = typer.Option(2, "--priority", "-p", min=1, max=3),
) -> None:
    """Add a new to-do with a DESCRIPTION."""
    typer.secho(
        f"""polygon-cli: list """
        f"""with priority: {priority}""",
        fg=typer.colors.GREEN,
    )


@app.command()
def search(phrase: str = typer.Option("--phrase",),)-> None:
    """Add a new to-do with a DESCRIPTION."""
    typer.secho(
        f"""polygon: search  results """
        f"""pass phrase to search""",
        fg=typer.colors.GREEN,
    )
    print(phrase)
    searchResult=rest_connect.search_details(phrase)
    print(searchResult)
# @app.command()
# def dataset(
#     description: List[str] = typer.Argument(...),
#     priority: int = typer.Option(2, "--priority", "-p", min=1, max=3),
# ) -> None:
#     """Add a new to-do with a DESCRIPTION."""
#     typer.secho(
#         f"""polygon-cli: list """
#         f"""with priority: {priority}""",
#         fg=typer.colors.GREEN,
#     )



# @app.command()
# def container(
#     description: List[str] = typer.Argument(...),
#     priority: int = typer.Option(2, "--priority", "-p", min=1, max=3),
# ) -> None:
#     """Add a new to-do with a DESCRIPTION."""
#     typer.secho(
#         f"""polygon-cli: list """
#         f"""with priority: {priority}""",
#         fg=typer.colors.GREEN,
#     )

