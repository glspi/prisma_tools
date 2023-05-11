"""prisma_tools.utils"""

import sys
from enum import Enum

import ruamel.yaml.scanner
from ruamel.yaml import YAML

from prisma_tools.PrismaSASECloudManaged_Python.access import prismaAccess
from prisma_tools.PrismaSASECloudManaged_Python.auth import saseAuthentication

# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
#     class prismaAccess: pass


DIFF_API_CALLS = {
    "gp_app": "paGPAppListApps",
    "sec_rule": "paSecrulesListRules",
    "url_profile": "paUrlProfileListProfiles",
}


class DiffType(str, Enum):
    gp_app = "gp_app"
    sec_rule = "sec_rule"
    url_profile = "url_profile"


def login(tsg_id: str, client_id: str, client_secret: str) -> prismaAccess.prismaAccess:
    """
    Log into Prisma Access

    Args:
        tsg_id: tenant service group id
        client_id: client_id
        client_secret: client_secret

    """
    # Login to Prisma using 'sdk' and get existing objects
    print("Logging into Prisma..")
    prisma = saseAuthentication.saseAuthentication()
    prisma.prismaAccessAuth(tsg_id, client_id, client_secret)
    prisma_api = prismaAccess.prismaAccess(prisma.saseToken)
    if not prisma_api.saseToken.get("bearerToken"):
        print("Error logging into Prisma, bad credentials.")
        sys.exit()
    print("Successfully logged into Prisma\n")

    return prisma_api


def load_yaml(filename: str) -> dict:
    """
    Load YAML

    Args:
        filename: name of YAML file

    """
    yaml = YAML(typ="safe")

    try:
        with open(filename) as fin:
            yml = yaml.load(fin)
    except FileNotFoundError:
        print(f"File {filename} was not found, try again!")
        sys.exit()
    except ruamel.yaml.scanner.ScannerError as e:
        print(f"\n\nError: {e}")
        print(f"\nFile {filename} has invalid syntax, please correct and try again")
        print("Error message is above.\n")
        sys.exit()

    return yml
