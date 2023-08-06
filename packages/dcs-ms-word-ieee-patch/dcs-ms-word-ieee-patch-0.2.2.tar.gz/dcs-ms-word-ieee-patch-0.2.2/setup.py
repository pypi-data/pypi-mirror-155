# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ieee_patch']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0', 'lxml>=4.9.0,<5.0.0', 'typer>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['ieee-patch = ieee_patch.patch:main',
                     'xml-pretty-print = ieee_patch.xml_pretty_print:main']}

setup_kwargs = {
    'name': 'dcs-ms-word-ieee-patch',
    'version': '0.2.2',
    'description': 'Patch IEEE citation format in Microsoft Word docx documents',
    'long_description': '# Microsoft Word IEEE Citation Patcher\n\nPost-processing script that patches IEEE citation format in [Microsoft Word][ms-word] documents in the [docx format][docx-format].\n\nWord does only allow to list citations one by one and has no integrated logic to group or sort them.\nEspecially in scientific documents it is often the case that multiple citations are added to the same paragraphs and it is likely that they are not in order.\nSorting and grouping citation references is a tedious task, so this script is here to help.\n\nAn original text like this\n\n> as shown by Brown [5], [4]; as mentioned earlier [9], [4], [5], [2], [7], [6]; Smith [4] and Brown and Jones [5]; Wood et al. [7]\n\nis transformed to this\n\n> as shown by Brown [4], [5]; as mentioned earlier [2], [4]-[7], [9]; Smith [4] and Brown and Jones [5]; Wood et al. [7]\n\nor with an optional compression option to this\n\n> as shown by Brown [4,5]; as mentioned earlier [2,4-7,9]; Smith [4] and Brown and Jones [5]; Wood et al. [7]\n\n\n## Installation\n\nPython >= 3.8 is required for this tool to work.\nThe package is hosted on [PyPI].\n\nTo install with pip, use the following command:\n\n```console\n$ pip install dcs-ms-word-ieee-patch\n```\n\nThis installs two CLI scripts, `ieee-patch` and `xml-pretty-print`.\n\n## Usage\n\nRun the script with the path to the \n\n```console\n$ ieee-patch /path/to/file.docx                 # on unix\n$ ieee-patch C:\\Users\\foobar\\Desktop\\file.docx  # on windows\n```\n\nThe script by default creates a file with the filename suffix `.patched` in the same folder as the original file and patches the content within this file which means the original file is left untouched.\n\nIn case the replacement should be done in-place, e.g., when space limitations apply, use the `--overwrite` CLI flag.\n**Please use this flag only if really necessary, since the original content cannot be restored after is has been overwritten!**\n\n# Legal notice\n\nThis project is not affiliated, associated, authorized, endorsed by, or in any way officially connected with the Microsoft Corporation, or any of its subsidiaries or its affiliates.\n\n\n[ms-word]: https://products.office.com/en-us/word\n[docx-format]: https://docs.microsoft.com/en-us/openspecs/office_standards/ms-docx/b839fe1f-e1ca-4fa6-8c26-5954d0abbccd\n[PyPI]: https://pypi.org/project/dcs-ms-word-ieee-patch/',
    'author': 'dotcs',
    'author_email': 'git@dotcs.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dotcs/ms-word-ieee-patch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
