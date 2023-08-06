# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['skipulagsstofnun']

package_data = \
{'': ['*']}

install_requires = \
['fiona>=1.8.21,<2.0.0', 'shapely>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'skipulagsstofnun',
    'version': '0.2.1',
    'description': 'Library to lookup polygons, coordinates and metadata of approved local site plans in Iceland',
    'long_description': "# skipulagsstofnun\n\nLibrary to lookup polygons, coordinates and metadata of approved local site plans in Iceland.\n\nUsed by [Planitor](https://www.planitor.io).\n\n## Install\n\n```bash\nbrew install gdal  # or similar\npoetry add skipulagsstofnun\n```\n\nor\n\n```bash\npip install skipulagsstofnun\n```\n\n## Use\n\n```python\n>>> from skipulagsstofnun import plans\n>>> shape, plan = plans.get_plan(64.1525571, -21.9508792)\n>>> plan\n{'id': 'skipulag_deiliskipulag.198969', 'type': 'Feature', 'skipnr': '8136', 'nrsveitarf': '0', 'sveitarfelag': 'Reykjavíkurborg', 'heiti': 'Deiliskipulag stgr. 1.116 og 1.115.3, Slippa- og Ellingsensreitur', 'skipstig': 'deiliskipulag', 'malsmed': 'nytt', 'dagsinnsett': None, 'dagsleidrett': datetime.date(2016, 4, 14), 'gagnaeigandi': 'Skipulagsstofnun', 'dagsheimild': None, 'heimild': None, 'nakvaemnix': '0', 'vinnslufer': None}\n```\n\nYou can construct a link to a page hosted by Skipulagsstofnun with the PDF\nscans for this local site plan.\n\n`http://skipulagsaaetlanir.skipulagsstofnun.is/skipulagvefur/display.aspx?numer={skipnr}`\n",
    'author': 'Jökull Sólberg',
    'author_email': 'jokull@solberg.is',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jokull/skipulagsstofnun',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
