# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pystrapi']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp']

setup_kwargs = {
    'name': 'pystrapi',
    'version': '3.1.0',
    'description': 'Work with Strapi from Python via REST API',
    'long_description': "# PyStrapi\n\nWork with Strapi from Python via REST API\n\n## Install\n\n```bash\npip install pystrapi\n```\n\n## Documentation\n\n[Full API Reference](./docs)\n\n## Examples\n\nQuick start:\n\n```python\nimport asyncio\nfrom pystrapi import StrapiClient\n\nasync def main():\n    strapi = StrapiClient(strapi_url)\n    await strapi.authorize(your_identifier, your_password) # optional\n    users = await strapi.get_entries('users', filters={'username': {'$eq': 'Pavel'}})\n    user_id = users['data'][0]['id']\n    await strapi.update_entry('users', user_id, data={'username': 'Mark'})\n\nasyncio.run(main())\n```\n\n## Development\n\n### Lint\nRun [prospector](https://prospector.landscape.io/):\n```\nprospector\n```\n\n### Create new release\n\nPush changes to 'main' branch following [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).\n\n",
    'author': 'Noam Nol',
    'author_email': 'noamnol19@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NoamNol/py-strapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
