"""prisma_tools.clone"""
from prisma_tools.PrismaSASECloudManaged_Python.access import (
    policyObjects,
    prismaAccess,
)


def duplicate(app: dict, prisma_sdk: policyObjects.policyObjects):
    """Not currently implemented"""

    app["name"] = f"{app['name']}-cloned"
    app.pop("folder")

    # resp = prisma_sdk.paGPAppCreate(app)
    # API does NOT support the only items I wanted to duplicate (agent/app configs).
    # Follow release notes, someday will change?


def gp_agent(name: str, prisma_api: prismaAccess.prismaAccess):
    """Not currently implemented"""

    prisma_sdk = policyObjects.policyObjects(prisma_api)
    existing_gp_apps = prisma_sdk.paGPAppListApps()

    found = False
    for app in existing_gp_apps:
        if app["name"] == name:
            duplicate(app=app, prisma_sdk=prisma_sdk)
            found = True
    if not found:
        print(f"{name} not found!")
    else:
        print(f"GP App: {name} has been cloned.")
