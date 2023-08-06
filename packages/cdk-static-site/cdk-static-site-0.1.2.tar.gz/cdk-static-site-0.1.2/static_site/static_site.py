from pathlib import Path

from aws_cdk import RemovalPolicy
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_cloudfront as cloudfront
from aws_cdk import aws_cloudfront_origins as origins
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_route53_targets as targets
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3_deployment
from constructs import Construct


class StaticSite(Construct):
    """CDK construct for the infrastructure and deployment of static websites."""

    def __init__(
        self,
        *,
        scope: Construct,
        construct_id: str,
        site_domain_name: str,
        hosted_zone_id: str,
        hosted_zone_name: str,
        domain_certificate_arn: str,
        **kwargs,
    ):
        """
        Create the infrastructure for the static website.

        Args:
            scope: The scope in which to define this construct.
            construct_id: The scoped construct ID.
            site_domain_name: The domain name where this site will be hosted.
            hosted_zone_id: The ID of the hosted zone created for the domain.
                This should be created beforehand either manually or through CDK/CloudFormation.
            hosted_zone_name: The name of the hosted zone created for the domain.
            domain_certificate_arn: The ARN of the SSL certificate created in AWS Certificate Manager.
                Note, this needs to be created in us-east-1.
            **kwargs:
        """
        super().__init__(scope, construct_id, **kwargs)

        self._bucket = self._create_site_bucket(site_domain_name)
        hosted_zone = self._get_hosted_zone(
            hosted_zone_name=hosted_zone_name,
            hosted_zone_id=hosted_zone_id,
        )
        certificate = self._get_certificate(certificate_arn=domain_certificate_arn)
        self._distribution = self._create_cloudfront_distribution(
            bucket=self.bucket,
            site_domain_name=site_domain_name,
            certificate=certificate,
        )
        self._create_route53_record(
            hosted_zone=hosted_zone,
            site_domain_name=site_domain_name,
            distribution=self._distribution,
        )

    def deploy(self, asset_path: str):
        """Deploy the static assets to the bucket and invalidate the distribution."""
        asset = s3_deployment.Source.asset(asset_path)
        s3_deployment.BucketDeployment(
            self,
            "S3Deployment",
            sources=[asset],
            destination_bucket=self.bucket,
            distribution=self.distribution,
            distribution_paths=["/*"],
        )

    @property
    def bucket(self) -> s3.IBucket:
        """The private S3 bucket the static assets will be uploaded to."""
        return self._bucket

    @property
    def distribution(self) -> cloudfront.IDistribution:
        """The CloudFront distribution exposing the contents of the S3 bucket."""
        return self._distribution

    def _create_site_bucket(self, site_domain_name: str) -> s3.Bucket:
        return s3.Bucket(
            self,
            "SiteBucket",
            bucket_name=site_domain_name,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

    def _create_cloudfront_distribution(
        self,
        *,
        bucket: s3.IBucket,
        site_domain_name: str,
        certificate: acm.ICertificate,
    ) -> cloudfront.IDistribution:
        # function_name is supplied to apply the workaround for https://github.com/aws/aws-cdk/issues/15523
        function_name = f"RouterFunction{self.node.addr}"

        function_code = Path(__file__).parent / "router.js"
        router_function = cloudfront.Function(
            self,
            function_name,
            code=cloudfront.FunctionCode.from_file(file_path=function_code.as_posix()),
            function_name=function_name,
        )

        return cloudfront.Distribution(
            self,
            "CloudFrontDistribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                function_associations=[
                    cloudfront.FunctionAssociation(
                        event_type=cloudfront.FunctionEventType.VIEWER_REQUEST,
                        function=router_function,
                    )
                ],
            ),
            domain_names=[site_domain_name],
            certificate=certificate,
            default_root_object="index.html",
        )

    def _get_hosted_zone(
        self, *, hosted_zone_name: str, hosted_zone_id: str
    ) -> route53.IHostedZone:
        return route53.HostedZone.from_hosted_zone_attributes(
            self,
            "HostedZone",
            zone_name=hosted_zone_name,
            hosted_zone_id=hosted_zone_id,
        )

    def _create_route53_record(
        self,
        *,
        hosted_zone: route53.IHostedZone,
        site_domain_name: str,
        distribution: cloudfront.IDistribution,
    ) -> route53.ARecord:
        return route53.ARecord(
            self,
            "SiteAliasRecord",
            record_name=site_domain_name,
            zone=hosted_zone,
            target=route53.RecordTarget.from_alias(
                targets.CloudFrontTarget(distribution)
            ),
        )

    def _get_certificate(self, certificate_arn: str) -> acm.ICertificate:
        return acm.Certificate.from_certificate_arn(
            self,
            "SiteCertificate",
            certificate_arn=certificate_arn,
        )
