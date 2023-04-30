"""prisma_tools.cli"""
from __future__ import annotations
import typer

from prisma_tools import add_objects, clone, utils

app = typer.Typer(
    name="ptools",
    add_completion=False,
    help="ptools: Prisma Access Tools",
)

state = {"prisma_api": None}


@app.callback()
def login(
    tsg_id: str = typer.Option(
        "", "-tsg", "--tsg-id", help="TSG ID (123456789)", prompt=True
    ),
    client_id: str = typer.Option(
        "",
        "-c",
        "--client-id",
        help="client_id (user@123456989.iam.panserviceaccount.com)",
        prompt=True,
    ),
    client_secret: str = typer.Option(
        "",
        "-s",
        "--client-secret",
        help="client_secret (xyzabce-ab12-12ce-1234-xyzabca123487)",
        prompt=True,
    ),
) -> None:
    prisma_api = utils.login(
        tsg_id=tsg_id, client_id=client_id, client_secret=client_secret
    )
    state["prisma_api"] = prisma_api


@app.command("migrate", help="Migrate objects from a Palo .xml File")
def migrate(
    filename: str = typer.Option(
        ..., "-f", "--filename", help="XML Filename containing Palo Config", prompt=True
    ),
) -> None:
    """
    Copy objects from Palo .xml file up to Prisma Access
    Supports:
        Addresses, Address-Groups
        Services, Service-Groups

    Args:
        filename: Name of .xml file from Palo containing the objects
    """
    add_objects.main(filename=filename, prisma_api=state["prisma_api"])


@app.command("clone", help="Clone objects in Prisma Access. (GP App only currently)")
def _clone(
    app_name: str = typer.Option(
        ...,
        "-a",
        "--app-name",
        help="Name of existing Global Protect App Config",
        prompt=True,
    ),
) -> None:
    """
    Clone GlobalProtect App Config within Prisma
    Supports:
        GlobalProtect App Config

    Args:
        app_name: Name of existing Global Protect App Config
    """
    print("To be implemented soon.")
    clone.gp_agent(name=app_name, prisma_api=state["prisma_api"])
