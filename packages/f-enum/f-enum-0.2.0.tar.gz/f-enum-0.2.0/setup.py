# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastenum']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'f-enum',
    'version': '0.2.0',
    'description': 'Patch for builtin enum module to achieve best performance',
    'long_description': "# fastenum\n\n###### Based on [python/cpython#17669](https://github.com/python/cpython/pull/17669) and [python/cpython#16483](https://github.com/python/cpython/pull/16483)\n\nPatch for stdlib `enum` that makes it *fast*.\n\n## How fast?\n\n- ~10x faster `name`/`value` access\n- ~6x faster access to enum members\n- ~2x faster values positive check\n- ~3x faster values negative check\n- ~3x faster iteration\n- ~100x faster new `Flags` and `IntFlags` creation for Python 3.8 and below\n\n## Wow this is fast! How do I use it?\n\nFirst, install it from PyPi using pip\n\n```shell\npip install f-enum\n```\n\nor using poetry\n\n```shell\npoetry add f-enum\n```\n\nThen enable the patch just by calling `fastenum.enable()` once at the start of your programm:\n\n```python\nimport fastenum\n\nfastenum.enable()\n```\n\nYou don't need to re-apply patch across different modules: once it's enabled, it'll work everywhere.\n\n## What's changed?\n\nfastenum is designed to give effortless boost for all enums from stdlib. That means that none of optimizations should break existing code, thus requiring no changes other than installing and activating the library.\n\nHere are summary of internal changes:\n\n- Optimized `Enum.__new__`\n- Remove `EnumMeta.__getattr__`\n- Store `Enum.name` and `.value` in members `__dict__` for faster access\n- Replace `Enum._member_names_` with `._unique_member_map_` for faster lookups and iteration (old arg still remains)\n- Replace `_EmumMeta._member_names` and `._last_values` with `.members` mapping (old args still remain)\n- Add support for direct setting and getting class attrs on `DynamicClassAttribute` without need to use slow `__getattr__`\n- Various minor improvements\n",
    'author': 'Bobronium',
    'author_email': 'appkiller16@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.2',
}


setup(**setup_kwargs)
