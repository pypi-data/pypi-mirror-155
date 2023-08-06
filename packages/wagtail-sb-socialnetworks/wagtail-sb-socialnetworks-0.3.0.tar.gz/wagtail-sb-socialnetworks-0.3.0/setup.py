# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wagtail_sb_socialnetworks', 'wagtail_sb_socialnetworks.migrations']

package_data = \
{'': ['*'], 'wagtail_sb_socialnetworks': ['locale/es/LC_MESSAGES/*']}

install_requires = \
['Django<5.0', 'wagtail<4.0']

setup_kwargs = {
    'name': 'wagtail-sb-socialnetworks',
    'version': '0.3.0',
    'description': 'Social Networks settings for wagtail sites.',
    'long_description': '![Community project](https://raw.githubusercontent.com/softbutterfly/wagtail-sb-socialnetworks/master/resources/softbutterfly-open-source-community-project.png)\n\n![PyPI - Supported versions](https://img.shields.io/pypi/pyversions/wagtail-sb-socialnetworks)\n![PyPI - Package version](https://img.shields.io/pypi/v/wagtail-sb-socialnetworks)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/wagtail-sb-socialnetworks)\n![PyPI - MIT License](https://img.shields.io/pypi/l/wagtail-sb-socialnetworks)\n\n[![Build Status](https://www.travis-ci.org/softbutterfly/wagtail-sb-socialnetworks.svg?branch=develop)](https://www.travis-ci.org/softbutterfly/wagtail-sb-socialnetworks)\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/3d703e48c1e44e9b830da5026f07c52d)](https://www.codacy.com/gh/softbutterfly/wagtail-sb-socialnetworks/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=softbutterfly/wagtail-sb-socialnetworks&amp;utm_campaign=Badge_Grade)\n[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/3d703e48c1e44e9b830da5026f07c52d)](https://www.codacy.com/gh/softbutterfly/wagtail-sb-socialnetworks/dashboard?utm_source=github.com&utm_medium=referral&utm_content=softbutterfly/wagtail-sb-socialnetworks&utm_campaign=Badge_Coverage)\n[![codecov](https://codecov.io/gh/softbutterfly/wagtail-sb-socialnetworks/branch/master/graph/badge.svg?token=pbqXUUOu1F)](https://codecov.io/gh/softbutterfly/wagtail-sb-socialnetworks)\n[![Requirements Status](https://requires.io/github/softbutterfly/wagtail-sb-socialnetworks/requirements.svg?branch=master)](https://requires.io/github/softbutterfly/wagtail-sb-socialnetworks/requirements/?branch=master)\n\n# Wagtail Social Networks\n\nWagtail package to manage sites social network profiles.\n\n## Requirements\n\n- Python 3.8, 3.9, 3.10\n\n## Install\n\n```bash\npip install wagtail-sb-socialnetworks\n```\n\n## Usage\n\nAdd `wagtail.contrib.settings` and `wagtail_sb_socialnetworks` to your `INSTALLED_APPS` settings\n\n```\nINSTALLED_APPS = [\n  # ...\n  "wagtail.contrib.settings",\n  "wagtail_sb_socialnetworks",\n  # ...\n]\n```\n\n## Docs\n\n- [Ejemplos](https://github.com/softbutterfly/wagtail-sb-socialnetworks/wiki)\n- [Wiki](https://github.com/softbutterfly/wagtail-sb-socialnetworks/wiki)\n\n## Changelog\n\nAll changes to versions of this library are listed in the [change history](CHANGELOG.md).\n\n## Development\n\nCheck out our [contribution guide](CONTRIBUTING.md).\n\n## Contributors\n\nSee the list of contributors [here](https://github.com/softbutterfly/wagtail-sb-socialnetworks/graphs/contributors).\n',
    'author': 'SoftButterfly Development Team',
    'author_email': 'dev@softbutterfly.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/softbutterfly/wagtail-sb-socialnetworks',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0.0',
}


setup(**setup_kwargs)
