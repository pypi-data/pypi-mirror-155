'''
# kong-core

[![NPM version](https://badge.fury.io/js/kong-core.svg)](https://badge.fury.io/js/kong-core)
[![PyPI version](https://badge.fury.io/py/kong-core.svg)](https://badge.fury.io/py/kong-core)

![Downloads](https://img.shields.io/badge/-DOWNLOADS:-brightgreen?color=gray)
![npm](https://img.shields.io/npm/dt/kong-core?label=npm&color=orange)
![PyPI](https://img.shields.io/pypi/dm/kong-core?label=pypi&color=blue)

Use this Kong CDK Construct Library to deploy Core common infrastructural constructs .

This CDK library automatically creates and configures recommended architecture on AWS by:

* *Amazon EKS*

  * Well architected EKS cluster from networking standpoint
  * Cluster autoscaler
  * Node termination handler
  * Secrets management from AWS Secrets Manager using CSI driver
  * mTLS using AWS ACM for pod to pod communication using private certificate authority and aws-pca-issuer
  * Use of IAM Role for Service Account (IRSA) where applicable
  * AWS EKS encryption at rest
  * Metrics server installation
  * Logs and metrics to cloudwatch using AWS CloudWatch Container insights
* *Elasticache*

  * private accessibility
  * multi az
  * auto failover
  * auto minor version upgrade
  * cwl output
* *RDS Features*

  * Encryption at rest
  * Private subnets
  * Multiaz
  * auto backup
  * Logs output to CloudWatch

## npm Package Installation:

```
yarn add --dev kong-core
# or
npm install kong-core --save-dev
```

## PyPI Package Installation:

```
pip install kong-core
```

# Sample

Try out https://github.com/kong/aws-samples for the complete sample application and instructions.

## Resources to learn about CDK

* [CDK TypeScript Workshop](https://cdkworkshop.com/20-typescript.html)
* [Video Introducing CDK by AWS with Demo](https://youtu.be/ZWCvNFUN-sU)
* [CDK Concepts](https://youtu.be/9As_ZIjUGmY)

## Related

Kong on AWS Hands on Workshop - https://kong.awsworkshop.io/

## Useful commands

* `rm -rf node_modules && rm package.json && rm package-lock.json && rm yarn.lock && rm tsconfig.dev.json` cleans the directory
* `npm install projen` installs projen
* `npx projen build`   Test + Compile + Build JSII packages
* `npx projen watch`   compile and run watch in background
* `npm run test`    perform the jest unit tests

## Tips

* Use a locked down version of `constructs` and `aws-cdk-lib`. Even with CDK V2 i saw https://github.com/aws/aws-cdk/issues/542 repeating when there is minor version mismatch of construcs. AWS CDK init commands generate package.json file without locked down version of constructs library.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_autoscaling
import aws_cdk.aws_certificatemanager
import aws_cdk.aws_ec2
import aws_cdk.aws_ecs
import aws_cdk.aws_eks
import aws_cdk.aws_elasticloadbalancingv2
import aws_cdk.aws_rds
import aws_cdk.aws_route53
import aws_cdk.aws_sqs
import constructs


class AcmPca(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="kong-core.AcmPca",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        hosted_zone_name: builtins.str,
        vpc: aws_cdk.aws_ec2.IVpc,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param hosted_zone_name: 
        :param vpc: 
        '''
        props = AcmPcaProps(hosted_zone_name=hosted_zone_name, vpc=vpc)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="privateCaArn")
    def private_ca_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateCaArn"))

    @private_ca_arn.setter
    def private_ca_arn(self, value: builtins.str) -> None:
        jsii.set(self, "privateCaArn", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="route53Zone")
    def route53_zone(self) -> aws_cdk.aws_route53.PrivateHostedZone:
        return typing.cast(aws_cdk.aws_route53.PrivateHostedZone, jsii.get(self, "route53Zone"))

    @route53_zone.setter
    def route53_zone(self, value: aws_cdk.aws_route53.PrivateHostedZone) -> None:
        jsii.set(self, "route53Zone", value)


