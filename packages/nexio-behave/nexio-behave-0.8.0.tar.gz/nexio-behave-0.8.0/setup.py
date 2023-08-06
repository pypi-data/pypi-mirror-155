# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nexio_behave',
 'nexio_behave.models',
 'nexio_behave.steps',
 'nexio_behave.test_utils']

package_data = \
{'': ['*']}

install_requires = \
['ansicolor>=0.3.2,<0.4.0',
 'behave>=1.2.6,<2.0.0',
 'jsonpath>=0.82,<0.83',
 'loguru>=0.6.0,<0.7.0',
 'pydantic>=1.9.0,<2.0.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'nexio-behave',
    'version': '0.8.0',
    'description': 'The Nexio Behave',
    'long_description': '# nexio-behave\n\nThe Nexio Behave\n\nFeatures:\n\n- <!-- list of features -->\n\nTable of Contents:\n\n- [Installation](#installation)\n- [Guide](#guide)\n- [Development](#development)\n\n## Installation\n\nnexio-behave requires Python 3.9 or above.\n\n```bash\npip install nexio-behave\n# or\npoetry add nexio-behave\n```\n\n## Guide\n\n<!-- Subsections explaining how to use the package -->\n\n## Development\n\nTo develop nexio-behave, install dependencies and enable the pre-commit hook:\n\n```bash\npip install pre-commit poetry\npoetry install\npre-commit install -t pre-commit -t pre-push\n```\n\nTo run tests:\n\n```bash\npoetry run pytest\n```\n',
    'author': 'Hongli Zhang',
    'author_email': 'hzhang@narrativescience.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NarrativeScience/nexio-behave',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
