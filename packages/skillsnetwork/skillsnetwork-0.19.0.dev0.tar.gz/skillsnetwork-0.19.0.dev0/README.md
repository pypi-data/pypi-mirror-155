# Skills Network Python Library

## Installation
### JupyterLite Installation
pip install skillsnetwork

### Regular Installation
pip install skillsnetwork[regular]

## Usage

TODO
## cvstudio

### Environment Variables
- `CV_STUDIO_TOKEN`
- `CV_STUDIO_BASE_URL`
- `IBMCLOUD_API_KEY`

### Python Code example
```
from datetime import datetime
import skillsnetwork.cvstudio
cvstudio = skillsnetwork.cvstudio.CVStudio('token')

cvstudio.report(started=datetime.now(), completed=datetime.now())

cvstudio.report(url="http://vision.skills.network")
```

### CLI example
```
# export CV_STUDIO_TOKEN="<token>"
# export CV_STUDIO_BASE_URL="<baseurl>"

cvstudio_report exampleTrainingRun.json
```

## Contributing
Please see [CONTRIBUTING.md](./CONTRIBUTING.md)

## Publishing
### From local
```bash
poetry publish
```
### From CI
TODO
