# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kgcl_schema', 'kgcl_schema.datamodel']

package_data = \
{'': ['*'], 'kgcl_schema': ['schema/*']}

install_requires = \
['linkml-runtime>=1.1.24,<2.0.0']

setup_kwargs = {
    'name': 'kgcl-schema',
    'version': '0.1.0',
    'description': 'Schema fro the KGCL project.',
    'long_description': '# KGCL-schema\n\nThis is the schema to the KGCL project.\n\n## Documentation\n[Read more here.](https://incatools.github.io/kgcl/)\n\n',
    'author': 'Chris Mungall',
    'author_email': 'cjmungall@lbl.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
