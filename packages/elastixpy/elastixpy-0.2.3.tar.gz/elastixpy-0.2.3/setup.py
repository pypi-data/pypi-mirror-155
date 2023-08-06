# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elastixpy']

package_data = \
{'': ['*']}

install_requires = \
['spython>=0.1.18,<0.3.0']

setup_kwargs = {
    'name': 'elastixpy',
    'version': '0.2.3',
    'description': 'Python wrapper for elastix',
    'long_description': '# elastixpy\n\nPython wrapper for elastix\n\n\n\n## Installation\n\n```bash\npip install elastixpy\n```\n\n## License\n\n[MIT](https://github.com/Svdvoort/elastixpy/blob/master/LICENSE)\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Svdvoort/elastixpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<3.11',
}


setup(**setup_kwargs)
