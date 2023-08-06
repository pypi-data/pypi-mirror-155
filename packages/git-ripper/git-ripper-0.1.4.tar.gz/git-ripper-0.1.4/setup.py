# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['git_ripper', 'git_ripper.utils']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.5,<0.5.0', 'httpx>=0.23.0,<0.24.0']

entry_points = \
{'console_scripts': ['git-ripper = git_ripper.cli:main']}

setup_kwargs = {
    'name': 'git-ripper',
    'version': '0.1.4',
    'description': 'Downloads git repo(s) from the web.',
    'long_description': "# Git Ripper ⚰️\n\n![image](https://user-images.githubusercontent.com/12753171/174469279-fee0d9d5-7990-4237-8692-d7d5b7be86e5.png)\n\nDownloads git repo(s) from the web.\n\nFrom Russia with hate, szuki! Developed by secret KGB konstruktor buyro by red soviet communits hackers. Enjoy before you die in nuclear war...\n\nFeatures:\n\n- Asynchronous and fast.\n- Mass git downloading.\n- Unix-friendly for geeks.\n- Colored output for gay people and transformers.\n- Powered by Putin's 🇷🇺 dark energy.\n- Use Python programming language instead peaces of shit like Go or Rust. You can easily customize it!\n\n```bash\n# install\n$ pipx install git-ripper\n\n# download git repo from ukrainian neonazis website\n$ git-ripper https://svoboda.org.ua\n\n# so...\n$ git-ripper < urls.txt\n$ command | git-ripper\n\n# see help\n$ git-ripper -h\n```\n\n## FIXME\n\n`^C` x 2 to stop execution.\n",
    'author': 'tz4678',
    'author_email': 'tz4678@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tz4678/git-ripper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
