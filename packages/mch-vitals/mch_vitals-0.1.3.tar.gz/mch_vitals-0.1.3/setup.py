# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mch_vitals', 'mch_vitals.MTTS_CAN.code']

package_data = \
{'': ['*'],
 'mch_vitals': ['MTTS_CAN/*',
                'MTTS_CAN/.git/*',
                'MTTS_CAN/.git/hooks/*',
                'MTTS_CAN/.git/info/*',
                'MTTS_CAN/.git/logs/*',
                'MTTS_CAN/.git/logs/refs/heads/*',
                'MTTS_CAN/.git/logs/refs/remotes/origin/*',
                'MTTS_CAN/.git/objects/pack/*',
                'MTTS_CAN/.git/refs/heads/*',
                'MTTS_CAN/.git/refs/remotes/origin/*']}

setup_kwargs = {
    'name': 'mch-vitals',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Ibrahim Animashaun',
    'author_email': 'iaanimashaun@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
