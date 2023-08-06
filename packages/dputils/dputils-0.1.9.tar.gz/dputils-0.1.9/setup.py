# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dputils']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'docx2txt>=0.8,<0.9',
 'fake-useragent>=0.1.11,<0.2.0',
 'fpdf2>=2.5.4,<3.0.0',
 'pdfminer.six>=20220524,<20220525',
 'python-docx>=0.8.11,<0.9.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'dputils',
    'version': '0.1.9',
    'description': 'This library is utility library from digipodium',
    'long_description': 'A python library which can be used to extraxct data from files, pdfs, doc(x) files, as well as save data into these files. This library can be used to scrape and extract webpage data from websites as well.\n\nFunctions from dputils.files:\n1. get_data: \n    - To import, use statement: \n        ```python3\n        from dputils.files import get_data\n        ``` \n    - Obtains data from files of any extension given as args(supports text files, binary files, pdf, doc for now, more coming!)\n    - sample call:\n        ```python3\n        content = get_data(r"sample.docx")\n        print(content)\n        ```\n    - Returns a string or binary data depending on the output arg\n\n2. save_data:\n    - To import, use statement:\n         ```python3\n        from dputils.files import save_data\n        ```\n    - save_data can be used to write and save data into a file of valid   extension.\n    - sample call: \n         ```python3\n        pdfContent = save_data("sample.pdf", "Sample text to insert")\n        print(pdfContent)\n        ```\n    - Returns True if file is successfully accessed and modified. Otherwise False.\n\nFunctions from dputils.scrape:\n1. get_webpage_data:\n    - To import, use statement: \n         ```python3\n        from dputils.scrape import get_webpage_data\n        ```\n    - get_webpage_data can be used to obtain data from any website in the   form of BeautifulSoup object\n    - sample call: \n        ```python3\n        soup = get_webpage_data("https://en.wikipedia.org/wiki/Hurricane_Leslie_(2018)")\n        print(type(soup))\n        ```\n    - Returns data as a BeautifulSoup object\n\n2. extract_one:\n    - To import, use statement: \n        ```python3\n        from dputils.scrape import extract_one\n        ```\n    - extract_one can be used to extract a data item as a dict from data in a given BeautifulSoup object\n    - sample call: \n        ```python3\n        soup = get_webpage_data("https://en.wikipedia.org/wiki/Hurricane_Leslie_(2018)")\n\n        dataDict = extract_one(soup, title = {\'tag\' : \'h1\', \'attrs\' : {\'id\' : \'firstHeading\'}, \'output\' : \'text\'})\n        print(dataDict)\n        ```\n    - Output will be of type dict\n\n3. extract_many:\n    - To import, use statement: \n        ```python3\n        from dputils.scrape import extract_many\n        ```\n    - extract_one can be used to extract several data items (as dict) stored in a list from data in a given BeautifulSoup object\n    - sample call: \n        ```python3\n        soup = get_webpage_data("https://www.amazon.com/s?k=headphones&crid=1DUUWW6PEVAJ1&sprefix=headphones%2Caps%2C161&ref=nb_sb_noss_1")\n        \n        extract_many(soup, \n                target = {\'tag\' : \'div\', \'attrs\' : {\'class\':\'s-main-slot s-result-list s-search-results sg-row\'}},\n                items =  {\'tag\' : \'div\', \'attrs\' : {\'class\':\'s-result-item\'}},\n                title =  {\'tag\' : \'h2\', \'attrs\' : {\'class\':\'a-size-mini a-spacing-none a-color-base s-line-clamp-2\'}})\n        ```\n    - Output will be of type list\n\nThese functions can used on python versions 3.8 or greater.\n\nReferences for more help: https://github.com/digipodium/dputils\n\nThank you for using dputils!',
    'author': 'AkulS1008',
    'author_email': 'akulsingh0708@gmail.com',
    'maintainer': 'Zaid Kamil',
    'maintainer_email': 'xaidmetamorphos@gmail.com',
    'url': 'https://github.com/digipodium/dputils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
