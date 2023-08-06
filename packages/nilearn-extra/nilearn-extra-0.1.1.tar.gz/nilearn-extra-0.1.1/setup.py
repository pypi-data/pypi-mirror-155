# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nilearn_extra', 'nilearn_extra.connectome']

package_data = \
{'': ['*']}

install_requires = \
['nilearn>=0.9.1,<0.10.0', 'scipy>=1.8,<2.0']

setup_kwargs = {
    'name': 'nilearn-extra',
    'version': '0.1.1',
    'description': 'Drop-in extra functionalities for nilearn (statistics for neuroimaging in Python)',
    'long_description': '# Nilearn Extra\n\n**Nilearn Extra** is a small add-on for *[Nilearn](https://nilearn.github.io/) (Statistics for NeuroImaging in Python)*. It currently adds some functional connectivity measures to the mix.\n\n## Installation\n\n```bash\npip install nilearn-extra\n```\n\n## Usage\n\n```diff\n- from nilearn.connectome import ConnectivityMeasure\n+ from nilearn_extra.connectome import ConnectivityMeasure\n```\n\n## Extra Connectivity Matrices\n\nNilearn Extra supports two additional connectivity matrices:\n- Chatterjee XiCorr (`kind="chatterjee"`) is a new correlation coefficient as described in [Chatterjee (2019)](https://arxiv.org/abs/1909.10140).\n- Transfer Entropy (`kind="transfer entropy"`) between regions X and Y is amount of uncertainty reduced in Y by knowing the past values of X. Transfer entropy is an asymmetric measure, so is the connectivity matrix.\n\n# Optional Dependencies\n\n```bash\n# transfer entropy connectivity requires `pyinform` package.\npip install pyinform\n```\n\n## Contributing\n\nWe use GitHub to fork and manage pull requests.\n\n## License\n\nBSD 3-Clause License. See the [LICENSE](LICENSE) file.\n',
    'author': 'Morteza Ansarinia',
    'author_email': 'ansarinia@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/morteza/nilearn-extra',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
