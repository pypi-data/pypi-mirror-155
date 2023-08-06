# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rustshed']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rustshed',
    'version': '0.2.1',
    'description': 'Rust types in Python.',
    'long_description': '# rustshed\n\n[![codecov](https://codecov.io/gh/pawelrubin/rustshed/branch/main/graph/badge.svg?token=LV5XXHDSF5)](https://codecov.io/gh/pawelrubin/rustshed)\n\nA collection of Rust types in Python with complete type annotations.\n\n### Supported Types\n\n- Option\n- Result\n\n## Install\n\n```shell\npip install rustshed\n```\n\n\n## Examples\n\n### Option\n\nThe `Option` type represents an optional value: every `Option[T]` is either `Some[T]` and contains a value of type `T`, or `Null` (`None` in Rust), and does not.\n\n```Python\nfrom typing import SupportsIndex, TypeVar\n\nfrom rustshed import Null, Option, Some\n\nT = TypeVar("T")\n\n\nclass SafeList(list[T]):\n    def get(self, index: SupportsIndex) -> Option[T]:\n        try:\n            return Some(self[index])\n        except IndexError:\n            return Null\n\na_list = SafeList([2, 1, 3, 7])\nprint(a_list.get(1))  # Some(value=1)\nprint(a_list.get(420))  # Null\n```\n\n### Result\n\nThe `Result` is the type used for returning and propagating errors: every `Result[T, E]` is either `Ok[T]`, representing success and containing a value of type `T`, or `Err[E]`, representing failure and containing an error of type `E`.\n\n```python\nfrom rustshed import to_result, Result\n\n\n@to_result[ValueError]\ndef parse(x: str) -> int:\n    return int(x)\n\n\ndef multiply(a: str, b: str) -> Result[int, str]:\n    # try to parse two strings and multiply them\n    # map a possible error to str\n    return parse(a).and_then(lambda n: parse(b).map(lambda m: n * m)).map_err(str)\n\n\nprint(multiply("21", "2"))  # Ok(value=42)\nprint(multiply("2!", "2"))  # Err(error="invalid literal for int() with base 10: \'2!\'")\n```\n\n### Rust\'s question mark (?) operator\n\nThe question mark (`?`) operator in Rust hides some of the boilerplate of propagating errors up the call stack. Implementing this operator in Python would require changes to the language grammar, hence in **rustshed** it had to be implemented differently.\n\n### Q property\n\nThe question mark\'s functionality has been implemented via the `Q` property (for both `Option` and `Result` types) combined with the `rustshed.result_shortcut` or `rustshed.option_shortcut` decorator.\n\n\n```python\nfrom rustshed import Ok, Result, to_result, result_shortcut\n\n\n@to_result[ValueError]\ndef parse(x: str) -> int:\n    return int(x)\n\n\n# explicit early error return with match statements\ndef try_to_parse_early_return(a: str, b: str) -> Result[int, ValueError]:\n    match parse(a):\n        case Ok(value):\n            x = value\n        case err:\n            return err\n\n    match parse(b):\n        case Ok(value):\n            y = value\n        case err:\n            return err\n\n    return Ok(x + y)\n\n\n# early error return using the Q property\n@result_shortcut\ndef try_to_parse(a: str, b: str) -> Result[int, ValueError]:\n    x = parse(a).Q\n    y = parse(b).Q\n    return Ok(x + y)\n\n```\n',
    'author': 'Paweł Rubin',
    'author_email': 'pawelrubindev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pawelrubin/rustshed',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
