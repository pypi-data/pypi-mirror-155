# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['week_by_week']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.4.2,<2.0.0']

setup_kwargs = {
    'name': 'week-by-week',
    'version': '3.14.0',
    'description': 'This Library accept pandas dataframe, date_column and optional end date If end date is not provide, current today will be use internally by the library',
    'long_description': '# This package "week by Week" \nis attempt to have Python library that \n1. Generate week range from pandas dataframe from the first\n   data point date to the current or a given date\n2. Group pandas row into weekly base on the date/timestamp column\n\n# Usage after installation\n```from week_by_week import WeekRange```\n\nInstantiate the class\n```get_weeks = WeekRange(df, \'timestamp\',\'2022/06/01\', WK_start=\'sun\')```\n\nRequired parameter are:\n    1. df -- pandas dataframe\n    2. timestamp -- date columnin your df\n    3. WK_start change between \'Mon\' to \'Sun\'\nOptional parameter:\n    1. end_date\n\ncall ```getAllweeks()`` method to retrieve all weeks       \n```weeks = get_weeks.getAllweeks()```\n\n\nAnd to retrieve data splitted into week range,\ninvoke ```getWeekData()``` \n\n`print(get_weeks.getWeekData())`\n\n\n\n',
    'author': 'Qamarudeen Muhammad',
    'author_email': 'qamarudeen.m@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/blueband/week_by_week',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
