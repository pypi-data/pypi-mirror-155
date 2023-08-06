'''
# kong-data-plane

[![NPM version](https://badge.fury.io/js/kong-data-plane.svg)](https://badge.fury.io/js/kong-data-plane)
[![PyPI version](https://badge.fury.io/py/kong-data-plane.svg)](https://badge.fury.io/py/kong-data-plane)

![Downloads](https://img.shields.io/badge/-DOWNLOADS:-brightgreen?color=gray)
![npm](https://img.shields.io/npm/dt/kong-data-plane?label=npm&color=orange)
![PyPI](https://img.shields.io/pypi/dm/kong-data-plane?label=pypi&color=blue)

Use this Kong CDK Construct Library to deploy Kong data plane on Amazon EKS .

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

## npm Package Installation:

```
yarn add --dev kong-data-plane
# or
npm install kong-data-plane --save-dev
```

## PyPI Package Installation:

```
pip install kong-data-plane
```

# Sample

Try out https://github.com/kong/aws-samples for the complete sample application and instructions.

## Resources to learn about CDK

* [CDK TypeScript Workshop](https://cdkworkshop.com/20-typescript.html)
* [Video Introducing CDK by AWS with Demo](https://youtu.be/ZWCvNFUN-sU)
* [CDK Concepts](https://youtu.be/9As_ZIjUGmY)

## Kong Hands on Workshop

https://kong.awsworkshop.io/
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

import aws_cdk.aws_ecs
import aws_cdk.aws_eks
import constructs


@jsii.data_type(
    jsii_type="kong-data-plane.DataPlaneTelemetryProps",
    jsii_struct_bases=[],
    name_mapping={
        "create_prometheus_workspace": "createPrometheusWorkspace",
        "prometheus_endpoint": "prometheusEndpoint",
    },
)
class DataPlaneTelemetryProps:
    def __init__(
        self,
        *,
        create_prometheus_workspace: builtins.bool,
        prometheus_endpoint: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create_prometheus_workspace: 
        :param prometheus_endpoint: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "create_prometheus_workspace": create_prometheus_workspace,
        }
        if prometheus_endpoint is not None:
            self._values["prometheus_endpoint"] = prometheus_endpoint

    @builtins.property
    def create_prometheus_workspace(self) -> builtins.bool:
        result = self._values.get("create_prometheus_workspace")
        assert result is not None, "Required property 'create_prometheus_workspace' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def prometheus_endpoint(self) -> typing.Optional[builtins.str]:
        result = self._values.get("prometheus_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataPlaneTelemetryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KongEcs(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="kong-data-plane.KongEcs",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cluster_dns: builtins.str,
        cluster_props: aws_cdk.aws_ecs.ClusterProps,
        desired_count: jsii.Number,
        kong_task_props: aws_cdk.aws_ecs.FargateTaskDefinitionProps,
        private_ca_arn: builtins.str,
        telemetry_dns: builtins.str,
        image: typing.Optional[builtins.str] = None,
        internet_facing: typing.Optional[builtins.bool] = None,
        license_secret: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cluster_dns: 
        :param cluster_props: 
        :param desired_count: 
        :param kong_task_props: 
        :param private_ca_arn: 
        :param telemetry_dns: 
        :param image: 
        :param internet_facing: 
        :param license_secret: 
        '''
        props = KongEcsDataPlaneProps(
            cluster_dns=cluster_dns,
            cluster_props=cluster_props,
            desired_count=desired_count,
            kong_task_props=kong_task_props,
            private_ca_arn=private_ca_arn,
            telemetry_dns=telemetry_dns,
            image=image,
            internet_facing=internet_facing,
            license_secret=license_secret,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="kong-data-plane.KongEcsDataPlaneProps",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_dns": "clusterDns",
        "cluster_props": "clusterProps",
        "desired_count": "desiredCount",
        "kong_task_props": "kongTaskProps",
        "private_ca_arn": "privateCaArn",
        "telemetry_dns": "telemetryDns",
        "image": "image",
        "internet_facing": "internetFacing",
        "license_secret": "licenseSecret",
    },
)
class KongEcsDataPlaneProps:
    def __init__(
        self,
        *,
        cluster_dns: builtins.str,
        cluster_props: aws_cdk.aws_ecs.ClusterProps,
        desired_count: jsii.Number,
        kong_task_props: aws_cdk.aws_ecs.FargateTaskDefinitionProps,
        private_ca_arn: builtins.str,
        telemetry_dns: builtins.str,
        image: typing.Optional[builtins.str] = None,
        internet_facing: typing.Optional[builtins.bool] = None,
        license_secret: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cluster_dns: 
        :param cluster_props: 
        :param desired_count: 
        :param kong_task_props: 
        :param private_ca_arn: 
        :param telemetry_dns: 
        :param image: 
        :param internet_facing: 
        :param license_secret: 
        '''
        if isinstance(cluster_props, dict):
            cluster_props = aws_cdk.aws_ecs.ClusterProps(**cluster_props)
        if isinstance(kong_task_props, dict):
            kong_task_props = aws_cdk.aws_ecs.FargateTaskDefinitionProps(**kong_task_props)
        self._values: typing.Dict[str, typing.Any] = {
            "cluster_dns": cluster_dns,
            "cluster_props": cluster_props,
            "desired_count": desired_count,
            "kong_task_props": kong_task_props,
            "private_ca_arn": private_ca_arn,
            "telemetry_dns": telemetry_dns,
        }
        if image is not None:
            self._values["image"] = image
        if internet_facing is not None:
            self._values["internet_facing"] = internet_facing
        if license_secret is not None:
            self._values["license_secret"] = license_secret

    @builtins.property
    def cluster_dns(self) -> builtins.str:
        '''
        :summary: Cluster DNS to connect to control plane
        '''
        result = self._values.get("cluster_dns")
        assert result is not None, "Required property 'cluster_dns' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster_props(self) -> aws_cdk.aws_ecs.ClusterProps:
        '''
        :summary: Define ClusterProps for ECS cluster
        '''
        result = self._values.get("cluster_props")
        assert result is not None, "Required property 'cluster_props' is missing"
        return typing.cast(aws_cdk.aws_ecs.ClusterProps, result)

    @builtins.property
    def desired_count(self) -> jsii.Number:
        result = self._values.get("desired_count")
        assert result is not None, "Required property 'desired_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def kong_task_props(self) -> aws_cdk.aws_ecs.FargateTaskDefinitionProps:
        '''
        :summary: ECS Task properties
        '''
        result = self._values.get("kong_task_props")
        assert result is not None, "Required property 'kong_task_props' is missing"
        return typing.cast(aws_cdk.aws_ecs.FargateTaskDefinitionProps, result)

    @builtins.property
    def private_ca_arn(self) -> builtins.str:
        '''
        :summary: PrivateCA Arn to use to generate certificates
        '''
        result = self._values.get("private_ca_arn")
        assert result is not None, "Required property 'private_ca_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def telemetry_dns(self) -> builtins.str:
        '''
        :summary: Telemetry DNS
        '''
        result = self._values.get("telemetry_dns")
        assert result is not None, "Required property 'telemetry_dns' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def image(self) -> typing.Optional[builtins.str]:
        '''
        :summary: Kong image with tag
        '''
        result = self._values.get("image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def internet_facing(self) -> typing.Optional[builtins.bool]:
        '''
        :summary: If Data plane is internet facing
        '''
        result = self._values.get("internet_facing")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def license_secret(self) -> typing.Optional[builtins.str]:
        '''
        :summary: Name of the Secret in AWS Secrets Manager
        '''
        result = self._values.get("license_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KongEcsDataPlaneProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KongEks(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="kong-data-plane.KongEks",
):
    '''
    :summary: The KongEks class.
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cluster_dns: builtins.str,
        data_plane_cluster_props: aws_cdk.aws_eks.ClusterProps,
        data_plane_node_props: aws_cdk.aws_eks.NodegroupOptions,
        kong_telemetry_options: DataPlaneTelemetryProps,
        license_secrets_name: builtins.str,
        private_ca_arn: builtins.str,
        telemetry_dns: builtins.str,
    ) -> None:
        '''
        :param scope: - represents the scope for all the resources.
        :param id: - this is a a scope-unique id.
        :param cluster_dns: 
        :param data_plane_cluster_props: 
        :param data_plane_node_props: 
        :param kong_telemetry_options: 
        :param license_secrets_name: 
        :param private_ca_arn: 
        :param telemetry_dns: 

        :access: public
        :since: 0.1.0
        :summary: Constructs a new instance of the KongEks class.
        '''
        props = KongEksDataPlaneProps(
            cluster_dns=cluster_dns,
            data_plane_cluster_props=data_plane_cluster_props,
            data_plane_node_props=data_plane_node_props,
            kong_telemetry_options=kong_telemetry_options,
            license_secrets_name=license_secrets_name,
            private_ca_arn=private_ca_arn,
            telemetry_dns=telemetry_dns,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="kong-data-plane.KongEksDataPlaneProps",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_dns": "clusterDns",
        "data_plane_cluster_props": "dataPlaneClusterProps",
        "data_plane_node_props": "dataPlaneNodeProps",
        "kong_telemetry_options": "kongTelemetryOptions",
        "license_secrets_name": "licenseSecretsName",
        "private_ca_arn": "privateCaArn",
        "telemetry_dns": "telemetryDns",
    },
)
class KongEksDataPlaneProps:
    def __init__(
        self,
        *,
        cluster_dns: builtins.str,
        data_plane_cluster_props: aws_cdk.aws_eks.ClusterProps,
        data_plane_node_props: aws_cdk.aws_eks.NodegroupOptions,
        kong_telemetry_options: DataPlaneTelemetryProps,
        license_secrets_name: builtins.str,
        private_ca_arn: builtins.str,
        telemetry_dns: builtins.str,
    ) -> None:
        '''
        :param cluster_dns: 
        :param data_plane_cluster_props: 
        :param data_plane_node_props: 
        :param kong_telemetry_options: 
        :param license_secrets_name: 
        :param private_ca_arn: 
        :param telemetry_dns: 
        '''
        if isinstance(data_plane_cluster_props, dict):
            data_plane_cluster_props = aws_cdk.aws_eks.ClusterProps(**data_plane_cluster_props)
        if isinstance(data_plane_node_props, dict):
            data_plane_node_props = aws_cdk.aws_eks.NodegroupOptions(**data_plane_node_props)
        if isinstance(kong_telemetry_options, dict):
            kong_telemetry_options = DataPlaneTelemetryProps(**kong_telemetry_options)
        self._values: typing.Dict[str, typing.Any] = {
            "cluster_dns": cluster_dns,
            "data_plane_cluster_props": data_plane_cluster_props,
            "data_plane_node_props": data_plane_node_props,
            "kong_telemetry_options": kong_telemetry_options,
            "license_secrets_name": license_secrets_name,
            "private_ca_arn": private_ca_arn,
            "telemetry_dns": telemetry_dns,
        }

    @builtins.property
    def cluster_dns(self) -> builtins.str:
        result = self._values.get("cluster_dns")
        assert result is not None, "Required property 'cluster_dns' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_plane_cluster_props(self) -> aws_cdk.aws_eks.ClusterProps:
        '''
        :see: https://docs.aws.amazon.com/cdk/api/latest/docs/
        :aws-cdk_aws-eks: .ClusterProps.html
        :summary: Control Plane EKS Cluster properties
        '''
        result = self._values.get("data_plane_cluster_props")
        assert result is not None, "Required property 'data_plane_cluster_props' is missing"
        return typing.cast(aws_cdk.aws_eks.ClusterProps, result)

    @builtins.property
    def data_plane_node_props(self) -> aws_cdk.aws_eks.NodegroupOptions:
        result = self._values.get("data_plane_node_props")
        assert result is not None, "Required property 'data_plane_node_props' is missing"
        return typing.cast(aws_cdk.aws_eks.NodegroupOptions, result)

    @builtins.property
    def kong_telemetry_options(self) -> DataPlaneTelemetryProps:
        result = self._values.get("kong_telemetry_options")
        assert result is not None, "Required property 'kong_telemetry_options' is missing"
        return typing.cast(DataPlaneTelemetryProps, result)

    @builtins.property
    def license_secrets_name(self) -> builtins.str:
        '''
        :summary: Name of the Secret in AWS Secrets Manager
        '''
        result = self._values.get("license_secrets_name")
        assert result is not None, "Required property 'license_secrets_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def private_ca_arn(self) -> builtins.str:
        result = self._values.get("private_ca_arn")
        assert result is not None, "Required property 'private_ca_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def telemetry_dns(self) -> builtins.str:
        result = self._values.get("telemetry_dns")
        assert result is not None, "Required property 'telemetry_dns' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KongEksDataPlaneProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DataPlaneTelemetryProps",
    "KongEcs",
    "KongEcsDataPlaneProps",
    "KongEks",
    "KongEksDataPlaneProps",
]

publication.publish()
