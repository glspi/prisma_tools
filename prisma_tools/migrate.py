"""prisma_tools.migrate"""
import sys
from typing import Any

from lxml import etree
from rich.pretty import pprint

from prisma_tools.PrismaSASECloudManaged_Python.access import (
    policyObjects,
    prismaAccess,
)

COPY_OBJECTS: dict = {}

COLOR_MAP = {
    "color1": "Red",
    "color2": "Green",
    "color3": "Blue",
    "color4": "Yellow",
    "color5": "Copper",
    "color6": "Orange",
    "color7": "Purple",
    "color8": "Gray",
    "color9": "Light Green",
    "color10": "Cyan",
    "color11": "Light Gray",
    "color12": "Blue Gray",
    "color13": "Lime",
    "color14": "Black",
    "color15": "Gold",
    "color16": "Brown",
    "color17": "Olive",
    "color19": "Maroon",
    "color20": "Red-Orange",
    "color21": "Yellow-Orange",
    "color22": "Forest Green",
    "color23": "Turquoise Blue",
    "color24": "Azure Blue",
    "color25": "Cerulean Blue",
    "color26": "Midnight Blue",
    "color27": "Medium Blue",
    "color28": "Cobalt Blue",
    "color29": "Violet Blue",
    "color30": "Blue Violet",
    "color31": "Medium Violet",
    "color32": "Medium Rose",
    "color33": "Lavender",
    "color34": "Orchid",
    "color35": "Thistle",
    "color36": "Peach",
    "color37": "Salmon",
    "color38": "Magenta",
    "color39": "Red Violet",
    "color40": "Mahogany",
    "color41": "Burnt Sienna",
    "color42": "Chestnut",
    "None": "None",
}


def get_tags_from_xml(tags):
    """Pull tags from XML"""
    my_tags = {}
    for tag in tags:
        name = tag.attrib["name"]
        color = tag.find("color")
        if name not in my_tags.keys():
            if color is None:
                my_tags[name] = {}
            else:
                my_tags[name] = {"color": COLOR_MAP[color.text]}
    return my_tags


def get_addresses_from_xml(addresses):
    """Pull address from XML"""

    my_addresses = {}
    for address in addresses:
        name = address.attrib["name"]
        my_addresses[name] = {}
        for tag in address:
            if tag.tag == "tag":
                my_addresses[name]["tag"] = []
                for member in tag:
                    my_addresses[name]["tag"].append(member.text)
            else:
                my_addresses[name][tag.tag.replace("-", "_")] = tag.text

    return my_addresses


def get_services_from_xml(services):
    """Pull service from XML"""

    my_services = {}
    for service in services:
        name = service.attrib["name"]
        my_services[name] = {}
        for xmltag in service:
            if xmltag.tag == "tag":
                my_services[name]["tag"] = []
                for member in xmltag:
                    my_services[name]["tag"].append(member.text)
            else:
                for protocol in xmltag.getchildren():
                    my_services[name]["protocol"] = {protocol.tag: {}}
                    for srcdst_port in protocol.getchildren():
                        if srcdst_port.tag == "override":
                            continue
                        #  NOT NEEDED FOR CURRENT PA, UPDATE THOUGH!
                        #     breakpoint()
                        #     override = srcdst_port.getchildren()[0].tag
                        #     timout = srcdst_port.find("override").find("timeout").text
                        #     my_services[protocol.tag]["override"] = {"timeout": timeout}
                        else:
                            my_services[name]["protocol"][protocol.tag][
                                srcdst_port.tag.replace("-", "_")
                            ] = srcdst_port.text

    return my_services


