![Logo](https://github.com/boonlogic/amber-python-sdk/blob/master/docs/BoonLogic.png?raw=true)

# Boon Amber Python SDK

An SDK for Boon Amber sensor analytics

- __Website__: [boonlogic.com](https://boonlogic.com)
- __Documentation__: [Boon Docs Main Page](https://docs.boonlogic.com)
- __SDK Functional Breakdown__: [amber-python-sdk classes and methods](https://boonlogic.github.io/amber-python-sdk/docs/boonamber/index.html)

## Installation

The Boon Amber SDK is a Python 3 project and can be installed via pip.

```
pip install boonamber
```

## Credentials setup

Note: An account in the Boon Amber cloud must be obtained from Boon Logic to use the Amber SDK.

The username and password should be placed in a file named _~/.Amber.license_ whose contents are the following:

```json
{
    "default": {
        "username": "AMBER-ACCOUNT-USERNAME",
        "password": "AMBER-ACCOUNT-PASSWORD",
        "server": "https://amber.boonlogic.com/v1"
    }
}
```

The _~/.Amber.license_ file will be consulted by the Amber SDK to find and authenticate your account credentials with the Amber server. Credentials may optionally be provided instead via the environment variables `AMBER_USERNAME` and `AMBER_PASSWORD`.

## Connectivity test

The following Python script provides a basic proof-of-connectivity:

[connect-example.py](examples/connect-example.py)

```python
import sys
import json
from boonamber import AmberClient, AmberCloudError, AmberUserError

# if you wish to turn off tls certificate warnings
# import urllib3
# urllib3.disable_warnings()
#
# Alternatively invoke python with -Wignore
#

# At initialization the client discovers Amber account credentials
# under the "default" entry in the ~/.Amber.license file.
#amber = AmberClient(verify=False)
amber = AmberClient()

try:
    # Get a list of all sensors belonging to the current user.
    version_info = amber.get_version()
except AmberCloudError as e:
    # AmberCloudError is raised upon any error response from the Amber server.
    print("Amber Cloud error: {}".format(e))
    sys.exit(1)
except AmberUserError as e:
    # AmberUserError is raised upon client-side usage errors with the SDK.
    print("Amber user error: {}".format(e))
    sys.exit(1)

print(json.dumps(version_info, indent=4))
```

Running the connect-example.py script should yield output like the following:
```
$ python connect-example.py
{
    "release": "0.0.405",
    "api-version": "/v1",
    "builder": "ec74f421",
    "expert-api": "dee23681",
    "expert-common": "300a588e",
    "nano-secure": "61c431e2",
    "swagger-ui": "914af396"
}
```
where the dictionary `{}` lists all sensors that currently exist under the given Boon Amber account.

## Full Example

Example to demonstrate each API call

[full-example.py](examples/full-example.py)

## Advanced CSV file processor

Example of streaming a .csv file.  Full Amber analytic results will be displayed after each streaming request.  

[stream-advanced.py](examples/stream-advanced.py)<br>
[output_current.csv](examples/output_current.csv)


## Pretrain example

Example of pretraining a .csv file

[pretrain-example.py](examples/pretrain-example.py)<br>
[output_current.csv](examples/output_current.csv)
