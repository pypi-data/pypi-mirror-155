# CDK Static Website Construct

This package contains a high-level CDK construct for describing the infrastructure of
a static website. The construct also features a `deploy` method to deploy static assets
for the website and invalidate the CloudFront distribution.

The CDK construct creates the private S3 bucket, where the website is hosted. The contents
of the bucket are exposed through a CloudFront distribution. Rather than allowing public
access to the bucket, OAI is used to allow access from CloudFront only.

Further reading: https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html

This construct also creates the necessary Route 53 records to route requests to
the CloudFront distribution. It also configures the distribution with a supplied
SSL certificate.

## Pre-requisites

This construct works with recent versions of CDK v2. There are similar constructs
on PyPI for v1 - one of the motivations for this package was to support v2.

If you are not familiar with CDK, have a read [here](https://aws.amazon.com/cdk/).

Registering a domain name, creating the hosted zone in Route 53 and creating the SSL
certificate are not in scope for this construct. These can be created manually or
through other automated ways on AWS.

Note, the certificate needs to be created in North Virginia (us-east-1).

Once these are created, you should have all the necessary inputs: the domain name,
domain certificate ARN, the hosted zone ID and the hosted zone name.

## How to use it?

Install the package using your favourite package manager, e.g.

```shell
pip install cdk-static-site
```

Within your stack, instantiate the construct
```python
from static_site import StaticSite

site = StaticSite(
    scope=self,
    construct_id="StaticSite",
    site_domain_name=site_domain_name,
    hosted_zone_id=hosted_zone_id,
    hosted_zone_name=hosted_zone_name,
    domain_certificate_arn=domain_certificate_arn,
)
```

and finally, deploy the static contents by supplying the directory path
to `deploy`:

```python
from pathlib import Path

contents_path = Path.cwd() / "public"  # or wherever your assets are located
site.deploy(contents_path.as_posix())
```

## Contribution

If you find any issues, or have suggestions to improve the construct, feel free to
open an issue/PR.
