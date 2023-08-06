# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hondana', 'hondana.types']

package_data = \
{'': ['*'], 'hondana': ['extras/*']}

modules = \
['py', 'tags']
install_requires = \
['aiohttp>=3.7.4,<4.0.0', 'typing-extensions>=4.1.1,<5.0.0']

extras_require = \
{'docs': ['sphinx>=5.0.0,<6.0.0', 'sphinxcontrib-trio', 'furo'],
 'speedups': ['orjson>=3.6.7,<4.0.0'],
 'tests': ['pytest']}

entry_points = \
{'console_scripts': ['version = hondana.__main__:show_version']}

setup_kwargs = {
    'name': 'hondana',
    'version': '3.0.5',
    'description': 'An asynchronous wrapper around the MangaDex v5 API',
    'long_description': '<div align="center">\n    <h1><a href="https://jisho.org/word/%E6%9C%AC%E6%A3%9A">Hondana 『本棚』</a></h1>\n    <a href=\'https://github.com/AbstractUmbra/Hondana/actions/workflows/build.yaml\'>\n        <img src=\'https://github.com/AbstractUmbra/Hondana/actions/workflows/build.yaml/badge.svg\' alt=\'Build status\' />\n    </a>\n    <a href=\'https://github.com/AbstractUmbra/Hondana/actions/workflows/coverage_and_lint.yaml\'>\n        <img src=\'https://github.com/AbstractUmbra/Hondana/actions/workflows/coverage_and_lint.yaml/badge.svg\' alt=\'Linting and Typechecking\' />\n    </a>\n</div>\n<div align="center">\n    <a href=\'https://api.mangadex.org/\'>\n        <img src=\'https://img.shields.io/website?down_color=red&down_message=offline&label=API%20Status&logo=MangaDex%20API&up_color=lime&up_message=online&url=https%3A%2F%2Fapi.mangadex.org%2Fping\' alt=\'API Status\'/>\n    </a>\n    <a href=\'https://hondana.readthedocs.io/en/latest/?badge=latest\'>\n        <img src=\'https://readthedocs.org/projects/hondana/badge/?version=latest\' alt=\'Documentation Status\' />\n    </a>\n</div>\n<h1></h1>\n<br>\n\nA lightweight and asynchronous wrapper around the [MangaDex v5 API](https://api.mangadex.org/docs.html).\nYou can see our stable docs [here](https://hondana.readthedocs.io/en/stable/)!\n\n## Features\nWe are currently at 100% feature compliance with the API.\n\n## Notes\n### Authenticated endpoints\nSadly (thankfully?) I am not an author on MangaDex, meaning I cannot test the creation endpoints for things like scanlators, artists, authors, manga or chapters.\nI have followed the API guidelines to the letter for these, but they may not work.\n\nAny help in testing them is greatly appreciated.\n\n### Upload & Creation\nFollowing the above, I can only use the public test manga for upload testing.\nThese are currently implemented and tested to the best of my ability.\n\n## Examples\nPlease take a look at the [examples](./examples/) directory for working examples.\n\n**NOTE**: More examples will follow as the library is developed.\n\n### API caveats to note\n- There are no API endpoints for Artist. It seems they are not differentiated from Author types except in name only.\n  - I have separated them logically, but under the hood all Artists are Authors and their `__eq__` reports as such.\n- The tags are locally cached since you **must** pass UUIDs to the api (and I do not think you\'re going to memorize those), there\'s a convenience method for updating the local cache as `Client.update_tags`\n  - I have added [an example](./examples/updating_local_tags.py) on how to do the above.\n  - To use these tags, you can see an example [here](./examples/search_manga.py#L17-L22).\n- [Settings related endpoints](https://api.mangadex.org/docs.html#operation/get-settings-template) are not currently exposed. I have implemented their documented use, but I do not expect them to currently function.\n  - Once this is exposed fully I will implement a richer interface.\n- Currently, if there are any errors in a chapter upload process, the error key does not contain filenames or identifiable information on exactly what file failed upload.\n  - This means that I locally compare the succeeded files with the ones missing from the full response payload. The examples have been updated with how to check for an error.\n\n### Contributing\nIf you would like to contribute to Hondana, please take a look at [the contributing guidelines](./.github/CONTRIBUTING.md) and follow the procedure there.\n\n\nIf you have any question please feel free to join my Discord server:\n<div align="left">\n    <a href="https://discord.gg/aYGYJxwqe5">\n        <img src="https://discordapp.com/api/guilds/705500489248145459/widget.png?style=banner2" alt="Discord Server"/>\n    </a>\n</div>\n',
    'author': 'Alex Nørgaard',
    'author_email': 'Umbra@AbstractUmbra.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AbstractUmbra/hondana',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
