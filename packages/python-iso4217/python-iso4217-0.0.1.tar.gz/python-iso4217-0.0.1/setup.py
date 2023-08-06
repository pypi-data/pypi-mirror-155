# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iso4217']

package_data = \
{'': ['*'], 'iso4217': ['data/*']}

modules = \
['__init__']
install_requires = \
['ijson>=3.1.4,<4.0.0']

setup_kwargs = {
    'name': 'python-iso4217',
    'version': '0.0.1',
    'description': 'Lightweight ISO 4217 currency package',
    'long_description': '# `python-iso4217`: fast currency data package for Python\n\n---\n\nThis python package automatically updates its own\ncurrency data using github actions and immediately release\nnew version of package with updates. So it\'s super fast and at the same time always contains fresh data.\n\n## Installation\n\n### Pip\n\n```bash\npip install python-iso4217\n```\n\n### Poetry\n\n```bash\npoetry add python-iso4217\n```\n\n## Usage\n\n```python\nfrom iso4217 import find_currency, iter_currency\n\n# Filters that could be applied:\n#   * currency_name\n#   * alphabetical_code\n#   * entity\n#   * decimal_places\n#   * numeric_code\n#   * withdrawal_date\n# The filters correspond to attributes of `Currency` class\n\n# accept arbitrary filters as key/value pairs\ncurrency = find_currency(currency_name="usd")\n\n# if currency was not found, the lib will immediately raise CurrencyNotFoundError\ndefunct_currency = find_currency(currency_name="abc123")\n\n# You need generator to lazy iter currencies? Ok\n\nfor c in iter_currency():\n# do something\n```\n\n## Advanced\n\n\n### Work with pydantic\n\n```python\nimport inspect\n\nfrom iso4217 import Currency as _Currency, find_currency\nfrom pydantic import BaseModel, root_validator, StrictInt\n\n\nclass Currency(BaseModel, _Currency):\n    __root__: StrictInt\n\n    @root_validator(pre=False, skip_on_failure=True)\n    def humanize(cls, values):\n        currency_numeric_code: int = values.get("__root__")\n        # inspect.getfullargspec(_Currency.__init__) will contain `self`, so we cut it off\n        orig_currency_cls_dunder_init_arg_names = inspect.getfullargspec(_Currency.__init__).args[1:]\n        currency = find_currency(numeric_code=currency_numeric_code)\n        return {\n            k: getattr(currency, k, None)\n            for k in orig_currency_cls_dunder_init_arg_names\n        }\n```',
    'author': 'GLEF1X',
    'author_email': 'glebgar567@gmail.com',
    'maintainer': 'GLEF1X',
    'maintainer_email': 'glebgar567@gmail.com',
    'url': 'https://github.com/GLEF1X/python-iso4217',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
