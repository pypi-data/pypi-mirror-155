# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pytest_data_suites']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=6.0,<8.0']

setup_kwargs = {
    'name': 'pytest-data-suites',
    'version': '1.0.3',
    'description': 'Class-based pytest parametrization',
    'long_description': "# pytest-data-suites\n\nClass-based test cases for `pytest`.\n\n## Usage example\n\n```python\nfrom pytest_data_suites import DataSuite\n\n\nclass MultiplicationDataSuite(DataSuite):\n    # Using TypedDict instead of dict here could clarify your code, but that's just a demo\n    positive_operands = dict(left_operand=2, right_operand=2, operation_result=4)\n    negative_operands = dict(left_operand=-3, right_operand=-7, operation_result=21)\n\n\n@MultiplicationDataSuite.parametrize\ndef test_multiplication(left_operand: float, right_operand: float, operation_result: float) -> None:\n    assert left_operand * right_operand == operation_result\n\n```\n",
    'author': 'Artem Novikov',
    'author_email': 'artnew@list.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/reartnew/pytest-data-suites',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
