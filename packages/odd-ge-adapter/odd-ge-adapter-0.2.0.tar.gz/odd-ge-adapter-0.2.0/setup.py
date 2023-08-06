# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['odd_ge_adapter',
 'odd_ge_adapter.adapters',
 'odd_ge_adapter.adapters.s3',
 'odd_ge_adapter.domain',
 'odd_ge_adapter.mappers',
 'odd_ge_adapter.storage']

package_data = \
{'': ['*']}

install_requires = \
['black>=22.3.0,<23.0.0',
 'boto3>=1.23.7,<2.0.0',
 'odd-collector-sdk>=0.2.3,<0.3.0',
 'odd-models==2.0.2',
 'oddrn-generator>=0.1.37,<0.2.0',
 'pytest>=7.1.2,<8.0.0',
 'requests>=2.24.0,<3.0.0',
 's3>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'odd-ge-adapter',
    'version': '0.2.0',
    'description': 'ODD adapter to Great Expectations',
    'long_description': '## ODD GreatExpectation adapter\n\nLibrary for GreatExpectation schema compatible json files for suites and validation, reads them from s3 storage and ingests to OpenDataDiscovery platform.\n\nSuites must include special metadata about folder with data which will be validated in the future.\nExample \n```json\n{\n  "expectation_suite_name": "notification",\n  ...\n  "meta": {\n    "batch_kwargs": {\n      ...\n      "odd_metadata": [\n        "s3://bucket/folder"\n      ]\n    }\n  }\n}\n```\n\nValidation results must include metadata about which file was validated.\nExample\n```json\n{\n  "meta": {\n    "batch_kwargs": {\n      ...\n      "odd_metadata": [\n        "s3://bucket/folder/file.csv"\n      ]\n    },\n    ...\n    "validation_time": "20220525T174015.717924Z"\n  },\n  "results": [...],\n  "success": true\n}\n```\n\n### Library usage\nInstall package\n```bash\npip install odd-ge-adapter\n```\n\nExample:\n```\nfrom odd_models.api_client import ODDApiClient\nfrom odd_ge_adapter.domain.plugin import S3StoragePlugin\nfrom odd_ge_adapter.adapters.s3.adapter import Adapter\n\nplatform = ODDApiClient(<PLATFORM_URL>)\n\n# aws credentials can be omitted and taken from the ENV variables \nconfig = S3StoragePlugin(\n    type="s3",\n    name="s3_storage",\n    bucket="",\n    results_key="",\n    suites_key="",\n    # aws_region="",\n    # aws_access_key_id="",\n    # aws_secret_access_key="",\n)\n\nadapter = Adapter(config)\nplatform.post_data_entity_list(data=adapter.get_data_entity_list())\n```\n\n\n### As collector usage\nIn progress...\n\n',
    'author': 'Open Data Discovery',
    'author_email': 'pypi@opendatadiscovery.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/opendatadiscovery/odd-ge-adapter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.8.12',
}


setup(**setup_kwargs)
