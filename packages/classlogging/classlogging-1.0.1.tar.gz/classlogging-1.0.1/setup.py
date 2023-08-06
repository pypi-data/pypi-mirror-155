# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['classlogging']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'classlogging',
    'version': '1.0.1',
    'description': 'Class-based logging facility',
    'long_description': '# classlogging\n\nClass-based logging facility.\n\n## Installation\n\n```shell\npip install classlogging\n```\n\n## Usage example\n\n```python\nimport classlogging\n\n\nclass MyClass(classlogging.LoggerMixin):\n    def test_log_value(self, value: str) -> None:\n        self.logger.debug(f"Got value: {value}")\n\n\nif __name__ == "__main__":\n    classlogging.configure_logging(level=classlogging.LogLevel.DEBUG)\n    MyClass().test_log_value("Foo")\n    # Writes to stderr:\n    # 2022-01-01 12:34:56,789 DEBUG [__main__.MyClass] Got value: Foo\n```\n',
    'author': 'Artem Novikov',
    'author_email': 'artnew@list.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/reartnew/classlogging',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
