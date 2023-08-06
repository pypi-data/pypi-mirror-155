# Skills Network Python Library

A python library for working with [Skills Network](https://skills.network).

## Installation
### JupyterLite Installation
```bash
pip install skillsnetwork
```

### Regular Installation (JupyterLab, CLI, etc.)
```bash
pip install skillsnetwork[regular]
```

## Usage

## JupyterLab / JupyterLite on Skills Network Labs
The `skillsnetwork` package provides a unified interface for reading/downloading
files in JupyterLab and JupyterLite.

### Reading a file
```python
content = await skillsnetwork.read("https://example.com/myfile")
```

### Downloading a file
```python
await skillsnetwork.download("https://example.com/myfile", filename=filename)
with open(filename, "r") as f:
    content = f.read()
```

## CV Studio

### Environment Variables
- `CV_STUDIO_TOKEN`
- `CV_STUDIO_BASE_URL`
- `IBMCLOUD_API_KEY`

### Python Code example
```python
from datetime import datetime
import skillsnetwork.cvstudio
cvstudio = skillsnetwork.cvstudio.CVStudio('token')

cvstudio.report(started=datetime.now(), completed=datetime.now())

cvstudio.report(url="http://vision.skills.network")
```

### CLI example
```bash
python -m 'skillsnetwork.cvstudio'
```

## Contributing
Please see [CONTRIBUTING.md](https://github.com/ibm-skills-network/skillsnetwork-python-library/blob/main/CONTRIBUTING.md)