@jsii.data_type(
    jsii_type="kong-core.AcmPcaProps",
    jsii_struct_bases=[],
    name_mapping={"hosted_zone_name": "hostedZoneName", "vpc": "vpc"},
)
class AcmPcaProps:
    def __init__(
        self,
        *,
        hosted_zone_name: builtins.str,
        vpc: aws_cdk.aws_ec2.IVpc,
    ) -> None:
        '''
        :param hosted_zone_name: 
        :param vpc: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "hosted_zone_name": hosted_zone_name,
            "vpc": vpc,
        }

    @builtins.property
    def hosted_zone_name(self) -> builtins.str:
        result = self._values.get("hosted_zone_name")
        assert result is not None, "Required property 'hosted_zone_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(aws_cdk.aws_ec2.IVpc, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AcmPcaProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AutoScalar(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="kong-core.AutoScalar",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cluster: aws_cdk.aws_eks.Cluster,
        namespace: builtins.str,
        nodegroup: aws_cdk.aws_eks.Nodegroup,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cluster: 
        :param namespace: 
        :param nodegroup: 
        '''
        props = AutoScalarProps(
            cluster=cluster, namespace=namespace, nodegroup=nodegroup
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="kong-core.AutoScalarProps",
    jsii_struct_bases=[],
    name_mapping={
        "cluster": "cluster",
        "namespace": "namespace",
        "nodegroup": "nodegroup",
    },
)
class AutoScalarProps:
    def __init__(
        self,
        *,
        cluster: aws_cdk.aws_eks.Cluster,
        namespace: builtins.str,
        nodegroup: aws_cdk.aws_eks.Nodegroup,
    ) -> None:
        '''
        :param cluster: 
        :param namespace: 
        :param nodegroup: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "cluster": cluster,
            "namespace": namespace,
            "nodegroup": nodegroup,
        }

    @builtins.property
    def cluster(self) -> aws_cdk.aws_eks.Cluster:
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(aws_cdk.aws_eks.Cluster, result)

    @builtins.property
    def namespace(self) -> builtins.str:
        result = self._values.get("namespace")
        assert result is not None, "Required property 'namespace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def nodegroup(self) -> aws_cdk.aws_eks.Nodegroup:
        result = self._values.get("nodegroup")
        assert result is not None, "Required property 'nodegroup' is missing"
        return typing.cast(aws_cdk.aws_eks.Nodegroup, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutoScalarProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AwsCertManager(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="kong-core.AwsCertManager",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cluster: aws_cdk.aws_eks.Cluster,
        cluster_issuer_name: builtins.str,
        private_ca_arn: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cluster: 
        :param cluster_issuer_name: 
        :param private_ca_arn: 
        '''
        props = AwsCertManagerProps(
            cluster=cluster,
            cluster_issuer_name=cluster_issuer_name,
            private_ca_arn=private_ca_arn,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="kong-core.AwsCertManagerProps",
    jsii_struct_bases=[],
    name_mapping={
        "cluster": "cluster",
        "cluster_issuer_name": "clusterIssuerName",
        "private_ca_arn": "privateCaArn",
    },
)
class AwsCertManagerProps:
    def __init__(
        self,
        *,
        cluster: aws_cdk.aws_eks.Cluster,
        cluster_issuer_name: builtins.str,
        private_ca_arn: builtins.str,
    ) -> None:
        '''
        :param cluster: 
        :param cluster_issuer_name: 
        :param private_ca_arn: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "cluster": cluster,
            "cluster_issuer_name": cluster_issuer_name,
            "private_ca_arn": private_ca_arn,
        }

    @builtins.property
    def cluster(self) -> aws_cdk.aws_eks.Cluster:
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(aws_cdk.aws_eks.Cluster, result)

    @builtins.property
    def cluster_issuer_name(self) -> builtins.str:
        result = self._values.get("cluster_issuer_name")
        assert result is not None, "Required property 'cluster_issuer_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def private_ca_arn(self) -> builtins.str:
        result = self._values.get("private_ca_arn")
        assert result is not None, "Required property 'private_ca_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsCertManagerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Certificates(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="kong-core.Certificates",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        dns_names: typing.Sequence[builtins.str],
        private_ca_arn: builtins.str,
        top_level_domain: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param dns_names: 
        :param private_ca_arn: 
        :param top_level_domain: 
        '''
        props = KongCertificatesProps(
            dns_names=dns_names,
            private_ca_arn=private_ca_arn,
            top_level_domain=top_level_domain,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> aws_cdk.aws_certificatemanager.CfnCertificate:
        return typing.cast(aws_cdk.aws_certificatemanager.CfnCertificate, jsii.get(self, "certificate"))

    @certificate.setter
    def certificate(self, value: aws_cdk.aws_certificatemanager.CfnCertificate) -> None:
        jsii.set(self, "certificate", value)


class CustomImage(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="kong-core.CustomImage",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        image_name: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param image_name: 
        '''
        props = KongCustomImageProps(image_name=image_name)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="kongCustomImage")
    def kong_custom_image(self) -> aws_cdk.aws_ecs.ContainerImage:
        return typing.cast(aws_cdk.aws_ecs.ContainerImage, jsii.get(self, "kongCustomImage"))

    @kong_custom_image.setter
    def kong_custom_image(self, value: aws_cdk.aws_ecs.ContainerImage) -> None:
        jsii.set(self, "kongCustomImage", value)


class EksNodeHandler(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="kong-core.EksNodeHandler",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cluster: aws_cdk.aws_eks.Cluster,
        nodegroup: aws_cdk.aws_autoscaling.AutoScalingGroup,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cluster: 
        :param nodegroup: 
        '''
        props = NodeHandlerProps(cluster=cluster, nodegroup=nodegroup)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="notificationQueue")
    def notification_queue(self) -> aws_cdk.aws_sqs.Queue:
        return typing.cast(aws_cdk.aws_sqs.Queue, jsii.get(self, "notificationQueue"))

    @notification_queue.setter
    def notification_queue(self, value: aws_cdk.aws_sqs.Queue) -> None:
        jsii.set(self, "notificationQueue", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> aws_cdk.aws_eks.ServiceAccount:
        return typing.cast(aws_cdk.aws_eks.ServiceAccount, jsii.get(self, "serviceAccount"))

    @service_account.setter
    def service_account(self, value: aws_cdk.aws_eks.ServiceAccount) -> None:
        jsii.set(self, "serviceAccount", value)


class ElastiCacheStack(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="kong-core.ElastiCacheStack",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        numberofnodegroups: jsii.Number,
        vpc: aws_cdk.aws_ec2.IVpc,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param numberofnodegroups: 
        :param vpc: 
        '''
        props = ElastiCacheStackProps(numberofnodegroups=numberofnodegroups, vpc=vpc)

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="kong-core.ElastiCacheStackProps",
    jsii_struct_bases=[],
    name_mapping={"numberofnodegroups": "numberofnodegroups", "vpc": "vpc"},
)
class ElastiCacheStackProps:
    def __init__(
        self,
        *,
        numberofnodegroups: jsii.Number,
        vpc: aws_cdk.aws_ec2.IVpc,
    ) -> None:
        '''
        :param numberofnodegroups: 
        :param vpc: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "numberofnodegroups": numberofnodegroups,
            "vpc": vpc,
        }

    @builtins.property
    def numberofnodegroups(self) -> jsii.Number:
        result = self._values.get("numberofnodegroups")
        assert result is not None, "Required property 'numberofnodegroups' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(aws_cdk.aws_ec2.IVpc, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ElastiCacheStackProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExternalDns(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="kong-core.ExternalDns",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cluster: aws_cdk.aws_eks.Cluster,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cluster: 
        '''
        props = ExternalDnsProps(cluster=cluster)

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="kong-core.ExternalDnsProps",
    jsii_struct_bases=[],
    name_mapping={"cluster": "cluster"},
)
class ExternalDnsProps:
    def __init__(self, *, cluster: aws_cdk.aws_eks.Cluster) -> None:
        '''
        :param cluster: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "cluster": cluster,
        }

    @builtins.property
    def cluster(self) -> aws_cdk.aws_eks.Cluster:
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(aws_cdk.aws_eks.Cluster, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalDnsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="kong-core.KongCertificatesProps",
    jsii_struct_bases=[],
    name_mapping={
        "dns_names": "dnsNames",
        "private_ca_arn": "privateCaArn",
        "top_level_domain": "topLevelDomain",
    },
)
class KongCertificatesProps:
    def __init__(
        self,
        *,
        dns_names: typing.Sequence[builtins.str],
        private_ca_arn: builtins.str,
        top_level_domain: builtins.str,
    ) -> None:
        '''
        :param dns_names: 
        :param private_ca_arn: 
        :param top_level_domain: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "dns_names": dns_names,
            "private_ca_arn": private_ca_arn,
            "top_level_domain": top_level_domain,
        }

    @builtins.property
    def dns_names(self) -> typing.List[builtins.str]:
        result = self._values.get("dns_names")
        assert result is not None, "Required property 'dns_names' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def private_ca_arn(self) -> builtins.str:
        result = self._values.get("private_ca_arn")
        assert result is not None, "Required property 'private_ca_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def top_level_domain(self) -> builtins.str:
        result = self._values.get("top_level_domain")
        assert result is not None, "Required property 'top_level_domain' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KongCertificatesProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="kong-core.KongCustomImageProps",
    jsii_struct_bases=[],
    name_mapping={"image_name": "imageName"},
)
class KongCustomImageProps:
    def __init__(self, *, image_name: builtins.str) -> None:
        '''
        :param image_name: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "image_name": image_name,
        }

    @builtins.property
    def image_name(self) -> builtins.str:
        result = self._values.get("image_name")
        assert result is not None, "Required property 'image_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KongCustomImageProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MetricsServer(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="kong-core.MetricsServer",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cluster: aws_cdk.aws_eks.Cluster,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cluster: 
        '''
        props = MetricsServerProps(cluster=cluster)

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="kong-core.MetricsServerProps",
    jsii_struct_bases=[],
    name_mapping={"cluster": "cluster"},
)
class MetricsServerProps:
    def __init__(self, *, cluster: aws_cdk.aws_eks.Cluster) -> None:
        '''
        :param cluster: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "cluster": cluster,
        }

    @builtins.property
    def cluster(self) -> aws_cdk.aws_eks.Cluster:
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(aws_cdk.aws_eks.Cluster, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetricsServerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="kong-core.Namespace")
class Namespace(enum.Enum):
    KONG_CONTROL_PLANE = "KONG_CONTROL_PLANE"
    TELEMETRY = "TELEMETRY"
    KONG_DATA_PLANE = "KONG_DATA_PLANE"
    AWS_PCA_ISSUER = "AWS_PCA_ISSUER"
    CERT_MANAGER = "CERT_MANAGER"


