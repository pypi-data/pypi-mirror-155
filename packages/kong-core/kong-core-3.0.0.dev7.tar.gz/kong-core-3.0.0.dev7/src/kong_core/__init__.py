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

import aws_cdk
import aws_cdk.aws_autoscaling
import aws_cdk.aws_certificatemanager
import aws_cdk.aws_ec2
import aws_cdk.aws_ecs
import aws_cdk.aws_eks
import aws_cdk.aws_elasticloadbalancingv2
import aws_cdk.aws_iam
import aws_cdk.aws_kms
import aws_cdk.aws_logs
import aws_cdk.aws_rds
import aws_cdk.aws_s3
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
        hosted_zone_name: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cluster: 
        :param hosted_zone_name: 
        '''
        props = ExternalDnsProps(cluster=cluster, hosted_zone_name=hosted_zone_name)

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="kong-core.ExternalDnsProps",
    jsii_struct_bases=[],
    name_mapping={"cluster": "cluster", "hosted_zone_name": "hostedZoneName"},
)
class ExternalDnsProps:
    def __init__(
        self,
        *,
        cluster: aws_cdk.aws_eks.Cluster,
        hosted_zone_name: builtins.str,
    ) -> None:
        '''
        :param cluster: 
        :param hosted_zone_name: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "cluster": cluster,
            "hosted_zone_name": hosted_zone_name,
        }

    @builtins.property
    def cluster(self) -> aws_cdk.aws_eks.Cluster:
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(aws_cdk.aws_eks.Cluster, result)

    @builtins.property
    def hosted_zone_name(self) -> builtins.str:
        result = self._values.get("hosted_zone_name")
        assert result is not None, "Required property 'hosted_zone_name' is missing"
        return typing.cast(builtins.str, result)

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
        character_set_name: typing.Optional[builtins.str] = None,
        credentials: typing.Optional[aws_cdk.aws_rds.Credentials] = None,
        storage_encrypted: typing.Optional[builtins.bool] = None,
        storage_encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        engine: aws_cdk.aws_rds.IInstanceEngine,
        allocated_storage: typing.Optional[jsii.Number] = None,
        allow_major_version_upgrade: typing.Optional[builtins.bool] = None,
        database_name: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional[aws_cdk.aws_ec2.InstanceType] = None,
        license_model: typing.Optional[aws_cdk.aws_rds.LicenseModel] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timezone: typing.Optional[builtins.str] = None,
        vpc: aws_cdk.aws_ec2.IVpc,
        auto_minor_version_upgrade: typing.Optional[builtins.bool] = None,
        availability_zone: typing.Optional[builtins.str] = None,
        backup_retention: typing.Optional[aws_cdk.Duration] = None,
        cloudwatch_logs_exports: typing.Optional[typing.Sequence[builtins.str]] = None,
        cloudwatch_logs_retention: typing.Optional[aws_cdk.aws_logs.RetentionDays] = None,
        cloudwatch_logs_retention_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        copy_tags_to_snapshot: typing.Optional[builtins.bool] = None,
        delete_automated_backups: typing.Optional[builtins.bool] = None,
        deletion_protection: typing.Optional[builtins.bool] = None,
        domain: typing.Optional[builtins.str] = None,
        domain_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        enable_performance_insights: typing.Optional[builtins.bool] = None,
        iam_authentication: typing.Optional[builtins.bool] = None,
        instance_identifier: typing.Optional[builtins.str] = None,
        iops: typing.Optional[jsii.Number] = None,
        max_allocated_storage: typing.Optional[jsii.Number] = None,
        monitoring_interval: typing.Optional[aws_cdk.Duration] = None,
        monitoring_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        multi_az: typing.Optional[builtins.bool] = None,
        option_group: typing.Optional[aws_cdk.aws_rds.IOptionGroup] = None,
        parameter_group: typing.Optional[aws_cdk.aws_rds.IParameterGroup] = None,
        performance_insight_encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        performance_insight_retention: typing.Optional[aws_cdk.aws_rds.PerformanceInsightRetention] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_backup_window: typing.Optional[builtins.str] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        processor_features: typing.Optional[aws_cdk.aws_rds.ProcessorFeatures] = None,
        publicly_accessible: typing.Optional[builtins.bool] = None,
        removal_policy: typing.Optional[aws_cdk.RemovalPolicy] = None,
        s3_export_buckets: typing.Optional[typing.Sequence[aws_cdk.aws_s3.IBucket]] = None,
        s3_export_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        s3_import_buckets: typing.Optional[typing.Sequence[aws_cdk.aws_s3.IBucket]] = None,
        s3_import_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        security_groups: typing.Optional[typing.Sequence[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        storage_type: typing.Optional[aws_cdk.aws_rds.StorageType] = None,
        subnet_group: typing.Optional[aws_cdk.aws_rds.ISubnetGroup] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param character_set_name: For supported engines, specifies the character set to associate with the DB instance. Default: - RDS default character set name
        :param credentials: Credentials for the administrative user. Default: - A username of 'admin' (or 'postgres' for PostgreSQL) and SecretsManager-generated password
        :param storage_encrypted: Indicates whether the DB instance is encrypted. Default: - true if storageEncryptionKey has been provided, false otherwise
        :param storage_encryption_key: The KMS key that's used to encrypt the DB instance. Default: - default master key if storageEncrypted is true, no key otherwise
        :param engine: The database engine.
        :param allocated_storage: The allocated storage size, specified in gibibytes (GiB). Default: 100
        :param allow_major_version_upgrade: Whether to allow major version upgrades. Default: false
        :param database_name: The name of the database. Default: - no name
        :param instance_type: The name of the compute and memory capacity for the instance. Default: - m5.large (or, more specifically, db.m5.large)
        :param license_model: The license model. Default: - RDS default license model
        :param parameters: The parameters in the DBParameterGroup to create automatically. You can only specify parameterGroup or parameters but not both. You need to use a versioned engine to auto-generate a DBParameterGroup. Default: - None
        :param timezone: The time zone of the instance. This is currently supported only by Microsoft Sql Server. Default: - RDS default timezone
        :param vpc: The VPC network where the DB subnet group should be created.
        :param auto_minor_version_upgrade: Indicates that minor engine upgrades are applied automatically to the DB instance during the maintenance window. Default: true
        :param availability_zone: The name of the Availability Zone where the DB instance will be located. Default: - no preference
        :param backup_retention: The number of days during which automatic DB snapshots are retained. Set to zero to disable backups. When creating a read replica, you must enable automatic backups on the source database instance by setting the backup retention to a value other than zero. Default: - Duration.days(1) for source instances, disabled for read replicas
        :param cloudwatch_logs_exports: The list of log types that need to be enabled for exporting to CloudWatch Logs. Default: - no log exports
        :param cloudwatch_logs_retention: The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``Infinity``. Default: - logs never expire
        :param cloudwatch_logs_retention_role: The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - a new role is created.
        :param copy_tags_to_snapshot: Indicates whether to copy all of the user-defined tags from the DB instance to snapshots of the DB instance. Default: true
        :param delete_automated_backups: Indicates whether automated backups should be deleted or retained when you delete a DB instance. Default: false
        :param deletion_protection: Indicates whether the DB instance should have deletion protection enabled. Default: - true if ``removalPolicy`` is RETAIN, false otherwise
        :param domain: The Active Directory directory ID to create the DB instance in. Default: - Do not join domain
        :param domain_role: The IAM role to be used when making API calls to the Directory Service. The role needs the AWS-managed policy AmazonRDSDirectoryServiceAccess or equivalent. Default: - The role will be created for you if {@link DatabaseInstanceNewProps#domain} is specified
        :param enable_performance_insights: Whether to enable Performance Insights for the DB instance. Default: - false, unless ``performanceInsightRentention`` or ``performanceInsightEncryptionKey`` is set.
        :param iam_authentication: Whether to enable mapping of AWS Identity and Access Management (IAM) accounts to database accounts. Default: false
        :param instance_identifier: A name for the DB instance. If you specify a name, AWS CloudFormation converts it to lowercase. Default: - a CloudFormation generated name
        :param iops: The number of I/O operations per second (IOPS) that the database provisions. The value must be equal to or greater than 1000. Default: - no provisioned iops
        :param max_allocated_storage: Upper limit to which RDS can scale the storage in GiB(Gibibyte). Default: - No autoscaling of RDS instance
        :param monitoring_interval: The interval, in seconds, between points when Amazon RDS collects enhanced monitoring metrics for the DB instance. Default: - no enhanced monitoring
        :param monitoring_role: Role that will be used to manage DB instance monitoring. Default: - A role is automatically created for you
        :param multi_az: Specifies if the database instance is a multiple Availability Zone deployment. Default: false
        :param option_group: The option group to associate with the instance. Default: - no option group
        :param parameter_group: The DB parameter group to associate with the instance. Default: - no parameter group
        :param performance_insight_encryption_key: The AWS KMS key for encryption of Performance Insights data. Default: - default master key
        :param performance_insight_retention: The amount of time, in days, to retain Performance Insights data. Default: 7
        :param port: The port for the instance. Default: - the default port for the chosen engine.
        :param preferred_backup_window: The daily time range during which automated backups are performed. Constraints: - Must be in the format ``hh24:mi-hh24:mi``. - Must be in Universal Coordinated Time (UTC). - Must not conflict with the preferred maintenance window. - Must be at least 30 minutes. Default: - a 30-minute window selected at random from an 8-hour block of time for each AWS Region. To see the time blocks available, see https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html#USER_WorkingWithAutomatedBackups.BackupWindow
        :param preferred_maintenance_window: The weekly time range (in UTC) during which system maintenance can occur. Format: ``ddd:hh24:mi-ddd:hh24:mi`` Constraint: Minimum 30-minute window Default: - a 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week. To see the time blocks available, see https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.Maintenance.html#Concepts.DBMaintenance
        :param processor_features: The number of CPU cores and the number of threads per core. Default: - the default number of CPU cores and threads per core for the chosen instance class. See https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html#USER_ConfigureProcessor
        :param publicly_accessible: Indicates whether the DB instance is an internet-facing instance. Default: - ``true`` if ``vpcSubnets`` is ``subnetType: SubnetType.PUBLIC``, ``false`` otherwise
        :param removal_policy: The CloudFormation policy to apply when the instance is removed from the stack or replaced during an update. Default: - RemovalPolicy.SNAPSHOT (remove the resource, but retain a snapshot of the data)
        :param s3_export_buckets: S3 buckets that you want to load data into. This property must not be used if ``s3ExportRole`` is used. For Microsoft SQL Server: Default: - None
        :param s3_export_role: Role that will be associated with this DB instance to enable S3 export. This property must not be used if ``s3ExportBuckets`` is used. For Microsoft SQL Server: Default: - New role is created if ``s3ExportBuckets`` is set, no role is defined otherwise
        :param s3_import_buckets: S3 buckets that you want to load data from. This feature is only supported by the Microsoft SQL Server, Oracle, and PostgreSQL engines. This property must not be used if ``s3ImportRole`` is used. For Microsoft SQL Server: Default: - None
        :param s3_import_role: Role that will be associated with this DB instance to enable S3 import. This feature is only supported by the Microsoft SQL Server, Oracle, and PostgreSQL engines. This property must not be used if ``s3ImportBuckets`` is used. For Microsoft SQL Server: Default: - New role is created if ``s3ImportBuckets`` is set, no role is defined otherwise
        :param security_groups: The security groups to assign to the DB instance. Default: - a new security group is created
        :param storage_type: The storage type. Storage types supported are gp2, io1, standard. Default: GP2
        :param subnet_group: Existing subnet group for the instance. Default: - a new subnet group will be created.
        :param vpc_subnets: The type of subnets to add to the created DB subnet group. Default: - private subnets
        '''
        props = aws_cdk.aws_rds.DatabaseInstanceProps(
            character_set_name=character_set_name,
            credentials=credentials,
            storage_encrypted=storage_encrypted,
            storage_encryption_key=storage_encryption_key,
            engine=engine,
            allocated_storage=allocated_storage,
            allow_major_version_upgrade=allow_major_version_upgrade,
            database_name=database_name,
            instance_type=instance_type,
            license_model=license_model,
            parameters=parameters,
            timezone=timezone,
            vpc=vpc,
            auto_minor_version_upgrade=auto_minor_version_upgrade,
            availability_zone=availability_zone,
            backup_retention=backup_retention,
            cloudwatch_logs_exports=cloudwatch_logs_exports,
            cloudwatch_logs_retention=cloudwatch_logs_retention,
            cloudwatch_logs_retention_role=cloudwatch_logs_retention_role,
            copy_tags_to_snapshot=copy_tags_to_snapshot,
            delete_automated_backups=delete_automated_backups,
            deletion_protection=deletion_protection,
            domain=domain,
            domain_role=domain_role,
            enable_performance_insights=enable_performance_insights,
            iam_authentication=iam_authentication,
            instance_identifier=instance_identifier,
            iops=iops,
            max_allocated_storage=max_allocated_storage,
            monitoring_interval=monitoring_interval,
            monitoring_role=monitoring_role,
            multi_az=multi_az,
            option_group=option_group,
            parameter_group=parameter_group,
            performance_insight_encryption_key=performance_insight_encryption_key,
            performance_insight_retention=performance_insight_retention,
            port=port,
            preferred_backup_window=preferred_backup_window,
            preferred_maintenance_window=preferred_maintenance_window,
            processor_features=processor_features,
            publicly_accessible=publicly_accessible,
            removal_policy=removal_policy,
            s3_export_buckets=s3_export_buckets,
            s3_export_role=s3_export_role,
            s3_import_buckets=s3_import_buckets,
            s3_import_role=s3_import_role,
            security_groups=security_groups,
            storage_type=storage_type,
            subnet_group=subnet_group,
            vpc_subnets=vpc_subnets,
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
        cluster: aws_cdk.aws_eks.Cluster,
        create_prometheus_workspace: builtins.bool,
        namespace: builtins.str,
        prometheus_endpoint: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cluster: 
        :param create_prometheus_workspace: 
        :param namespace: 
        :param prometheus_endpoint: 
        '''
        props = TelemetryProps(
            cluster=cluster,
            create_prometheus_workspace=create_prometheus_workspace,
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
        "cluster": "cluster",
        "create_prometheus_workspace": "createPrometheusWorkspace",
        "namespace": "namespace",
        "prometheus_endpoint": "prometheusEndpoint",
    },
)
class TelemetryProps:
    def __init__(
        self,
        *,
        cluster: aws_cdk.aws_eks.Cluster,
        create_prometheus_workspace: builtins.bool,
        namespace: builtins.str,
        prometheus_endpoint: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cluster: 
        :param create_prometheus_workspace: 
        :param namespace: 
        :param prometheus_endpoint: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "cluster": cluster,
            "create_prometheus_workspace": create_prometheus_workspace,
            "namespace": namespace,
        }
        if prometheus_endpoint is not None:
            self._values["prometheus_endpoint"] = prometheus_endpoint

    @builtins.property
    def cluster(self) -> aws_cdk.aws_eks.Cluster:
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(aws_cdk.aws_eks.Cluster, result)

    @builtins.property
    def create_prometheus_workspace(self) -> builtins.bool:
        result = self._values.get("create_prometheus_workspace")
        assert result is not None, "Required property 'create_prometheus_workspace' is missing"
        return typing.cast(builtins.bool, result)

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
    "RdsStack",
    "SecretsManager",
    "SecretsManagerProps",
    "Telemetry",
    "TelemetryProps",
    "Tls",
]

publication.publish()
