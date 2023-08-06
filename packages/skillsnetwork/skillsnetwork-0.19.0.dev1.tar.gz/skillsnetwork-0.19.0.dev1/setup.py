# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['skillsnetwork',
 'skillsnetwork.cvstudio',
 'skillsnetwork.cvstudio.download_all',
 'skillsnetwork.cvstudio.download_model',
 'skillsnetwork.cvstudio.ping',
 'skillsnetwork.cvstudio.report',
 'skillsnetwork.cvstudio.upload_model']

package_data = \
{'': ['*']}

install_requires = \
['ibm-cos-sdk>=2.11,<3.0',
 'ipython>=8.4.0,<9.0.0',
 'ipywidgets>=7.7.0,<8.0.0',
 'requests>=2.28.0,<3.0.0',
 'tqdm>=4.64.0,<5.0.0']

setup_kwargs = {
    'name': 'skillsnetwork',
    'version': '0.19.0.dev1',
    'description': 'Library for working with Skills Network',
    'long_description': '# Skills Network Python Library\n\nA python library for working with [Skills Network](https://skills.network).\n\n## Installation\n### JupyterLite Installation\n```bash\npip install skillsnetwork\n```\n\n### Regular Installation (JupyterLab, CLI, etc.)\n```bash\npip install skillsnetwork[regular]\n```\n\n## Usage\n\n## JupyterLab / JupyterLite on Skills Network Labs\nThe `skillsnetwork` package provides a unified interface for reading/downloading\nfiles in JupyterLab and JupyterLite.\n\n### Reading a file\n```python\ncontent = await skillsnetwork.read("https://example.com/myfile")\n```\n\n### Downloading a file\n```python\nawait skillsnetwork.download("https://example.com/myfile", filename=filename)\nwith open(filename, "r") as f:\n    content = f.read()\n```\n\n## CV Studio\n\n### Environment Variables\n- `CV_STUDIO_TOKEN`\n- `CV_STUDIO_BASE_URL`\n- `IBMCLOUD_API_KEY`\n\n### Python Code example\n```python\nfrom datetime import datetime\nimport skillsnetwork.cvstudio\ncvstudio = skillsnetwork.cvstudio.CVStudio(\'token\')\n\ncvstudio.report(started=datetime.now(), completed=datetime.now())\n\ncvstudio.report(url="http://vision.skills.network")\n```\n\n### CLI example\n```bash\npython -m \'skillsnetwork.cvstudio\'\n```\n\n## Contributing\nPlease see [CONTRIBUTING.md](https://github.com/ibm-skills-network/skillsnetwork-python-library/blob/main/CONTRIBUTING.md)\n',
    'author': 'Bradley Steinfeld',
    'author_email': 'bs@ibm.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
