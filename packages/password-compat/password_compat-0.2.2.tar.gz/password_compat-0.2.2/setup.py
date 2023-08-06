# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['password_compat']
install_requires = \
['bcrypt>=3.2.0,<4.0.0']

setup_kwargs = {
    'name': 'password-compat',
    'version': '0.2.2',
    'description': "PHP's password_compat like library for Python",
    'long_description': "# password_compat_python\n\nThis library provides something similar to PHP's [password_hash](https://www.php.net/manual/function.password-hash.php) and [password_verify](https://www.php.net/manual/function.password-verify.php) functions.\n\n# see also\n\nhttps://github.com/ircmaxell/password_compat\n\n# license\n\nMIT or Apache-2.0\n",
    'author': 'masinc',
    'author_email': 'masinc000@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/masinc/password_compat-python',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
