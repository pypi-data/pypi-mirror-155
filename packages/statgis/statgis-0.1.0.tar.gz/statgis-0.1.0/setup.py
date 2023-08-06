# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['statgis', 'statgis.gee']

package_data = \
{'': ['*']}

install_requires = \
['earthengine-api>=0.1,<0.2', 'pandas>=1.3,<2.0']

setup_kwargs = {
    'name': 'statgis',
    'version': '0.1.0',
    'description': 'Functions for spatial data analysis developed by StatGIS.org',
    'long_description': "# Statgis Toolbox\n\n`statgis` is a Python package developed and maintained by StatGIS.org used to perform several spatial data science analysis.This package counts with function operate with Google Earth Engine.\n\n## Dependencies\n\nThis package depends of [earthengine-api](https://developers.google.com/earth-engine/tutorials/community/intro-to-python-api) and [geopandas](https://geopandas.org/en/stable/getting_started.html).\n\n```bash\n$ conda install geopandas\n$ conda install earthengine-api\n```\n\nTo use `earthengine-api` you have to sing up to [Google Earth Engine](https://earthengine.google.com/new_signup/) and authneticate with the comand `Authenticate()`.\n\n```Python\nimport ee\n\nee.Authenticate()\n```\n\n## Installation\n\nTo install `statgis` you only have to run the `pip install` comand:\n\n```bash\n$ pip install statgis\n```\n\nThe current version of statgis is 0.1.0.\n\n## Contribution\n\nTo contribute you have to read and understand the [code of conduct](CONDUCT.md) and the [contributing guideline](CONTRIBUTING.md).\n\n## License\n\nThis software is protected by a GPUv3 License that let you use and copy the software but, you can't develop your own version. The complete description is in the [license file](LICENSE.txt).\n\n## Credits\n\nAll the attribution of the development and maintance of this package is for StatGIS.org and its developers team:\n\n- Sebástian Narváez.\n- Brayan Navarro.\n- Cristian Carrascal.\n",
    'author': 'Narváez, Sebástian',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
