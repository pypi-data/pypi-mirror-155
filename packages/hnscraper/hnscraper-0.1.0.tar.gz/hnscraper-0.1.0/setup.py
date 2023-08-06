# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hnscraper']

package_data = \
{'': ['*']}

install_requires = \
['BeautifulSoup4>=4.11.1,<5.0.0',
 'jupyterlab>=3.4.3,<4.0.0',
 'notebook>=6.4.12,<7.0.0',
 'pathlib>=1.0.1,<2.0.0',
 'pymongo>=4.1.1,<5.0.0',
 'requests>=2.28.0,<3.0.0']

entry_points = \
{'console_scripts': ['hnscraper = hnscraper.main:main']}

setup_kwargs = {
    'name': 'hnscraper',
    'version': '0.1.0',
    'description': 'Hackernews Scraper',
    'long_description': '# Hackernews-Scraping\n![Tests](https://github.com/pushp1997/Hackernews-Scraping/actions/workflows/tests.yml/badge.svg)\n### Business Requirements:\n\n1. Scrape TheHackernews.com and store the result (Description, Image, Title, Url) in mongo db\n2. Maintain two relations - 1 with the url and title of the blog and other one with url and its meta data like (Description, Image, Title, Author)\n\n### Requirements:\n\n-   python3\n-   pip\n-   python libraries:\n    _ requests\n    _ BeautifulSoup4\n    _ pymongo\n    _ jupyterlab \\* notebook\n-   MongoDB\n-   git\n\n## To run the application on your local machine:\n\n### Clone the repository:\n\n1. Type the following in your terminal\n\n    `git clone https://github.com/pushp1997/Hackernews-Scraping.git`\n\n2. Change the directory into the repository\n\n    `cd ./Hackernews-Scraping`\n\n3. Create python virtual environment\n\n    `python3 -m venv ./scrapeVenv`\n\n4. Activate the virtual environment created\n\n    - On linux / MacOS :\n      `source ./scrapeVenv/bin/activate`\n    - On Windows (cmd) :\n      `"./scrapeVenv/Scripts/activate.bat"`\n    - On Windows (powershell) :\n      `"./scrapeVenv/Scripts/activate.ps1"`\n\n5. Install python requirements\n\n    `pip install -r requirements.txt`\n\n6. Open the ipynb using jupyter notebook\n\n    `jupyter notebook "Hackernews Scraper.ipynb"`\n\n7. Run the notebook, you will be asked to provide inputs for no of pages to scrape to get the post and your MongoDB database URI to store the posts data.\n\n8. Open mongodb shell connecting to the same URI you provided to the ipynb notebook while running it.\n\n9. Change the database\n\n    `use hackernews`\n\n10. Print the documents in the \'url-title\' collection\n\n    `db["url-title"].find().pretty()`\n\n11. Print the documents in the \'url-others\' collection\n\n    `db["url-others"].find().pretty()`\n',
    'author': 'Pushp Vashisht',
    'author_email': 'pushptyagi1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pushp1997/Hackernews-Scraping/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
