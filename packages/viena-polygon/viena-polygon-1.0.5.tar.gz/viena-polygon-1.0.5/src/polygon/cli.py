"""This module provides the CLI."""
# cli-module/cli.py
import json
from pathlib import Path
from typing import List, Optional

import sqlparse
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
def search(phrase: str = typer.Option("None","--phrase",),
           sql: str = typer.Option("None","--sql",),)-> None:
    """Add a new to-do with a DESCRIPTION."""
    typer.secho(
        f"""polygon: search  results """
        f"""pass phrase to search""",
        fg=typer.colors.GREEN,
    )
    if(phrase !="None"):
        searchResult=rest_connect.search_details(phrase)
        print(searchResult)
    else:
        parsedSql=pharsesql(sql)
        searchResult = rest_connect.search_details(phrase,parsedSql)
        print(searchResult)

def pharsesql(sql):
    statements = sqlparse.split(sql)
    #print(statements)
    # statements
    # ['select * from foo;', 'select * from bar;']

    # Format the first statement and print it out:
    first = statements[0]
    #print(sqlparse.format(first, reindent=True, keyword_case='upper'))
    # SELECT *
    # FROM foo;

    # Parsing a SQL statement:
    parsed = sqlparse.parse(first)[0]
    #print(parsed.tokens)
    counter = 0
    for tok in parsed.tokens:
        counter = counter + 1
        #print("counter=" + str(counter))
        # print("token="+str(tok))
        IN_WHERE = False
        input_dict = {}
        if tok.is_group:
            for sub_tok in tok.tokens:
                # print("sub_token=" + str(sub_tok))
                if sub_tok.normalized == 'WHERE':
                    IN_WHERE = True
                if IN_WHERE and sub_tok.is_group:
                    # handle where clause
                    #print("sub_token||" + str(sub_tok))
                    #print("sub_token||" + str(sub_tok.value.replace('=', ':')))
                    # strip quotes out
                    input_dict[sub_tok.left.value] = sub_tok.right.value
                    for sub_sub_tok in sub_tok.tokens:
                        k=0
                        #print("sub_sub_tok=" + str(sub_sub_tok))
                        # pass

    input_json_data = json.dumps(input_dict)
    return input_json_data
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

