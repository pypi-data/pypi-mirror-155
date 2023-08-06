# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ploonetide',
 'ploonetide.forecaster',
 'ploonetide.numerical',
 'ploonetide.odes',
 'ploonetide.tests',
 'ploonetide.utils']

package_data = \
{'': ['*']}

install_requires = \
['argparse>=1.0',
 'astroplan>=0.7',
 'astropy>=5.0',
 'astroquery>=0.3.9',
 'beautifulsoup4>=1.0',
 'h5py>=1.0',
 'matplotlib>=1.5.3',
 'mechanicalsoup>=1.0',
 'natsort>=1.0',
 'numpy>=1.18',
 'pandas>=1.1.4',
 'pyfiglet>=0.7.6',
 'scipy>=0.19.0',
 'seaborn>=0.11.2',
 'tqdm>=4.25.0',
 'uncertainties>=1.0']

setup_kwargs = {
    'name': 'ploonetide',
    'version': '1.0.1',
    'description': 'Calculate tidal interactions in planetary systems',
    'long_description': 'Tidal Evolution of Star-Planet-Moon systems (and ploonets!)\n===========================================================\n\n**Ploonetide is a friendly-user package for calculating tidal evolution of compact systems with Python.**\n\n|test-badge| |pypi-badge| |pypi-downloads| |astropy-badge| |docs-badge|\n\n.. |pypi-badge| image:: https://badge.fury.io/py/ploonetide.svg\n                :target: https://badge.fury.io/py/ploonetide\n.. |pypi-downloads| image:: https://pepy.tech/badge/ploonetide/month\n                :target: https://pepy.tech/project/ploonetide\n.. |test-badge| image:: https://github.com/JAAlvarado-Montes/ploonetide/workflows/ploonetide-build-test/badge.svg\n                 :target: https://github.com/JAAlvarado-Montes/ploonetide/actions?query=workflow%3Aploonetide-build-test\n.. |astropy-badge| image:: https://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat\n                   :target: http://www.astropy.org\n.. |docs-badge| image:: https://readthedocs.org/projects/ploonetide/badge/?version=latest\n                 :target: https://ploonetide.readthedocs.io/en/latest/?badge=latest\n                 :alt: Documentation Status\n\n**Ploonetide** is an open-source Python package which offers a simple and user-friendly way\nto calculate tidal evolution of compact planetary systems.\n\n.. Image:: ./docs/source/_static/images/logo.png\n\nDocumentation\n-------------\n\nRead the documentation at `Read the Docs <https://ploonetide.readthedocs.io/en/latest/>`_.\n\n\nQuickstart\n----------\n\nPlease visit our quickstart guide at `Short Tutorial <https://ploonetide.readthedocs.io/en/latest/>`_.\n\n\nContributing\n------------\n\nWe welcome community contributions!\nPlease read the  guidelines at `CONTRIBUTING <https://github.com/JAAlvarado-Montes/ploonetide/blob/develop/CONTRIBUTING.rst>`_.\n\n\nCiting\n------\n\nIf you find Ploonetide useful in your research, please cite it and give us a GitHub star!\nPlease read the citation instructions at `CITATION <https://github.com/JAAlvarado-Montes/ploonetide/blob/develop/CITATION>`_.\n\n\nContact\n-------\nPloonetide is an open source community project created by `the authors <AUTHORS.rst>`_.\nThe best way to contact us is to `open an issue <https://github.com/JAAlvarado-Montes/ploonetide/issues/new>`_ or to e-mail  jaime-andres.alvarado-montes@hdr.mq.edu.au.\n',
    'author': 'Jaime A. Alvarado-Montes',
    'author_email': 'rasjaime@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JAAlvarado-Montes/ploonetide',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
