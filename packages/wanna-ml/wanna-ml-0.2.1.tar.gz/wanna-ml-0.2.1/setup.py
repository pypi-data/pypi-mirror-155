# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wanna',
 'wanna.cli',
 'wanna.cli.plugins',
 'wanna.components',
 'wanna.components.templates',
 'wanna.components.templates.base.{{ cookiecutter.component_slug }}',
 'wanna.components.templates.base.{{ cookiecutter.component_slug }}.src.{{ '
 'cookiecutter.component_slug }}',
 'wanna.components.templates.base.{{ cookiecutter.component_slug }}.tests',
 'wanna.core',
 'wanna.core.deployment',
 'wanna.core.loggers',
 'wanna.core.models',
 'wanna.core.services',
 'wanna.core.templates',
 'wanna.core.utils']

package_data = \
{'': ['*'], 'wanna.components.templates': ['base/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'PyYAML>=5.4.0,<6.0.0',
 'case-converter>=1.0.2,<2.0.0',
 'checksumdir>=1.2.0,<2.0.0',
 'cookiecutter>=2.1.1,<3.0.0',
 'cron-validator>=1.0.6,<2.0.0',
 'email-validator>=1.2.1,<2.0.0',
 'emoji>=1.7.0,<2.0.0',
 'gitpython>=3.1.27,<4.0.0',
 'google-api-core>=2.7.3,<3.0.0',
 'google-cloud-aiplatform>=1.13.0,<2.0.0',
 'google-cloud-build>=3.8.2,<4.0.0',
 'google-cloud-compute>=1.3.0,<2.0.0',
 'google-cloud-functions>=1.6.0,<2.0.0',
 'google-cloud-logging>=3.1.2,<4.0.0',
 'google-cloud-monitoring>=2.9.2,<3.0.0',
 'google-cloud-notebooks>=1.3.0,<2.0.0',
 'google-cloud-pipeline-components>=1.0.6,<2.0.0',
 'google-cloud-resource-manager>=1.4.1,<2.0.0',
 'google-cloud-scheduler>=2.6.3,<3.0.0',
 'google-cloud-storage>=1.44,<2.0',
 'halo>=0.0.31,<0.0.32',
 'importlib-metadata>=4.0,<5.0',
 'kfp>=1.8.12,<2.0.0',
 'packaging>=21.3,<22.0',
 'pathvalidate>=2.5.0,<3.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'python-on-whales>=0.43.0,<0.44.0',
 'pyyaml-include>=1.3,<2.0',
 'smart-open[gcs]>=6.0,<7.0',
 'treelib>=1.6.1,<2.0.0',
 'typer>=0.4.1,<0.5.0',
 'waiting>=1.4.1,<2.0.0']

entry_points = \
{'console_scripts': ['wanna = wanna.cli.__main__:wanna']}

setup_kwargs = {
    'name': 'wanna-ml',
    'version': '0.2.1',
    'description': 'CLI tool for managing ML projects on Vertex AI',
    'long_description': '# WANNA-ML\n\n---\n\n<p align="center" font-style="italic"> \n<em> Complete MLOps framework for Vertex-AI  </em>\n</p>\n\n---\n\n\n# About WANNA-ML\n\nWANNA-ML is a CLI tool that helps researchers, data scientists, and ML Engineers quickly adapt to Google Cloud Platform (GCP) and get started on the cloud in almost no time.\n\nIt makes it easy to start a Jupyter notebook, run training jobs and pipelines, build a Docker container, export logs to Tensorboards, and much more.\n\nWe build on top of Vertex-AI managed services and integrate with other GCP services like Cloud Build and Artifact Registry to provide you with a standardized structure for managing ML assets on GCP.\n\n\n## Help\n\nSee the [documentation](https://avast.github.io/wanna-ml/) for more details.\n\n\n## Get started\n\n### Installation\nInstall using `pip install -U wanna-ml`.\n\nFor more information on the installation process and requirements, visit out [installation page in documentation](https://avast.github.io/wanna-ml/installation)\n\n### Authentication\nWANNA-ML relies on `gcloud` for user authentication. \n\n1. Install the `gcloud` CLI - follow [official guide](https://cloud.google.com/sdk/docs/install)\n2. Authenticate with the `gcloud init`\n3. Set you Google Application Credentials `gcloud auth application-default login`\n\n### Docker Build\nYou can use a local Docker daemon to build Docker images, but it is not required. \nYou are free to choose between local building on GCP Cloud Build. \nIf you prefer local Docker image building, install  [Docker Desktop](https://www.docker.com/products/docker-desktop/).\n\n### GCP IAM Roles and Permissions\nDifferent WANNA-ML calls require different GCP permissions to create given resources on GCP. Our [documentation page](https://avast.github.io/wanna-ml/)\nlists recommended GCP IAM roles for each `wanna` command.\n\n## Examples\nJump to [the samples](https://github.com/avast/wanna-ml/tree/master/samples) to see a complete solution \nfor various use cases.\n\n## Issues\nPlease report issues to [GitHub](https://github.com/avast/wanna-ml/issues).\n\n## Contributing\nYour contributions are always welcome, see [CONTRIBUTING.md](https://github.com/avast/wanna-ml/blob/master/CONTRIBUTING.md) for more information.\nIf you like WANNA-ML, don\'t forget to give our project a star! \n\n## Licence\nDistributed under the MIT License - see [LICENSE](https://github.com/avast/wanna-ml/blob/master/LICENCE).\n',
    'author': 'Joao Da Silva',
    'author_email': 'joao.silva1@avast.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://avast.github.io/wanna-ml',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
