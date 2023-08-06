# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['poetry_stickywheel_plugin']
entry_points = \
{'poetry.application.plugin': ['stickywheel = '
                               'poetry_stickywheel_plugin:StickyWheelsPlugin']}

setup_kwargs = {
    'name': 'poetry-stickywheel-plugin',
    'version': '0.0.1',
    'description': '',
    'long_description': '# Poetry StickyWheel Plugin\n\n<p class="lead">\nA poetry plugin to pin version dependencies when building packages with local folder dependencies.\n</p>\n\n## 🛠 Installing\n\n```\npoetry self add poetry-stickywheel-plugin\n```\n\n## 📚 Help\n\nThis plugin will rewrite folder dependencies in your poetry projects dependencies with version dependencies.\n\nThe version will be extracted from the dependencies pyproject.toml and applied as a semver match.\n\nAssuming a `pyproject.toml` such as:\n\n```\n[tool.poetry]\nname = "a"\nversion = "0.1.0"\ndescription = ""\nauthors = []\nreadme = "README.md"\n\n[tool.poetry.dependencies]\nb = {path = "../b", develop = true}\n```\n\nand the dependency `pyproject.toml`\n\n```\n[tool.poetry]\nname = "b"\nversion = "1.2.3"\ndescription = ""\nauthors = []\nreadme = "README.md"\n```\n\nthe dependency will be rewritten as if it had been defined as:\n\n```\nb = "^1.2.3"\n```\n\n## ⚖️ Licence\n\nThis project is licensed under the [MIT licence][mit_licence].\n\nAll documentation and images are licenced under the \n[Creative Commons Attribution-ShareAlike 4.0 International License][cc_by_sa].\n\n## 📝 Meta\n\nThis project uses [Semantic Versioning][semvar].\n\n[discussions]: https://github.com/artisanofcode/poetry-stickywheel-plugin/discussions\n[mit_licence]: http://dan.mit-license.org/\n[cc_by_sa]: https://creativecommons.org/licenses/by-sa/4.0/\n[semvar]: http://semver.org/',
    'author': 'Daniel Knell',
    'author_email': 'contact@danielknell.co.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
