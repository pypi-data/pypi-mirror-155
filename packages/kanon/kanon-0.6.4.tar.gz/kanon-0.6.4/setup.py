# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kanon',
 'kanon.calendars',
 'kanon.models',
 'kanon.tables',
 'kanon.units',
 'kanon.utils',
 'kanon.utils.types']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=5.0,<6.0',
 'matplotlib>=3.5.1,<4.0.0',
 'numpy>=1.22.0,<2.0.0',
 'pandas>=1.3.5,<2.0.0',
 'requests>=2.27.1,<3.0.0']

extras_require = \
{':python_version >= "3.8" and python_version < "3.11"': ['scipy>=1.7.3,<2.0.0'],
 'docs': ['nbsphinx>=0.8.8,<0.9.0',
          'papermill>=2.3.3,<3.0.0',
          'ipykernel>=6.6.1,<7.0.0',
          'ipython>=8.0.0,<9.0.0',
          'sphinx-astropy>=1.7.0,<2.0.0',
          'sphinx-rtd-theme>=1.0.0,<2.0.0'],
 'notebook': ['nbformat>=5.1.3,<6.0.0',
              'papermill>=2.3.3,<3.0.0',
              'ipykernel>=6.6.1,<7.0.0',
              'ipython>=8.0.0,<9.0.0']}

setup_kwargs = {
    'name': 'kanon',
    'version': '0.6.4',
    'description': 'History of astronomy library',
    'long_description': '.. image:: https://github.com/legau/kanon/workflows/CI/badge.svg\n    :target: https://github.com/legau/kanon/actions\n    :alt: GitHub Pipeline Status\n.. image:: https://codecov.io/gh/legau/kanon/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/legau/kanon/branch/master\n    :alt: Coverage\n.. image:: https://readthedocs.org/projects/kanon/badge/?version=latest\n    :target: https://kanon.readthedocs.io/en/latest/?badge=latest\n    :alt: Docs status\n.. image:: https://img.shields.io/pypi/v/kanon\n    :target: https://pypi.org/project/kanon/\n    :alt: Kanon Pypi\n.. image:: https://shields.io/badge/python-v3.8-blue\n    :target: https://www.python.org/downloads/release/python-380/\n    :alt: Python 3.8\n.. image:: http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat\n    :target: http://www.astropy.org\n    :alt: Powered by Astropy Badge\n.. image:: https://zenodo.org/badge/344498058.svg\n   :target: https://zenodo.org/badge/latestdoi/344498058\n\n\n--------\n\n**Kanon** is the History of Astronomy Python package and tools.\n\nCurrent Features\n________________\n\n`units`\n\n- Define standard positional numeral systems with standard arithmetics (`BasedReal`)\n- Set your own precision contexts and algorithms on arithmetical operations (`PrecisionContext`)\n- Keep track of all operations\n\n`tables`\n\n- Build or import ancient astronomical tables\n- Perform arithmetical and statistical operations\n- Support for `BasedReal` values\n\n`calendars`\n\n- Define new calendar types\n- Date conversions\n\n`models`\n\n- Collection of mathematical models used for all kinds of geocentric astronomical tables\n\nHow to use\n__________\n\nInstall the package with `pip`\n\n.. code:: bash\n\n    pip install kanon\n\nImport Kanon and begin trying all its features\n\n.. code:: python\n\n    import kanon.units as u\n\n    a = u.Sexagesimal(1,2,3)\n    b = u.Sexagesimal(2,1,59)\n\n    a + b\n    # 3,4,2 ;\n\n\nDevelopment\n___________\n\nTo start developing on this project you need to install\nthe package with `poetry` (`Installing Poetry <https://python-poetry.org/docs/>`)\n\n.. code:: bash\n\n    git clone https://github.com/legau/kanon.git\n    cd kanon\n    poetry install\n\nThe changes you make in the code are reflected on your Python environment.\n\nActivate pre-commit checks :\n\n.. code:: bash\n\n    pre-commit install\n\nTests\n_____\n\nRun tests with tox\n\n.. code:: bash\n\n    # source code tests\n    tox -e test\n\n    # example notebooks tests\n    tox -e test_notebooks\n\n    # linting\n    pre-commit run --all-files\n',
    'author': 'Léni Gauffier',
    'author_email': 'lenigauffier@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://dishas.obspm.fr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
