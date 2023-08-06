# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['raclients', 'raclients.graph', 'raclients.modelclient']

package_data = \
{'': ['*']}

install_requires = \
['Authlib>=1.0.1,<2.0.0',
 'fastapi>=0.78.0,<0.79.0',
 'gql>=3.3.0,<4.0.0',
 'httpx>=0.23.0,<0.24.0',
 'more-itertools>=8.13.0,<9.0.0',
 'pydantic>=1.9.1,<2.0.0',
 'ramodels>=7.0.2,<8.0.0',
 'structlog>=21.5.0,<22.0.0',
 'tenacity>=8.0.1,<9.0.0',
 'tqdm>=4.64.0,<5.0.0']

setup_kwargs = {
    'name': 'raclients',
    'version': '1.2.5',
    'description': 'Clients for OS2mo/LoRa',
    'long_description': '<!--\nSPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>\nSPDX-License-Identifier: MPL-2.0\n-->\n\n\n# RA Clients\n\nOS2mo/LoRa clients\n\n<!--\n## Versioning\nThis project uses [Semantic Versioning](https://semver.org/) with the following strategy:\n- MAJOR: Incompatible changes to existing data models\n- MINOR: Backwards compatible updates to existing data models OR new models added\n- PATCH: Backwards compatible bug fixes\n\n## Getting Started\n\nTODO: README section missing!\n\n### Prerequisites\n\n\nTODO: README section missing!\n\n### Installing\n\nTODO: README section missing!\n\n## Running the tests\n\nTODO: README section missing!\n\n## Deployment\n\nTODO: README section missing!\n\n## Built With\n\nTODO: README section missing!\n\n## Authors\n\nMagenta ApS <https://magenta.dk>\n\nTODO: README section missing!\n-->\n## License\n- This project: [MPL-2.0](MPL-2.0.txt)\n- Dependencies:\n  - pydantic: [MIT](MIT.txt)\n\nThis project uses [REUSE](https://reuse.software) for licensing. All licenses can be found in the [LICENSES folder](LICENSES/) of the project.\n',
    'author': 'Magenta',
    'author_email': 'info@magenta.dk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://magenta.dk/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
