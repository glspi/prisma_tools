from prisma_tools import utils


def test_load_yaml():
    filename = "sample-copy-objects.yml"
    yaml = utils.load_yaml(filename)
    assert isinstance(yaml, dict)

