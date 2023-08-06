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
['ipython>=8.4.0,<9.0.0',
 'ipywidgets>=7.7.0,<8.0.0',
 'requests>=2.28.0,<3.0.0',
 'tqdm>=4.64.0,<5.0.0']

extras_require = \
{'regular': ['ibm-cos-sdk>=2.11,<3.0']}

setup_kwargs = {
    'name': 'skillsnetwork',
    'version': '0.19.0.dev0',
    'description': 'Library for working with Skills Network',
    'long_description': '# Skills Network Python Library\n\n## Installation\n### JupyterLite Installation\npip install skillsnetwork\n\n### Regular Installation\npip install skillsnetwork[regular]\n\n## Usage\n\nTODO\n## cvstudio\n\n### Environment Variables\n- `CV_STUDIO_TOKEN`\n- `CV_STUDIO_BASE_URL`\n- `IBMCLOUD_API_KEY`\n\n### Python Code example\n```\nfrom datetime import datetime\nimport skillsnetwork.cvstudio\ncvstudio = skillsnetwork.cvstudio.CVStudio(\'token\')\n\ncvstudio.report(started=datetime.now(), completed=datetime.now())\n\ncvstudio.report(url="http://vision.skills.network")\n```\n\n### CLI example\n```\n# export CV_STUDIO_TOKEN="<token>"\n# export CV_STUDIO_BASE_URL="<baseurl>"\n\ncvstudio_report exampleTrainingRun.json\n```\n\n## Contributing\nPlease see [CONTRIBUTING.md](./CONTRIBUTING.md)\n\n## Publishing\n### From local\n```bash\npoetry publish\n```\n### From CI\nTODO\n',
    'author': 'Bradley Steinfeld',
    'author_email': 'bs@ibm.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
