# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsonschema_default']

package_data = \
{'': ['*']}

install_requires = \
['xeger>=0.3.5,<0.4.0']

setup_kwargs = {
    'name': 'jsonschema-default',
    'version': '1.3.1',
    'description': 'Create default objects from a JSON schema',
    'long_description': '# jsonschema-instance\n\nA Python package that creates default objects from a JSON schema.\n\n## Note\nThis is not a validator. Inputs should be valid JSON schemas. For Python you can use the [jsonschema](https://github.com/Julian/jsonschema) package to validate schemas.\n\n## Installation\n```\npip install jsonschema-default\n```\n\n## Usage\n```python\nimport jsonschema_default\n\ndefault_obj = jsonschema_default.create_from("<schema>")\n```\n\n## Development\n- Install and configure [Poetry](https://python-poetry.org/)\n\n```bash\npip install --user poetry\n```\n\nSee [Installation](https://python-poetry.org/docs/#installation) for the official guide.\n\n- Install the dependencies using \n\n```bash\n# Configure poetry to create a local venv directory\npoetry config virtualenvs.in-project true\n\npoetry install\n```',
    'author': 'Martin Boos',
    'author_email': 'mboos@outlook.com',
    'maintainer': 'Martin Boos',
    'maintainer_email': 'mboos@outlook.com',
    'url': 'https://github.com/mnboos/jsonschema-default',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
