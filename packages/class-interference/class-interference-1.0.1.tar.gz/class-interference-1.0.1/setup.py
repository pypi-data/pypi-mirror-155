# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['class_interference']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'class-interference',
    'version': '1.0.1',
    'description': 'Monkey patching utilities for classes',
    'long_description': '# class-interference\n\nMonkey patching utilities for classes.\n\n## Installation\n\n```shell\npip install class-interference\n```\n\n# Usage example\n\n```python\nfrom class_interference import Extension, inject, extend_all\n\n\nclass LibraryClass:\n    def library_method(self, *args, **kwargs):\n        return None\n\n\nclass LibraryClassExtension(LibraryClass, Extension):\n    @inject\n    def library_method(self, *args, **kwargs):\n        original_value = self.super_ext.library_method(*args, **kwargs)\n        if original_value is None:\n            raise ValueError\n        return original_value\n\n\nextend_all()\n\nif __name__ == "__main__":\n    library_class_instance = LibraryClass()\n    library_class_instance.library_method()  # raises ValueError\n\n```\n',
    'author': 'Artem Novikov',
    'author_email': 'artnew@list.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/reartnew/class-interference',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