def get_addr_groups_from_xml(address_groups):
    """Pull address group from XML"""

    my_addr_groups = {}
    for group in address_groups:
        name = group.attrib["name"]
        my_addr_groups[name] = {}
        for xmltag in group:
            if xmltag.tag == "tag":
                my_addr_groups[name]["tag"] = []
                for member in xmltag:
                    my_addr_groups[name]["tag"].append(member.text)
            else:
                if xmltag.tag == "dynamic":
                    print(
                        f"Dynamic group type (group: {name}) is currently unsupported."
                    )
                    sys.exit()
                my_addr_groups[name]["static"] = []
                for member in xmltag.getchildren():
                    my_addr_groups[name]["static"].append(member.text)

                # my_addr_groups[name][tag.tag.replace("-","_")] = xmltag.text

    return my_addr_groups


def get_svc_groups_from_xml(
    service_groups: list[etree.ElementTree],
) -> dict[str, str | list[str]]:
    """Pull service group from XML"""

    my_svc_groups: dict = {}

    for group in service_groups:
        name = group.attrib["name"]
        my_svc_groups[name] = {}
        for xmltag in group:
            if xmltag.tag == "tag":
                my_svc_groups[name]["tag"] = []
                for member in xmltag:
                    my_svc_groups[name]["tag"].append(member.text)
            else:
                my_svc_groups[name]["members"] = []
                members = xmltag.getchildren()
                for member in members:
                    my_svc_groups[name]["members"].append(member.text)

    return my_svc_groups


def get_objs_from_xml(
    obj: str, config: etree.ElementTree
) -> dict[str, dict[str, str | list[str]]]:
    """
    Get objects from XML

    Args:
        obj: object type
        config: XML config as etree

    """
    my_args = {}
    my_func = None
    if obj == "tags":
        object_xpath = (
            "./devices/entry[@name='localhost.localdomain']"
            "/vsys/entry[@name='vsys1']/tag/entry"
        )
        objs = config.xpath(object_xpath)
        my_func = get_tags_from_xml
        my_args["tags"] = objs
    elif obj == "addresses":
        object_xpath = (
            "./devices/entry[@name='localhost.localdomain']"
            "/vsys/entry[@name='vsys1']/address/entry"
        )
        objs = config.xpath(object_xpath)
        my_func = get_addresses_from_xml
        my_args["addresses"] = objs
    elif obj == "services":
        object_xpath = (
            "./devices/entry[@name='localhost.localdomain']"
            "/vsys/entry[@name='vsys1']/service/entry"
        )
        objs = config.xpath(object_xpath)
        my_func = get_services_from_xml
        my_args["services"] = objs
    elif obj == "address_groups":
        object_xpath = (
            "./devices/entry[@name='localhost.localdomain']"
            "/vsys/entry[@name='vsys1']/address-group/entry"
        )
        objs = config.xpath(object_xpath)
        my_func = get_addr_groups_from_xml
        my_args["address_groups"] = objs
    elif obj == "service_groups":
        object_xpath = (
            "./devices/entry[@name='localhost.localdomain']"
            "/vsys/entry[@name='vsys1']/service-group/entry"
        )
        objs = config.xpath(object_xpath)
        my_func = get_svc_groups_from_xml
        my_args["service_groups"] = objs
    if not my_func:
        print(f"Unsupported object type '{obj}'.")
        sys.exit()
    objs = my_func(**my_args)
    return objs


def load_objects(filename: str) -> dict[str, dict[str, str | list[str]]]:
    """
    Pull objects from Palo XML file

    Args:
        filename: Name of XML file

    """
    try:
        with open(filename) as fin:
            configstr = fin.read()
    except FileNotFoundError:
        print(f"File: {filename} not found!")
        sys.exit()
    try:
        config = etree.fromstring(configstr)
    except etree.XMLSyntaxError as exc:
        print(exc)
        print("\nInvalid XML File...try again! Our best guess is up there ^^^\n")
        sys.exit()

    my_dict: dict = {
        "tags": {},
        "addresses": {},
        "services": {},
        "address_groups": {},
        "service_groups": {},
    }
    for obj in my_dict.keys():
        my_dict[obj] = get_objs_from_xml(obj, config)

    return my_dict


