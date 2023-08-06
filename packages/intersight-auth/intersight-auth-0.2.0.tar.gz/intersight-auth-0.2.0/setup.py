# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['intersight_auth']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=37.0.2,<38.0.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'intersight-auth',
    'version': '0.2.0',
    'description': 'Intersight Authentication helper for requests',
    'long_description': '# intersight-auth\n\nThis module provides an authentication helper for requests to make it easy to make [Intersight API](https://intersight.com/apidocs/introduction/overview/) calls using [requests](https://requests.readthedocs.io/en/latest/). \n\n## Install\n\n```\npip install intersight-auth\n```\n\n## Example using a file for the secret key\n\n``` Python\nimport sys\n\nfrom intersight_auth import IntersightAuth\nfrom requests import Session\n\nsession = Session()\nsession.auth = IntersightAuth("XYZ/XYZ/XYZ", "key.pem")\n\nresponse = session.get("https://intersight.com/api/v1/ntp/Policies")\n\nif not response.ok:\n    print(f"Error: {response.status_code} {response.reason}")\n    sys.exit(1)\n\nfor policy in response.json()["Results"]:\n    print(f"{policy[\'Name\']}")\n```\n\n## Example using a multiline (a.k.a. heredoc) string for the secret key\n\nThe secret key must still be in PEM format even if it\'s a string instead of a file.\n\n``` Python\nmy_secret_key=\'\'\'\n-----BEGIN RSA PRIVATE KEY-----\nABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890/abcdefghizjklmnopqrstuvwxy\nABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890/abcdefghizjklmnopqrstuvwxy\nABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890/abcdefghizjklmnopqrstuvwxy\nABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890/abcdefghizjklmnopqrstuvwxy\nABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890/abcdefghizjklmnopqrstuvwxy\nABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890/abcdefghizjklmnopqrstuvwxy\nABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890/abcdefghizjklmnopqrstuvwxy\nABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890/abcdefghizjklmnopqrstuvwxy\nABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890/abcdefghizjklmnopqrstuvwxy\nABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890/abcdefghizjklmnopqrstuvwxy\nABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890/abcdefghizjklmnopqrstuvwxy\nABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890/abcdefghizjklmnopqrstuvwxy\nABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890/abcdefghizjklmnopqrstuvwxy\nABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890/abcdefghizjklmnopqrstuvwxy\nABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890/abcdefghizjklmnopqrstuvwxy\nABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890/abcdefghizjklmnopqrstuvwxy\nABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890/abcdefghizjklmnopqrstuvwxy\nABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890/abcdefghizjklmnopqrstuvwxy\nABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890/abcdefghizjklmnopqrstuvwxy\nABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890/abcdefghizjklmnopqrstuvwxy\nABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890/abcdefghizjklmnopqrstuvwxy\nABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890/abcdefghizjklmnopqrstuvwxy\nABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890/abcdefghizjklmnopqrstuvwxy\nABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890/abcdefghizjklmnopqrstuvwxy\nABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890/abcdefghizjklmnopqrstuvwxy\nABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890/abcdefghizjkl=\n-----END RSA PRIVATE KEY-----\n\'\'\'\n\nsession = Session()\nsession.auth = IntersightAuth(\n    api_key_id="XYZ/XYZ/XYZ", \n    secret_key_string=my_secret_key\n    )\n\nresponse = session.get("https://intersight.com/api/v1/ntp/Policies")\n\nif not response.ok:\n    print(f"Error: {response.status_code} {response.reason}")\n    sys.exit(1)\n\nfor policy in response.json()["Results"]:\n    print(f"{policy[\'Name\']}")\n```\n',
    'author': 'Chris Gascoigne',
    'author_email': 'cgascoig@cisco.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cgascoig/intersight-auth',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
