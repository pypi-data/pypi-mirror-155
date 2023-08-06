# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['notia', 'notia.errors', 'notia.models']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.0,<4.0.0',
 'click>=8.0.3,<9.0.0',
 'ipywidgets>=7.7.0,<8.0.0',
 'pandas>=1.3,<2.0',
 'pydantic>=1.9.0,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich>=12.2.0,<13.0.0']

setup_kwargs = {
    'name': 'notia',
    'version': '0.6.0',
    'description': 'A library for interacting with the Notia.ai platform',
    'long_description': '<div align="center">\n<img src="https://raw.githubusercontent.com/notia-ai/client/master/resources/imgs/notia-gh-logo.png" width=60%/><br/>  \n</div>\n<p align="center">\n<a href="https://pypi.org/project/notia/">\n    <img alt="PyPi Release" src="https://img.shields.io/pypi/v/notia">\n</a> \n</p>\n\n\n---\n\nUse Notia to supercharge your models with the latest training data.\n\n-   Browse 100s of datasets from top companies and institutions.\n-   Directly integrates with Jupyter for easy sharing and distribution.\n-   Focus on the data science. Spend less time manually scraping and cleaning data.\n-   Reproduce any experiment without any Google Drive, Dropbox etc.\n\n## ⚡️ Quick Install\n\nTo install notia, simply:\n\n```bash\npip install notia\n```\n\n## Usage\n\n```python\nimport notia\nnotia.login()\n\nnotia.search("Yelp")\n\ntrain_df = notia.load_dataset("XXXXX", split="train")\n```\n\n## Contributing\n\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n',
    'author': 'Notia.ai',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://notia.ai',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
