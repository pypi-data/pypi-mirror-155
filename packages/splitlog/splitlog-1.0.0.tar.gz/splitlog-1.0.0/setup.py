# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['splitlog']

package_data = \
{'': ['*']}

install_requires = \
['importlib-metadata>=4.8,<5.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'pytz>=2022.1,<2023.0']

entry_points = \
{'console_scripts': ['splitlog = splitlog.__main__:main']}

setup_kwargs = {
    'name': 'splitlog',
    'version': '1.0.0',
    'description': 'Utility to split aggregated logs from Apache Hadoop Yarn applications into a folder hierarchy',
    'long_description': "splitlog\n========\n \nHadoop Yarn application logs aggregate all container logs of a Yarn application into a single file. This makes it very\ndifficult to use Unix command line tools to analyze these logs: Grep will search over all containers and context\nprovided for hits often does not include Yarn container name or host name. `splitlog` splits a combined logfile for all\ncontainers of an application into a file system hierarchy suitable for further analysis:\n\n```\noutputfolder\n|--. hadoopnode1\n|  |--. container_a_b\n|  |  |--> stderr.log\n|  |  '--> stdout.log\n|  |  \n|  '--. container_x_y\n|     |--> stderr.log\n|     '--> stdout.log\n|\n'--. hadoopnode2\n   `--. container_p_q\n      |--> stderr.log\n      `--> stdout.log\n```\n \nInstallation\n------------\nPython 3.6+ must be available.\n\n1. Create a a new venv using `python -m venv .venv`\n2. Activate venv using `. .venv/bin/activate`\n3. Run `python -m pip install -e splitlog`\n \nHow to use\n----------\n\nRead logs from standard input:\n```shell script\nyarn logs -applicationId application_1582815261257_232080 | python -m splitlog application_1582815261257_232080\n```\n\nRead logs from file `application_1582815261257_232080.log`:\n```shell script\npython -m splitlog -i application_1582815261257_232080.log application_1582815261257_232080 \n```\n",
    'author': 'Sebastian Klemke',
    'author_email': 'pypi@nerdheim.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/splitlog/splitlog.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