def create_tag(name, value, prisma_sdk):
    """Create Tag"""

    if value.get("color"):
        tag = {"name": name, "color": value["color"]}
    else:
        tag = {"name": name}

    _ = prisma_sdk.paTagCreate(tag)


def create_addresses(name, value, prisma_sdk):
    """Create Address"""

    address = {"name": name}
    address.update(value)

    _ = prisma_sdk.paAddressesCreate(address)


def create_services(name, value, prisma_sdk):
    """Create Service"""

    service = {"name": name}
    service.update(value)

    _ = prisma_sdk.paServicesCreateService(service)


def create_addr_groups(name, value, prisma_sdk):
    """Create Address Group"""

    group = {"name": name}
    group.update(value)

    _ = prisma_sdk.paAddressGroupsCreate(group)


def create_svc_groups(name, value, prisma_sdk):
    """Create Service Croup"""

    group = {"name": name}
    group.update(value)

    _ = prisma_sdk.paServiceGroupsCreate(group)


def check_for_tags(
    xml_objs: dict[str, dict[str, Any]], existing_tag_names: list[str]
) -> None:
    """
    Check the objects for other tags, which will need to be migrated

    Args:
        xml_objs: object data obtained from XML
        existing_tag_names: list of existing tags

    """
    for _type, objects in COPY_OBJECTS.copy().items():
        if _type == "tags":
            continue
        if not objects:
            continue
        for obj_name in objects.copy():
            try:
                if "tag" in xml_objs[_type][obj_name].keys():
                    tags = xml_objs[_type][obj_name]["tag"]
                    for tag in tags:
                        if (
                            tag not in existing_tag_names
                            and tag not in COPY_OBJECTS["tags"]
                        ):
                            COPY_OBJECTS["tags"].append(tag)
            except KeyError:
                print(f"Warning: {obj_name} not found! Skipping..")
                COPY_OBJECTS[_type].remove(obj_name)
                continue


def check_addr_groups(
    objects: list[str],
    xml_objs: dict[str, dict[str, Any]],
    existing_addr_group_names: list[str],
) -> bool:
    """Check Address Groups"""

    repeat = False
    for obj_name in objects:
        for member in xml_objs["address_groups"][obj_name]["static"]:
            if (
                member in COPY_OBJECTS["addresses"]
                or member in COPY_OBJECTS["address_groups"]
                or member in existing_addr_group_names
            ):
                continue
            if member in xml_objs["addresses"]:
                COPY_OBJECTS["addresses"].append(member)
            elif member in xml_objs["address_groups"]:
                COPY_OBJECTS["address_groups"].append(member)
                repeat = True
    return repeat


def check_svc_groups(
    objects: list[str],
    xml_objs: dict[str, dict[str, Any]],
    existing_svc_group_names: list[str],
) -> bool:
    """Check Service Groups"""

    repeat = False
    for obj_name in objects:
        for member in xml_objs["service_groups"][obj_name]["members"]:
            if (
                member in COPY_OBJECTS["services"]
                or member in COPY_OBJECTS["service_groups"]
                or member in existing_svc_group_names
            ):
                continue
            if member in xml_objs["services"]:
                COPY_OBJECTS["services"].append(member)
            elif member in xml_objs["service_groups"]:
                COPY_OBJECTS["service_groups"].append(member)
                repeat = True
    return repeat


def check_groups(
    xml_objs: dict[str, dict[str, Any]],
    existing_addr_group_names: list[str],
    existing_svc_group_names: list[str],
) -> None:
    """
    Check the groups for other members/groups that indirectly also need to be migrated

    Calls specific addr group/svc group function as needed

    Args:
        xml_objs: object data obtained from XML
        existing_addr_group_names: Address groups already in Prisma Access
        existing_svc_group_names: Service groups already in Prisma Access

    """
    for _type, objects in COPY_OBJECTS.copy().items():
        if _type in ("tags", "addresses", "services"):
            continue
        if not objects:
            continue
        if _type == "address_groups":
            repeat = True
            while repeat:
                repeat = check_addr_groups(
                    objects.copy(), xml_objs, existing_addr_group_names
                )
        if _type == "service_groups":
            repeat = True
            while repeat:
                repeat = check_svc_groups(
                    objects.copy(), xml_objs, existing_svc_group_names
                )


