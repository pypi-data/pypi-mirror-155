# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['onekey_client', 'onekey_client.keys', 'onekey_client.queries']

package_data = \
{'': ['*']}

install_requires = \
['Authlib>=0.15.3,<0.16.0',
 'httpx==0.23.0',
 'importlib-resources>=5.1.2,<6.0.0',
 'pydantic==1.8.2']

setup_kwargs = {
    'name': 'onekey-client',
    'version': '2.0.1',
    'description': 'ONEKEY API client',
    'long_description': '# ONEKEY API Client\n\nThis is the official Python client for the\n[ONEKEY](https://www.onekey.com/) public API.\n\n# Usage\n\nFirst, you have to log in and select a tenant:\n\n```python\nfrom onekey_client import Client\n\nYOUR_API_URL = "https://demo.onekey.com/api"\n\nclient = Client(api_url=YOUR_API_URL)\n\nclient.login(EMAIL, PASSWORD)\ntenant = client.get_tenant("Environment name")\nclient.use_tenant(tenant)\n```\n\nAfter you logged in and selected the tenant, you can query the GraphQL API\n\n```python\nGET_ALL_FIRMWARES = """\nquery {\n  allFirmwares {\n    id\n    name\n  }\n}\n"""\nres = client.query(GET_ALL_FIRMWARES)\nprint(res)\n\nGET_PRODUCT_GROUPS = """\nquery {\n  allProductGroups {\n    id\n    name\n  }\n}\n"""\nres = client.query(GET_PRODUCT_GROUPS)\ndefault_product_group = next(pg for pg in res["allProductGroups"] if pg["name"] == "Default")\n```\n\nYou can upload firmwares:\n\n```python\nmetadata = FirmwareMetadata(\n    name="myFirmware",\n    vendor_name="myVendor",\n    product_name="myProduct",\n    product_group_id=default_product_group["id"],\n)\n\nfirmware_path = Path("/path/to/firmware.bin")\nres = client.upload_firmware(metadata, firmware_path, enable_monitoring=True)\nprint(res)\n```\n\n# Support\n\nYou can create a [new issue in this repo](https://github.com/onekey-sec/python-client/issues/new)\nor contact us at support@onekey.com.\n',
    'author': 'ONEKEY',
    'author_email': 'support@onekey.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.onekey.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
