# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['example_template_service', 'example_template_service.api_v1']

package_data = \
{'': ['*']}

install_requires = \
['example-template-core==0.1.0',
 'example-template-foundation==1.0.0',
 'fastapi>=0.63.0,<0.64.0',
 'prometheus-client>=0.6.0',
 'pydantic>=1.7.3,<1.8.0',
 'python-multipart>=0.0.5,<0.0.6',
 'uvicorn>=0.13.3,<0.14.0']

entry_points = \
{'console_scripts': ['example_template_service_web_start = '
                     'example_template_service.run:run_cli',
                     'run-cli = example_template_service.run:run_cli']}

setup_kwargs = {
    'name': 'example-template-service',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Anustup Das',
    'author_email': 'anustup@mediadistillery.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