@jsii.enum(jsii_type="kong-core.Nlb")
class Nlb(enum.Enum):
    KONG_CP_ADMIN_LB_SUFFIX = "KONG_CP_ADMIN_LB_SUFFIX"
    KONG_CP_MANAGER_LB_SUFFIX = "KONG_CP_MANAGER_LB_SUFFIX"
    KONG_CP_DEVPORTAL_LB_SUFFIX = "KONG_CP_DEVPORTAL_LB_SUFFIX"
    KONG_DP_LB_SUFFIX = "KONG_DP_LB_SUFFIX"


@jsii.data_type(
    jsii_type="kong-core.NlbProps",
    jsii_struct_bases=[],
    name_mapping={"internet_facing": "internetFacing", "name": "name", "vpc": "vpc"},
)
class NlbProps:
    def __init__(
        self,
        *,
        internet_facing: builtins.bool,
        name: builtins.str,
        vpc: aws_cdk.aws_ec2.IVpc,
    ) -> None:
        '''
        :param internet_facing: 
        :param name: 
        :param vpc: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "internet_facing": internet_facing,
            "name": name,
            "vpc": vpc,
        }

    @builtins.property
    def internet_facing(self) -> builtins.bool:
        result = self._values.get("internet_facing")
        assert result is not None, "Required property 'internet_facing' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(aws_cdk.aws_ec2.IVpc, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NlbProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NlbStack(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="kong-core.NlbStack",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        internet_facing: builtins.bool,
        name: builtins.str,
        vpc: aws_cdk.aws_ec2.IVpc,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param internet_facing: 
        :param name: 
        :param vpc: 
        '''
        props = NlbProps(internet_facing=internet_facing, name=name, vpc=vpc)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="kongNlb")
    def kong_nlb(self) -> aws_cdk.aws_elasticloadbalancingv2.NetworkLoadBalancer:
        return typing.cast(aws_cdk.aws_elasticloadbalancingv2.NetworkLoadBalancer, jsii.get(self, "kongNlb"))

    @kong_nlb.setter
    def kong_nlb(
        self,
        value: aws_cdk.aws_elasticloadbalancingv2.NetworkLoadBalancer,
    ) -> None:
        jsii.set(self, "kongNlb", value)


