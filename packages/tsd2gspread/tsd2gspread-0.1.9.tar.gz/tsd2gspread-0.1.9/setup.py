# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tsd2gspread']

package_data = \
{'': ['*']}

install_requires = \
['gspread>=5.0.0,<6.0.0']

setup_kwargs = {
    'name': 'tsd2gspread',
    'version': '0.1.9',
    'description': 'Time Series Data to Google Sheets',
    'long_description': "# tsd2gspread\nA tool to write Time Series Data to Google Sheets,\nusing [gspread](https://github.com/burnash/gspread).\n\n# Requirement\n\n* Python 3.6 or later\n\n# Installation\n\n    $ pip install tsd2gspread\n\n# Preparation\n\n## Service account\n\nGet a service account file (json) for Google APIs following [Authentication — gspread 3.7.0 documentation](https://gspread.readthedocs.io/en/latest/oauth2.html#for-bots-using-service-account).\n\n## Google Sheets\n\nTsd2Gspread can create new Google Sheets if you want.\n\nOtherwise, you can use prepared Google Sheets.\n\nTo allow the service account to access the Sheet,\ngo to the Sheet and share it with `client_email` from the above service account file.\n\n# Example\n\n## Use Tsd2Gspread directly\n\n    import tsd2gspread\n\n    tg = tsd2gspread.get(\n        service_account='~/service_account.json',\n        sheet_name='MySheet',\n        create=1,\n        worksheet_name='MyWork',\n        columns='foo,bar,\n        share='rcmdnk@gmail.com')\n\n    # Make function to get data\n    def get_data():\n        foo = 1\n        bar = 2\n        return (foo, bar)\n\n    # Set data getter\n    tg.get_data = get_data\n\n    # Write Time Series Data to Google Sheets\n    tg.write()\n\nThis will make Google Sheets like:\n\nDatetime|foo|bar\n-|-|-\n2021-04-30 12:34:56|1|2\n\nOptions for `get`:\n\nOption|Mean|Default\n:-|:-|:-\nconfig_file|Configuration file of Tsd2Gspread.|None\nservice_account|Path for the **service_account.json** (Google API service_account file).<br> If  `None`, tsd2gspread(gspread) will use **~/.config/gspread/service_account.json**.|`None`\nsheet_name|If set, Sheet is searched by name.|`None`\ncreate|If set to 1, new Sheet is created if it is not found by name.<br>Only works if **sheet_name** is not `None`|`None`\nsheet_url|If set, Sheet is searched by URL.|`None`\nsheet_key|If set, Sheet is searched by key.|`None`\nworksheet_name|Work sheet name.|`None`\ncolumns|Column names separated by `,`.<br>If set, the title like will be inserted when the sheet is created.|`None`\nshare|Email address of your Google account. <br>If it is not set, only the service account can access to the Sheet and you can not see the Sheet from your account.|`None`\nperm_type|Ref [API Reference - gspread](https://gspread.readthedocs.io/en/latest/api.html): client.insert_permission |`user`\nperm_type|Ref [API Reference - gspread](https://gspread.readthedocs.io/en/latest/api.html): client.insert_permission|`owner`\nadd_datetime|If set to 1, current time is added to the data as the first column.|1\ntimedelta|The time offset from UTC.|0\ntimeformat|The time format to be written.|`%Y-%m-%d %H:%M:%S`\nvalue_input_option|If `add_datetime` is 1, use `USER_ENTERED` to fill datetime value as datetime.<br>Ref [API Reference - gspread](https://gspread.readthedocs.io/en/latest/api.html):Wworksheet.append_row|`USER_ENTERED`\n\n\nIf you set options by the configuration file, write options as\n\n    OPTION=VALUE\n\nand give the file name as `config_file`.\n\n## Make new inherited class from Tsd2Gspread\n\n    from tsd2gspread import Tsd2Gspread\n\n    class MyClass(Tsd2Gspread):\n        def get_data(self):\n            foo = 1\n            bar = 2\n            return (foo, bar)\n\n    tg = MyClass(\n        service_account='~/service_account.json',\n        sheet_name='MySheet',\n        create=1,\n        worksheet_name='MyWork',\n        columns='foo,bar,\n        share='rcmdnk@gmail.com')\n\n    # Write Time Series Data to Google Sheets\n    tg.write()\n",
    'author': 'rcmdnk',
    'author_email': 'rcmdnk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rcmdnk/tsd2gspread',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
