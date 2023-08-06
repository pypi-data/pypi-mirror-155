# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['envchain_shellenv']

package_data = \
{'': ['*'], 'envchain_shellenv': ['examples/*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'keyring[keyring]>=23.5.1,<24.0.0']

entry_points = \
{'console_scripts': ['eesh = envchain_shellenv.cli:main_sync',
                     'envchain-shellenv = envchain_shellenv.cli:main_sync']}

setup_kwargs = {
    'name': 'envchain-shellenv',
    'version': '1.0.0',
    'description': 'envchain shellenv - prints export statements for your secrets in the keychain',
    'long_description': '# envchain shellenv\n\n`envchain-shellenv` - prints export statements for your secrets in the keychain\n\nso that you can do `eval "$(envchain-shellenv)"`.\n\nUse with [`envchain`](https://github.com/sorah/envchain) for maximum convenience.\n\n- [envchain shellenv](#envchain-shellenv)\n  - [Quick Start](#quick-start)\n  - [Installation](#installation)\n    - [Prerequisites](#prerequisites)\n    - [pipx](#pipx)\n    - [pip](#pip)\n  - [Usage:](#usage)\n  - [Example](#example)\n    - [Example config file](#example-config-file)\n  - [Develop](#develop)\n\n## Quick Start\n```bash\n# install envchain first, and add your secrets to your keychain app via envchain\n# for macOS with Homebrew, run `brew install envchain\'.\n# see https://github.com/sorah/envchain for more details.\n\n# install envchain-shellenv\npipx install envchain-shellenv || pip install envchain-shellenv\n\n# creates an example config at ~/.config/envchain-shellenv/keychain.ini\nenvchain-shellenv --create-example-config\n# edit config file with your favorite editor\nvim ~/.config/envchain-shellenv/keychain.ini\n\n# export your envchain secrets in the current shell\neval "$(envchain-shellenv)"\n# optionally add this line to your shell startup file\n```\n\n## Installation\n\n### Prerequisites\n- Required:\n  - [`envchain`](https://github.com/sorah/envchain)\n- Optional:\n  - [`keyring`](https://github.com/jaraco/keyring)\n\n    `keyring` is installed by default if you install `envchain-shellenv` with pipx.\n\n    To use keyring when installing with `pip`, do `pip install \'envchain-shellenv[keyring]\'`.\n\n### pipx\n\nThis is the recommended installation method.\n\n```\n$ pipx install envchain-shellenv\n```\n\n### [pip](https://pypi.org/project/envchain-shellenv/)\n\n```\n$ pip install envchain-shellenv\n```\n\n## Usage:\n\n`envchain-shellenv` prints export statements for your secrets in the keychain,\n\nwhen you need your secrets in your shell env, just do `eval "$(envchain-shellenv)"`.\n\n```\n$ eesh -h # `eesh\' is just an alias for `envchain-shellenv\', you can use either.\n\nusage: envchain-shellenv [-h] [-c CONFIG] [--create-example-config] [-u {envchain,keyring}] [--version]\n\nenvchain shellenv - prints export statements for your secrets in the keychain\n\noptions:\n  -h, --help            show this help message and exit\n  -c CONFIG, --config CONFIG\n                        config file (default: /Users/tscp/.config/envchain-shellenv/keychain.ini)\n  --create-example-config\n                        create example config file (default: False)\n  -u {envchain,keyring}, --use {envchain,keyring}\n                        What to use to extract secrets (default: envchain)\n  --version, -V         show program\'s version number and exit\n\nCreated by Teddy Xinyuan Chen || Homepage: https://github.com/tddschn/envchain-shellenv\n```\n\n## Example\n\n### Example config file\n\n```yaml\ntest:\n  TEST: TEST_SEC\n  MULTILINE:\naws: # the envchain namespace\n  AWS_SECRET_KEY:\n  AWS_ROOT_PW: envchain-aws-root-pw\n  # sets AWS_ROOT_PW env var to envchain-aws-root-pw in the aws namespace of envchain\nno-item:\n  # this will be skipped\n\n```\n\n\n## Develop\n\n```\n$ git clone https://github.com/tddschn/envchain-shellenv.git\n$ cd envchain-shellenv\n$ poetry install\n```',
    'author': 'Xinyuan Chen',
    'author_email': '45612704+tddschn@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tddschn/envchain-shellenv',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
