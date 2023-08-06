# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['property_accessor']
setup_kwargs = {
    'name': 'property-accessor',
    'version': '0.1.0',
    'description': '',
    'long_description': '# property_accessor\nPython property accessor module util\n\n\n### Installation:\n```shell\n> poetry add property-accessor\n```\n\n### Usage\n\n```python\nfrom property_accessor import PropertyAccessor\nfrom dataclasses import dataclass, field\n\n\n@dataclass\nclass Category:\n    code: str\n\n@dataclass\nclass Product:\n\n    name: str\n    sku: str\n    price: float\n    categories: list[Category] = field(default=list)\n\n\naccessor = PropertyAccessor(None)\n\naccessor.set(\'sku\', \'t-shirt-01\')\naccessor.set(\'name\', \'t-shirt basic black\')\naccessor.set(\'price\', 39.9)\naccessor.set(\'categories[0].code\', \'t-shits\')\n\nprint(accessor.get(\'name\')) # t-shirt basic black\nprint(accessor.get(\'categories[0].code\')) # t-shirt\n\n\nprint(accessor.data) # AnonymousObject(sku=\'t-shirt-01\', name=\'t-shirt basic black\', price=39.9, categories=[AnonymousObject(code="t-shirts")])\nprint(accessor.data.cast(Product)) # Product(sku=\'t-shirt-01\', name=\'t-shirt basic black\', price=39.9, categories=[Category(code="t-shirts")])\n```',
    'author': 'Elielton Kremer',
    'author_email': 'elieltonkremer2392@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
