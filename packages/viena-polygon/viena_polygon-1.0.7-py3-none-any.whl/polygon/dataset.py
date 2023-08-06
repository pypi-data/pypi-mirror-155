"""This module provides the CLI."""
# cli-module/cli.py
import json
from typing import List, Optional
import typer
from polygon import rest_connect
app = typer.Typer()


@app.command()
def list():
    typer.echo(f"list")
    #call the endpoint to get list of datasets in account
    #rest-connect with the json
    datasetList=rest_connect.dataset_list()
    print(json.dumps(datasetList, indent=3))

@app.command()
def create(name:str = typer.Option("None","--name","--n"),
    classname: Optional[List[str]] = typer.Option("","--classname",),
    clodustoragename: str = typer.Option("None","--clodustoragename","--n"),
) -> None:
    classes=[]
    for id in classname:
        classes.append(id)
    createDataset = rest_connect.createDataset(name, classname, clodustoragename)
    print(createDataset)

#list_datasetname_or_id
@app.command()
def merge(name:str = typer.Option("None","--name","--n"),
    datasetid: Optional[List[str]] = typer.Option("","--datasetid",),
    datasetname: Optional[List[str]] = typer.Option("","--datasetname",),
) -> None:
    typer.secho(
        f"""polygon: dataset merge """
        f"""pass in a list of datasetnames or dataset ids""",
        fg=typer.colors.GREEN,
    )
    dataset_id_list=[]
    dataset_name_list=[]
    for id in datasetname:
        dataset_name_list.append(id)
    for id in datasetid:
        dataset_id_list.append(id)
    datasetDetails = rest_connect.dataset_merge(dataset_id_list,dataset_name_list, name)
    print(datasetDetails)
    #get the list - the options can be -ids or -names
    # if -ids the list has datasetids -names then the list has datasetnames
    # based on the options get the list and use them to merge the dataset
    #create proper json and call the endpoint to merge dataset


@app.command()
def delete(name: str = typer.Option("None","--name"),id: str = typer.Option("None","--id",),)-> None:
    """Add a new to-do with a DESCRIPTION."""
    typer.secho(
        f"""polygon: dataset delete """
        f"""pass datasetname or dataset id""",
        fg=typer.colors.GREEN,
    )
    deletestatus = rest_connect.dataset_delete(name, id)
    print(deletestatus)
    # the options can be -id or -name
    # based on the options take the input and
    #create proper json and call the endpoint to merge dataset

@app.command()
def details(name: str = typer.Option("None","--name"),id: str = typer.Option("None","--id",),)-> None:
    """Add a new to-do with a DESCRIPTION."""
    typer.secho(
        f"""polygon: dataset details """
        f"""pass datasetname or dataset id""",
        fg=typer.colors.GREEN,
    )
    datasetDetails=rest_connect.dataset_details(name,id)
    print(json.dumps(datasetDetails, indent=3))

    # the options can be -id or -name
    # based on the options take the input and
    #create proper json and call the endpoint to merge dataset





if __name__ == "__main__":
    app()



# list_datasetname_or_id: List[str] = typer.Argument(...),
# priority: int = typer.Option(2, "--priority", "-p", min=1, max=3),
