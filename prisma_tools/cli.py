"""prisma_tools.cli"""
import typer

from prisma_tools import diff, migrate, utils
from prisma_tools.PrismaSASECloudManaged_Python.access import prismaAccess

app = typer.Typer(
    name="ptools",
    help="ptools: Prisma Access Tools",
)


typer_tsg_id = typer.Option(
    "", "-tsg", "--tsg-id", help="TSG ID (123456789)", prompt=True, metavar="TSG ID"
)
typer_client_id = typer.Option(
    "",
    "-c",
    "--client-id",
    help="Client ID (user@123456989.iam.panserviceaccount.com)",
    prompt=True,
    metavar="Client ID",
)
typer_client_secret = typer.Option(
    "",
    "-s",
    "--client-secret",
    help="Client Secret (xyzabce-ab12-12ce-1234-xyzabca123487)",
    prompt=True,
    metavar="Client Secret",
)


def login(tsg_id: str, client_id: str, client_secret: str) -> prismaAccess.prismaAccess:
    """
    Log into Prisma Access

    Args:
        tsg_id: tenant service group id
        client_id: client_id
        client_secret: client_secret

    """
    prisma_api = utils.login(
        tsg_id=tsg_id, client_id=client_id, client_secret=client_secret
    )
    return prisma_api


@app.command("migrate", help="Migrate objects from a Palo .xml File")
def _migrate(
    tsg_id: str = typer_tsg_id,
    client_id: str = typer_client_id,
    client_secret: str = typer_client_secret,
    filename: str = typer.Option(
        "",
        "-f",
        "--filename",
        help="XML Filename containing Palo Config",
        prompt=True,
        metavar="Palo XML File",
    ),
    objects: str = typer.Option(
        "",
        "-o",
        "--objects",
        help="YAML Filename containing objects to be migrated",
        prompt=True,
        metavar="YAML Objects File",
    ),
) -> None:
    """
    Copy objects from Palo .xml file up to Prisma Access

    Supports:
        Addresses, Address-Groups
        Services, Service-Groups

    Args:
        filename: Name of Palo .xml configuration file
        objects: Name of .yml file containing objects to be migrated
        tsg_id: tenant service group id
        client_id: client_id
        client_secret: client_secret

    """
    copy_objects = utils.load_yaml(objects)
    prisma_api = login(tsg_id=tsg_id, client_id=client_id, client_secret=client_secret)
    migrate.run(filename=filename, prisma_api=prisma_api, copy_objects=copy_objects)


@app.command("diff", help="Provide html diff of various Prisma objects")
def _diff(
    tsg_id: str = typer_tsg_id,
    client_id: str = typer_client_id,
    client_secret: str = typer_client_secret,
    object_type: utils.DiffType = typer.Option(
        "", "-o", "--object-type", case_sensitive=False, help="Object Type"
    ),
) -> None:
    """
    Compare two objects and provide html based diff output

    Args:
        object_type: Choice of supported object types
        tsg_id: tenant service group id
        client_id: client_id
        client_secret: client_secret

    """
    prisma_api = login(tsg_id=tsg_id, client_id=client_id, client_secret=client_secret)
    diff.run(prisma_api=prisma_api, object_type=object_type)
