# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['static_site']

package_data = \
{'': ['*']}

install_requires = \
['aws-cdk-lib>=2.28,<3.0']

setup_kwargs = {
    'name': 'cdk-static-site',
    'version': '0.1.1',
    'description': '',
    'long_description': '# CDK Static Website Construct\n\nThis package contains a high-level CDK construct for describing the infrastructure of\na static website. The construct also features a `deploy` method to deploy static assets\nfor the website and invalidate the CloudFront distribution.\n\nThe CDK construct creates the private S3 bucket, where the website is hosted. The contents\nof the bucket are exposed through a CloudFront distribution. Rather than allowing public\naccess to the bucket, OAI is used to allow access from CloudFront only.\n\nFurther reading: https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html\n\nThis construct also creates the necessary Route 53 records to route requests to\nthe CloudFront distribution. It also configures the distribution with a supplied\nSSL certificate.\n\n## Pre-requisites\n\nThis construct works with recent versions of CDK v2. There are similar constructs\non PyPI for v1 - one of the motivations for this package was to support v2.\n\nIf you are not familiar with CDK, have a read [here](https://aws.amazon.com/cdk/).\n\nRegistering a domain name, creating the hosted zone in Route 53 and creating the SSL\ncertificate are not in scope for this construct. These can be created manually or\nthrough other automated ways on AWS.\n\nNote, the certificate needs to be created in North Virginia (us-east-1).\n\nOnce these are created, you should have all the necessary inputs: the domain name,\ndomain certificate ARN, the hosted zone ID and the hosted zone name.\n\n## How to use it?\n\nInstall the package using your favourite package manager, e.g.\n\n```shell\npip install cdk-static-site\n```\n\nWithin your stack, instantiate the construct\n```python\nfrom static_site import StaticSite\n\nsite = StaticSite(\n    scope=self,\n    construct_id="StaticSite",\n    site_domain_name=site_domain_name,\n    hosted_zone_id=hosted_zone_id,\n    hosted_zone_name=hosted_zone_name,\n    domain_certificate_arn=domain_certificate_arn,\n)\n```\n\nand finally, deploy the static contents by supplying the directory path\nto `deploy`:\n\n```python\nfrom pathlib import Path\n\ncontents_path = Path.cwd() / "public"  # or wherever your assets are located\nsite.deploy(contents_path.as_posix())\n```\n\n## Contribution\n\nIf you find any issues, or have suggestions to improve the construct, feel free to\nopen an issue/PR.\n',
    'author': 'David Steiner',
    'author_email': 'david_j_steiner@yahoo.co.nz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/davidsteiner/cdk-static-site',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
