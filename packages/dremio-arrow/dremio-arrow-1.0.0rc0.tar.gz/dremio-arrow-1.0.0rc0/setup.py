# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dremioarrow', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.3,<=1.4', 'pyarrow>=7.0,<=8.0']

extras_require = \
{'dev': ['pre-commit>=2.17.0,<3.0.0',
         'bump2version>=1.0.1,<2.0.0',
         'tox>=3.20.1,<4.0.0',
         'virtualenv==20.13.2',
         'requests>=2.27.1,<3.0.0',
         'types-requests>=2.27.11,<3.0.0'],
 'doc': ['mkdocs>=1.2.3,<2.0.0',
         'mkdocs-material>=8.2.5,<9.0.0',
         'mkdocstrings>=0.18.0,<0.19.0',
         'mkdocs-include-markdown-plugin>=1.0.0,<2.0.0',
         'mkdocs-git-revision-date-localized-plugin>=1.0.0,<2.0.0',
         'mkdocs-autorefs>=0.4.1,<0.5.0'],
 'test': ['black>=22.3.0,<23.0.0',
          'isort>=5.10.1,<6.0.0',
          'flake8>=3.9,<4.0',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'mypy>=0.931,<0.932',
          'pytest>=7.0.1,<8.0.0',
          'pytest-cov>=3.0.0,<4.0.0'],
 'toy': ['ipython>=7.32,<8.0', 'jupyterlab>=3.3.1,<4.0.0']}

setup_kwargs = {
    'name': 'dremio-arrow',
    'version': '1.0.0rc0',
    'description': 'Dremio SQL Lakehouse Arrow Flight Client.',
    'long_description': '# Dremio SQL Lakehouse Arrow Flight Client\n\n\n[![python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-blue)](https://pypi.org/project/dremio-arrow/)\n\nArrow Flight is a high-speed, distributed protocol designed to handle big data, providing increase in throughput between client applications and Dremio.\nThis Dremio Arrow Flight Client is based on [python official examples](https://github.com/dremio-hub/arrow-flight-client-examples/tree/main/python).\n\n> Disclaimer: This project is not affliated to [dremio](dremio.com) in any way. It is a tool that I developed while at CIFOR-ICRAF and now we have decided to open source it for wider community use. While I may not have enough time to actively maintain it, the tool is stable enough to sustain future use cases. Besides, community contribution is warmly welcome in form of PRs and forks.\n\n\n* Documentation: <https://jaysnm.github.io/dremio-arrow/>\n* GitHub: <https://github.com/jaysnm/dremio-arrow>\n* PyPI: <https://pypi.org/project/dremio-arrow/>\n* Free software: Apache-2.0\n\n\n## Flight Basics\n\nThe Arrow Flight libraries provide a development framework for implementing a service that can send and receive data streams. A Flight server supports several basic kinds of requests:\n\n- **Handshake**: a simple request to determine whether the client is authorized and, in some cases, to establish an implementation-defined session token to use for future requests\n- **ListFlights**: return a list of available data streams\n- **GetSchema**: return the schema for a data stream\n- **GetFlightInfo**: return an “access plan” for a dataset of interest, possibly requiring consuming multiple data streams. This request can accept custom serialized commands containing, for example, your specific application parameters.\n- **DoGet**: send a data stream to a client\n- **DoPut**: receive a data stream from a client\n- **DoAction**: perform an implementation-specific action and return any results, i.e. a generalized function call\n- **ListActions**: return a list of available action types\n\n> More details can be found [here](https://arrow.apache.org/blog/2019/10/13/introducing-arrow-flight/)\n\n![Illustration](https://arrow.apache.org/img/20191014_flight_simple.png)\n\n\n## Installation\n\nPlease see installation notes [here](https://jaysnm.github.io/dremio-arrow/installation/)\n',
    'author': 'Jason Kinyua',
    'author_email': 'jaysnmury@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jaysnm/dremio-arrow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