@jsii.data_type(
    jsii_type="kong-core.NodeHandlerProps",
    jsii_struct_bases=[],
    name_mapping={"cluster": "cluster", "nodegroup": "nodegroup"},
)
class NodeHandlerProps:
    def __init__(
        self,
        *,
        cluster: aws_cdk.aws_eks.Cluster,
        nodegroup: aws_cdk.aws_autoscaling.AutoScalingGroup,
    ) -> None:
        '''
        :param cluster: 
        :param nodegroup: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "cluster": cluster,
            "nodegroup": nodegroup,
        }

    @builtins.property
    def cluster(self) -> aws_cdk.aws_eks.Cluster:
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(aws_cdk.aws_eks.Cluster, result)

    @builtins.property
    def nodegroup(self) -> aws_cdk.aws_autoscaling.AutoScalingGroup:
        result = self._values.get("nodegroup")
        assert result is not None, "Required property 'nodegroup' is missing"
        return typing.cast(aws_cdk.aws_autoscaling.AutoScalingGroup, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NodeHandlerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="kong-core.RdsProps",
    jsii_struct_bases=[],
    name_mapping={
        "databasename": "databasename",
        "postgresversion": "postgresversion",
        "username": "username",
        "vpc": "vpc",
    },
)
class RdsProps:
    def __init__(
        self,
        *,
        databasename: builtins.str,
        postgresversion: aws_cdk.aws_rds.PostgresEngineVersion,
        username: builtins.str,
        vpc: aws_cdk.aws_ec2.IVpc,
    ) -> None:
        '''
        :param databasename: 
        :param postgresversion: 
        :param username: 
        :param vpc: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "databasename": databasename,
            "postgresversion": postgresversion,
            "username": username,
            "vpc": vpc,
        }

    @builtins.property
    def databasename(self) -> builtins.str:
        result = self._values.get("databasename")
        assert result is not None, "Required property 'databasename' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def postgresversion(self) -> aws_cdk.aws_rds.PostgresEngineVersion:
        result = self._values.get("postgresversion")
        assert result is not None, "Required property 'postgresversion' is missing"
        return typing.cast(aws_cdk.aws_rds.PostgresEngineVersion, result)

    @builtins.property
    def username(self) -> builtins.str:
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(aws_cdk.aws_ec2.IVpc, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RdsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RdsStack(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="kong-core.RdsStack",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        databasename: builtins.str,
        postgresversion: aws_cdk.aws_rds.PostgresEngineVersion,
        username: builtins.str,
        vpc: aws_cdk.aws_ec2.IVpc,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param databasename: 
        :param postgresversion: 
        :param username: 
        :param vpc: 
        '''
        props = RdsProps(
            databasename=databasename,
            postgresversion=postgresversion,
            username=username,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="kongPostgresSql")
    def kong_postgres_sql(self) -> aws_cdk.aws_rds.DatabaseInstance:
        return typing.cast(aws_cdk.aws_rds.DatabaseInstance, jsii.get(self, "kongPostgresSql"))

    @kong_postgres_sql.setter
    def kong_postgres_sql(self, value: aws_cdk.aws_rds.DatabaseInstance) -> None:
        jsii.set(self, "kongPostgresSql", value)


class SecretsManager(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="kong-core.SecretsManager",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cluster: aws_cdk.aws_eks.Cluster,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cluster: 
        '''
        props = SecretsManagerProps(cluster=cluster)

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="kong-core.SecretsManagerProps",
    jsii_struct_bases=[],
    name_mapping={"cluster": "cluster"},
)
class SecretsManagerProps:
    def __init__(self, *, cluster: aws_cdk.aws_eks.Cluster) -> None:
        '''
        :param cluster: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "cluster": cluster,
        }

    @builtins.property
    def cluster(self) -> aws_cdk.aws_eks.Cluster:
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(aws_cdk.aws_eks.Cluster, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretsManagerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Telemetry(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="kong-core.Telemetry",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cacertname: builtins.str,
        cluster: aws_cdk.aws_eks.Cluster,
        cluster_issuer_name: builtins.str,
        create_prometheus_workspace: builtins.bool,
        dns_names: typing.Sequence[builtins.str],
        hosted_zone_name: builtins.str,
        namespace: builtins.str,
        prometheus_endpoint: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cacertname: 
        :param cluster: 
        :param cluster_issuer_name: 
        :param create_prometheus_workspace: 
        :param dns_names: 
        :param hosted_zone_name: 
        :param namespace: 
        :param prometheus_endpoint: 
        '''
        props = TelemetryProps(
            cacertname=cacertname,
            cluster=cluster,
            cluster_issuer_name=cluster_issuer_name,
            create_prometheus_workspace=create_prometheus_workspace,
            dns_names=dns_names,
            hosted_zone_name=hosted_zone_name,
            namespace=namespace,
            prometheus_endpoint=prometheus_endpoint,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="prometheusEndpoint")
    def prometheus_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prometheusEndpoint"))

    @prometheus_endpoint.setter
    def prometheus_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "prometheusEndpoint", value)


