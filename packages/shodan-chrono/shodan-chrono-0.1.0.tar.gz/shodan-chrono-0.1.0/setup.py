# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chrono']

package_data = \
{'': ['*']}

install_requires = \
['construct>=2.10.68,<3.0.0', 'shodan>=1.27.0,<2.0.0']

setup_kwargs = {
    'name': 'shodan-chrono',
    'version': '0.1.0',
    'description': 'Create a progress bar that you can view on chrono.shodan.io',
    'long_description': '# Shodan Chrono: Python\n\n## Quickstart\n\nInstall the library using:\n\n```shell\npip install shodan-chrono\n```\n\nAnd then use it in your code:\n\n```python\nimport chrono\n\nitems = [i for i in range(100)]\nwith chrono.progress("My Script", len(items), api_key="YOUR SHODAN API KEY") as pb:\n    for item in items:\n        # Do something\n        # Update the progress bar after we\'ve processed the item\n        pb.update()\n```\n\nYou can also tell the progress bar to update by more than 1 tick:\n\n```python\n    pb.update(5)  # Tell Chrono that we\'ve processed 5 items\n```\n\n## Configuring the API key\n\nThe Chrono API requires a [Shodan API key](https://account.shodan.io) and there are 3 possible ways you can provide that:\n\n* Initialize the Shodan CLI on your local machine: ``shodan init YOUR_API_KEY``\n* Set the ``SHODAN_API_KEY``  environment variable. For example: ``export SHODAN_API_KEY="YOUR KEY"``\n* Use the ``api_key`` parameter on the ``chrono.progress()`` class\n\nIf you\'re already using the Shodan CLI for other things then you won\'t need to configure anything in order to use Chrono.\n\n## Contributing\n\nCheckout the repository and then use ``poetry`` to manage the dependencies, virtual environment and packaging. To get started, simply run the following command once you\'re in the ``python/`` subdirectory of this repository:\n\n```shell\npoetry install\n```\n',
    'author': 'John Matherly',
    'author_email': 'jmath@shodan.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://chrono.shodan.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
