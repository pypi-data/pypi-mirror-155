# requests-iam-session

AWSSession class that extends [BaseUrlSession](https://toolbelt.readthedocs.io/en/latest/sessions.html) from [requests](https://docs.python-requests.org/en/master/) and automatically authenticates through IAM. 

## Installation

```
poetry add requests-iam-session
```

## Usage example
```python
from requests_iam_session import AWSSession

session = AWSSession("https://example.com/")
response = session.get("/users/1")

print(response.json())
```
