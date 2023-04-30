"""prisma_tools.utils"""

import sys

from prisma_tools.PrismaSASECloudManaged_Python.access import prismaAccess
from prisma_tools.PrismaSASECloudManaged_Python.auth import saseAuthentication


def login(tsg_id: str, client_id: str, client_secret: str) -> prismaAccess:
    # Login to Prisma using 'sdk' and get existing objects
    print("Logging into Prisma..")
    prisma = saseAuthentication.saseAuthentication()
    prisma.prismaAccessAuth(tsg_id, client_id, client_secret)
    prisma_api = prismaAccess.prismaAccess(prisma.saseToken)
    if not prisma_api.saseToken.get("bearerToken"):
        print("Error logging into Prisma, bad credentials.")
        sys.exit()
    print("Successfully logged into Prisma")

    return prisma_api
