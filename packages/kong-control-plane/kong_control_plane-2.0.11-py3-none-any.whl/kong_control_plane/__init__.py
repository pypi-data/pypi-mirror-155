'''
# kong-control-plane

[![NPM version](https://badge.fury.io/js/kong-control-plane.svg)](https://badge.fury.io/js/kong-control-plane)
[![PyPI version](https://badge.fury.io/py/kong-control-plane.svg)](https://badge.fury.io/py/kong-control-plane)

![Downloads](https://img.shields.io/badge/-DOWNLOADS:-brightgreen?color=gray)
![npm](https://img.shields.io/npm/dt/kong-control-plane?label=npm&color=orange)
![PyPI](https://img.shields.io/pypi/dm/kong-control-plane?label=pypi&color=blue)

Use this Kong CDK Construct Library to deploy Kong control plane on Amazon EKS .

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
yarn add --dev kong-control-plane
# or
npm install kong-control-plane --save-dev
```

## PyPI Package Installation:

```
pip install kong-control-plane
```

# Sample

Try out https://github.com/kong/aws-samples for the complete sample application and instructions.

## Resources to learn about CDK

* [CDK TypeScript Workshop](https://cdkworkshop.com/20-typescript.html)
* [Video Introducing CDK by AWS with Demo](https://youtu.be/ZWCvNFUN-sU)
* [CDK Concepts](https://youtu.be/9As_ZIjUGmY)

## Related

Kong on AWS Hands on Workshop - https://kong.awsworkshop.io/
Kong Data plane on AWS contruct - FILLME
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
import aws_cdk.aws_rds
import constructs


@jsii.data_type(
    jsii_type="kong-control-plane.AdminProps",
    jsii_struct_bases=[],
    name_mapping={
        "enable_http": "enableHttp",
        "http_port": "httpPort",
        "https_port": "httpsPort",
    },
)
class AdminProps:
    def __init__(
        self,
        *,
        enable_http: typing.Optional[builtins.bool] = None,
        http_port: typing.Optional[jsii.Number] = None,
        https_port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enable_http: 
        :param http_port: 
        :param https_port: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if enable_http is not None:
            self._values["enable_http"] = enable_http
        if http_port is not None:
            self._values["http_port"] = http_port
        if https_port is not None:
            self._values["https_port"] = https_port

    @builtins.property
    def enable_http(self) -> typing.Optional[builtins.bool]:
        '''
        :summary: Enable Kong Admin on http
        '''
        result = self._values.get("enable_http")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def http_port(self) -> typing.Optional[jsii.Number]:
        '''
        :summary: Kong Admin Http Port
        '''
        result = self._values.get("http_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def https_port(self) -> typing.Optional[jsii.Number]:
        '''
        :summary: Kong Admin Https Port
        '''
        result = self._values.get("https_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AdminProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="kong-control-plane.ClusterProps",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "port": "port"},
)
class ClusterProps:
    def __init__(
        self,
        *,
        enabled: builtins.bool,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enabled: 
        :param port: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "enabled": enabled,
        }
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def enabled(self) -> builtins.bool:
        '''
        :summary: Enable Cluster  communication
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''
        :summary: Cluster communication port
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="kong-control-plane.ClusterTelemetryProps",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "port": "port"},
)
class ClusterTelemetryProps:
    def __init__(
        self,
        *,
        enabled: builtins.bool,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enabled: 
        :param port: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "enabled": enabled,
        }
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def enabled(self) -> builtins.bool:
        '''
        :summary: Enable Cluster Telemetry
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''
        :summary: Enable Cluster Telemetry port
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClusterTelemetryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="kong-control-plane.ControlPlaneClusterProps",
    jsii_struct_bases=[],
    name_mapping={
        "eks_cluster_props": "eksClusterProps",
        "kong_telemetry_options": "kongTelemetryOptions",
        "kong_helm_options": "kongHelmOptions",
    },
)
class ControlPlaneClusterProps:
    def __init__(
        self,
        *,
        eks_cluster_props: aws_cdk.aws_eks.ClusterProps,
        kong_telemetry_options: "ControlPlaneTelemetryProps",
        kong_helm_options: typing.Optional[aws_cdk.aws_eks.HelmChartOptions] = None,
    ) -> None:
        '''
        :param eks_cluster_props: 
        :param kong_telemetry_options: 
        :param kong_helm_options: 
        '''
        if isinstance(eks_cluster_props, dict):
            eks_cluster_props = aws_cdk.aws_eks.ClusterProps(**eks_cluster_props)
        if isinstance(kong_telemetry_options, dict):
            kong_telemetry_options = ControlPlaneTelemetryProps(**kong_telemetry_options)
        if isinstance(kong_helm_options, dict):
            kong_helm_options = aws_cdk.aws_eks.HelmChartOptions(**kong_helm_options)
        self._values: typing.Dict[str, typing.Any] = {
            "eks_cluster_props": eks_cluster_props,
            "kong_telemetry_options": kong_telemetry_options,
        }
        if kong_helm_options is not None:
            self._values["kong_helm_options"] = kong_helm_options

    @builtins.property
    def eks_cluster_props(self) -> aws_cdk.aws_eks.ClusterProps:
        result = self._values.get("eks_cluster_props")
        assert result is not None, "Required property 'eks_cluster_props' is missing"
        return typing.cast(aws_cdk.aws_eks.ClusterProps, result)

    @builtins.property
    def kong_telemetry_options(self) -> "ControlPlaneTelemetryProps":
        result = self._values.get("kong_telemetry_options")
        assert result is not None, "Required property 'kong_telemetry_options' is missing"
        return typing.cast("ControlPlaneTelemetryProps", result)

    @builtins.property
    def kong_helm_options(self) -> typing.Optional[aws_cdk.aws_eks.HelmChartOptions]:
        result = self._values.get("kong_helm_options")
        return typing.cast(typing.Optional[aws_cdk.aws_eks.HelmChartOptions], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ControlPlaneClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="kong-control-plane.ControlPlaneTelemetryProps",
    jsii_struct_bases=[],
    name_mapping={
        "create_prometheus_workspace": "createPrometheusWorkspace",
        "prometheus_endpoint": "prometheusEndpoint",
    },
)
class ControlPlaneTelemetryProps:
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
        return "ControlPlaneTelemetryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="kong-control-plane.DevPortalProps",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "port": "port"},
)
class DevPortalProps:
    def __init__(
        self,
        *,
        enabled: builtins.bool,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enabled: 
        :param port: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "enabled": enabled,
        }
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def enabled(self) -> builtins.bool:
        '''
        :summary: Enable Kong Dev Portal
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''
        :summary: Enable Kong DevPortal Port
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DevPortalProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="kong-control-plane.EksControlPlaneProps",
    jsii_struct_bases=[],
    name_mapping={
        "control_plane_cluster_props": "controlPlaneClusterProps",
        "control_plane_node_props": "controlPlaneNodeProps",
        "hosted_zone_name": "hostedZoneName",
        "license_secrets_name": "licenseSecretsName",
        "namespace": "namespace",
        "rds_props": "rdsProps",
    },
)
class EksControlPlaneProps:
    def __init__(
        self,
        *,
        control_plane_cluster_props: ControlPlaneClusterProps,
        control_plane_node_props: aws_cdk.aws_eks.NodegroupOptions,
        hosted_zone_name: builtins.str,
        license_secrets_name: builtins.str,
        namespace: builtins.str,
        rds_props: "RdsDatabaseProps",
    ) -> None:
        '''
        :param control_plane_cluster_props: 
        :param control_plane_node_props: 
        :param hosted_zone_name: 
        :param license_secrets_name: 
        :param namespace: 
        :param rds_props: 
        '''
        if isinstance(control_plane_cluster_props, dict):
            control_plane_cluster_props = ControlPlaneClusterProps(**control_plane_cluster_props)
        if isinstance(control_plane_node_props, dict):
            control_plane_node_props = aws_cdk.aws_eks.NodegroupOptions(**control_plane_node_props)
        if isinstance(rds_props, dict):
            rds_props = RdsDatabaseProps(**rds_props)
        self._values: typing.Dict[str, typing.Any] = {
            "control_plane_cluster_props": control_plane_cluster_props,
            "control_plane_node_props": control_plane_node_props,
            "hosted_zone_name": hosted_zone_name,
            "license_secrets_name": license_secrets_name,
            "namespace": namespace,
            "rds_props": rds_props,
        }

    @builtins.property
    def control_plane_cluster_props(self) -> ControlPlaneClusterProps:
        '''
        :see: https://docs.aws.amazon.com/cdk/api/latest/docs/
        :aws-cdk_aws-eks: .ClusterProps.html
        :summary: Control Plane EKS Cluster properties
        '''
        result = self._values.get("control_plane_cluster_props")
        assert result is not None, "Required property 'control_plane_cluster_props' is missing"
        return typing.cast(ControlPlaneClusterProps, result)

    @builtins.property
    def control_plane_node_props(self) -> aws_cdk.aws_eks.NodegroupOptions:
        '''
        :see: https://docs.aws.amazon.com/cdk/api/latest/docs/
        :aws-cdk_aws-eks: .AutoScalingGroupCapacityOptions.html
        :summary: Kong Control Plane EKS Nodes properties
        '''
        result = self._values.get("control_plane_node_props")
        assert result is not None, "Required property 'control_plane_node_props' is missing"
        return typing.cast(aws_cdk.aws_eks.NodegroupOptions, result)

    @builtins.property
    def hosted_zone_name(self) -> builtins.str:
        '''
        :summary: Name of the hosted zone
        '''
        result = self._values.get("hosted_zone_name")
        assert result is not None, "Required property 'hosted_zone_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def license_secrets_name(self) -> builtins.str:
        '''
        :summary: Name of the Secret in AWS Secrets Manager
        '''
        result = self._values.get("license_secrets_name")
        assert result is not None, "Required property 'license_secrets_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace(self) -> builtins.str:
        '''
        :summary: Kubernetes Namespace to install Kong Control Plane
        '''
        result = self._values.get("namespace")
        assert result is not None, "Required property 'namespace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rds_props(self) -> "RdsDatabaseProps":
        '''
        :summary: RDS Database properties
        '''
        result = self._values.get("rds_props")
        assert result is not None, "Required property 'rds_props' is missing"
        return typing.cast("RdsDatabaseProps", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksControlPlaneProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KongEcs(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="kong-control-plane.KongEcs",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        cluster_props: aws_cdk.aws_ecs.ClusterProps,
        desired_count: jsii.Number,
        hosted_zone_name: builtins.str,
        kong_features_props: "KongFeatureProps",
        kong_task_props: aws_cdk.aws_ecs.FargateTaskDefinitionProps,
        rds_props: "RdsDatabaseProps",
        image: typing.Optional[builtins.str] = None,
        internet_facing: typing.Optional[builtins.bool] = None,
        license_secret: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cluster_props: 
        :param desired_count: 
        :param hosted_zone_name: 
        :param kong_features_props: 
        :param kong_task_props: 
        :param rds_props: 
        :param image: 
        :param internet_facing: 
        :param license_secret: 
        '''
        props = KongEcsControlPlaneProps(
            cluster_props=cluster_props,
            desired_count=desired_count,
            hosted_zone_name=hosted_zone_name,
            kong_features_props=kong_features_props,
            kong_task_props=kong_task_props,
            rds_props=rds_props,
            image=image,
            internet_facing=internet_facing,
            license_secret=license_secret,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="controlPlane")
    def control_plane(self) -> aws_cdk.aws_ecs.Cluster:
        return typing.cast(aws_cdk.aws_ecs.Cluster, jsii.get(self, "controlPlane"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clusterDns")
    def cluster_dns(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterDns"))

    @cluster_dns.setter
    def cluster_dns(self, value: builtins.str) -> None:
        jsii.set(self, "clusterDns", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="privateCaArn")
    def private_ca_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateCaArn"))

    @private_ca_arn.setter
    def private_ca_arn(self, value: builtins.str) -> None:
        jsii.set(self, "privateCaArn", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="telemetryDns")
    def telemetry_dns(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "telemetryDns"))

    @telemetry_dns.setter
    def telemetry_dns(self, value: builtins.str) -> None:
        jsii.set(self, "telemetryDns", value)


@jsii.data_type(
    jsii_type="kong-control-plane.KongEcsControlPlaneProps",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_props": "clusterProps",
        "desired_count": "desiredCount",
        "hosted_zone_name": "hostedZoneName",
        "kong_features_props": "kongFeaturesProps",
        "kong_task_props": "kongTaskProps",
        "rds_props": "rdsProps",
        "image": "image",
        "internet_facing": "internetFacing",
        "license_secret": "licenseSecret",
    },
)
class KongEcsControlPlaneProps:
    def __init__(
        self,
        *,
        cluster_props: aws_cdk.aws_ecs.ClusterProps,
        desired_count: jsii.Number,
        hosted_zone_name: builtins.str,
        kong_features_props: "KongFeatureProps",
        kong_task_props: aws_cdk.aws_ecs.FargateTaskDefinitionProps,
        rds_props: "RdsDatabaseProps",
        image: typing.Optional[builtins.str] = None,
        internet_facing: typing.Optional[builtins.bool] = None,
        license_secret: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cluster_props: 
        :param desired_count: 
        :param hosted_zone_name: 
        :param kong_features_props: 
        :param kong_task_props: 
        :param rds_props: 
        :param image: 
        :param internet_facing: 
        :param license_secret: 
        '''
        if isinstance(cluster_props, dict):
            cluster_props = aws_cdk.aws_ecs.ClusterProps(**cluster_props)
        if isinstance(kong_features_props, dict):
            kong_features_props = KongFeatureProps(**kong_features_props)
        if isinstance(kong_task_props, dict):
            kong_task_props = aws_cdk.aws_ecs.FargateTaskDefinitionProps(**kong_task_props)
        if isinstance(rds_props, dict):
            rds_props = RdsDatabaseProps(**rds_props)
        self._values: typing.Dict[str, typing.Any] = {
            "cluster_props": cluster_props,
            "desired_count": desired_count,
            "hosted_zone_name": hosted_zone_name,
            "kong_features_props": kong_features_props,
            "kong_task_props": kong_task_props,
            "rds_props": rds_props,
        }
        if image is not None:
            self._values["image"] = image
        if internet_facing is not None:
            self._values["internet_facing"] = internet_facing
        if license_secret is not None:
            self._values["license_secret"] = license_secret

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
    def hosted_zone_name(self) -> builtins.str:
        '''
        :summary: Name of the hosted zone
        '''
        result = self._values.get("hosted_zone_name")
        assert result is not None, "Required property 'hosted_zone_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kong_features_props(self) -> "KongFeatureProps":
        '''
        :summary: Kong Features properties
        '''
        result = self._values.get("kong_features_props")
        assert result is not None, "Required property 'kong_features_props' is missing"
        return typing.cast("KongFeatureProps", result)

    @builtins.property
    def kong_task_props(self) -> aws_cdk.aws_ecs.FargateTaskDefinitionProps:
        '''
        :summary: ECS Task properties
        '''
        result = self._values.get("kong_task_props")
        assert result is not None, "Required property 'kong_task_props' is missing"
        return typing.cast(aws_cdk.aws_ecs.FargateTaskDefinitionProps, result)

    @builtins.property
    def rds_props(self) -> "RdsDatabaseProps":
        '''
        :summary: RDS Database properties
        '''
        result = self._values.get("rds_props")
        assert result is not None, "Required property 'rds_props' is missing"
        return typing.cast("RdsDatabaseProps", result)

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
        :summary: If control plane is internet facing
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
        return "KongEcsControlPlaneProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KongEks(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="kong-control-plane.KongEks",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        control_plane_cluster_props: ControlPlaneClusterProps,
        control_plane_node_props: aws_cdk.aws_eks.NodegroupOptions,
        hosted_zone_name: builtins.str,
        license_secrets_name: builtins.str,
        namespace: builtins.str,
        rds_props: "RdsDatabaseProps",
    ) -> None:
        '''
        :param scope: - represents the scope for all the resources.
        :param id: - this is a a scope-unique id.
        :param control_plane_cluster_props: 
        :param control_plane_node_props: 
        :param hosted_zone_name: 
        :param license_secrets_name: 
        :param namespace: 
        :param rds_props: 

        :access: public
        :since: 0.1.0
        :summary: Constructs a new instance of the KongEks class.
        '''
        props = EksControlPlaneProps(
            control_plane_cluster_props=control_plane_cluster_props,
            control_plane_node_props=control_plane_node_props,
            hosted_zone_name=hosted_zone_name,
            license_secrets_name=license_secrets_name,
            namespace=namespace,
            rds_props=rds_props,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="controlPlane")
    def control_plane(self) -> aws_cdk.aws_eks.Cluster:
        return typing.cast(aws_cdk.aws_eks.Cluster, jsii.get(self, "controlPlane"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clusterDns")
    def cluster_dns(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterDns"))

    @cluster_dns.setter
    def cluster_dns(self, value: builtins.str) -> None:
        jsii.set(self, "clusterDns", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="privateCaArn")
    def private_ca_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateCaArn"))

    @private_ca_arn.setter
    def private_ca_arn(self, value: builtins.str) -> None:
        jsii.set(self, "privateCaArn", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="telemetryDns")
    def telemetry_dns(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "telemetryDns"))

    @telemetry_dns.setter
    def telemetry_dns(self, value: builtins.str) -> None:
        jsii.set(self, "telemetryDns", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="prometheusEndpoint")
    def prometheus_endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prometheusEndpoint"))

    @prometheus_endpoint.setter
    def prometheus_endpoint(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "prometheusEndpoint", value)


@jsii.data_type(
    jsii_type="kong-control-plane.KongFeatureProps",
    jsii_struct_bases=[],
    name_mapping={
        "admin_props": "adminProps",
        "cluster_props": "clusterProps",
        "cluster_telemetry_props": "clusterTelemetryProps",
        "dev_portal_props": "devPortalProps",
        "kong_bootstrap_migration": "kongBootstrapMigration",
        "kong_manager_props": "kongManagerProps",
    },
)
class KongFeatureProps:
    def __init__(
        self,
        *,
        admin_props: AdminProps,
        cluster_props: ClusterProps,
        cluster_telemetry_props: ClusterTelemetryProps,
        dev_portal_props: DevPortalProps,
        kong_bootstrap_migration: builtins.bool,
        kong_manager_props: "KongManagerProps",
    ) -> None:
        '''
        :param admin_props: 
        :param cluster_props: 
        :param cluster_telemetry_props: 
        :param dev_portal_props: 
        :param kong_bootstrap_migration: 
        :param kong_manager_props: 
        '''
        if isinstance(admin_props, dict):
            admin_props = AdminProps(**admin_props)
        if isinstance(cluster_props, dict):
            cluster_props = ClusterProps(**cluster_props)
        if isinstance(cluster_telemetry_props, dict):
            cluster_telemetry_props = ClusterTelemetryProps(**cluster_telemetry_props)
        if isinstance(dev_portal_props, dict):
            dev_portal_props = DevPortalProps(**dev_portal_props)
        if isinstance(kong_manager_props, dict):
            kong_manager_props = KongManagerProps(**kong_manager_props)
        self._values: typing.Dict[str, typing.Any] = {
            "admin_props": admin_props,
            "cluster_props": cluster_props,
            "cluster_telemetry_props": cluster_telemetry_props,
            "dev_portal_props": dev_portal_props,
            "kong_bootstrap_migration": kong_bootstrap_migration,
            "kong_manager_props": kong_manager_props,
        }

    @builtins.property
    def admin_props(self) -> AdminProps:
        '''
        :summary: Kong Admin Props
        '''
        result = self._values.get("admin_props")
        assert result is not None, "Required property 'admin_props' is missing"
        return typing.cast(AdminProps, result)

    @builtins.property
    def cluster_props(self) -> ClusterProps:
        '''
        :summary: Kong Cluster Props
        '''
        result = self._values.get("cluster_props")
        assert result is not None, "Required property 'cluster_props' is missing"
        return typing.cast(ClusterProps, result)

    @builtins.property
    def cluster_telemetry_props(self) -> ClusterTelemetryProps:
        '''
        :summary: Kong Telemetry Props
        '''
        result = self._values.get("cluster_telemetry_props")
        assert result is not None, "Required property 'cluster_telemetry_props' is missing"
        return typing.cast(ClusterTelemetryProps, result)

    @builtins.property
    def dev_portal_props(self) -> DevPortalProps:
        '''
        :summary: Kong DevPortal Props
        '''
        result = self._values.get("dev_portal_props")
        assert result is not None, "Required property 'dev_portal_props' is missing"
        return typing.cast(DevPortalProps, result)

    @builtins.property
    def kong_bootstrap_migration(self) -> builtins.bool:
        '''
        :summary: Kong Database Migration enable flag
        '''
        result = self._values.get("kong_bootstrap_migration")
        assert result is not None, "Required property 'kong_bootstrap_migration' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def kong_manager_props(self) -> "KongManagerProps":
        '''
        :summary: Kong Manager Props
        '''
        result = self._values.get("kong_manager_props")
        assert result is not None, "Required property 'kong_manager_props' is missing"
        return typing.cast("KongManagerProps", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KongFeatureProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="kong-control-plane.KongManagerProps",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "enable_http": "enableHttp",
        "http_port": "httpPort",
        "https_port": "httpsPort",
    },
)
class KongManagerProps:
    def __init__(
        self,
        *,
        enabled: builtins.bool,
        enable_http: typing.Optional[builtins.bool] = None,
        http_port: typing.Optional[jsii.Number] = None,
        https_port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enabled: 
        :param enable_http: 
        :param http_port: 
        :param https_port: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "enabled": enabled,
        }
        if enable_http is not None:
            self._values["enable_http"] = enable_http
        if http_port is not None:
            self._values["http_port"] = http_port
        if https_port is not None:
            self._values["https_port"] = https_port

    @builtins.property
    def enabled(self) -> builtins.bool:
        '''
        :summary: Enable Kong Manager
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def enable_http(self) -> typing.Optional[builtins.bool]:
        '''
        :summary: Enable Kong Manager over https
        '''
        result = self._values.get("enable_http")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def http_port(self) -> typing.Optional[jsii.Number]:
        '''
        :summary: Enable Kong Manager http port
        '''
        result = self._values.get("http_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def https_port(self) -> typing.Optional[jsii.Number]:
        '''
        :summary: Kong Manager https port
        '''
        result = self._values.get("https_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KongManagerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="kong-control-plane.RdsDatabaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "databasename": "databasename",
        "postgresversion": "postgresversion",
        "username": "username",
    },
)
class RdsDatabaseProps:
    def __init__(
        self,
        *,
        databasename: builtins.str,
        postgresversion: aws_cdk.aws_rds.PostgresEngineVersion,
        username: builtins.str,
    ) -> None:
        '''
        :param databasename: 
        :param postgresversion: 
        :param username: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "databasename": databasename,
            "postgresversion": postgresversion,
            "username": username,
        }

    @builtins.property
    def databasename(self) -> builtins.str:
        '''
        :summary: Database name to be used for Artifactory
        '''
        result = self._values.get("databasename")
        assert result is not None, "Required property 'databasename' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def postgresversion(self) -> aws_cdk.aws_rds.PostgresEngineVersion:
        '''
        :see: https://docs.aws.amazon.com/cdk/api/latest/docs/
        :aws-cdk_aws-rds: .PostgresEngineVersion.html
        :summary: RDS PostGres Engine Version
        '''
        result = self._values.get("postgresversion")
        assert result is not None, "Required property 'postgresversion' is missing"
        return typing.cast(aws_cdk.aws_rds.PostgresEngineVersion, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''
        :summary: Master username to be used for RDS
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RdsDatabaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AdminProps",
    "ClusterProps",
    "ClusterTelemetryProps",
    "ControlPlaneClusterProps",
    "ControlPlaneTelemetryProps",
    "DevPortalProps",
    "EksControlPlaneProps",
    "KongEcs",
    "KongEcsControlPlaneProps",
    "KongEks",
    "KongFeatureProps",
    "KongManagerProps",
    "RdsDatabaseProps",
]

publication.publish()
