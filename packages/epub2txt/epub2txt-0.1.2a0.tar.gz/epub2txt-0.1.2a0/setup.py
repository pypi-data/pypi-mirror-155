# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['epub2txt']

package_data = \
{'': ['*']}

install_requires = \
['absl-py>=0.11.0,<0.12.0',
 'ebooklib>=0.17.1,<0.18.0',
 'httpx>=0.16.1,<0.17.0',
 'logzero>=1.6.3,<2.0.0',
 'tqdm>=4.56.0,<5.0.0']

entry_points = \
{'console_scripts': ['epub2txt = epub2txt.__main__:main']}

setup_kwargs = {
    'name': 'epub2txt',
    'version': '0.1.2a0',
    'description': 'Convert epub to txt with additonal utils',
    'long_description': '# epub2txt [![Codacy Badge](https://app.codacy.com/project/badge/Grade/05c422da73a14c23b87b0657af9c8df7)](https://www.codacy.com/gh/ffreemt/epub2txt/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ffreemt/epub2txt&amp;utm_campaign=Badge_Grade)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/epub2txt.svg)](https://badge.fury.io/py/epub2txt)\n\nConvert epub to txt with additonal utils\n\n<!--- Refer to dualtext-epub\\der_fanger_de_en.py\n\t\t__main__.py refer to tmx2epub.__main__\n--->\n\n## Installation\n\n```bash\npip install epub2txt\n# pip install epub2txt -U  # to upgrade\n```\n\n## Usage\n\n### From command line\n\n```bash\n# convert test.epub to test.txt\nepub2txt -f test.epub\n\n# browse for epub file, txt file will be in the same directory as the epub file\nepub2txt\n\n# show epub book info: title and toc\nepub2txt -i\n\n# show more epub book info: title, toc, metadata, spine (list of stuff packed into the epub)\nepub2txt -m\n\n# show epub2txt version\nepub2txt -V\n\n```\n\n### `python` code\n\n```python\nfrom epub2txt import epub2txt\n# from a url to epub\nurl = "https://github.com/ffreemt/tmx2epub/raw/master/tests/1.tmx.epub"\nres = epub2txt(url)\n\n# from a local epub file\nfilepath = r"tests\\test.epub"\nres = epub2txt(filepath)\n\n```\n\n## TODO\n*   Extract a single chapter\n*   Batch conversion of several epub files\n\n',
    'author': 'freemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/epub2txt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
