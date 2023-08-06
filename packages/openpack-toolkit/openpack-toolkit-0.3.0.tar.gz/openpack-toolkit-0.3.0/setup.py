# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openpack_toolkit',
 'openpack_toolkit.activity',
 'openpack_toolkit.codalab',
 'openpack_toolkit.codalab.operation_segmentation',
 'openpack_toolkit.configs',
 'openpack_toolkit.configs.datasets',
 'openpack_toolkit.data',
 'openpack_toolkit.utils']

package_data = \
{'': ['*']}

install_requires = \
['numpy<1.22.0', 'omegaconf>=2.2.2,<3.0.0', 'pandas>=1.2.4', 'sklearn>=0.0']

setup_kwargs = {
    'name': 'openpack-toolkit',
    'version': '0.3.0',
    'description': 'Toolkit for OpenPack Dataset',
    'long_description': '# OpenPack Dataset Toolkit (optk)\n\n![OpenPack Challenge Logo](./img/OpenPackCHALLENG-black.png)\n\n[![Test](https://github.com/open-pack/openpack-toolkit/actions/workflows/test.yaml/badge.svg)](https://github.com/open-pack/openpack-toolkit/actions/workflows/test.yaml)\n[![API Docs - GitHub Pages](https://github.com/open-pack/openpack-toolkit/actions/workflows/deploy-docs.yaml/badge.svg)](https://github.com/open-pack/openpack-toolkit/actions/workflows/deploy-docs.yaml)\n\n"OpenPack Dataset" is a new large-scale multi modal dataset of manual packing process.\nOpenPack is an open access logistics-dataset for human activity recognition, which contains human movement and package information from 17 distinct subjects.\nThis repository provide utilities to explore our exciting dataset.\n\n## Setup\n\nWe provide some utility functions as python package. You can install via pip with the following command.\n\n```bash\n# Pip\npip install openpack-toolkit\n\n# Poetry\npoetry add  openpack-toolkit\n```\n\n## Documentation\n\n- [Dataset Page](https://open-pack.github.io/)\n- [API Docs](https://open-pack.github.io/openpack-toolkit/openpack_toolkit/)\n\n### Dataset Descriptions\n\n- [Subjects & Recording Scenarios](./docs/USER.md)\n- [Activity Class Definition](./docs/ANNOTATION.md)\n- [Modality](./docs/DATA_STREAM.md)\n- [Data Split (Train/Val/Test/Submission)](./docs/DATA_SPLIT.md)\n\n## Examples (PyTorch)\n\nSee [openpack-torch](https://github.com/open-pack/openpack-torch) for more dietail.\n\n- [U-Net with Accelration Data](https://github.com/open-pack/openpack-torch/tree/main/examples/unet)\n- [ST-GCN with Keypoints Data](https://github.com/open-pack/openpack-torch/tree/main/examples/st-gcn)\n\n## License\n\nopenpack-toolkit has a MIT license, as found in the [LICENSE](./LICENCE) file.\n\n----\n\n## Generate Document\n\n```bash\npdoc --html --output-dir docs --force openpack_toolkit/\n```\n',
    'author': 'Yoshimura Naoya',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://open-pack.github.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.11,<4.0.0',
}


setup(**setup_kwargs)