@jsii.data_type(
    jsii_type="kong-core.TelemetryProps",
    jsii_struct_bases=[],
    name_mapping={
        "cacertname": "cacertname",
        "cluster": "cluster",
        "cluster_issuer_name": "clusterIssuerName",
        "create_prometheus_workspace": "createPrometheusWorkspace",
        "dns_names": "dnsNames",
        "hosted_zone_name": "hostedZoneName",
        "namespace": "namespace",
        "prometheus_endpoint": "prometheusEndpoint",
    },
)
class TelemetryProps:
    def __init__(
        self,
        *,
        cacertname: builtins.str,
        cluster: aws_cdk.aws_eks.Cluster,
        cluster_issuer_name: builtins.str,
        create_prometheus_workspace: builtins.bool,
        dns_names: typing.Sequence[builtins.str],
        hosted_zone_name: builtins.str,
        namespace: builtins.str,
        prometheus_endpoint: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cacertname: 
        :param cluster: 
        :param cluster_issuer_name: 
        :param create_prometheus_workspace: 
        :param dns_names: 
        :param hosted_zone_name: 
        :param namespace: 
        :param prometheus_endpoint: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "cacertname": cacertname,
            "cluster": cluster,
            "cluster_issuer_name": cluster_issuer_name,
            "create_prometheus_workspace": create_prometheus_workspace,
            "dns_names": dns_names,
            "hosted_zone_name": hosted_zone_name,
            "namespace": namespace,
        }
        if prometheus_endpoint is not None:
            self._values["prometheus_endpoint"] = prometheus_endpoint

    @builtins.property
    def cacertname(self) -> builtins.str:
        result = self._values.get("cacertname")
        assert result is not None, "Required property 'cacertname' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster(self) -> aws_cdk.aws_eks.Cluster:
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(aws_cdk.aws_eks.Cluster, result)

    @builtins.property
    def cluster_issuer_name(self) -> builtins.str:
        result = self._values.get("cluster_issuer_name")
        assert result is not None, "Required property 'cluster_issuer_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def create_prometheus_workspace(self) -> builtins.bool:
        result = self._values.get("create_prometheus_workspace")
        assert result is not None, "Required property 'create_prometheus_workspace' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def dns_names(self) -> typing.List[builtins.str]:
        result = self._values.get("dns_names")
        assert result is not None, "Required property 'dns_names' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def hosted_zone_name(self) -> builtins.str:
        result = self._values.get("hosted_zone_name")
        assert result is not None, "Required property 'hosted_zone_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace(self) -> builtins.str:
        result = self._values.get("namespace")
        assert result is not None, "Required property 'namespace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def prometheus_endpoint(self) -> typing.Optional[builtins.str]:
        result = self._values.get("prometheus_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TelemetryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="kong-core.Tls")
class Tls(enum.Enum):
    ADOT_CERTNAME = "ADOT_CERTNAME"
    KONG_CP_CERTNAME = "KONG_CP_CERTNAME"
    KONG_CP_CLUSTER_ISSUER_NAME = "KONG_CP_CLUSTER_ISSUER_NAME"
    KONG_DP_CERTNAME = "KONG_DP_CERTNAME"
    KONG_DP_CLUSTER_ISSUER_NAME = "KONG_DP_CLUSTER_ISSUER_NAME"


__all__ = [
    "AcmPca",
    "AcmPcaProps",
    "AutoScalar",
    "AutoScalarProps",
    "AwsCertManager",
    "AwsCertManagerProps",
    "Certificates",
    "CustomImage",
    "EksNodeHandler",
    "ElastiCacheStack",
    "ElastiCacheStackProps",
    "ExternalDns",
    "ExternalDnsProps",
    "KongCertificatesProps",
    "KongCustomImageProps",
    "MetricsServer",
    "MetricsServerProps",
    "Namespace",
    "Nlb",
    "NlbProps",
    "NlbStack",
    "NodeHandlerProps",
    "RdsProps",
    "RdsStack",
    "SecretsManager",
    "SecretsManagerProps",
    "Telemetry",
    "TelemetryProps",
    "Tls",
]

publication.publish()