def get_prisma_objects(prisma_sdk: policyObjects.policyObjects) -> dict:
    """
    Get objects from Prisma Access

    Args:
        prisma_sdk: prismaAccess API policyObjects (containing actual api calls)

    """
    existing_tag_names = [tag["name"] for tag in prisma_sdk.paTagsListTags()]
    existing_address_names = [
        address["name"] for address in prisma_sdk.paAddressesListAddresses()
    ]
    existing_addr_group_names = [
        group["name"] for group in prisma_sdk.paAddressGroupsListAddressGroups()
    ]
    existing_service_names = [
        service["name"] for service in prisma_sdk.paServicesListServices()
    ]
    existing_svc_group_names = [
        group["name"] for group in prisma_sdk.paServiceGroupsListServiceGroups()
    ]

    obj_names = {
        "tags": existing_tag_names,
        "addresses": existing_address_names,
        "address_groups": existing_addr_group_names,
        "services": existing_service_names,
        "service_groups": existing_svc_group_names,
    }

    return obj_names


def create_prisma_objects(
    xml_objs: dict[str, dict[str, Any]],
    existing_obj_names: dict[str, list[str]],
    prisma_sdk: policyObjects.policyObjects,
) -> None:
    """
    Create objects in Prisma Access

    Args:
        xml_objs: object data obtained from XML
        existing_obj_names: object names already in Prisma Access
        prisma_sdk: prismaAccess API policyObjects (containing actual api calls)

    """
    for _type, obj_names in COPY_OBJECTS.items():
        if _type == "tags":
            create = create_tag
        elif _type == "addresses":
            create = create_addresses
        elif _type == "address_groups":
            create = create_addr_groups
        elif _type == "services":
            create = create_services
        elif _type == "service_groups":
            create = create_svc_groups
        else:
            print(f"Unsupported object type '{_type}'.")
            sys.exit()

        for obj_name in obj_names:
            if obj_name in xml_objs[_type].keys():
                if obj_name not in existing_obj_names[_type]:
                    value = xml_objs[_type][obj_name]
                    create(obj_name, value, prisma_sdk)
                else:
                    print(f"{_type} {obj_name} already exists, not creating!")


def run(filename: str, prisma_api: prismaAccess.prismaAccess, copy_objects: dict):
    """
    Migration Entry Point

    Args:
        filename: XML Filename containing Palo configuration
        prisma_api: prismaAccess API Object
        copy_objects: dictionary of all objects to be migrated

    """
    prisma_sdk = policyObjects.policyObjects(prisma_api)
    global COPY_OBJECTS
    COPY_OBJECTS = copy_objects
    if not COPY_OBJECTS["tags"]:
        COPY_OBJECTS["tags"] = []

    # Get objects from XML, converted to dict
    xml_objs = load_objects(filename)
    print("Retrieved XML objects.")

    print("Getting all objects.")
    existing_obj_names = get_prisma_objects(prisma_sdk)
    print("Retrieved existing objects.\n")

    # Update COPY_OBJECTS groups to add members of the groups as well
    check_groups(
        xml_objs,
        existing_obj_names["address_groups"],
        existing_obj_names["service_groups"],
    )

    # Update tags to create them first if necessary
    check_for_tags(xml_objs, existing_obj_names["tags"])

    # Creating Objects
    print("\nCreating the below in Prisma Access (Shared):")
    pprint(COPY_OBJECTS)
    yesno = ""
    while yesno.lower() not in ("y", "n", "yes", "no"):
        yesno = input("Continue? (yes/no): ")
    if yesno in ("yes", "y"):
        create_prisma_objects(xml_objs, existing_obj_names, prisma_sdk)
    else:
        print("Exiting..\n")
