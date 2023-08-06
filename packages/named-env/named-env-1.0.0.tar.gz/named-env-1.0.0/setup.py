# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['named_env']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'named-env',
    'version': '1.0.0',
    'description': 'Class-based environment variables typed specification',
    'long_description': '# named-env\n\nClass-based environment variables typed specification.\n\n## Usage example\n\n```python\nfrom named_env import EnvironmentNamespace, RequiredInteger\nimport os\n\n\nclass WebApplicationEnvironmentNamespace(EnvironmentNamespace):\n    WEB_SERVER_PORT = RequiredInteger()\n\n\nenv = WebApplicationEnvironmentNamespace()\n\nif __name__ == "__main__":\n    os.environ["WEB_SERVER_PORT"] = "80"\n    print(env.WEB_SERVER_PORT)  # 80\n    print(type(env.WEB_SERVER_PORT))  # int\n```\n',
    'author': 'Artem Novikov',
    'author_email': 'artnew@list.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/reartnew/named-env',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
