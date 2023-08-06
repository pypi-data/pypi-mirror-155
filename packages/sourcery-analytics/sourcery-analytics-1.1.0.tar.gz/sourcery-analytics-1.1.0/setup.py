# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sourcery_analytics', 'sourcery_analytics.cli', 'sourcery_analytics.metrics']

package_data = \
{'': ['*']}

install_requires = \
['astroid==2.11.6',
 'more-itertools==8.13.0',
 'pydantic==1.9.1',
 'rich==12.4.4',
 'tomli==2.0.1',
 'typer==0.4.1']

entry_points = \
{'console_scripts': ['sourcery-analytics = sourcery_analytics.main:app']}

setup_kwargs = {
    'name': 'sourcery-analytics',
    'version': '1.1.0',
    'description': 'sourcery-analytics is a library and command-line interface (CLI) for analyzing the code quality of Python packages, modules, or source code.',
    'long_description': '# Sourcery Analytics\n\n<a href="https://pypi.org/project/sourcery-analytics/">![PyPI](https://img.shields.io/pypi/v/sourcery-analytics)</a>\n![build, test, and publish docs](https://github.com/sourcery-ai/sourcery-analytics/actions/workflows/on_push_main.yml/badge.svg)\n<a href="https://github.com/psf/black">![code style](https://img.shields.io/badge/code%20style-black-000000.svg)</a>\n<a href="https://sourcery-analytics.sourcery.ai/">![docs](https://img.shields.io/badge/docs-github.io-green.svg)</a>\n\n---\n\n`sourcery-analytics` is a command line tool and library for statically analyzing Python code quality.\n\nGet started by installing using `pip`:\n\n```shell\npip install sourcery-analytics\n```\n\nThis will install `sourcery-analytics` as a command-line tool.\n\nTo identify code quality issues:\n\n```shell\nsourcery-analytics assess path/to/file.py\n```\n\nExample:\n\n```shell\nsourcery-analytics assess sourcery_analytics/metrics\n```\n\n```\nsourcery_analytics/metrics/cyclomatic_complexity.py:47: error: working_memory of cyclomatic_complexity is 34 exceeding threshold of 20\nFound 1 errors.\n```\n\nTo analyze a single Python file, use the `analyze` subcommand:\n\n```shell\nsourcery-analytics analyze path/to/file.py\n```\n\nExample:\n\n```shell\nsourcery-analytics analyze sourcery_analytics/analysis.py\n```\n\n```\n┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┓\n┃ Method                                      ┃ length ┃ cyclomatic_complexity ┃ cognitive_complexity ┃ working_memory ┃\n┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━┩\n│ sourcery_analytics.analysis.analyze         │      5 │                     1 │                    0 │              8 │\n│ sourcery_analytics.analysis.analyze_methods │      4 │                     1 │                    1 │             12 │\n└─────────────────────────────────────────────┴────────┴───────────────────────┴──────────────────────┴────────────────┘\n```\n\nAlternatively, import and run analysis using the library:\n\n```python\nfrom sourcery_analytics import analyze_methods\nsource = """\n    def cast_spell(self, spell):\n        if self.power < spell.power:\n            raise InsufficientPower\n        print(f"{self.name} cast {spell.name}!")\n"""\nanalyze_methods(source)\n# [{\'method_qualname\': \'.cast_spell\', \'method_length\': 3, \'method_cyclomatic_complexity\': 1, \'method_cognitive_complexity\': 1, \'method_working_memory\': 6}]\n```\n\nFor more, see the [docs](https://sourcery-analytics.sourcery.ai/).\n\n### Repoanalysis.com\nYou can see how hundreds of top projects measure across different code quality metrics and see how your priojects compare at [repoanalysis.com](https://repoanalysis.com/)\n\n### Developed by Sourcery\nSourcery Analytics was originally developed by the team at [Sourcery](https://sourcery.ai/?utm_source=sourcery-analytics). Sourcery is an automated coding assistant to help Python developers review and improve their code while they work. Sourcery has a built in library of 100+ core rules and you can extend it further to create custom rules for any scenario.\n',
    'author': 'Ben Martineau',
    'author_email': 'ben@sourcery.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sourcery-ai/sourcery-analytics',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
