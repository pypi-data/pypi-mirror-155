# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_dynamic_shields',
 'django_dynamic_shields.data',
 'django_dynamic_shields.models',
 'django_dynamic_shields.views']

package_data = \
{'': ['*']}

install_requires = \
['Django>=4.0.5,<5.0.0', 'typing-extensions>=4.2.0,<5.0.0']

setup_kwargs = {
    'name': 'django-dynamic-shields',
    'version': '0.2.0',
    'description': '',
    'long_description': '# django-dynamic-shields\n\n[![release](https://github.com/Uno-Takashi/django-dynamic-shields/actions/workflows/release.yml/badge.svg?branch=main)](https://github.com/Uno-Takashi/django-dynamic-shields/actions/workflows/release.yml)\n[![CodeQL](https://github.com/Uno-Takashi/django-dynamic-shields/actions/workflows/codeql-analysis.yml/badge.svg?branch=main&event=push)](https://github.com/Uno-Takashi/django-dynamic-shields/actions/workflows/codeql-analysis.yml)\n[![bandit](https://github.com/Uno-Takashi/django-dynamic-shields/actions/workflows/bandit.yml/badge.svg?branch=main&event=push)](https://github.com/Uno-Takashi/django-dynamic-shields/actions/workflows/bandit.yml)\n[![pyt](https://github.com/Uno-Takashi/django-dynamic-shields/actions/workflows/pyt.yml/badge.svg?branch=main&event=push)](https://github.com/Uno-Takashi/django-dynamic-shields/actions/workflows/pyt.yml)\n[![lizard](https://github.com/Uno-Takashi/django-dynamic-shields/actions/workflows/lizard.yml/badge.svg?branch=main&event=push)](https://github.com/Uno-Takashi/django-dynamic-shields/actions/workflows/lizard.yml)\n[![pyre](https://github.com/Uno-Takashi/django-dynamic-shields/actions/workflows/pyre.yml/badge.svg?branch=main&event=push)](https://github.com/Uno-Takashi/django-dynamic-shields/actions/workflows/pyre.yml)\n\n![GitHub contributors](https://img.shields.io/github/contributors/Uno-Takashi/django-dynamic-shields?color=g)\n![GitHub all releases](https://img.shields.io/github/downloads/Uno-Takashi/django-dynamic-shields/total)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/Uno-Takashi/django-dynamic-shields/blob/main/LICENSE)\n[![Python](https://img.shields.io/badge/-Python-F9DC3E.svg?logo=python&style=flat)](https://www.python.org/)\n[![Django](https://img.shields.io/badge/-Django-092E20.svg?logo=django&style=flat)](https://www.djangoproject.com/)\n\n## 📚 Overview\n\n## ⚒️ Develop\n\n## 📝 License\n\n- [MIT License](https://github.com/Uno-Takashi/django-dynamic-shields/blob/main/LICENSE)\n\n![GitHub watchers](https://img.shields.io/github/watchers/Uno-Takashi/django-dynamic-shields?style=social)\n![GitHub Repo stars](https://img.shields.io/github/stars/Uno-Takashi/django-dynamic-shields?style=social)\n![GitHub forks](https://img.shields.io/github/forks/Uno-Takashi/django-dynamic-shields?style=social)\n',
    'author': 'Takashi Uno',
    'author_email': 'euno.eng@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
