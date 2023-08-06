# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['resolve_ec2_id']
install_requires = \
['typer>=0.4.0,<0.5.0']

extras_require = \
{':python_version < "3.8"': ['typing-extensions>=4.0.1,<5.0.0']}

entry_points = \
{'console_scripts': ['resolve-ec2-id = resolve_ec2_id:app']}

setup_kwargs = {
    'name': 'resolve-ec2-id',
    'version': '1.0.1',
    'description': 'Look up the EC2 instance ID given an instance name.',
    'long_description': '# resolve-ec2-id\n\n## Links\n\n- [GitLab](https://gitlab.com/bmares/resolve-ec2-id)\n- [GitHub](https://github.com/maresb/resolve-ec2-id)\n- [PyPI](https://pypi.org/project/resolve-ec2-id/)\n\n## Introduction\n\nThis is a simple command-line tool which looks up the EC2 instance ID given an instance name:\n\n```bash\n$ resolve-ec2-id my-named-instance\ni-1234567890abcdef0\n```\n\nCurrently this tool only works with default credentials. Consider configuring them with environment variables or using a program like [aws-vault](https://github.com/99designs/aws-vault).\n\n## Alternatives\n\nThis package is perhaps not so useful because very similar functionality can be accomplished with AWS CLI as follows:\n\n```bash\naws ec2 describe-instances --filters \'Name=tag:Name,Values=my-named-instance\' --query \'Reservations[*].Instances[*].{Instance:InstanceId}\' --output text\n```\n\nHowever, this tool has slightly better error-handling; the above AWS CLI command will not generate an error in the case that no instance is found.\n\n## Installation\n\nIn order to install in a clean and isolated Python environment, it is recommended to use [pipx](https://github.com/pypa/pipx):\n\n```bash\npipx install resolve-ec2-id\n```\n\n## Examples\n\nAssuming you are using the Bash shell, to start an instance if you know the name but not the ID:\n\n```bash\n$ aws ec2 start-instances --output=yaml --instance-ids="$(resolve-ec2-id my-named-instance)"\nStartingInstances:\n- CurrentState:\n    Code: 0\n    Name: pending\n  InstanceId: i-1234567890abcdef0\n  PreviousState:\n    Code: 80\n    Name: stopped\n```\n\nThis can also be used from within Python:\n\n```python\nfrom resolve_ec2_id import resolve_ec2_id\n\nec2_id = resolve_ec2_id(\'my-named-instance\')\n```\n\n## Requirements\n\nBeyond the base dependencies which install automatically, this requires either [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) or [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#installation). (I did not make `boto3` a dependency because it isn\'t needed if AWS CLI is already installed.)\n',
    'author': 'Ben Mares',
    'author_email': 'services-resolve-ec2-id@tensorial.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
