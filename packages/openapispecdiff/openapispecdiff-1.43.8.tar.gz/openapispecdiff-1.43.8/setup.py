# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openapispecdiff']

package_data = \
{'': ['*']}

install_requires = \
['openapi-core==0.13.4',
 'openapi-schema-validator==0.1.1',
 'openapi-spec-validator==0.2.9',
 'openapispecdiff',
 'prance==0.21.8.0']

entry_points = \
{'console_scripts': ['openapidiff = openapispecdiff.OpenApiSpecDiff:main']}

setup_kwargs = {
    'name': 'openapispecdiff',
    'version': '1.43.8',
    'description': 'Difference between two OpenAPISpec files',
    'long_description': '# OpenAPISpecDiff\n\nOpenAPISpecDiff is a Python library for comparing two OpenAPI specs and identifying the difference between them. \n\nVisit https://www.cloudvector.com/api-shark-free-observability-security-monitoring-tool/#apishark\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.\n\n```bash\npip install openapispecdiff\n```\n\n## Usage\n\n```python openapispecdiff \n\n****************************************************************************************************\nCloudVector APIShark - OpenAPI spec diff checker plugin\n****************************************************************************************************\nEnter absolute path to Old API SPEC: ../input.json\nEnter absolute path to new API SPEC : ../input1.json \n```\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)',
    'long_description_content_type': 'text/markdown',
    'author': 'Bala',
    'author_email': 'balak@cloudvector.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
