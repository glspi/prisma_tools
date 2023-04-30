from prisma_tools import add_objects
from rich.pretty import pprint


filename = "./tests/pa-tests.xml"
xml_objs = add_objects.load_objects(filename)


def test_mvp_objs():
    mvp_objs = {
        "tags": {"tag1": {"color": "Orange"}, "tag-no-color": {}},
        "addresses": {
            "IPv4-Sinkhole": {"ip_netmask": "72.5.65.111/32"},
            "addr-fqdn1": {"fqdn": "test1.com", "tag": ["tag1"]},
            "addr-ipnetmask1": {"ip_netmask": "1.1.1.1/30", "tag": ["tag1"]},
        },
        "services": {
            "SMTP": {"protocol": {"tcp": {"port": "25"}}},
            "svc ports 1": {"protocol": {"tcp": {"port": "111"}}},
            "svc_2": {"protocol": {"tcp": {"port": "222"}}},
        },
        "address_groups": {
            "addr_grp_1": {"static": ["test1.COM", "addr 1", "addr 2", "addr 3"]},
            "addr_grp_2": {"static": ["addr-fqdn1"]},
        },
        "service_groups": {
            "svc_grp_1": {"members": ["svc ports 1"]},
            "svc_grp_2": {"members": ["svc_2", "svc ports 1"]},
        },
    }

    # pprint(xml_objs)
    assert mvp_objs == xml_objs


def test_copy_objs1():
    TEST_COPY_OBJECTS = {
        "tags": [],
        "addresses": ["addr-ipnetmask1"],
        "address_groups": ["addr_grp_2"],
        "services": [],
        "service_groups": [],
    }
    maybe_correct = {
        "tags": ["tag1"],
        "addresses": ["addr-ipnetmask1", "addr-fqdn1"],
        "address_groups": ["addr_grp_2"],
        "services": [],
        "service_groups": [],
    }

    add_objects.COPY_OBJECTS = TEST_COPY_OBJECTS
    add_objects.check_groups(xml_objs, [], [])
    add_objects.check_for_tags(xml_objs, [])
    # pprint(add_objects.COPY_OBJECTS)

    assert maybe_correct == add_objects.COPY_OBJECTS


if __name__ == "__main__":
    test_copy_objs()
