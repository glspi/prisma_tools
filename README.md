Prisma Access Miscellaneous CLI Tools
========
Command line tool(s) to assist with Prisma Access. Currently there are 2 tools:

- Migrate objects from Palo XML to Prisma Access
- Compare two objects within Prisma Access via HTML diff output

#### Requirements
- Python 3.10+

For authentication into Prisma Access, you'll need your API credentials:
- Tenant Service Group ID (TSG ID)
- Client ID
- Client Secret

To obtain these credentials, follow the steps found [here.](https://docs.paloaltonetworks.com/common-services/identity-and-access-access-management/manage-identity-and-access/add-service-accounts)

## Installation
Optional but recommended:
- `python -m venv MYVENVNAME`
- `source MYVENVNAME/bin/activate`

Install:
- `pip install git+https://github.com/glspi/prisma_tools.git`

## Usage
The installation process will install an executable `ptools` on your path. Run `ptools --help` for help.
You can also get help for each individual command (migrate, diff) via `ptools COMMAND --help`

All tools require the API credentials, which can be passed in using the available flags (see --help), or can
be entered via prompts if not provided within the command itself.

If any option required by a command is not input via a cli flag, you will be prompted to provide it at runtime.

### Migrating objects to Prisma: (ptools migrate)
This will copy objects from a Palo XML config into Prisma Access. Use the sample file found [here](sample-copy-objects.yml) to choose
which objects you want to migrate from XML to Prisma.

Supported Object Types:
- address objects
- service objects
- address groups
- service groups
- tags

If you choose a group, all member objects will automatically be added to the migration list.
If an object has an existing tag, the tag will automatically be added to the migration list.

Before any new objects are created, you will be presented with the 'final' list of objects to create, 
and prompted to continue when ready.

`ptools migrate -o myobjects.yml -f palo-config.xml`

### Compare two objects within Prisma: (ptools diff)
Choose the object type you would like to compare, and then enter the names of the objects via prompts.

Supported Object Types:
- Global Protect App/config
- Security Rules
- URL Profiles
- *more can be added easily, just ask!*

`ptools diff -o <object_type>`
(see --help for exact object type names)

Output will be generated in an HTML file which you can load in any browser to view.
