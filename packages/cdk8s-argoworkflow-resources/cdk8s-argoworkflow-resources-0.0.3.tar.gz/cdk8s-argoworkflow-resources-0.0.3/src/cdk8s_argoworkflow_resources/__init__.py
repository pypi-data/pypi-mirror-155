'''
# replace this
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

import cdk8s
import constructs
from .k8s import (
    Affinity as _Affinity_a7d59e98,
    ConfigMapKeySelector as _ConfigMapKeySelector_655813de,
    Container as _Container_7c687a93,
    ContainerPort as _ContainerPort_1a56bbf5,
    CreateOptions as _CreateOptions_33e095be,
    EnvFromSource as _EnvFromSource_35bf044a,
    EnvVar as _EnvVar_1741b5ed,
    HostAlias as _HostAlias_82563da2,
    IntOrString as _IntOrString_f14b6057,
    KubePersistentVolumeClaimProps as _KubePersistentVolumeClaimProps_f5d98fb6,
    LabelSelector as _LabelSelector_2d5da14b,
    Lifecycle as _Lifecycle_780bc732,
    ListMeta as _ListMeta_fcb8bed2,
    LocalObjectReference as _LocalObjectReference_cdc737d6,
    ObjectMeta as _ObjectMeta_77a65d46,
    ObjectReference as _ObjectReference_880f8d2d,
    OwnerReference as _OwnerReference_a16cc249,
    PersistentVolumeClaimSpec as _PersistentVolumeClaimSpec_fc09a257,
    PodDisruptionBudgetSpec as _PodDisruptionBudgetSpec_8bcdde1e,
    PodDnsConfig as _PodDnsConfig_4c2fa008,
    PodSecurityContext as _PodSecurityContext_c3a517d7,
    Probe as _Probe_6e8f94fa,
    ResourceRequirements as _ResourceRequirements_892d16ec,
    SecretKeySelector as _SecretKeySelector_3834a17e,
    SecurityContext as _SecurityContext_a4b1b9fb,
    Toleration as _Toleration_aec52105,
    Volume as _Volume_05ce2014,
    VolumeDevice as _VolumeDevice_aae53ff5,
    VolumeMount as _VolumeMount_366b43c7,
)


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.ArchiveStrategy",
    jsii_struct_bases=[],
    name_mapping={"none": "none", "tar": "tar", "zip": "zip"},
)
class ArchiveStrategy:
    def __init__(
        self,
        *,
        none: typing.Optional["NoneStrategy"] = None,
        tar: typing.Optional["TarStrategy"] = None,
        zip: typing.Optional["ZipStrategy"] = None,
    ) -> None:
        '''
        :param none: 
        :param tar: 
        :param zip: 
        '''
        if isinstance(none, dict):
            none = NoneStrategy(**none)
        if isinstance(tar, dict):
            tar = TarStrategy(**tar)
        if isinstance(zip, dict):
            zip = ZipStrategy(**zip)
        self._values: typing.Dict[str, typing.Any] = {}
        if none is not None:
            self._values["none"] = none
        if tar is not None:
            self._values["tar"] = tar
        if zip is not None:
            self._values["zip"] = zip

    @builtins.property
    def none(self) -> typing.Optional["NoneStrategy"]:
        result = self._values.get("none")
        return typing.cast(typing.Optional["NoneStrategy"], result)

    @builtins.property
    def tar(self) -> typing.Optional["TarStrategy"]:
        result = self._values.get("tar")
        return typing.cast(typing.Optional["TarStrategy"], result)

    @builtins.property
    def zip(self) -> typing.Optional["ZipStrategy"]:
        result = self._values.get("zip")
        return typing.cast(typing.Optional["ZipStrategy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArchiveStrategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.ArchivedWorkflowDeletedResponse",
    jsii_struct_bases=[],
    name_mapping={},
)
class ArchivedWorkflowDeletedResponse:
    def __init__(self) -> None:
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArchivedWorkflowDeletedResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArgoWorkflowClusterWorkflowTemplate(
    cdk8s.ApiObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.ArgoWorkflowClusterWorkflowTemplate",
):
    def __init__(
        self,
        scope: constructs.Construct,
        name: builtins.str,
        *,
        metadata: _ObjectMeta_77a65d46,
        spec: "WorkflowTemplateSpec",
        api_version: typing.Optional[builtins.str] = None,
        kind: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param name: -
        :param metadata: 
        :param spec: 
        :param api_version: 
        :param kind: 
        '''
        props = ClusterWorkflowTemplate(
            metadata=metadata, spec=spec, api_version=api_version, kind=kind
        )

        jsii.create(self.__class__, self, [scope, name, props])

    @jsii.member(jsii_name="manifest") # type: ignore[misc]
    @builtins.classmethod
    def manifest(
        cls,
        *,
        metadata: _ObjectMeta_77a65d46,
        spec: "WorkflowTemplateSpec",
        api_version: typing.Optional[builtins.str] = None,
        kind: typing.Optional[builtins.str] = None,
    ) -> typing.Any:
        '''
        :param metadata: 
        :param spec: 
        :param api_version: 
        :param kind: 
        '''
        props = ClusterWorkflowTemplate(
            metadata=metadata, spec=spec, api_version=api_version, kind=kind
        )

        return typing.cast(typing.Any, jsii.sinvoke(cls, "manifest", [props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="GVK")
    def GVK(cls) -> cdk8s.GroupVersionKind:
        return typing.cast(cdk8s.GroupVersionKind, jsii.sget(cls, "GVK"))


class ArgoWorkflowCronWorkflow(
    cdk8s.ApiObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.ArgoWorkflowCronWorkflow",
):
    def __init__(
        self,
        scope: constructs.Construct,
        name: builtins.str,
        *,
        metadata: _ObjectMeta_77a65d46,
        spec: "CronWorkflowSpec",
        status: typing.Optional["CronWorkflowStatus"] = None,
    ) -> None:
        '''
        :param scope: -
        :param name: -
        :param metadata: 
        :param spec: 
        :param status: 
        '''
        props = CronWorkflow(metadata=metadata, spec=spec, status=status)

        jsii.create(self.__class__, self, [scope, name, props])

    @jsii.member(jsii_name="manifest") # type: ignore[misc]
    @builtins.classmethod
    def manifest(
        cls,
        *,
        metadata: _ObjectMeta_77a65d46,
        spec: "CronWorkflowSpec",
        status: typing.Optional["CronWorkflowStatus"] = None,
    ) -> typing.Any:
        '''
        :param metadata: 
        :param spec: 
        :param status: 
        '''
        props = CronWorkflow(metadata=metadata, spec=spec, status=status)

        return typing.cast(typing.Any, jsii.sinvoke(cls, "manifest", [props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="GVK")
    def GVK(cls) -> cdk8s.GroupVersionKind:
        return typing.cast(cdk8s.GroupVersionKind, jsii.sget(cls, "GVK"))


class ArgoWorkflowWorkflowTemplate(
    cdk8s.ApiObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.ArgoWorkflowWorkflowTemplate",
):
    def __init__(
        self,
        scope: constructs.Construct,
        name: builtins.str,
        *,
        metadata: _ObjectMeta_77a65d46,
        spec: "WorkflowTemplateSpec",
        api_version: typing.Optional[builtins.str] = None,
        kind: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param name: -
        :param metadata: 
        :param spec: 
        :param api_version: 
        :param kind: 
        '''
        props = WorkflowTemplate(
            metadata=metadata, spec=spec, api_version=api_version, kind=kind
        )

        jsii.create(self.__class__, self, [scope, name, props])

    @jsii.member(jsii_name="manifest") # type: ignore[misc]
    @builtins.classmethod
    def manifest(
        cls,
        *,
        metadata: _ObjectMeta_77a65d46,
        spec: "WorkflowTemplateSpec",
        api_version: typing.Optional[builtins.str] = None,
        kind: typing.Optional[builtins.str] = None,
    ) -> typing.Any:
        '''
        :param metadata: 
        :param spec: 
        :param api_version: 
        :param kind: 
        '''
        props = WorkflowTemplate(
            metadata=metadata, spec=spec, api_version=api_version, kind=kind
        )

        return typing.cast(typing.Any, jsii.sinvoke(cls, "manifest", [props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="GVK")
    def GVK(cls) -> cdk8s.GroupVersionKind:
        return typing.cast(cdk8s.GroupVersionKind, jsii.sget(cls, "GVK"))


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.Arguments",
    jsii_struct_bases=[],
    name_mapping={"artifacts": "artifacts", "parameters": "parameters"},
)
class Arguments:
    def __init__(
        self,
        *,
        artifacts: typing.Optional[typing.Sequence["Artifact"]] = None,
        parameters: typing.Optional[typing.Sequence["Parameter"]] = None,
    ) -> None:
        '''
        :param artifacts: 
        :param parameters: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if artifacts is not None:
            self._values["artifacts"] = artifacts
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def artifacts(self) -> typing.Optional[typing.List["Artifact"]]:
        result = self._values.get("artifacts")
        return typing.cast(typing.Optional[typing.List["Artifact"]], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.List["Parameter"]]:
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.List["Parameter"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Arguments(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.Artifact",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "archive": "archive",
        "archive_logs": "archiveLogs",
        "artifactory": "artifactory",
        "from_": "from",
        "from_expression": "fromExpression",
        "gcs": "gcs",
        "git": "git",
        "global_name": "globalName",
        "hdfs": "hdfs",
        "http": "http",
        "mode": "mode",
        "optional": "optional",
        "oss": "oss",
        "path": "path",
        "raw": "raw",
        "recurse_mode": "recurseMode",
        "s3": "s3",
        "sub_path": "subPath",
    },
)
class Artifact:
    def __init__(
        self,
        *,
        name: builtins.str,
        archive: typing.Optional[ArchiveStrategy] = None,
        archive_logs: typing.Optional[builtins.bool] = None,
        artifactory: typing.Optional["ArtifactoryArtifact"] = None,
        from_: typing.Optional[builtins.str] = None,
        from_expression: typing.Optional[builtins.str] = None,
        gcs: typing.Optional["GCSArtifact"] = None,
        git: typing.Optional["GitArtifact"] = None,
        global_name: typing.Optional[builtins.str] = None,
        hdfs: typing.Optional["HDFSArtifact"] = None,
        http: typing.Optional["HTTPArtifact"] = None,
        mode: typing.Optional[jsii.Number] = None,
        optional: typing.Optional[builtins.bool] = None,
        oss: typing.Optional["OSSArtifact"] = None,
        path: typing.Optional[builtins.str] = None,
        raw: typing.Optional["RawArtifact"] = None,
        recurse_mode: typing.Optional[builtins.bool] = None,
        s3: typing.Optional["S3Artifact"] = None,
        sub_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: 
        :param archive: 
        :param archive_logs: 
        :param artifactory: 
        :param from_: 
        :param from_expression: 
        :param gcs: 
        :param git: 
        :param global_name: 
        :param hdfs: 
        :param http: 
        :param mode: 
        :param optional: 
        :param oss: 
        :param path: 
        :param raw: 
        :param recurse_mode: 
        :param s3: 
        :param sub_path: 
        '''
        if isinstance(archive, dict):
            archive = ArchiveStrategy(**archive)
        if isinstance(artifactory, dict):
            artifactory = ArtifactoryArtifact(**artifactory)
        if isinstance(gcs, dict):
            gcs = GCSArtifact(**gcs)
        if isinstance(git, dict):
            git = GitArtifact(**git)
        if isinstance(hdfs, dict):
            hdfs = HDFSArtifact(**hdfs)
        if isinstance(http, dict):
            http = HTTPArtifact(**http)
        if isinstance(oss, dict):
            oss = OSSArtifact(**oss)
        if isinstance(raw, dict):
            raw = RawArtifact(**raw)
        if isinstance(s3, dict):
            s3 = S3Artifact(**s3)
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }
        if archive is not None:
            self._values["archive"] = archive
        if archive_logs is not None:
            self._values["archive_logs"] = archive_logs
        if artifactory is not None:
            self._values["artifactory"] = artifactory
        if from_ is not None:
            self._values["from_"] = from_
        if from_expression is not None:
            self._values["from_expression"] = from_expression
        if gcs is not None:
            self._values["gcs"] = gcs
        if git is not None:
            self._values["git"] = git
        if global_name is not None:
            self._values["global_name"] = global_name
        if hdfs is not None:
            self._values["hdfs"] = hdfs
        if http is not None:
            self._values["http"] = http
        if mode is not None:
            self._values["mode"] = mode
        if optional is not None:
            self._values["optional"] = optional
        if oss is not None:
            self._values["oss"] = oss
        if path is not None:
            self._values["path"] = path
        if raw is not None:
            self._values["raw"] = raw
        if recurse_mode is not None:
            self._values["recurse_mode"] = recurse_mode
        if s3 is not None:
            self._values["s3"] = s3
        if sub_path is not None:
            self._values["sub_path"] = sub_path

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def archive(self) -> typing.Optional[ArchiveStrategy]:
        result = self._values.get("archive")
        return typing.cast(typing.Optional[ArchiveStrategy], result)

    @builtins.property
    def archive_logs(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("archive_logs")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def artifactory(self) -> typing.Optional["ArtifactoryArtifact"]:
        result = self._values.get("artifactory")
        return typing.cast(typing.Optional["ArtifactoryArtifact"], result)

    @builtins.property
    def from_(self) -> typing.Optional[builtins.str]:
        result = self._values.get("from_")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def from_expression(self) -> typing.Optional[builtins.str]:
        result = self._values.get("from_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gcs(self) -> typing.Optional["GCSArtifact"]:
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["GCSArtifact"], result)

    @builtins.property
    def git(self) -> typing.Optional["GitArtifact"]:
        result = self._values.get("git")
        return typing.cast(typing.Optional["GitArtifact"], result)

    @builtins.property
    def global_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("global_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hdfs(self) -> typing.Optional["HDFSArtifact"]:
        result = self._values.get("hdfs")
        return typing.cast(typing.Optional["HDFSArtifact"], result)

    @builtins.property
    def http(self) -> typing.Optional["HTTPArtifact"]:
        result = self._values.get("http")
        return typing.cast(typing.Optional["HTTPArtifact"], result)

    @builtins.property
    def mode(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("mode")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def optional(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("optional")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def oss(self) -> typing.Optional["OSSArtifact"]:
        result = self._values.get("oss")
        return typing.cast(typing.Optional["OSSArtifact"], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def raw(self) -> typing.Optional["RawArtifact"]:
        result = self._values.get("raw")
        return typing.cast(typing.Optional["RawArtifact"], result)

    @builtins.property
    def recurse_mode(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("recurse_mode")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def s3(self) -> typing.Optional["S3Artifact"]:
        result = self._values.get("s3")
        return typing.cast(typing.Optional["S3Artifact"], result)

    @builtins.property
    def sub_path(self) -> typing.Optional[builtins.str]:
        result = self._values.get("sub_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Artifact(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.ArtifactLocation",
    jsii_struct_bases=[],
    name_mapping={
        "archive_logs": "archiveLogs",
        "artifactory": "artifactory",
        "gcs": "gcs",
        "git": "git",
        "hdfs": "hdfs",
        "http": "http",
        "oss": "oss",
        "raw": "raw",
        "s3": "s3",
    },
)
class ArtifactLocation:
    def __init__(
        self,
        *,
        archive_logs: typing.Optional[builtins.bool] = None,
        artifactory: typing.Optional["ArtifactoryArtifact"] = None,
        gcs: typing.Optional["GCSArtifact"] = None,
        git: typing.Optional["GitArtifact"] = None,
        hdfs: typing.Optional["HDFSArtifact"] = None,
        http: typing.Optional["HTTPArtifact"] = None,
        oss: typing.Optional["OSSArtifact"] = None,
        raw: typing.Optional["RawArtifact"] = None,
        s3: typing.Optional["S3Artifact"] = None,
    ) -> None:
        '''
        :param archive_logs: 
        :param artifactory: 
        :param gcs: 
        :param git: 
        :param hdfs: 
        :param http: 
        :param oss: 
        :param raw: 
        :param s3: 
        '''
        if isinstance(artifactory, dict):
            artifactory = ArtifactoryArtifact(**artifactory)
        if isinstance(gcs, dict):
            gcs = GCSArtifact(**gcs)
        if isinstance(git, dict):
            git = GitArtifact(**git)
        if isinstance(hdfs, dict):
            hdfs = HDFSArtifact(**hdfs)
        if isinstance(http, dict):
            http = HTTPArtifact(**http)
        if isinstance(oss, dict):
            oss = OSSArtifact(**oss)
        if isinstance(raw, dict):
            raw = RawArtifact(**raw)
        if isinstance(s3, dict):
            s3 = S3Artifact(**s3)
        self._values: typing.Dict[str, typing.Any] = {}
        if archive_logs is not None:
            self._values["archive_logs"] = archive_logs
        if artifactory is not None:
            self._values["artifactory"] = artifactory
        if gcs is not None:
            self._values["gcs"] = gcs
        if git is not None:
            self._values["git"] = git
        if hdfs is not None:
            self._values["hdfs"] = hdfs
        if http is not None:
            self._values["http"] = http
        if oss is not None:
            self._values["oss"] = oss
        if raw is not None:
            self._values["raw"] = raw
        if s3 is not None:
            self._values["s3"] = s3

    @builtins.property
    def archive_logs(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("archive_logs")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def artifactory(self) -> typing.Optional["ArtifactoryArtifact"]:
        result = self._values.get("artifactory")
        return typing.cast(typing.Optional["ArtifactoryArtifact"], result)

    @builtins.property
    def gcs(self) -> typing.Optional["GCSArtifact"]:
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["GCSArtifact"], result)

    @builtins.property
    def git(self) -> typing.Optional["GitArtifact"]:
        result = self._values.get("git")
        return typing.cast(typing.Optional["GitArtifact"], result)

    @builtins.property
    def hdfs(self) -> typing.Optional["HDFSArtifact"]:
        result = self._values.get("hdfs")
        return typing.cast(typing.Optional["HDFSArtifact"], result)

    @builtins.property
    def http(self) -> typing.Optional["HTTPArtifact"]:
        result = self._values.get("http")
        return typing.cast(typing.Optional["HTTPArtifact"], result)

    @builtins.property
    def oss(self) -> typing.Optional["OSSArtifact"]:
        result = self._values.get("oss")
        return typing.cast(typing.Optional["OSSArtifact"], result)

    @builtins.property
    def raw(self) -> typing.Optional["RawArtifact"]:
        result = self._values.get("raw")
        return typing.cast(typing.Optional["RawArtifact"], result)

    @builtins.property
    def s3(self) -> typing.Optional["S3Artifact"]:
        result = self._values.get("s3")
        return typing.cast(typing.Optional["S3Artifact"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactLocation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.ArtifactPaths",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "archive": "archive",
        "archive_logs": "archiveLogs",
        "artifactory": "artifactory",
        "from_": "from",
        "from_expression": "fromExpression",
        "gcs": "gcs",
        "git": "git",
        "global_name": "globalName",
        "hdfs": "hdfs",
        "http": "http",
        "mode": "mode",
        "optional": "optional",
        "oss": "oss",
        "path": "path",
        "raw": "raw",
        "recurse_mode": "recurseMode",
        "s3": "s3",
        "sub_path": "subPath",
    },
)
class ArtifactPaths:
    def __init__(
        self,
        *,
        name: builtins.str,
        archive: typing.Optional[ArchiveStrategy] = None,
        archive_logs: typing.Optional[builtins.bool] = None,
        artifactory: typing.Optional["ArtifactoryArtifact"] = None,
        from_: typing.Optional[builtins.str] = None,
        from_expression: typing.Optional[builtins.str] = None,
        gcs: typing.Optional["GCSArtifact"] = None,
        git: typing.Optional["GitArtifact"] = None,
        global_name: typing.Optional[builtins.str] = None,
        hdfs: typing.Optional["HDFSArtifact"] = None,
        http: typing.Optional["HTTPArtifact"] = None,
        mode: typing.Optional[jsii.Number] = None,
        optional: typing.Optional[builtins.bool] = None,
        oss: typing.Optional["OSSArtifact"] = None,
        path: typing.Optional[builtins.str] = None,
        raw: typing.Optional["RawArtifact"] = None,
        recurse_mode: typing.Optional[builtins.bool] = None,
        s3: typing.Optional["S3Artifact"] = None,
        sub_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: 
        :param archive: 
        :param archive_logs: 
        :param artifactory: 
        :param from_: 
        :param from_expression: 
        :param gcs: 
        :param git: 
        :param global_name: 
        :param hdfs: 
        :param http: 
        :param mode: 
        :param optional: 
        :param oss: 
        :param path: 
        :param raw: 
        :param recurse_mode: 
        :param s3: 
        :param sub_path: 
        '''
        if isinstance(archive, dict):
            archive = ArchiveStrategy(**archive)
        if isinstance(artifactory, dict):
            artifactory = ArtifactoryArtifact(**artifactory)
        if isinstance(gcs, dict):
            gcs = GCSArtifact(**gcs)
        if isinstance(git, dict):
            git = GitArtifact(**git)
        if isinstance(hdfs, dict):
            hdfs = HDFSArtifact(**hdfs)
        if isinstance(http, dict):
            http = HTTPArtifact(**http)
        if isinstance(oss, dict):
            oss = OSSArtifact(**oss)
        if isinstance(raw, dict):
            raw = RawArtifact(**raw)
        if isinstance(s3, dict):
            s3 = S3Artifact(**s3)
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }
        if archive is not None:
            self._values["archive"] = archive
        if archive_logs is not None:
            self._values["archive_logs"] = archive_logs
        if artifactory is not None:
            self._values["artifactory"] = artifactory
        if from_ is not None:
            self._values["from_"] = from_
        if from_expression is not None:
            self._values["from_expression"] = from_expression
        if gcs is not None:
            self._values["gcs"] = gcs
        if git is not None:
            self._values["git"] = git
        if global_name is not None:
            self._values["global_name"] = global_name
        if hdfs is not None:
            self._values["hdfs"] = hdfs
        if http is not None:
            self._values["http"] = http
        if mode is not None:
            self._values["mode"] = mode
        if optional is not None:
            self._values["optional"] = optional
        if oss is not None:
            self._values["oss"] = oss
        if path is not None:
            self._values["path"] = path
        if raw is not None:
            self._values["raw"] = raw
        if recurse_mode is not None:
            self._values["recurse_mode"] = recurse_mode
        if s3 is not None:
            self._values["s3"] = s3
        if sub_path is not None:
            self._values["sub_path"] = sub_path

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def archive(self) -> typing.Optional[ArchiveStrategy]:
        result = self._values.get("archive")
        return typing.cast(typing.Optional[ArchiveStrategy], result)

    @builtins.property
    def archive_logs(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("archive_logs")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def artifactory(self) -> typing.Optional["ArtifactoryArtifact"]:
        result = self._values.get("artifactory")
        return typing.cast(typing.Optional["ArtifactoryArtifact"], result)

    @builtins.property
    def from_(self) -> typing.Optional[builtins.str]:
        result = self._values.get("from_")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def from_expression(self) -> typing.Optional[builtins.str]:
        result = self._values.get("from_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gcs(self) -> typing.Optional["GCSArtifact"]:
        result = self._values.get("gcs")
        return typing.cast(typing.Optional["GCSArtifact"], result)

    @builtins.property
    def git(self) -> typing.Optional["GitArtifact"]:
        result = self._values.get("git")
        return typing.cast(typing.Optional["GitArtifact"], result)

    @builtins.property
    def global_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("global_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hdfs(self) -> typing.Optional["HDFSArtifact"]:
        result = self._values.get("hdfs")
        return typing.cast(typing.Optional["HDFSArtifact"], result)

    @builtins.property
    def http(self) -> typing.Optional["HTTPArtifact"]:
        result = self._values.get("http")
        return typing.cast(typing.Optional["HTTPArtifact"], result)

    @builtins.property
    def mode(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("mode")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def optional(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("optional")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def oss(self) -> typing.Optional["OSSArtifact"]:
        result = self._values.get("oss")
        return typing.cast(typing.Optional["OSSArtifact"], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def raw(self) -> typing.Optional["RawArtifact"]:
        result = self._values.get("raw")
        return typing.cast(typing.Optional["RawArtifact"], result)

    @builtins.property
    def recurse_mode(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("recurse_mode")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def s3(self) -> typing.Optional["S3Artifact"]:
        result = self._values.get("s3")
        return typing.cast(typing.Optional["S3Artifact"], result)

    @builtins.property
    def sub_path(self) -> typing.Optional[builtins.str]:
        result = self._values.get("sub_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactPaths(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.ArtifactRepositoryRef",
    jsii_struct_bases=[],
    name_mapping={"config_map": "configMap", "key": "key"},
)
class ArtifactRepositoryRef:
    def __init__(
        self,
        *,
        config_map: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param config_map: 
        :param key: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if config_map is not None:
            self._values["config_map"] = config_map
        if key is not None:
            self._values["key"] = key

    @builtins.property
    def config_map(self) -> typing.Optional[builtins.str]:
        result = self._values.get("config_map")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRepositoryRef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.ArtifactRepositoryRefStatus",
    jsii_struct_bases=[],
    name_mapping={
        "config_map": "configMap",
        "default": "default",
        "key": "key",
        "namespace": "namespace",
    },
)
class ArtifactRepositoryRefStatus:
    def __init__(
        self,
        *,
        config_map: typing.Optional[builtins.str] = None,
        default: typing.Optional[builtins.bool] = None,
        key: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param config_map: 
        :param default: 
        :param key: 
        :param namespace: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if config_map is not None:
            self._values["config_map"] = config_map
        if default is not None:
            self._values["default"] = default
        if key is not None:
            self._values["key"] = key
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def config_map(self) -> typing.Optional[builtins.str]:
        result = self._values.get("config_map")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("default")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactRepositoryRefStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.ArtifactoryArtifact",
    jsii_struct_bases=[],
    name_mapping={
        "url": "url",
        "password_secret": "passwordSecret",
        "username_secret": "usernameSecret",
    },
)
class ArtifactoryArtifact:
    def __init__(
        self,
        *,
        url: builtins.str,
        password_secret: typing.Optional[_SecretKeySelector_3834a17e] = None,
        username_secret: typing.Optional[_SecretKeySelector_3834a17e] = None,
    ) -> None:
        '''
        :param url: 
        :param password_secret: 
        :param username_secret: 
        '''
        if isinstance(password_secret, dict):
            password_secret = _SecretKeySelector_3834a17e(**password_secret)
        if isinstance(username_secret, dict):
            username_secret = _SecretKeySelector_3834a17e(**username_secret)
        self._values: typing.Dict[str, typing.Any] = {
            "url": url,
        }
        if password_secret is not None:
            self._values["password_secret"] = password_secret
        if username_secret is not None:
            self._values["username_secret"] = username_secret

    @builtins.property
    def url(self) -> builtins.str:
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password_secret(self) -> typing.Optional[_SecretKeySelector_3834a17e]:
        result = self._values.get("password_secret")
        return typing.cast(typing.Optional[_SecretKeySelector_3834a17e], result)

    @builtins.property
    def username_secret(self) -> typing.Optional[_SecretKeySelector_3834a17e]:
        result = self._values.get("username_secret")
        return typing.cast(typing.Optional[_SecretKeySelector_3834a17e], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactoryArtifact(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.Backoff",
    jsii_struct_bases=[],
    name_mapping={
        "duration": "duration",
        "factor": "factor",
        "max_duration": "maxDuration",
    },
)
class Backoff:
    def __init__(
        self,
        *,
        duration: typing.Optional[builtins.str] = None,
        factor: typing.Optional[_IntOrString_f14b6057] = None,
        max_duration: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param duration: 
        :param factor: 
        :param max_duration: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if duration is not None:
            self._values["duration"] = duration
        if factor is not None:
            self._values["factor"] = factor
        if max_duration is not None:
            self._values["max_duration"] = max_duration

    @builtins.property
    def duration(self) -> typing.Optional[builtins.str]:
        result = self._values.get("duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def factor(self) -> typing.Optional[_IntOrString_f14b6057]:
        result = self._values.get("factor")
        return typing.cast(typing.Optional[_IntOrString_f14b6057], result)

    @builtins.property
    def max_duration(self) -> typing.Optional[builtins.str]:
        result = self._values.get("max_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Backoff(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.Cache",
    jsii_struct_bases=[],
    name_mapping={"config_map": "configMap"},
)
class Cache:
    def __init__(self, *, config_map: _ConfigMapKeySelector_655813de) -> None:
        '''
        :param config_map: 
        '''
        if isinstance(config_map, dict):
            config_map = _ConfigMapKeySelector_655813de(**config_map)
        self._values: typing.Dict[str, typing.Any] = {
            "config_map": config_map,
        }

    @builtins.property
    def config_map(self) -> _ConfigMapKeySelector_655813de:
        result = self._values.get("config_map")
        assert result is not None, "Required property 'config_map' is missing"
        return typing.cast(_ConfigMapKeySelector_655813de, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Cache(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.ClusterWorkflowTemplate",
    jsii_struct_bases=[],
    name_mapping={
        "metadata": "metadata",
        "spec": "spec",
        "api_version": "apiVersion",
        "kind": "kind",
    },
)
class ClusterWorkflowTemplate:
    def __init__(
        self,
        *,
        metadata: _ObjectMeta_77a65d46,
        spec: "WorkflowTemplateSpec",
        api_version: typing.Optional[builtins.str] = None,
        kind: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param metadata: 
        :param spec: 
        :param api_version: 
        :param kind: 
        '''
        if isinstance(metadata, dict):
            metadata = _ObjectMeta_77a65d46(**metadata)
        if isinstance(spec, dict):
            spec = WorkflowTemplateSpec(**spec)
        self._values: typing.Dict[str, typing.Any] = {
            "metadata": metadata,
            "spec": spec,
        }
        if api_version is not None:
            self._values["api_version"] = api_version
        if kind is not None:
            self._values["kind"] = kind

    @builtins.property
    def metadata(self) -> _ObjectMeta_77a65d46:
        result = self._values.get("metadata")
        assert result is not None, "Required property 'metadata' is missing"
        return typing.cast(_ObjectMeta_77a65d46, result)

    @builtins.property
    def spec(self) -> "WorkflowTemplateSpec":
        result = self._values.get("spec")
        assert result is not None, "Required property 'spec' is missing"
        return typing.cast("WorkflowTemplateSpec", result)

    @builtins.property
    def api_version(self) -> typing.Optional[builtins.str]:
        result = self._values.get("api_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kind(self) -> typing.Optional[builtins.str]:
        result = self._values.get("kind")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClusterWorkflowTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.ClusterWorkflowTemplateDeleteResponse",
    jsii_struct_bases=[],
    name_mapping={},
)
class ClusterWorkflowTemplateDeleteResponse:
    def __init__(self) -> None:
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClusterWorkflowTemplateDeleteResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.ClusterWorkflowTemplateLintRequest",
    jsii_struct_bases=[],
    name_mapping={"create_options": "createOptions", "template": "template"},
)
class ClusterWorkflowTemplateLintRequest:
    def __init__(
        self,
        *,
        create_options: typing.Optional[_CreateOptions_33e095be] = None,
        template: typing.Optional[ClusterWorkflowTemplate] = None,
    ) -> None:
        '''
        :param create_options: 
        :param template: 
        '''
        if isinstance(create_options, dict):
            create_options = _CreateOptions_33e095be(**create_options)
        if isinstance(template, dict):
            template = ClusterWorkflowTemplate(**template)
        self._values: typing.Dict[str, typing.Any] = {}
        if create_options is not None:
            self._values["create_options"] = create_options
        if template is not None:
            self._values["template"] = template

    @builtins.property
    def create_options(self) -> typing.Optional[_CreateOptions_33e095be]:
        result = self._values.get("create_options")
        return typing.cast(typing.Optional[_CreateOptions_33e095be], result)

    @builtins.property
    def template(self) -> typing.Optional[ClusterWorkflowTemplate]:
        result = self._values.get("template")
        return typing.cast(typing.Optional[ClusterWorkflowTemplate], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClusterWorkflowTemplateLintRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.ClusterWorkflowTemplateList",
    jsii_struct_bases=[],
    name_mapping={
        "items": "items",
        "metadata": "metadata",
        "api_version": "apiVersion",
        "kind": "kind",
    },
)
class ClusterWorkflowTemplateList:
    def __init__(
        self,
        *,
        items: typing.Sequence[ClusterWorkflowTemplate],
        metadata: _ListMeta_fcb8bed2,
        api_version: typing.Optional[builtins.str] = None,
        kind: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param items: 
        :param metadata: 
        :param api_version: 
        :param kind: 
        '''
        if isinstance(metadata, dict):
            metadata = _ListMeta_fcb8bed2(**metadata)
        self._values: typing.Dict[str, typing.Any] = {
            "items": items,
            "metadata": metadata,
        }
        if api_version is not None:
            self._values["api_version"] = api_version
        if kind is not None:
            self._values["kind"] = kind

    @builtins.property
    def items(self) -> typing.List[ClusterWorkflowTemplate]:
        result = self._values.get("items")
        assert result is not None, "Required property 'items' is missing"
        return typing.cast(typing.List[ClusterWorkflowTemplate], result)

    @builtins.property
    def metadata(self) -> _ListMeta_fcb8bed2:
        result = self._values.get("metadata")
        assert result is not None, "Required property 'metadata' is missing"
        return typing.cast(_ListMeta_fcb8bed2, result)

    @builtins.property
    def api_version(self) -> typing.Optional[builtins.str]:
        result = self._values.get("api_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kind(self) -> typing.Optional[builtins.str]:
        result = self._values.get("kind")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClusterWorkflowTemplateList(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.ClusterWorkflowTemplateUpdateRequest",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "template": "template"},
)
class ClusterWorkflowTemplateUpdateRequest:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        template: typing.Optional[ClusterWorkflowTemplate] = None,
    ) -> None:
        '''
        :param name: 
        :param template: 
        '''
        if isinstance(template, dict):
            template = ClusterWorkflowTemplate(**template)
        self._values: typing.Dict[str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if template is not None:
            self._values["template"] = template

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template(self) -> typing.Optional[ClusterWorkflowTemplate]:
        result = self._values.get("template")
        return typing.cast(typing.Optional[ClusterWorkflowTemplate], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClusterWorkflowTemplateUpdateRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.Condition",
    jsii_struct_bases=[],
    name_mapping={"message": "message", "status": "status", "type": "type"},
)
class Condition:
    def __init__(
        self,
        *,
        message: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param message: 
        :param status: 
        :param type: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if message is not None:
            self._values["message"] = message
        if status is not None:
            self._values["status"] = status
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def message(self) -> typing.Optional[builtins.str]:
        result = self._values.get("message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Condition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.ContainerNode",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "args": "args",
        "command": "command",
        "dependencies": "dependencies",
        "env": "env",
        "env_from": "envFrom",
        "image": "image",
        "image_pull_policy": "imagePullPolicy",
        "lifecycle": "lifecycle",
        "liveness_probe": "livenessProbe",
        "ports": "ports",
        "readiness_probe": "readinessProbe",
        "resources": "resources",
        "security_context": "securityContext",
        "startup_probe": "startupProbe",
        "stdin": "stdin",
        "stdin_once": "stdinOnce",
        "termination_message_path": "terminationMessagePath",
        "termination_message_policy": "terminationMessagePolicy",
        "tty": "tty",
        "volume_devices": "volumeDevices",
        "volume_mounts": "volumeMounts",
        "working_dir": "workingDir",
    },
)
class ContainerNode:
    def __init__(
        self,
        *,
        name: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        env: typing.Optional[typing.Sequence[_EnvVar_1741b5ed]] = None,
        env_from: typing.Optional[typing.Sequence[_EnvFromSource_35bf044a]] = None,
        image: typing.Optional[builtins.str] = None,
        image_pull_policy: typing.Optional[builtins.str] = None,
        lifecycle: typing.Optional[_Lifecycle_780bc732] = None,
        liveness_probe: typing.Optional[_Probe_6e8f94fa] = None,
        ports: typing.Optional[typing.Sequence[_ContainerPort_1a56bbf5]] = None,
        readiness_probe: typing.Optional[_Probe_6e8f94fa] = None,
        resources: typing.Optional[_ResourceRequirements_892d16ec] = None,
        security_context: typing.Optional[_SecurityContext_a4b1b9fb] = None,
        startup_probe: typing.Optional[_Probe_6e8f94fa] = None,
        stdin: typing.Optional[builtins.bool] = None,
        stdin_once: typing.Optional[builtins.bool] = None,
        termination_message_path: typing.Optional[builtins.str] = None,
        termination_message_policy: typing.Optional[builtins.str] = None,
        tty: typing.Optional[builtins.bool] = None,
        volume_devices: typing.Optional[typing.Sequence[_VolumeDevice_aae53ff5]] = None,
        volume_mounts: typing.Optional[typing.Sequence[_VolumeMount_366b43c7]] = None,
        working_dir: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: 
        :param args: 
        :param command: 
        :param dependencies: 
        :param env: 
        :param env_from: 
        :param image: 
        :param image_pull_policy: 
        :param lifecycle: 
        :param liveness_probe: 
        :param ports: 
        :param readiness_probe: 
        :param resources: 
        :param security_context: 
        :param startup_probe: 
        :param stdin: 
        :param stdin_once: 
        :param termination_message_path: 
        :param termination_message_policy: 
        :param tty: 
        :param volume_devices: 
        :param volume_mounts: 
        :param working_dir: 
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _Lifecycle_780bc732(**lifecycle)
        if isinstance(liveness_probe, dict):
            liveness_probe = _Probe_6e8f94fa(**liveness_probe)
        if isinstance(readiness_probe, dict):
            readiness_probe = _Probe_6e8f94fa(**readiness_probe)
        if isinstance(resources, dict):
            resources = _ResourceRequirements_892d16ec(**resources)
        if isinstance(security_context, dict):
            security_context = _SecurityContext_a4b1b9fb(**security_context)
        if isinstance(startup_probe, dict):
            startup_probe = _Probe_6e8f94fa(**startup_probe)
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }
        if args is not None:
            self._values["args"] = args
        if command is not None:
            self._values["command"] = command
        if dependencies is not None:
            self._values["dependencies"] = dependencies
        if env is not None:
            self._values["env"] = env
        if env_from is not None:
            self._values["env_from"] = env_from
        if image is not None:
            self._values["image"] = image
        if image_pull_policy is not None:
            self._values["image_pull_policy"] = image_pull_policy
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if liveness_probe is not None:
            self._values["liveness_probe"] = liveness_probe
        if ports is not None:
            self._values["ports"] = ports
        if readiness_probe is not None:
            self._values["readiness_probe"] = readiness_probe
        if resources is not None:
            self._values["resources"] = resources
        if security_context is not None:
            self._values["security_context"] = security_context
        if startup_probe is not None:
            self._values["startup_probe"] = startup_probe
        if stdin is not None:
            self._values["stdin"] = stdin
        if stdin_once is not None:
            self._values["stdin_once"] = stdin_once
        if termination_message_path is not None:
            self._values["termination_message_path"] = termination_message_path
        if termination_message_policy is not None:
            self._values["termination_message_policy"] = termination_message_policy
        if tty is not None:
            self._values["tty"] = tty
        if volume_devices is not None:
            self._values["volume_devices"] = volume_devices
        if volume_mounts is not None:
            self._values["volume_mounts"] = volume_mounts
        if working_dir is not None:
            self._values["working_dir"] = working_dir

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dependencies(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("dependencies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.List[_EnvVar_1741b5ed]]:
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.List[_EnvVar_1741b5ed]], result)

    @builtins.property
    def env_from(self) -> typing.Optional[typing.List[_EnvFromSource_35bf044a]]:
        result = self._values.get("env_from")
        return typing.cast(typing.Optional[typing.List[_EnvFromSource_35bf044a]], result)

    @builtins.property
    def image(self) -> typing.Optional[builtins.str]:
        result = self._values.get("image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_pull_policy(self) -> typing.Optional[builtins.str]:
        result = self._values.get("image_pull_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_Lifecycle_780bc732]:
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_Lifecycle_780bc732], result)

    @builtins.property
    def liveness_probe(self) -> typing.Optional[_Probe_6e8f94fa]:
        result = self._values.get("liveness_probe")
        return typing.cast(typing.Optional[_Probe_6e8f94fa], result)

    @builtins.property
    def ports(self) -> typing.Optional[typing.List[_ContainerPort_1a56bbf5]]:
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.List[_ContainerPort_1a56bbf5]], result)

    @builtins.property
    def readiness_probe(self) -> typing.Optional[_Probe_6e8f94fa]:
        result = self._values.get("readiness_probe")
        return typing.cast(typing.Optional[_Probe_6e8f94fa], result)

    @builtins.property
    def resources(self) -> typing.Optional[_ResourceRequirements_892d16ec]:
        result = self._values.get("resources")
        return typing.cast(typing.Optional[_ResourceRequirements_892d16ec], result)

    @builtins.property
    def security_context(self) -> typing.Optional[_SecurityContext_a4b1b9fb]:
        result = self._values.get("security_context")
        return typing.cast(typing.Optional[_SecurityContext_a4b1b9fb], result)

    @builtins.property
    def startup_probe(self) -> typing.Optional[_Probe_6e8f94fa]:
        result = self._values.get("startup_probe")
        return typing.cast(typing.Optional[_Probe_6e8f94fa], result)

    @builtins.property
    def stdin(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("stdin")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stdin_once(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("stdin_once")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def termination_message_path(self) -> typing.Optional[builtins.str]:
        result = self._values.get("termination_message_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def termination_message_policy(self) -> typing.Optional[builtins.str]:
        result = self._values.get("termination_message_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tty(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("tty")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def volume_devices(self) -> typing.Optional[typing.List[_VolumeDevice_aae53ff5]]:
        result = self._values.get("volume_devices")
        return typing.cast(typing.Optional[typing.List[_VolumeDevice_aae53ff5]], result)

    @builtins.property
    def volume_mounts(self) -> typing.Optional[typing.List[_VolumeMount_366b43c7]]:
        result = self._values.get("volume_mounts")
        return typing.cast(typing.Optional[typing.List[_VolumeMount_366b43c7]], result)

    @builtins.property
    def working_dir(self) -> typing.Optional[builtins.str]:
        result = self._values.get("working_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerNode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.ContainerSetTemplate",
    jsii_struct_bases=[],
    name_mapping={"containers": "containers", "volume_mounts": "volumeMounts"},
)
class ContainerSetTemplate:
    def __init__(
        self,
        *,
        containers: typing.Sequence[ContainerNode],
        volume_mounts: typing.Optional[typing.Sequence[_VolumeMount_366b43c7]] = None,
    ) -> None:
        '''
        :param containers: 
        :param volume_mounts: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "containers": containers,
        }
        if volume_mounts is not None:
            self._values["volume_mounts"] = volume_mounts

    @builtins.property
    def containers(self) -> typing.List[ContainerNode]:
        result = self._values.get("containers")
        assert result is not None, "Required property 'containers' is missing"
        return typing.cast(typing.List[ContainerNode], result)

    @builtins.property
    def volume_mounts(self) -> typing.Optional[typing.List[_VolumeMount_366b43c7]]:
        result = self._values.get("volume_mounts")
        return typing.cast(typing.Optional[typing.List[_VolumeMount_366b43c7]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerSetTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.ContinueOn",
    jsii_struct_bases=[],
    name_mapping={"error": "error", "failed": "failed"},
)
class ContinueOn:
    def __init__(
        self,
        *,
        error: typing.Optional[builtins.bool] = None,
        failed: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param error: 
        :param failed: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if error is not None:
            self._values["error"] = error
        if failed is not None:
            self._values["failed"] = failed

    @builtins.property
    def error(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("error")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def failed(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("failed")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContinueOn(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.Counter",
    jsii_struct_bases=[],
    name_mapping={"value": "value"},
)
class Counter:
    def __init__(self, *, value: builtins.str) -> None:
        '''
        :param value: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "value": value,
        }

    @builtins.property
    def value(self) -> builtins.str:
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Counter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.CreateCronWorkflowRequest",
    jsii_struct_bases=[],
    name_mapping={
        "create_options": "createOptions",
        "cron_workflow": "cronWorkflow",
        "namespace": "namespace",
    },
)
class CreateCronWorkflowRequest:
    def __init__(
        self,
        *,
        create_options: typing.Optional[_CreateOptions_33e095be] = None,
        cron_workflow: typing.Optional["CronWorkflow"] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create_options: 
        :param cron_workflow: 
        :param namespace: 
        '''
        if isinstance(create_options, dict):
            create_options = _CreateOptions_33e095be(**create_options)
        if isinstance(cron_workflow, dict):
            cron_workflow = CronWorkflow(**cron_workflow)
        self._values: typing.Dict[str, typing.Any] = {}
        if create_options is not None:
            self._values["create_options"] = create_options
        if cron_workflow is not None:
            self._values["cron_workflow"] = cron_workflow
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def create_options(self) -> typing.Optional[_CreateOptions_33e095be]:
        result = self._values.get("create_options")
        return typing.cast(typing.Optional[_CreateOptions_33e095be], result)

    @builtins.property
    def cron_workflow(self) -> typing.Optional["CronWorkflow"]:
        result = self._values.get("cron_workflow")
        return typing.cast(typing.Optional["CronWorkflow"], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CreateCronWorkflowRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.CreateS3BucketOptions",
    jsii_struct_bases=[],
    name_mapping={"object_locking": "objectLocking"},
)
class CreateS3BucketOptions:
    def __init__(
        self,
        *,
        object_locking: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param object_locking: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if object_locking is not None:
            self._values["object_locking"] = object_locking

    @builtins.property
    def object_locking(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("object_locking")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CreateS3BucketOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.CronWorkflow",
    jsii_struct_bases=[],
    name_mapping={"metadata": "metadata", "spec": "spec", "status": "status"},
)
class CronWorkflow:
    def __init__(
        self,
        *,
        metadata: _ObjectMeta_77a65d46,
        spec: "CronWorkflowSpec",
        status: typing.Optional["CronWorkflowStatus"] = None,
    ) -> None:
        '''
        :param metadata: 
        :param spec: 
        :param status: 
        '''
        if isinstance(metadata, dict):
            metadata = _ObjectMeta_77a65d46(**metadata)
        if isinstance(spec, dict):
            spec = CronWorkflowSpec(**spec)
        if isinstance(status, dict):
            status = CronWorkflowStatus(**status)
        self._values: typing.Dict[str, typing.Any] = {
            "metadata": metadata,
            "spec": spec,
        }
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def metadata(self) -> _ObjectMeta_77a65d46:
        result = self._values.get("metadata")
        assert result is not None, "Required property 'metadata' is missing"
        return typing.cast(_ObjectMeta_77a65d46, result)

    @builtins.property
    def spec(self) -> "CronWorkflowSpec":
        result = self._values.get("spec")
        assert result is not None, "Required property 'spec' is missing"
        return typing.cast("CronWorkflowSpec", result)

    @builtins.property
    def status(self) -> typing.Optional["CronWorkflowStatus"]:
        result = self._values.get("status")
        return typing.cast(typing.Optional["CronWorkflowStatus"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CronWorkflow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.CronWorkflowDeletedResponse",
    jsii_struct_bases=[],
    name_mapping={},
)
class CronWorkflowDeletedResponse:
    def __init__(self) -> None:
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CronWorkflowDeletedResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.CronWorkflowList",
    jsii_struct_bases=[],
    name_mapping={
        "items": "items",
        "metadata": "metadata",
        "api_version": "apiVersion",
        "kind": "kind",
    },
)
class CronWorkflowList:
    def __init__(
        self,
        *,
        items: typing.Sequence[CronWorkflow],
        metadata: _ListMeta_fcb8bed2,
        api_version: typing.Optional[builtins.str] = None,
        kind: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param items: 
        :param metadata: 
        :param api_version: 
        :param kind: 
        '''
        if isinstance(metadata, dict):
            metadata = _ListMeta_fcb8bed2(**metadata)
        self._values: typing.Dict[str, typing.Any] = {
            "items": items,
            "metadata": metadata,
        }
        if api_version is not None:
            self._values["api_version"] = api_version
        if kind is not None:
            self._values["kind"] = kind

    @builtins.property
    def items(self) -> typing.List[CronWorkflow]:
        result = self._values.get("items")
        assert result is not None, "Required property 'items' is missing"
        return typing.cast(typing.List[CronWorkflow], result)

    @builtins.property
    def metadata(self) -> _ListMeta_fcb8bed2:
        result = self._values.get("metadata")
        assert result is not None, "Required property 'metadata' is missing"
        return typing.cast(_ListMeta_fcb8bed2, result)

    @builtins.property
    def api_version(self) -> typing.Optional[builtins.str]:
        result = self._values.get("api_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kind(self) -> typing.Optional[builtins.str]:
        result = self._values.get("kind")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CronWorkflowList(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.CronWorkflowResumeRequest",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "namespace": "namespace"},
)
class CronWorkflowResumeRequest:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: 
        :param namespace: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CronWorkflowResumeRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.CronWorkflowSpec",
    jsii_struct_bases=[],
    name_mapping={
        "schedule": "schedule",
        "workflow_spec": "workflowSpec",
        "concurrency_policy": "concurrencyPolicy",
        "failed_jobs_history_limit": "failedJobsHistoryLimit",
        "starting_deadline_seconds": "startingDeadlineSeconds",
        "successful_jobs_history_limit": "successfulJobsHistoryLimit",
        "suspend": "suspend",
        "timezone": "timezone",
        "workflow_metadata": "workflowMetadata",
    },
)
class CronWorkflowSpec:
    def __init__(
        self,
        *,
        schedule: builtins.str,
        workflow_spec: "WorkflowSpec",
        concurrency_policy: typing.Optional[builtins.str] = None,
        failed_jobs_history_limit: typing.Optional[jsii.Number] = None,
        starting_deadline_seconds: typing.Optional[jsii.Number] = None,
        successful_jobs_history_limit: typing.Optional[jsii.Number] = None,
        suspend: typing.Optional[builtins.bool] = None,
        timezone: typing.Optional[builtins.str] = None,
        workflow_metadata: typing.Optional[_ObjectMeta_77a65d46] = None,
    ) -> None:
        '''
        :param schedule: 
        :param workflow_spec: 
        :param concurrency_policy: 
        :param failed_jobs_history_limit: 
        :param starting_deadline_seconds: 
        :param successful_jobs_history_limit: 
        :param suspend: 
        :param timezone: 
        :param workflow_metadata: 
        '''
        if isinstance(workflow_spec, dict):
            workflow_spec = WorkflowSpec(**workflow_spec)
        if isinstance(workflow_metadata, dict):
            workflow_metadata = _ObjectMeta_77a65d46(**workflow_metadata)
        self._values: typing.Dict[str, typing.Any] = {
            "schedule": schedule,
            "workflow_spec": workflow_spec,
        }
        if concurrency_policy is not None:
            self._values["concurrency_policy"] = concurrency_policy
        if failed_jobs_history_limit is not None:
            self._values["failed_jobs_history_limit"] = failed_jobs_history_limit
        if starting_deadline_seconds is not None:
            self._values["starting_deadline_seconds"] = starting_deadline_seconds
        if successful_jobs_history_limit is not None:
            self._values["successful_jobs_history_limit"] = successful_jobs_history_limit
        if suspend is not None:
            self._values["suspend"] = suspend
        if timezone is not None:
            self._values["timezone"] = timezone
        if workflow_metadata is not None:
            self._values["workflow_metadata"] = workflow_metadata

    @builtins.property
    def schedule(self) -> builtins.str:
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workflow_spec(self) -> "WorkflowSpec":
        result = self._values.get("workflow_spec")
        assert result is not None, "Required property 'workflow_spec' is missing"
        return typing.cast("WorkflowSpec", result)

    @builtins.property
    def concurrency_policy(self) -> typing.Optional[builtins.str]:
        result = self._values.get("concurrency_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def failed_jobs_history_limit(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("failed_jobs_history_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def starting_deadline_seconds(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("starting_deadline_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def successful_jobs_history_limit(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("successful_jobs_history_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def suspend(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("suspend")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def timezone(self) -> typing.Optional[builtins.str]:
        result = self._values.get("timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workflow_metadata(self) -> typing.Optional[_ObjectMeta_77a65d46]:
        result = self._values.get("workflow_metadata")
        return typing.cast(typing.Optional[_ObjectMeta_77a65d46], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CronWorkflowSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.CronWorkflowStatus",
    jsii_struct_bases=[],
    name_mapping={
        "active": "active",
        "conditions": "conditions",
        "last_scheduled_time": "lastScheduledTime",
    },
)
class CronWorkflowStatus:
    def __init__(
        self,
        *,
        active: typing.Sequence[_ObjectReference_880f8d2d],
        conditions: typing.Sequence[Condition],
        last_scheduled_time: datetime.datetime,
    ) -> None:
        '''
        :param active: 
        :param conditions: 
        :param last_scheduled_time: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "active": active,
            "conditions": conditions,
            "last_scheduled_time": last_scheduled_time,
        }

    @builtins.property
    def active(self) -> typing.List[_ObjectReference_880f8d2d]:
        result = self._values.get("active")
        assert result is not None, "Required property 'active' is missing"
        return typing.cast(typing.List[_ObjectReference_880f8d2d], result)

    @builtins.property
    def conditions(self) -> typing.List[Condition]:
        result = self._values.get("conditions")
        assert result is not None, "Required property 'conditions' is missing"
        return typing.cast(typing.List[Condition], result)

    @builtins.property
    def last_scheduled_time(self) -> datetime.datetime:
        result = self._values.get("last_scheduled_time")
        assert result is not None, "Required property 'last_scheduled_time' is missing"
        return typing.cast(datetime.datetime, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CronWorkflowStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.CronWorkflowSuspendRequest",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "namespace": "namespace"},
)
class CronWorkflowSuspendRequest:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: 
        :param namespace: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CronWorkflowSuspendRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.DAGTask",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "arguments": "arguments",
        "continue_on": "continueOn",
        "dependencies": "dependencies",
        "depends": "depends",
        "on_exit": "onExit",
        "template": "template",
        "template_ref": "templateRef",
        "when": "when",
        "with_items": "withItems",
        "with_param": "withParam",
        "with_sequence": "withSequence",
    },
)
class DAGTask:
    def __init__(
        self,
        *,
        name: builtins.str,
        arguments: typing.Optional[Arguments] = None,
        continue_on: typing.Optional[ContinueOn] = None,
        dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        depends: typing.Optional[builtins.str] = None,
        on_exit: typing.Optional[builtins.str] = None,
        template: typing.Optional[builtins.str] = None,
        template_ref: typing.Optional["TemplateRef"] = None,
        when: typing.Optional[builtins.str] = None,
        with_items: typing.Optional[typing.Sequence[typing.Any]] = None,
        with_param: typing.Optional[builtins.str] = None,
        with_sequence: typing.Optional["Sequence"] = None,
    ) -> None:
        '''
        :param name: 
        :param arguments: 
        :param continue_on: 
        :param dependencies: 
        :param depends: 
        :param on_exit: 
        :param template: 
        :param template_ref: 
        :param when: 
        :param with_items: 
        :param with_param: 
        :param with_sequence: 
        '''
        if isinstance(arguments, dict):
            arguments = Arguments(**arguments)
        if isinstance(continue_on, dict):
            continue_on = ContinueOn(**continue_on)
        if isinstance(template_ref, dict):
            template_ref = TemplateRef(**template_ref)
        if isinstance(with_sequence, dict):
            with_sequence = Sequence(**with_sequence)
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }
        if arguments is not None:
            self._values["arguments"] = arguments
        if continue_on is not None:
            self._values["continue_on"] = continue_on
        if dependencies is not None:
            self._values["dependencies"] = dependencies
        if depends is not None:
            self._values["depends"] = depends
        if on_exit is not None:
            self._values["on_exit"] = on_exit
        if template is not None:
            self._values["template"] = template
        if template_ref is not None:
            self._values["template_ref"] = template_ref
        if when is not None:
            self._values["when"] = when
        if with_items is not None:
            self._values["with_items"] = with_items
        if with_param is not None:
            self._values["with_param"] = with_param
        if with_sequence is not None:
            self._values["with_sequence"] = with_sequence

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def arguments(self) -> typing.Optional[Arguments]:
        result = self._values.get("arguments")
        return typing.cast(typing.Optional[Arguments], result)

    @builtins.property
    def continue_on(self) -> typing.Optional[ContinueOn]:
        result = self._values.get("continue_on")
        return typing.cast(typing.Optional[ContinueOn], result)

    @builtins.property
    def dependencies(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("dependencies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def depends(self) -> typing.Optional[builtins.str]:
        result = self._values.get("depends")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def on_exit(self) -> typing.Optional[builtins.str]:
        result = self._values.get("on_exit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template(self) -> typing.Optional[builtins.str]:
        result = self._values.get("template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template_ref(self) -> typing.Optional["TemplateRef"]:
        result = self._values.get("template_ref")
        return typing.cast(typing.Optional["TemplateRef"], result)

    @builtins.property
    def when(self) -> typing.Optional[builtins.str]:
        result = self._values.get("when")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def with_items(self) -> typing.Optional[typing.List[typing.Any]]:
        result = self._values.get("with_items")
        return typing.cast(typing.Optional[typing.List[typing.Any]], result)

    @builtins.property
    def with_param(self) -> typing.Optional[builtins.str]:
        result = self._values.get("with_param")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def with_sequence(self) -> typing.Optional["Sequence"]:
        result = self._values.get("with_sequence")
        return typing.cast(typing.Optional["Sequence"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DAGTask(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.DAGTemplate",
    jsii_struct_bases=[],
    name_mapping={"tasks": "tasks", "fail_fast": "failFast", "target": "target"},
)
class DAGTemplate:
    def __init__(
        self,
        *,
        tasks: typing.Sequence[DAGTask],
        fail_fast: typing.Optional[builtins.bool] = None,
        target: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param tasks: 
        :param fail_fast: 
        :param target: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "tasks": tasks,
        }
        if fail_fast is not None:
            self._values["fail_fast"] = fail_fast
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def tasks(self) -> typing.List[DAGTask]:
        result = self._values.get("tasks")
        assert result is not None, "Required property 'tasks' is missing"
        return typing.cast(typing.List[DAGTask], result)

    @builtins.property
    def fail_fast(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("fail_fast")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DAGTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.Data",
    jsii_struct_bases=[],
    name_mapping={"source": "source", "transformation": "transformation"},
)
class Data:
    def __init__(
        self,
        *,
        source: "DataSource",
        transformation: typing.Sequence["TransformationStep"],
    ) -> None:
        '''
        :param source: 
        :param transformation: 
        '''
        if isinstance(source, dict):
            source = DataSource(**source)
        self._values: typing.Dict[str, typing.Any] = {
            "source": source,
            "transformation": transformation,
        }

    @builtins.property
    def source(self) -> "DataSource":
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast("DataSource", result)

    @builtins.property
    def transformation(self) -> typing.List["TransformationStep"]:
        result = self._values.get("transformation")
        assert result is not None, "Required property 'transformation' is missing"
        return typing.cast(typing.List["TransformationStep"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Data(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.DataSource",
    jsii_struct_bases=[],
    name_mapping={"artifact_paths": "artifactPaths"},
)
class DataSource:
    def __init__(
        self,
        *,
        artifact_paths: typing.Optional[ArtifactPaths] = None,
    ) -> None:
        '''
        :param artifact_paths: 
        '''
        if isinstance(artifact_paths, dict):
            artifact_paths = ArtifactPaths(**artifact_paths)
        self._values: typing.Dict[str, typing.Any] = {}
        if artifact_paths is not None:
            self._values["artifact_paths"] = artifact_paths

    @builtins.property
    def artifact_paths(self) -> typing.Optional[ArtifactPaths]:
        result = self._values.get("artifact_paths")
        return typing.cast(typing.Optional[ArtifactPaths], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.Event",
    jsii_struct_bases=[],
    name_mapping={"selector": "selector"},
)
class Event:
    def __init__(self, *, selector: builtins.str) -> None:
        '''
        :param selector: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "selector": selector,
        }

    @builtins.property
    def selector(self) -> builtins.str:
        result = self._values.get("selector")
        assert result is not None, "Required property 'selector' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Event(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.EventResponse",
    jsii_struct_bases=[],
    name_mapping={},
)
class EventResponse:
    def __init__(self) -> None:
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.ExecutorConfig",
    jsii_struct_bases=[],
    name_mapping={"service_account_name": "serviceAccountName"},
)
class ExecutorConfig:
    def __init__(
        self,
        *,
        service_account_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service_account_name: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if service_account_name is not None:
            self._values["service_account_name"] = service_account_name

    @builtins.property
    def service_account_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("service_account_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExecutorConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.GCSArtifact",
    jsii_struct_bases=[],
    name_mapping={
        "key": "key",
        "bucket": "bucket",
        "service_account_key_secret": "serviceAccountKeySecret",
    },
)
class GCSArtifact:
    def __init__(
        self,
        *,
        key: builtins.str,
        bucket: typing.Optional[builtins.str] = None,
        service_account_key_secret: typing.Optional[_SecretKeySelector_3834a17e] = None,
    ) -> None:
        '''
        :param key: 
        :param bucket: 
        :param service_account_key_secret: 
        '''
        if isinstance(service_account_key_secret, dict):
            service_account_key_secret = _SecretKeySelector_3834a17e(**service_account_key_secret)
        self._values: typing.Dict[str, typing.Any] = {
            "key": key,
        }
        if bucket is not None:
            self._values["bucket"] = bucket
        if service_account_key_secret is not None:
            self._values["service_account_key_secret"] = service_account_key_secret

    @builtins.property
    def key(self) -> builtins.str:
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bucket(self) -> typing.Optional[builtins.str]:
        result = self._values.get("bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account_key_secret(
        self,
    ) -> typing.Optional[_SecretKeySelector_3834a17e]:
        result = self._values.get("service_account_key_secret")
        return typing.cast(typing.Optional[_SecretKeySelector_3834a17e], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GCSArtifact(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.Gauge",
    jsii_struct_bases=[],
    name_mapping={"realtime": "realtime", "value": "value"},
)
class Gauge:
    def __init__(self, *, realtime: builtins.bool, value: builtins.str) -> None:
        '''
        :param realtime: 
        :param value: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "realtime": realtime,
            "value": value,
        }

    @builtins.property
    def realtime(self) -> builtins.bool:
        result = self._values.get("realtime")
        assert result is not None, "Required property 'realtime' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def value(self) -> builtins.str:
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Gauge(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.GetUserInfoResponse",
    jsii_struct_bases=[],
    name_mapping={
        "email": "email",
        "email_verified": "emailVerified",
        "groups": "groups",
        "issuer": "issuer",
        "service_account_name": "serviceAccountName",
        "subject": "subject",
    },
)
class GetUserInfoResponse:
    def __init__(
        self,
        *,
        email: typing.Optional[builtins.str] = None,
        email_verified: typing.Optional[builtins.bool] = None,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        issuer: typing.Optional[builtins.str] = None,
        service_account_name: typing.Optional[builtins.str] = None,
        subject: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param email: 
        :param email_verified: 
        :param groups: 
        :param issuer: 
        :param service_account_name: 
        :param subject: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if email is not None:
            self._values["email"] = email
        if email_verified is not None:
            self._values["email_verified"] = email_verified
        if groups is not None:
            self._values["groups"] = groups
        if issuer is not None:
            self._values["issuer"] = issuer
        if service_account_name is not None:
            self._values["service_account_name"] = service_account_name
        if subject is not None:
            self._values["subject"] = subject

    @builtins.property
    def email(self) -> typing.Optional[builtins.str]:
        result = self._values.get("email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email_verified(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("email_verified")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def groups(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def issuer(self) -> typing.Optional[builtins.str]:
        result = self._values.get("issuer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("service_account_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject(self) -> typing.Optional[builtins.str]:
        result = self._values.get("subject")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GetUserInfoResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.GitArtifact",
    jsii_struct_bases=[],
    name_mapping={
        "repo": "repo",
        "depth": "depth",
        "fetch": "fetch",
        "insecure_ignore_host_key": "insecureIgnoreHostKey",
        "password_secret": "passwordSecret",
        "revision": "revision",
        "ssh_private_key_secret": "sshPrivateKeySecret",
        "username_secret": "usernameSecret",
    },
)
class GitArtifact:
    def __init__(
        self,
        *,
        repo: builtins.str,
        depth: typing.Optional[jsii.Number] = None,
        fetch: typing.Optional[typing.Sequence[builtins.str]] = None,
        insecure_ignore_host_key: typing.Optional[builtins.bool] = None,
        password_secret: typing.Optional[_SecretKeySelector_3834a17e] = None,
        revision: typing.Optional[builtins.str] = None,
        ssh_private_key_secret: typing.Optional[_SecretKeySelector_3834a17e] = None,
        username_secret: typing.Optional[_SecretKeySelector_3834a17e] = None,
    ) -> None:
        '''
        :param repo: 
        :param depth: 
        :param fetch: 
        :param insecure_ignore_host_key: 
        :param password_secret: 
        :param revision: 
        :param ssh_private_key_secret: 
        :param username_secret: 
        '''
        if isinstance(password_secret, dict):
            password_secret = _SecretKeySelector_3834a17e(**password_secret)
        if isinstance(ssh_private_key_secret, dict):
            ssh_private_key_secret = _SecretKeySelector_3834a17e(**ssh_private_key_secret)
        if isinstance(username_secret, dict):
            username_secret = _SecretKeySelector_3834a17e(**username_secret)
        self._values: typing.Dict[str, typing.Any] = {
            "repo": repo,
        }
        if depth is not None:
            self._values["depth"] = depth
        if fetch is not None:
            self._values["fetch"] = fetch
        if insecure_ignore_host_key is not None:
            self._values["insecure_ignore_host_key"] = insecure_ignore_host_key
        if password_secret is not None:
            self._values["password_secret"] = password_secret
        if revision is not None:
            self._values["revision"] = revision
        if ssh_private_key_secret is not None:
            self._values["ssh_private_key_secret"] = ssh_private_key_secret
        if username_secret is not None:
            self._values["username_secret"] = username_secret

    @builtins.property
    def repo(self) -> builtins.str:
        result = self._values.get("repo")
        assert result is not None, "Required property 'repo' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def depth(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("depth")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def fetch(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("fetch")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def insecure_ignore_host_key(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("insecure_ignore_host_key")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def password_secret(self) -> typing.Optional[_SecretKeySelector_3834a17e]:
        result = self._values.get("password_secret")
        return typing.cast(typing.Optional[_SecretKeySelector_3834a17e], result)

    @builtins.property
    def revision(self) -> typing.Optional[builtins.str]:
        result = self._values.get("revision")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssh_private_key_secret(self) -> typing.Optional[_SecretKeySelector_3834a17e]:
        result = self._values.get("ssh_private_key_secret")
        return typing.cast(typing.Optional[_SecretKeySelector_3834a17e], result)

    @builtins.property
    def username_secret(self) -> typing.Optional[_SecretKeySelector_3834a17e]:
        result = self._values.get("username_secret")
        return typing.cast(typing.Optional[_SecretKeySelector_3834a17e], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitArtifact(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.GoogleProtobufAny",
    jsii_struct_bases=[],
    name_mapping={"type_url": "typeUrl", "value": "value"},
)
class GoogleProtobufAny:
    def __init__(
        self,
        *,
        type_url: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type_url: 
        :param value: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if type_url is not None:
            self._values["type_url"] = type_url
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def type_url(self) -> typing.Optional[builtins.str]:
        result = self._values.get("type_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GoogleProtobufAny(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.GrpcGatewayRuntimeError",
    jsii_struct_bases=[],
    name_mapping={
        "code": "code",
        "details": "details",
        "error": "error",
        "message": "message",
    },
)
class GrpcGatewayRuntimeError:
    def __init__(
        self,
        *,
        code: typing.Optional[jsii.Number] = None,
        details: typing.Optional[typing.Sequence[GoogleProtobufAny]] = None,
        error: typing.Optional[builtins.str] = None,
        message: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param code: 
        :param details: 
        :param error: 
        :param message: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if code is not None:
            self._values["code"] = code
        if details is not None:
            self._values["details"] = details
        if error is not None:
            self._values["error"] = error
        if message is not None:
            self._values["message"] = message

    @builtins.property
    def code(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("code")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def details(self) -> typing.Optional[typing.List[GoogleProtobufAny]]:
        result = self._values.get("details")
        return typing.cast(typing.Optional[typing.List[GoogleProtobufAny]], result)

    @builtins.property
    def error(self) -> typing.Optional[builtins.str]:
        result = self._values.get("error")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def message(self) -> typing.Optional[builtins.str]:
        result = self._values.get("message")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GrpcGatewayRuntimeError(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.GrpcGatewayRuntimeStreamError",
    jsii_struct_bases=[],
    name_mapping={
        "details": "details",
        "grpc_code": "grpcCode",
        "http_code": "httpCode",
        "http_status": "httpStatus",
        "message": "message",
    },
)
class GrpcGatewayRuntimeStreamError:
    def __init__(
        self,
        *,
        details: typing.Optional[typing.Sequence[GoogleProtobufAny]] = None,
        grpc_code: typing.Optional[jsii.Number] = None,
        http_code: typing.Optional[jsii.Number] = None,
        http_status: typing.Optional[builtins.str] = None,
        message: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param details: 
        :param grpc_code: 
        :param http_code: 
        :param http_status: 
        :param message: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if details is not None:
            self._values["details"] = details
        if grpc_code is not None:
            self._values["grpc_code"] = grpc_code
        if http_code is not None:
            self._values["http_code"] = http_code
        if http_status is not None:
            self._values["http_status"] = http_status
        if message is not None:
            self._values["message"] = message

    @builtins.property
    def details(self) -> typing.Optional[typing.List[GoogleProtobufAny]]:
        result = self._values.get("details")
        return typing.cast(typing.Optional[typing.List[GoogleProtobufAny]], result)

    @builtins.property
    def grpc_code(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("grpc_code")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def http_code(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("http_code")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def http_status(self) -> typing.Optional[builtins.str]:
        result = self._values.get("http_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def message(self) -> typing.Optional[builtins.str]:
        result = self._values.get("message")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GrpcGatewayRuntimeStreamError(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.HDFSArtifact",
    jsii_struct_bases=[],
    name_mapping={
        "path": "path",
        "addresses": "addresses",
        "force": "force",
        "hdfs_user": "hdfsUser",
        "krb_c_cache_secret": "krbCCacheSecret",
        "krb_config_config_map": "krbConfigConfigMap",
        "krb_keytab_secret": "krbKeytabSecret",
        "krb_realm": "krbRealm",
        "krb_service_principal_name": "krbServicePrincipalName",
        "krb_username": "krbUsername",
    },
)
class HDFSArtifact:
    def __init__(
        self,
        *,
        path: builtins.str,
        addresses: typing.Optional[typing.Sequence[builtins.str]] = None,
        force: typing.Optional[builtins.bool] = None,
        hdfs_user: typing.Optional[builtins.str] = None,
        krb_c_cache_secret: typing.Optional[_SecretKeySelector_3834a17e] = None,
        krb_config_config_map: typing.Optional[_ConfigMapKeySelector_655813de] = None,
        krb_keytab_secret: typing.Optional[_SecretKeySelector_3834a17e] = None,
        krb_realm: typing.Optional[builtins.str] = None,
        krb_service_principal_name: typing.Optional[builtins.str] = None,
        krb_username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param path: 
        :param addresses: 
        :param force: 
        :param hdfs_user: 
        :param krb_c_cache_secret: 
        :param krb_config_config_map: 
        :param krb_keytab_secret: 
        :param krb_realm: 
        :param krb_service_principal_name: 
        :param krb_username: 
        '''
        if isinstance(krb_c_cache_secret, dict):
            krb_c_cache_secret = _SecretKeySelector_3834a17e(**krb_c_cache_secret)
        if isinstance(krb_config_config_map, dict):
            krb_config_config_map = _ConfigMapKeySelector_655813de(**krb_config_config_map)
        if isinstance(krb_keytab_secret, dict):
            krb_keytab_secret = _SecretKeySelector_3834a17e(**krb_keytab_secret)
        self._values: typing.Dict[str, typing.Any] = {
            "path": path,
        }
        if addresses is not None:
            self._values["addresses"] = addresses
        if force is not None:
            self._values["force"] = force
        if hdfs_user is not None:
            self._values["hdfs_user"] = hdfs_user
        if krb_c_cache_secret is not None:
            self._values["krb_c_cache_secret"] = krb_c_cache_secret
        if krb_config_config_map is not None:
            self._values["krb_config_config_map"] = krb_config_config_map
        if krb_keytab_secret is not None:
            self._values["krb_keytab_secret"] = krb_keytab_secret
        if krb_realm is not None:
            self._values["krb_realm"] = krb_realm
        if krb_service_principal_name is not None:
            self._values["krb_service_principal_name"] = krb_service_principal_name
        if krb_username is not None:
            self._values["krb_username"] = krb_username

    @builtins.property
    def path(self) -> builtins.str:
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def addresses(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("addresses")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def force(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("force")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def hdfs_user(self) -> typing.Optional[builtins.str]:
        result = self._values.get("hdfs_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def krb_c_cache_secret(self) -> typing.Optional[_SecretKeySelector_3834a17e]:
        result = self._values.get("krb_c_cache_secret")
        return typing.cast(typing.Optional[_SecretKeySelector_3834a17e], result)

    @builtins.property
    def krb_config_config_map(self) -> typing.Optional[_ConfigMapKeySelector_655813de]:
        result = self._values.get("krb_config_config_map")
        return typing.cast(typing.Optional[_ConfigMapKeySelector_655813de], result)

    @builtins.property
    def krb_keytab_secret(self) -> typing.Optional[_SecretKeySelector_3834a17e]:
        result = self._values.get("krb_keytab_secret")
        return typing.cast(typing.Optional[_SecretKeySelector_3834a17e], result)

    @builtins.property
    def krb_realm(self) -> typing.Optional[builtins.str]:
        result = self._values.get("krb_realm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def krb_service_principal_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("krb_service_principal_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def krb_username(self) -> typing.Optional[builtins.str]:
        result = self._values.get("krb_username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HDFSArtifact(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.HTTPArtifact",
    jsii_struct_bases=[],
    name_mapping={"url": "url", "headers": "headers"},
)
class HTTPArtifact:
    def __init__(
        self,
        *,
        url: builtins.str,
        headers: typing.Optional[typing.Sequence["Header"]] = None,
    ) -> None:
        '''
        :param url: 
        :param headers: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "url": url,
        }
        if headers is not None:
            self._values["headers"] = headers

    @builtins.property
    def url(self) -> builtins.str:
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def headers(self) -> typing.Optional[typing.List["Header"]]:
        result = self._values.get("headers")
        return typing.cast(typing.Optional[typing.List["Header"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HTTPArtifact(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.Header",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class Header:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: 
        :param value: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Header(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.Histogram",
    jsii_struct_bases=[],
    name_mapping={"buckets": "buckets", "value": "value"},
)
class Histogram:
    def __init__(
        self,
        *,
        buckets: typing.Sequence[jsii.Number],
        value: builtins.str,
    ) -> None:
        '''
        :param buckets: 
        :param value: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "buckets": buckets,
            "value": value,
        }

    @builtins.property
    def buckets(self) -> typing.List[jsii.Number]:
        result = self._values.get("buckets")
        assert result is not None, "Required property 'buckets' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    @builtins.property
    def value(self) -> builtins.str:
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Histogram(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.InfoResponse",
    jsii_struct_bases=[],
    name_mapping={"links": "links", "managed_namespace": "managedNamespace"},
)
class InfoResponse:
    def __init__(
        self,
        *,
        links: typing.Optional[typing.Sequence["Link"]] = None,
        managed_namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param links: 
        :param managed_namespace: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if links is not None:
            self._values["links"] = links
        if managed_namespace is not None:
            self._values["managed_namespace"] = managed_namespace

    @builtins.property
    def links(self) -> typing.Optional[typing.List["Link"]]:
        result = self._values.get("links")
        return typing.cast(typing.Optional[typing.List["Link"]], result)

    @builtins.property
    def managed_namespace(self) -> typing.Optional[builtins.str]:
        result = self._values.get("managed_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InfoResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.Inputs",
    jsii_struct_bases=[],
    name_mapping={"artifacts": "artifacts", "parameters": "parameters"},
)
class Inputs:
    def __init__(
        self,
        *,
        artifacts: typing.Optional[typing.Sequence[Artifact]] = None,
        parameters: typing.Optional[typing.Sequence["Parameter"]] = None,
    ) -> None:
        '''
        :param artifacts: 
        :param parameters: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if artifacts is not None:
            self._values["artifacts"] = artifacts
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def artifacts(self) -> typing.Optional[typing.List[Artifact]]:
        result = self._values.get("artifacts")
        return typing.cast(typing.Optional[typing.List[Artifact]], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.List["Parameter"]]:
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.List["Parameter"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Inputs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.Link",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "scope": "scope", "url": "url"},
)
class Link:
    def __init__(
        self,
        *,
        name: builtins.str,
        scope: builtins.str,
        url: builtins.str,
    ) -> None:
        '''
        :param name: 
        :param scope: 
        :param url: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "scope": scope,
            "url": url,
        }

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scope(self) -> builtins.str:
        result = self._values.get("scope")
        assert result is not None, "Required property 'scope' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Link(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.LintCronWorkflowRequest",
    jsii_struct_bases=[],
    name_mapping={"cron_workflow": "cronWorkflow", "namespace": "namespace"},
)
class LintCronWorkflowRequest:
    def __init__(
        self,
        *,
        cron_workflow: typing.Optional[CronWorkflow] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cron_workflow: 
        :param namespace: 
        '''
        if isinstance(cron_workflow, dict):
            cron_workflow = CronWorkflow(**cron_workflow)
        self._values: typing.Dict[str, typing.Any] = {}
        if cron_workflow is not None:
            self._values["cron_workflow"] = cron_workflow
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def cron_workflow(self) -> typing.Optional[CronWorkflow]:
        result = self._values.get("cron_workflow")
        return typing.cast(typing.Optional[CronWorkflow], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LintCronWorkflowRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.LogEntry",
    jsii_struct_bases=[],
    name_mapping={"content": "content", "pod_name": "podName"},
)
class LogEntry:
    def __init__(
        self,
        *,
        content: typing.Optional[builtins.str] = None,
        pod_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param content: 
        :param pod_name: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if content is not None:
            self._values["content"] = content
        if pod_name is not None:
            self._values["pod_name"] = pod_name

    @builtins.property
    def content(self) -> typing.Optional[builtins.str]:
        result = self._values.get("content")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pod_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("pod_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogEntry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.MemoizationStatus",
    jsii_struct_bases=[],
    name_mapping={"cache_name": "cacheName", "hit": "hit", "key": "key"},
)
class MemoizationStatus:
    def __init__(
        self,
        *,
        cache_name: builtins.str,
        hit: builtins.bool,
        key: builtins.str,
    ) -> None:
        '''
        :param cache_name: 
        :param hit: 
        :param key: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "cache_name": cache_name,
            "hit": hit,
            "key": key,
        }

    @builtins.property
    def cache_name(self) -> builtins.str:
        result = self._values.get("cache_name")
        assert result is not None, "Required property 'cache_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hit(self) -> builtins.bool:
        result = self._values.get("hit")
        assert result is not None, "Required property 'hit' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def key(self) -> builtins.str:
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MemoizationStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.Memoize",
    jsii_struct_bases=[],
    name_mapping={"cache": "cache", "key": "key", "max_age": "maxAge"},
)
class Memoize:
    def __init__(
        self,
        *,
        cache: Cache,
        key: builtins.str,
        max_age: builtins.str,
    ) -> None:
        '''
        :param cache: 
        :param key: 
        :param max_age: 
        '''
        if isinstance(cache, dict):
            cache = Cache(**cache)
        self._values: typing.Dict[str, typing.Any] = {
            "cache": cache,
            "key": key,
            "max_age": max_age,
        }

    @builtins.property
    def cache(self) -> Cache:
        result = self._values.get("cache")
        assert result is not None, "Required property 'cache' is missing"
        return typing.cast(Cache, result)

    @builtins.property
    def key(self) -> builtins.str:
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def max_age(self) -> builtins.str:
        result = self._values.get("max_age")
        assert result is not None, "Required property 'max_age' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Memoize(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.Metadata",
    jsii_struct_bases=[],
    name_mapping={"annotations": "annotations", "labels": "labels"},
)
class Metadata:
    def __init__(
        self,
        *,
        annotations: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param annotations: 
        :param labels: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if annotations is not None:
            self._values["annotations"] = annotations
        if labels is not None:
            self._values["labels"] = labels

    @builtins.property
    def annotations(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Metadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.MetricLabel",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class MetricLabel:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: 
        :param value: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetricLabel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.Metrics",
    jsii_struct_bases=[],
    name_mapping={"prometheus": "prometheus"},
)
class Metrics:
    def __init__(self, *, prometheus: typing.Sequence["Prometheus"]) -> None:
        '''
        :param prometheus: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "prometheus": prometheus,
        }

    @builtins.property
    def prometheus(self) -> typing.List["Prometheus"]:
        result = self._values.get("prometheus")
        assert result is not None, "Required property 'prometheus' is missing"
        return typing.cast(typing.List["Prometheus"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Metrics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.Mutex",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class Mutex:
    def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param name: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Mutex(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.MutexHolding",
    jsii_struct_bases=[],
    name_mapping={"holder": "holder", "mutex": "mutex"},
)
class MutexHolding:
    def __init__(
        self,
        *,
        holder: typing.Optional[builtins.str] = None,
        mutex: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param holder: 
        :param mutex: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if holder is not None:
            self._values["holder"] = holder
        if mutex is not None:
            self._values["mutex"] = mutex

    @builtins.property
    def holder(self) -> typing.Optional[builtins.str]:
        result = self._values.get("holder")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mutex(self) -> typing.Optional[builtins.str]:
        result = self._values.get("mutex")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MutexHolding(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.MutexStatus",
    jsii_struct_bases=[],
    name_mapping={"holding": "holding", "waiting": "waiting"},
)
class MutexStatus:
    def __init__(
        self,
        *,
        holding: typing.Optional[typing.Sequence[MutexHolding]] = None,
        waiting: typing.Optional[typing.Sequence[MutexHolding]] = None,
    ) -> None:
        '''
        :param holding: 
        :param waiting: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if holding is not None:
            self._values["holding"] = holding
        if waiting is not None:
            self._values["waiting"] = waiting

    @builtins.property
    def holding(self) -> typing.Optional[typing.List[MutexHolding]]:
        result = self._values.get("holding")
        return typing.cast(typing.Optional[typing.List[MutexHolding]], result)

    @builtins.property
    def waiting(self) -> typing.Optional[typing.List[MutexHolding]]:
        result = self._values.get("waiting")
        return typing.cast(typing.Optional[typing.List[MutexHolding]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MutexStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.NodeStatus",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "name": "name",
        "type": "type",
        "boundary_id": "boundaryID",
        "children": "children",
        "daemoned": "daemoned",
        "display_name": "displayName",
        "estimated_duration": "estimatedDuration",
        "finished_at": "finishedAt",
        "host_node_name": "hostNodeName",
        "inputs": "inputs",
        "memoization_status": "memoizationStatus",
        "message": "message",
        "outbound_nodes": "outboundNodes",
        "outputs": "outputs",
        "phase": "phase",
        "pod_ip": "podIP",
        "progress": "progress",
        "resources_duration": "resourcesDuration",
        "started_at": "startedAt",
        "synchronization_status": "synchronizationStatus",
        "template_name": "templateName",
        "template_ref": "templateRef",
        "template_scope": "templateScope",
    },
)
class NodeStatus:
    def __init__(
        self,
        *,
        id: builtins.str,
        name: builtins.str,
        type: builtins.str,
        boundary_id: typing.Optional[builtins.str] = None,
        children: typing.Optional[typing.Sequence[builtins.str]] = None,
        daemoned: typing.Optional[builtins.bool] = None,
        display_name: typing.Optional[builtins.str] = None,
        estimated_duration: typing.Optional[jsii.Number] = None,
        finished_at: typing.Optional[datetime.datetime] = None,
        host_node_name: typing.Optional[builtins.str] = None,
        inputs: typing.Optional[Inputs] = None,
        memoization_status: typing.Optional[MemoizationStatus] = None,
        message: typing.Optional[builtins.str] = None,
        outbound_nodes: typing.Optional[typing.Sequence[builtins.str]] = None,
        outputs: typing.Optional["Outputs"] = None,
        phase: typing.Optional[builtins.str] = None,
        pod_ip: typing.Optional[builtins.str] = None,
        progress: typing.Optional[builtins.str] = None,
        resources_duration: typing.Optional[typing.Mapping[builtins.str, jsii.Number]] = None,
        started_at: typing.Optional[datetime.datetime] = None,
        synchronization_status: typing.Optional["NodeSynchronizationStatus"] = None,
        template_name: typing.Optional[builtins.str] = None,
        template_ref: typing.Optional["TemplateRef"] = None,
        template_scope: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: 
        :param name: 
        :param type: 
        :param boundary_id: 
        :param children: 
        :param daemoned: 
        :param display_name: 
        :param estimated_duration: 
        :param finished_at: 
        :param host_node_name: 
        :param inputs: 
        :param memoization_status: 
        :param message: 
        :param outbound_nodes: 
        :param outputs: 
        :param phase: 
        :param pod_ip: 
        :param progress: 
        :param resources_duration: 
        :param started_at: 
        :param synchronization_status: 
        :param template_name: 
        :param template_ref: 
        :param template_scope: 
        '''
        if isinstance(inputs, dict):
            inputs = Inputs(**inputs)
        if isinstance(memoization_status, dict):
            memoization_status = MemoizationStatus(**memoization_status)
        if isinstance(outputs, dict):
            outputs = Outputs(**outputs)
        if isinstance(synchronization_status, dict):
            synchronization_status = NodeSynchronizationStatus(**synchronization_status)
        if isinstance(template_ref, dict):
            template_ref = TemplateRef(**template_ref)
        self._values: typing.Dict[str, typing.Any] = {
            "id": id,
            "name": name,
            "type": type,
        }
        if boundary_id is not None:
            self._values["boundary_id"] = boundary_id
        if children is not None:
            self._values["children"] = children
        if daemoned is not None:
            self._values["daemoned"] = daemoned
        if display_name is not None:
            self._values["display_name"] = display_name
        if estimated_duration is not None:
            self._values["estimated_duration"] = estimated_duration
        if finished_at is not None:
            self._values["finished_at"] = finished_at
        if host_node_name is not None:
            self._values["host_node_name"] = host_node_name
        if inputs is not None:
            self._values["inputs"] = inputs
        if memoization_status is not None:
            self._values["memoization_status"] = memoization_status
        if message is not None:
            self._values["message"] = message
        if outbound_nodes is not None:
            self._values["outbound_nodes"] = outbound_nodes
        if outputs is not None:
            self._values["outputs"] = outputs
        if phase is not None:
            self._values["phase"] = phase
        if pod_ip is not None:
            self._values["pod_ip"] = pod_ip
        if progress is not None:
            self._values["progress"] = progress
        if resources_duration is not None:
            self._values["resources_duration"] = resources_duration
        if started_at is not None:
            self._values["started_at"] = started_at
        if synchronization_status is not None:
            self._values["synchronization_status"] = synchronization_status
        if template_name is not None:
            self._values["template_name"] = template_name
        if template_ref is not None:
            self._values["template_ref"] = template_ref
        if template_scope is not None:
            self._values["template_scope"] = template_scope

    @builtins.property
    def id(self) -> builtins.str:
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def boundary_id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("boundary_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def children(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("children")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def daemoned(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("daemoned")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def estimated_duration(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("estimated_duration")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def finished_at(self) -> typing.Optional[datetime.datetime]:
        result = self._values.get("finished_at")
        return typing.cast(typing.Optional[datetime.datetime], result)

    @builtins.property
    def host_node_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("host_node_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inputs(self) -> typing.Optional[Inputs]:
        result = self._values.get("inputs")
        return typing.cast(typing.Optional[Inputs], result)

    @builtins.property
    def memoization_status(self) -> typing.Optional[MemoizationStatus]:
        result = self._values.get("memoization_status")
        return typing.cast(typing.Optional[MemoizationStatus], result)

    @builtins.property
    def message(self) -> typing.Optional[builtins.str]:
        result = self._values.get("message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def outbound_nodes(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("outbound_nodes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def outputs(self) -> typing.Optional["Outputs"]:
        result = self._values.get("outputs")
        return typing.cast(typing.Optional["Outputs"], result)

    @builtins.property
    def phase(self) -> typing.Optional[builtins.str]:
        result = self._values.get("phase")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pod_ip(self) -> typing.Optional[builtins.str]:
        result = self._values.get("pod_ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def progress(self) -> typing.Optional[builtins.str]:
        result = self._values.get("progress")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resources_duration(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, jsii.Number]]:
        result = self._values.get("resources_duration")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, jsii.Number]], result)

    @builtins.property
    def started_at(self) -> typing.Optional[datetime.datetime]:
        result = self._values.get("started_at")
        return typing.cast(typing.Optional[datetime.datetime], result)

    @builtins.property
    def synchronization_status(self) -> typing.Optional["NodeSynchronizationStatus"]:
        result = self._values.get("synchronization_status")
        return typing.cast(typing.Optional["NodeSynchronizationStatus"], result)

    @builtins.property
    def template_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("template_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template_ref(self) -> typing.Optional["TemplateRef"]:
        result = self._values.get("template_ref")
        return typing.cast(typing.Optional["TemplateRef"], result)

    @builtins.property
    def template_scope(self) -> typing.Optional[builtins.str]:
        result = self._values.get("template_scope")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NodeStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.NodeSynchronizationStatus",
    jsii_struct_bases=[],
    name_mapping={"waiting": "waiting"},
)
class NodeSynchronizationStatus:
    def __init__(self, *, waiting: typing.Optional[builtins.str] = None) -> None:
        '''
        :param waiting: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if waiting is not None:
            self._values["waiting"] = waiting

    @builtins.property
    def waiting(self) -> typing.Optional[builtins.str]:
        result = self._values.get("waiting")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NodeSynchronizationStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.NoneStrategy",
    jsii_struct_bases=[],
    name_mapping={},
)
class NoneStrategy:
    def __init__(self) -> None:
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NoneStrategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.OSSArtifact",
    jsii_struct_bases=[],
    name_mapping={
        "key": "key",
        "access_key_secret": "accessKeySecret",
        "bucket": "bucket",
        "create_bucket_if_not_present": "createBucketIfNotPresent",
        "endpoint": "endpoint",
        "secret_key_secret": "secretKeySecret",
        "security_token": "securityToken",
    },
)
class OSSArtifact:
    def __init__(
        self,
        *,
        key: builtins.str,
        access_key_secret: typing.Optional[_SecretKeySelector_3834a17e] = None,
        bucket: typing.Optional[builtins.str] = None,
        create_bucket_if_not_present: typing.Optional[builtins.bool] = None,
        endpoint: typing.Optional[builtins.str] = None,
        secret_key_secret: typing.Optional[_SecretKeySelector_3834a17e] = None,
        security_token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: 
        :param access_key_secret: 
        :param bucket: 
        :param create_bucket_if_not_present: 
        :param endpoint: 
        :param secret_key_secret: 
        :param security_token: 
        '''
        if isinstance(access_key_secret, dict):
            access_key_secret = _SecretKeySelector_3834a17e(**access_key_secret)
        if isinstance(secret_key_secret, dict):
            secret_key_secret = _SecretKeySelector_3834a17e(**secret_key_secret)
        self._values: typing.Dict[str, typing.Any] = {
            "key": key,
        }
        if access_key_secret is not None:
            self._values["access_key_secret"] = access_key_secret
        if bucket is not None:
            self._values["bucket"] = bucket
        if create_bucket_if_not_present is not None:
            self._values["create_bucket_if_not_present"] = create_bucket_if_not_present
        if endpoint is not None:
            self._values["endpoint"] = endpoint
        if secret_key_secret is not None:
            self._values["secret_key_secret"] = secret_key_secret
        if security_token is not None:
            self._values["security_token"] = security_token

    @builtins.property
    def key(self) -> builtins.str:
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_key_secret(self) -> typing.Optional[_SecretKeySelector_3834a17e]:
        result = self._values.get("access_key_secret")
        return typing.cast(typing.Optional[_SecretKeySelector_3834a17e], result)

    @builtins.property
    def bucket(self) -> typing.Optional[builtins.str]:
        result = self._values.get("bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def create_bucket_if_not_present(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("create_bucket_if_not_present")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def endpoint(self) -> typing.Optional[builtins.str]:
        result = self._values.get("endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_key_secret(self) -> typing.Optional[_SecretKeySelector_3834a17e]:
        result = self._values.get("secret_key_secret")
        return typing.cast(typing.Optional[_SecretKeySelector_3834a17e], result)

    @builtins.property
    def security_token(self) -> typing.Optional[builtins.str]:
        result = self._values.get("security_token")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OSSArtifact(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.Outputs",
    jsii_struct_bases=[],
    name_mapping={
        "artifacts": "artifacts",
        "exit_code": "exitCode",
        "parameters": "parameters",
        "result": "result",
    },
)
class Outputs:
    def __init__(
        self,
        *,
        artifacts: typing.Optional[typing.Sequence[Artifact]] = None,
        exit_code: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Sequence["Parameter"]] = None,
        result: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param artifacts: 
        :param exit_code: 
        :param parameters: 
        :param result: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if artifacts is not None:
            self._values["artifacts"] = artifacts
        if exit_code is not None:
            self._values["exit_code"] = exit_code
        if parameters is not None:
            self._values["parameters"] = parameters
        if result is not None:
            self._values["result"] = result

    @builtins.property
    def artifacts(self) -> typing.Optional[typing.List[Artifact]]:
        result = self._values.get("artifacts")
        return typing.cast(typing.Optional[typing.List[Artifact]], result)

    @builtins.property
    def exit_code(self) -> typing.Optional[builtins.str]:
        result = self._values.get("exit_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.List["Parameter"]]:
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.List["Parameter"]], result)

    @builtins.property
    def result(self) -> typing.Optional[builtins.str]:
        result = self._values.get("result")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Outputs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.Parameter",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "default": "default",
        "enum": "enum",
        "global_name": "globalName",
        "value": "value",
        "value_from": "valueFrom",
    },
)
class Parameter:
    def __init__(
        self,
        *,
        name: builtins.str,
        default: typing.Optional[builtins.str] = None,
        enum: typing.Optional[typing.Sequence[builtins.str]] = None,
        global_name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
        value_from: typing.Optional["ValueFrom"] = None,
    ) -> None:
        '''
        :param name: 
        :param default: 
        :param enum: 
        :param global_name: 
        :param value: 
        :param value_from: 
        '''
        if isinstance(value_from, dict):
            value_from = ValueFrom(**value_from)
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }
        if default is not None:
            self._values["default"] = default
        if enum is not None:
            self._values["enum"] = enum
        if global_name is not None:
            self._values["global_name"] = global_name
        if value is not None:
            self._values["value"] = value
        if value_from is not None:
            self._values["value_from"] = value_from

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default(self) -> typing.Optional[builtins.str]:
        result = self._values.get("default")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enum(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("enum")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def global_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("global_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value_from(self) -> typing.Optional["ValueFrom"]:
        result = self._values.get("value_from")
        return typing.cast(typing.Optional["ValueFrom"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Parameter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.PodGC",
    jsii_struct_bases=[],
    name_mapping={"label_selector": "labelSelector", "strategy": "strategy"},
)
class PodGC:
    def __init__(
        self,
        *,
        label_selector: typing.Optional[_LabelSelector_2d5da14b] = None,
        strategy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param label_selector: 
        :param strategy: 
        '''
        if isinstance(label_selector, dict):
            label_selector = _LabelSelector_2d5da14b(**label_selector)
        self._values: typing.Dict[str, typing.Any] = {}
        if label_selector is not None:
            self._values["label_selector"] = label_selector
        if strategy is not None:
            self._values["strategy"] = strategy

    @builtins.property
    def label_selector(self) -> typing.Optional[_LabelSelector_2d5da14b]:
        result = self._values.get("label_selector")
        return typing.cast(typing.Optional[_LabelSelector_2d5da14b], result)

    @builtins.property
    def strategy(self) -> typing.Optional[builtins.str]:
        result = self._values.get("strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PodGC(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.Prometheus",
    jsii_struct_bases=[],
    name_mapping={
        "help": "help",
        "name": "name",
        "counter": "counter",
        "gauge": "gauge",
        "histogram": "histogram",
        "labels": "labels",
        "when": "when",
    },
)
class Prometheus:
    def __init__(
        self,
        *,
        help: builtins.str,
        name: builtins.str,
        counter: typing.Optional[Counter] = None,
        gauge: typing.Optional[Gauge] = None,
        histogram: typing.Optional[Histogram] = None,
        labels: typing.Optional[typing.Sequence[MetricLabel]] = None,
        when: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param help: 
        :param name: 
        :param counter: 
        :param gauge: 
        :param histogram: 
        :param labels: 
        :param when: 
        '''
        if isinstance(counter, dict):
            counter = Counter(**counter)
        if isinstance(gauge, dict):
            gauge = Gauge(**gauge)
        if isinstance(histogram, dict):
            histogram = Histogram(**histogram)
        self._values: typing.Dict[str, typing.Any] = {
            "help": help,
            "name": name,
        }
        if counter is not None:
            self._values["counter"] = counter
        if gauge is not None:
            self._values["gauge"] = gauge
        if histogram is not None:
            self._values["histogram"] = histogram
        if labels is not None:
            self._values["labels"] = labels
        if when is not None:
            self._values["when"] = when

    @builtins.property
    def help(self) -> builtins.str:
        result = self._values.get("help")
        assert result is not None, "Required property 'help' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def counter(self) -> typing.Optional[Counter]:
        result = self._values.get("counter")
        return typing.cast(typing.Optional[Counter], result)

    @builtins.property
    def gauge(self) -> typing.Optional[Gauge]:
        result = self._values.get("gauge")
        return typing.cast(typing.Optional[Gauge], result)

    @builtins.property
    def histogram(self) -> typing.Optional[Histogram]:
        result = self._values.get("histogram")
        return typing.cast(typing.Optional[Histogram], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.List[MetricLabel]]:
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.List[MetricLabel]], result)

    @builtins.property
    def when(self) -> typing.Optional[builtins.str]:
        result = self._values.get("when")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Prometheus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.RawArtifact",
    jsii_struct_bases=[],
    name_mapping={"data": "data"},
)
class RawArtifact:
    def __init__(self, *, data: builtins.str) -> None:
        '''
        :param data: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "data": data,
        }

    @builtins.property
    def data(self) -> builtins.str:
        result = self._values.get("data")
        assert result is not None, "Required property 'data' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RawArtifact(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.ResourceTemplate",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "failure_condition": "failureCondition",
        "flags": "flags",
        "manifest": "manifest",
        "merge_strategy": "mergeStrategy",
        "set_owner_reference": "setOwnerReference",
        "success_condition": "successCondition",
    },
)
class ResourceTemplate:
    def __init__(
        self,
        *,
        action: builtins.str,
        failure_condition: typing.Optional[builtins.str] = None,
        flags: typing.Optional[typing.Sequence[builtins.str]] = None,
        manifest: typing.Optional[builtins.str] = None,
        merge_strategy: typing.Optional[builtins.str] = None,
        set_owner_reference: typing.Optional[builtins.bool] = None,
        success_condition: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param action: 
        :param failure_condition: 
        :param flags: 
        :param manifest: 
        :param merge_strategy: 
        :param set_owner_reference: 
        :param success_condition: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "action": action,
        }
        if failure_condition is not None:
            self._values["failure_condition"] = failure_condition
        if flags is not None:
            self._values["flags"] = flags
        if manifest is not None:
            self._values["manifest"] = manifest
        if merge_strategy is not None:
            self._values["merge_strategy"] = merge_strategy
        if set_owner_reference is not None:
            self._values["set_owner_reference"] = set_owner_reference
        if success_condition is not None:
            self._values["success_condition"] = success_condition

    @builtins.property
    def action(self) -> builtins.str:
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def failure_condition(self) -> typing.Optional[builtins.str]:
        result = self._values.get("failure_condition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def flags(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("flags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def manifest(self) -> typing.Optional[builtins.str]:
        result = self._values.get("manifest")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def merge_strategy(self) -> typing.Optional[builtins.str]:
        result = self._values.get("merge_strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def set_owner_reference(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("set_owner_reference")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def success_condition(self) -> typing.Optional[builtins.str]:
        result = self._values.get("success_condition")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResourceTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.RetryAffinity",
    jsii_struct_bases=[],
    name_mapping={"node_anti_affinity": "nodeAntiAffinity"},
)
class RetryAffinity:
    def __init__(
        self,
        *,
        node_anti_affinity: typing.Optional["RetryNodeAntiAffinity"] = None,
    ) -> None:
        '''
        :param node_anti_affinity: 
        '''
        if isinstance(node_anti_affinity, dict):
            node_anti_affinity = RetryNodeAntiAffinity(**node_anti_affinity)
        self._values: typing.Dict[str, typing.Any] = {}
        if node_anti_affinity is not None:
            self._values["node_anti_affinity"] = node_anti_affinity

    @builtins.property
    def node_anti_affinity(self) -> typing.Optional["RetryNodeAntiAffinity"]:
        result = self._values.get("node_anti_affinity")
        return typing.cast(typing.Optional["RetryNodeAntiAffinity"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RetryAffinity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.RetryNodeAntiAffinity",
    jsii_struct_bases=[],
    name_mapping={},
)
class RetryNodeAntiAffinity:
    def __init__(self) -> None:
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RetryNodeAntiAffinity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.RetryStrategy",
    jsii_struct_bases=[],
    name_mapping={
        "affinity": "affinity",
        "backoff": "backoff",
        "limit": "limit",
        "retry_policy": "retryPolicy",
    },
)
class RetryStrategy:
    def __init__(
        self,
        *,
        affinity: typing.Optional[RetryAffinity] = None,
        backoff: typing.Optional[Backoff] = None,
        limit: typing.Optional[_IntOrString_f14b6057] = None,
        retry_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param affinity: 
        :param backoff: 
        :param limit: 
        :param retry_policy: 
        '''
        if isinstance(affinity, dict):
            affinity = RetryAffinity(**affinity)
        if isinstance(backoff, dict):
            backoff = Backoff(**backoff)
        self._values: typing.Dict[str, typing.Any] = {}
        if affinity is not None:
            self._values["affinity"] = affinity
        if backoff is not None:
            self._values["backoff"] = backoff
        if limit is not None:
            self._values["limit"] = limit
        if retry_policy is not None:
            self._values["retry_policy"] = retry_policy

    @builtins.property
    def affinity(self) -> typing.Optional[RetryAffinity]:
        result = self._values.get("affinity")
        return typing.cast(typing.Optional[RetryAffinity], result)

    @builtins.property
    def backoff(self) -> typing.Optional[Backoff]:
        result = self._values.get("backoff")
        return typing.cast(typing.Optional[Backoff], result)

    @builtins.property
    def limit(self) -> typing.Optional[_IntOrString_f14b6057]:
        result = self._values.get("limit")
        return typing.cast(typing.Optional[_IntOrString_f14b6057], result)

    @builtins.property
    def retry_policy(self) -> typing.Optional[builtins.str]:
        result = self._values.get("retry_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RetryStrategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.S3Artifact",
    jsii_struct_bases=[],
    name_mapping={
        "access_key_secret": "accessKeySecret",
        "bucket": "bucket",
        "create_bucket_if_not_present": "createBucketIfNotPresent",
        "endpoint": "endpoint",
        "insecure": "insecure",
        "key": "key",
        "region": "region",
        "role_arn": "roleARN",
        "secret_key_secret": "secretKeySecret",
        "use_sdk_creds": "useSDKCreds",
    },
)
class S3Artifact:
    def __init__(
        self,
        *,
        access_key_secret: typing.Optional[_SecretKeySelector_3834a17e] = None,
        bucket: typing.Optional[builtins.str] = None,
        create_bucket_if_not_present: typing.Optional[CreateS3BucketOptions] = None,
        endpoint: typing.Optional[builtins.str] = None,
        insecure: typing.Optional[builtins.bool] = None,
        key: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        secret_key_secret: typing.Optional[_SecretKeySelector_3834a17e] = None,
        use_sdk_creds: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param access_key_secret: 
        :param bucket: 
        :param create_bucket_if_not_present: 
        :param endpoint: 
        :param insecure: 
        :param key: 
        :param region: 
        :param role_arn: 
        :param secret_key_secret: 
        :param use_sdk_creds: 
        '''
        if isinstance(access_key_secret, dict):
            access_key_secret = _SecretKeySelector_3834a17e(**access_key_secret)
        if isinstance(create_bucket_if_not_present, dict):
            create_bucket_if_not_present = CreateS3BucketOptions(**create_bucket_if_not_present)
        if isinstance(secret_key_secret, dict):
            secret_key_secret = _SecretKeySelector_3834a17e(**secret_key_secret)
        self._values: typing.Dict[str, typing.Any] = {}
        if access_key_secret is not None:
            self._values["access_key_secret"] = access_key_secret
        if bucket is not None:
            self._values["bucket"] = bucket
        if create_bucket_if_not_present is not None:
            self._values["create_bucket_if_not_present"] = create_bucket_if_not_present
        if endpoint is not None:
            self._values["endpoint"] = endpoint
        if insecure is not None:
            self._values["insecure"] = insecure
        if key is not None:
            self._values["key"] = key
        if region is not None:
            self._values["region"] = region
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if secret_key_secret is not None:
            self._values["secret_key_secret"] = secret_key_secret
        if use_sdk_creds is not None:
            self._values["use_sdk_creds"] = use_sdk_creds

    @builtins.property
    def access_key_secret(self) -> typing.Optional[_SecretKeySelector_3834a17e]:
        result = self._values.get("access_key_secret")
        return typing.cast(typing.Optional[_SecretKeySelector_3834a17e], result)

    @builtins.property
    def bucket(self) -> typing.Optional[builtins.str]:
        result = self._values.get("bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def create_bucket_if_not_present(self) -> typing.Optional[CreateS3BucketOptions]:
        result = self._values.get("create_bucket_if_not_present")
        return typing.cast(typing.Optional[CreateS3BucketOptions], result)

    @builtins.property
    def endpoint(self) -> typing.Optional[builtins.str]:
        result = self._values.get("endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def insecure(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("insecure")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_key_secret(self) -> typing.Optional[_SecretKeySelector_3834a17e]:
        result = self._values.get("secret_key_secret")
        return typing.cast(typing.Optional[_SecretKeySelector_3834a17e], result)

    @builtins.property
    def use_sdk_creds(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("use_sdk_creds")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3Artifact(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.ScriptTemplate",
    jsii_struct_bases=[],
    name_mapping={
        "image": "image",
        "source": "source",
        "args": "args",
        "command": "command",
        "env": "env",
        "env_from": "envFrom",
        "image_pull_policy": "imagePullPolicy",
        "lifecycle": "lifecycle",
        "liveness_probe": "livenessProbe",
        "name": "name",
        "ports": "ports",
        "readiness_probe": "readinessProbe",
        "resources": "resources",
        "security_context": "securityContext",
        "startup_probe": "startupProbe",
        "stdin": "stdin",
        "stdin_once": "stdinOnce",
        "termination_message_path": "terminationMessagePath",
        "termination_message_policy": "terminationMessagePolicy",
        "tty": "tty",
        "volume_devices": "volumeDevices",
        "volume_mounts": "volumeMounts",
        "working_dir": "workingDir",
    },
)
class ScriptTemplate:
    def __init__(
        self,
        *,
        image: builtins.str,
        source: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        env: typing.Optional[typing.Sequence[_EnvVar_1741b5ed]] = None,
        env_from: typing.Optional[typing.Sequence[_EnvFromSource_35bf044a]] = None,
        image_pull_policy: typing.Optional[builtins.str] = None,
        lifecycle: typing.Optional[_Lifecycle_780bc732] = None,
        liveness_probe: typing.Optional[_Probe_6e8f94fa] = None,
        name: typing.Optional[builtins.str] = None,
        ports: typing.Optional[typing.Sequence[_ContainerPort_1a56bbf5]] = None,
        readiness_probe: typing.Optional[_Probe_6e8f94fa] = None,
        resources: typing.Optional[_ResourceRequirements_892d16ec] = None,
        security_context: typing.Optional[_SecurityContext_a4b1b9fb] = None,
        startup_probe: typing.Optional[_Probe_6e8f94fa] = None,
        stdin: typing.Optional[builtins.bool] = None,
        stdin_once: typing.Optional[builtins.bool] = None,
        termination_message_path: typing.Optional[builtins.str] = None,
        termination_message_policy: typing.Optional[builtins.str] = None,
        tty: typing.Optional[builtins.bool] = None,
        volume_devices: typing.Optional[typing.Sequence[_VolumeDevice_aae53ff5]] = None,
        volume_mounts: typing.Optional[typing.Sequence[_VolumeMount_366b43c7]] = None,
        working_dir: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param image: 
        :param source: 
        :param args: 
        :param command: 
        :param env: 
        :param env_from: 
        :param image_pull_policy: 
        :param lifecycle: 
        :param liveness_probe: 
        :param name: 
        :param ports: 
        :param readiness_probe: 
        :param resources: 
        :param security_context: 
        :param startup_probe: 
        :param stdin: 
        :param stdin_once: 
        :param termination_message_path: 
        :param termination_message_policy: 
        :param tty: 
        :param volume_devices: 
        :param volume_mounts: 
        :param working_dir: 
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _Lifecycle_780bc732(**lifecycle)
        if isinstance(liveness_probe, dict):
            liveness_probe = _Probe_6e8f94fa(**liveness_probe)
        if isinstance(readiness_probe, dict):
            readiness_probe = _Probe_6e8f94fa(**readiness_probe)
        if isinstance(resources, dict):
            resources = _ResourceRequirements_892d16ec(**resources)
        if isinstance(security_context, dict):
            security_context = _SecurityContext_a4b1b9fb(**security_context)
        if isinstance(startup_probe, dict):
            startup_probe = _Probe_6e8f94fa(**startup_probe)
        self._values: typing.Dict[str, typing.Any] = {
            "image": image,
            "source": source,
        }
        if args is not None:
            self._values["args"] = args
        if command is not None:
            self._values["command"] = command
        if env is not None:
            self._values["env"] = env
        if env_from is not None:
            self._values["env_from"] = env_from
        if image_pull_policy is not None:
            self._values["image_pull_policy"] = image_pull_policy
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if liveness_probe is not None:
            self._values["liveness_probe"] = liveness_probe
        if name is not None:
            self._values["name"] = name
        if ports is not None:
            self._values["ports"] = ports
        if readiness_probe is not None:
            self._values["readiness_probe"] = readiness_probe
        if resources is not None:
            self._values["resources"] = resources
        if security_context is not None:
            self._values["security_context"] = security_context
        if startup_probe is not None:
            self._values["startup_probe"] = startup_probe
        if stdin is not None:
            self._values["stdin"] = stdin
        if stdin_once is not None:
            self._values["stdin_once"] = stdin_once
        if termination_message_path is not None:
            self._values["termination_message_path"] = termination_message_path
        if termination_message_policy is not None:
            self._values["termination_message_policy"] = termination_message_policy
        if tty is not None:
            self._values["tty"] = tty
        if volume_devices is not None:
            self._values["volume_devices"] = volume_devices
        if volume_mounts is not None:
            self._values["volume_mounts"] = volume_mounts
        if working_dir is not None:
            self._values["working_dir"] = working_dir

    @builtins.property
    def image(self) -> builtins.str:
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> builtins.str:
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.List[_EnvVar_1741b5ed]]:
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.List[_EnvVar_1741b5ed]], result)

    @builtins.property
    def env_from(self) -> typing.Optional[typing.List[_EnvFromSource_35bf044a]]:
        result = self._values.get("env_from")
        return typing.cast(typing.Optional[typing.List[_EnvFromSource_35bf044a]], result)

    @builtins.property
    def image_pull_policy(self) -> typing.Optional[builtins.str]:
        result = self._values.get("image_pull_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_Lifecycle_780bc732]:
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_Lifecycle_780bc732], result)

    @builtins.property
    def liveness_probe(self) -> typing.Optional[_Probe_6e8f94fa]:
        result = self._values.get("liveness_probe")
        return typing.cast(typing.Optional[_Probe_6e8f94fa], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ports(self) -> typing.Optional[typing.List[_ContainerPort_1a56bbf5]]:
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.List[_ContainerPort_1a56bbf5]], result)

    @builtins.property
    def readiness_probe(self) -> typing.Optional[_Probe_6e8f94fa]:
        result = self._values.get("readiness_probe")
        return typing.cast(typing.Optional[_Probe_6e8f94fa], result)

    @builtins.property
    def resources(self) -> typing.Optional[_ResourceRequirements_892d16ec]:
        result = self._values.get("resources")
        return typing.cast(typing.Optional[_ResourceRequirements_892d16ec], result)

    @builtins.property
    def security_context(self) -> typing.Optional[_SecurityContext_a4b1b9fb]:
        result = self._values.get("security_context")
        return typing.cast(typing.Optional[_SecurityContext_a4b1b9fb], result)

    @builtins.property
    def startup_probe(self) -> typing.Optional[_Probe_6e8f94fa]:
        result = self._values.get("startup_probe")
        return typing.cast(typing.Optional[_Probe_6e8f94fa], result)

    @builtins.property
    def stdin(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("stdin")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stdin_once(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("stdin_once")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def termination_message_path(self) -> typing.Optional[builtins.str]:
        result = self._values.get("termination_message_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def termination_message_policy(self) -> typing.Optional[builtins.str]:
        result = self._values.get("termination_message_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tty(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("tty")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def volume_devices(self) -> typing.Optional[typing.List[_VolumeDevice_aae53ff5]]:
        result = self._values.get("volume_devices")
        return typing.cast(typing.Optional[typing.List[_VolumeDevice_aae53ff5]], result)

    @builtins.property
    def volume_mounts(self) -> typing.Optional[typing.List[_VolumeMount_366b43c7]]:
        result = self._values.get("volume_mounts")
        return typing.cast(typing.Optional[typing.List[_VolumeMount_366b43c7]], result)

    @builtins.property
    def working_dir(self) -> typing.Optional[builtins.str]:
        result = self._values.get("working_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScriptTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.SemaphoreHolding",
    jsii_struct_bases=[],
    name_mapping={"holders": "holders", "semaphore": "semaphore"},
)
class SemaphoreHolding:
    def __init__(
        self,
        *,
        holders: typing.Optional[typing.Sequence[builtins.str]] = None,
        semaphore: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param holders: 
        :param semaphore: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if holders is not None:
            self._values["holders"] = holders
        if semaphore is not None:
            self._values["semaphore"] = semaphore

    @builtins.property
    def holders(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("holders")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def semaphore(self) -> typing.Optional[builtins.str]:
        result = self._values.get("semaphore")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SemaphoreHolding(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.SemaphoreRef",
    jsii_struct_bases=[],
    name_mapping={"config_map_key_ref": "configMapKeyRef"},
)
class SemaphoreRef:
    def __init__(
        self,
        *,
        config_map_key_ref: typing.Optional[_ConfigMapKeySelector_655813de] = None,
    ) -> None:
        '''
        :param config_map_key_ref: 
        '''
        if isinstance(config_map_key_ref, dict):
            config_map_key_ref = _ConfigMapKeySelector_655813de(**config_map_key_ref)
        self._values: typing.Dict[str, typing.Any] = {}
        if config_map_key_ref is not None:
            self._values["config_map_key_ref"] = config_map_key_ref

    @builtins.property
    def config_map_key_ref(self) -> typing.Optional[_ConfigMapKeySelector_655813de]:
        result = self._values.get("config_map_key_ref")
        return typing.cast(typing.Optional[_ConfigMapKeySelector_655813de], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SemaphoreRef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.SemaphoreStatus",
    jsii_struct_bases=[],
    name_mapping={"holding": "holding", "waiting": "waiting"},
)
class SemaphoreStatus:
    def __init__(
        self,
        *,
        holding: typing.Optional[typing.Sequence[SemaphoreHolding]] = None,
        waiting: typing.Optional[typing.Sequence[SemaphoreHolding]] = None,
    ) -> None:
        '''
        :param holding: 
        :param waiting: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if holding is not None:
            self._values["holding"] = holding
        if waiting is not None:
            self._values["waiting"] = waiting

    @builtins.property
    def holding(self) -> typing.Optional[typing.List[SemaphoreHolding]]:
        result = self._values.get("holding")
        return typing.cast(typing.Optional[typing.List[SemaphoreHolding]], result)

    @builtins.property
    def waiting(self) -> typing.Optional[typing.List[SemaphoreHolding]]:
        result = self._values.get("waiting")
        return typing.cast(typing.Optional[typing.List[SemaphoreHolding]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SemaphoreStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.Sequence",
    jsii_struct_bases=[],
    name_mapping={
        "count": "count",
        "end": "end",
        "format": "format",
        "start": "start",
    },
)
class Sequence:
    def __init__(
        self,
        *,
        count: typing.Optional[_IntOrString_f14b6057] = None,
        end: typing.Optional[_IntOrString_f14b6057] = None,
        format: typing.Optional[builtins.str] = None,
        start: typing.Optional[_IntOrString_f14b6057] = None,
    ) -> None:
        '''
        :param count: 
        :param end: 
        :param format: 
        :param start: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if count is not None:
            self._values["count"] = count
        if end is not None:
            self._values["end"] = end
        if format is not None:
            self._values["format"] = format
        if start is not None:
            self._values["start"] = start

    @builtins.property
    def count(self) -> typing.Optional[_IntOrString_f14b6057]:
        result = self._values.get("count")
        return typing.cast(typing.Optional[_IntOrString_f14b6057], result)

    @builtins.property
    def end(self) -> typing.Optional[_IntOrString_f14b6057]:
        result = self._values.get("end")
        return typing.cast(typing.Optional[_IntOrString_f14b6057], result)

    @builtins.property
    def format(self) -> typing.Optional[builtins.str]:
        result = self._values.get("format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start(self) -> typing.Optional[_IntOrString_f14b6057]:
        result = self._values.get("start")
        return typing.cast(typing.Optional[_IntOrString_f14b6057], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Sequence(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.Submit",
    jsii_struct_bases=[],
    name_mapping={
        "workflow_template_ref": "workflowTemplateRef",
        "arguments": "arguments",
        "metadata": "metadata",
    },
)
class Submit:
    def __init__(
        self,
        *,
        workflow_template_ref: "WorkflowTemplateRef",
        arguments: typing.Optional[Arguments] = None,
        metadata: typing.Optional[_ObjectMeta_77a65d46] = None,
    ) -> None:
        '''
        :param workflow_template_ref: 
        :param arguments: 
        :param metadata: 
        '''
        if isinstance(workflow_template_ref, dict):
            workflow_template_ref = WorkflowTemplateRef(**workflow_template_ref)
        if isinstance(arguments, dict):
            arguments = Arguments(**arguments)
        if isinstance(metadata, dict):
            metadata = _ObjectMeta_77a65d46(**metadata)
        self._values: typing.Dict[str, typing.Any] = {
            "workflow_template_ref": workflow_template_ref,
        }
        if arguments is not None:
            self._values["arguments"] = arguments
        if metadata is not None:
            self._values["metadata"] = metadata

    @builtins.property
    def workflow_template_ref(self) -> "WorkflowTemplateRef":
        result = self._values.get("workflow_template_ref")
        assert result is not None, "Required property 'workflow_template_ref' is missing"
        return typing.cast("WorkflowTemplateRef", result)

    @builtins.property
    def arguments(self) -> typing.Optional[Arguments]:
        result = self._values.get("arguments")
        return typing.cast(typing.Optional[Arguments], result)

    @builtins.property
    def metadata(self) -> typing.Optional[_ObjectMeta_77a65d46]:
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[_ObjectMeta_77a65d46], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Submit(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.SubmitOpts",
    jsii_struct_bases=[],
    name_mapping={
        "annotations": "annotations",
        "dry_run": "dryRun",
        "entry_point": "entryPoint",
        "generate_name": "generateName",
        "labels": "labels",
        "name": "name",
        "owner_reference": "ownerReference",
        "parameter_file": "parameterFile",
        "parameters": "parameters",
        "server_dry_run": "serverDryRun",
        "service_account": "serviceAccount",
    },
)
class SubmitOpts:
    def __init__(
        self,
        *,
        annotations: typing.Optional[builtins.str] = None,
        dry_run: typing.Optional[builtins.bool] = None,
        entry_point: typing.Optional[builtins.str] = None,
        generate_name: typing.Optional[builtins.str] = None,
        labels: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        owner_reference: typing.Optional[_OwnerReference_a16cc249] = None,
        parameter_file: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Sequence[builtins.str]] = None,
        server_dry_run: typing.Optional[builtins.bool] = None,
        service_account: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param annotations: 
        :param dry_run: 
        :param entry_point: 
        :param generate_name: 
        :param labels: 
        :param name: 
        :param owner_reference: 
        :param parameter_file: 
        :param parameters: 
        :param server_dry_run: 
        :param service_account: 
        '''
        if isinstance(owner_reference, dict):
            owner_reference = _OwnerReference_a16cc249(**owner_reference)
        self._values: typing.Dict[str, typing.Any] = {}
        if annotations is not None:
            self._values["annotations"] = annotations
        if dry_run is not None:
            self._values["dry_run"] = dry_run
        if entry_point is not None:
            self._values["entry_point"] = entry_point
        if generate_name is not None:
            self._values["generate_name"] = generate_name
        if labels is not None:
            self._values["labels"] = labels
        if name is not None:
            self._values["name"] = name
        if owner_reference is not None:
            self._values["owner_reference"] = owner_reference
        if parameter_file is not None:
            self._values["parameter_file"] = parameter_file
        if parameters is not None:
            self._values["parameters"] = parameters
        if server_dry_run is not None:
            self._values["server_dry_run"] = server_dry_run
        if service_account is not None:
            self._values["service_account"] = service_account

    @builtins.property
    def annotations(self) -> typing.Optional[builtins.str]:
        result = self._values.get("annotations")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dry_run(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("dry_run")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def entry_point(self) -> typing.Optional[builtins.str]:
        result = self._values.get("entry_point")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def generate_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("generate_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[builtins.str]:
        result = self._values.get("labels")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def owner_reference(self) -> typing.Optional[_OwnerReference_a16cc249]:
        result = self._values.get("owner_reference")
        return typing.cast(typing.Optional[_OwnerReference_a16cc249], result)

    @builtins.property
    def parameter_file(self) -> typing.Optional[builtins.str]:
        result = self._values.get("parameter_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def server_dry_run(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("server_dry_run")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SubmitOpts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.SuppliedValueFrom",
    jsii_struct_bases=[],
    name_mapping={},
)
class SuppliedValueFrom:
    def __init__(self) -> None:
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SuppliedValueFrom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.SuspendTemplate",
    jsii_struct_bases=[],
    name_mapping={"duration": "duration"},
)
class SuspendTemplate:
    def __init__(self, *, duration: typing.Optional[builtins.str] = None) -> None:
        '''
        :param duration: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if duration is not None:
            self._values["duration"] = duration

    @builtins.property
    def duration(self) -> typing.Optional[builtins.str]:
        result = self._values.get("duration")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SuspendTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.Synchronization",
    jsii_struct_bases=[],
    name_mapping={"mutex": "mutex", "semaphore": "semaphore"},
)
class Synchronization:
    def __init__(
        self,
        *,
        mutex: typing.Optional[Mutex] = None,
        semaphore: typing.Optional[SemaphoreRef] = None,
    ) -> None:
        '''
        :param mutex: 
        :param semaphore: 
        '''
        if isinstance(mutex, dict):
            mutex = Mutex(**mutex)
        if isinstance(semaphore, dict):
            semaphore = SemaphoreRef(**semaphore)
        self._values: typing.Dict[str, typing.Any] = {}
        if mutex is not None:
            self._values["mutex"] = mutex
        if semaphore is not None:
            self._values["semaphore"] = semaphore

    @builtins.property
    def mutex(self) -> typing.Optional[Mutex]:
        result = self._values.get("mutex")
        return typing.cast(typing.Optional[Mutex], result)

    @builtins.property
    def semaphore(self) -> typing.Optional[SemaphoreRef]:
        result = self._values.get("semaphore")
        return typing.cast(typing.Optional[SemaphoreRef], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Synchronization(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.SynchronizationStatus",
    jsii_struct_bases=[],
    name_mapping={"mutex": "mutex", "semaphore": "semaphore"},
)
class SynchronizationStatus:
    def __init__(
        self,
        *,
        mutex: typing.Optional[MutexStatus] = None,
        semaphore: typing.Optional[SemaphoreStatus] = None,
    ) -> None:
        '''
        :param mutex: 
        :param semaphore: 
        '''
        if isinstance(mutex, dict):
            mutex = MutexStatus(**mutex)
        if isinstance(semaphore, dict):
            semaphore = SemaphoreStatus(**semaphore)
        self._values: typing.Dict[str, typing.Any] = {}
        if mutex is not None:
            self._values["mutex"] = mutex
        if semaphore is not None:
            self._values["semaphore"] = semaphore

    @builtins.property
    def mutex(self) -> typing.Optional[MutexStatus]:
        result = self._values.get("mutex")
        return typing.cast(typing.Optional[MutexStatus], result)

    @builtins.property
    def semaphore(self) -> typing.Optional[SemaphoreStatus]:
        result = self._values.get("semaphore")
        return typing.cast(typing.Optional[SemaphoreStatus], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SynchronizationStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.TTLStrategy",
    jsii_struct_bases=[],
    name_mapping={
        "seconds_after_completion": "secondsAfterCompletion",
        "seconds_after_failure": "secondsAfterFailure",
        "seconds_after_success": "secondsAfterSuccess",
    },
)
class TTLStrategy:
    def __init__(
        self,
        *,
        seconds_after_completion: typing.Optional[jsii.Number] = None,
        seconds_after_failure: typing.Optional[jsii.Number] = None,
        seconds_after_success: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param seconds_after_completion: 
        :param seconds_after_failure: 
        :param seconds_after_success: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if seconds_after_completion is not None:
            self._values["seconds_after_completion"] = seconds_after_completion
        if seconds_after_failure is not None:
            self._values["seconds_after_failure"] = seconds_after_failure
        if seconds_after_success is not None:
            self._values["seconds_after_success"] = seconds_after_success

    @builtins.property
    def seconds_after_completion(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("seconds_after_completion")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def seconds_after_failure(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("seconds_after_failure")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def seconds_after_success(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("seconds_after_success")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TTLStrategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.TarStrategy",
    jsii_struct_bases=[],
    name_mapping={"compression_level": "compressionLevel"},
)
class TarStrategy:
    def __init__(
        self,
        *,
        compression_level: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param compression_level: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if compression_level is not None:
            self._values["compression_level"] = compression_level

    @builtins.property
    def compression_level(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("compression_level")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TarStrategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.Template",
    jsii_struct_bases=[],
    name_mapping={
        "active_deadline_seconds": "activeDeadlineSeconds",
        "affinity": "affinity",
        "archive_location": "archiveLocation",
        "automount_service_account_token": "automountServiceAccountToken",
        "container": "container",
        "container_set": "containerSet",
        "daemon": "daemon",
        "dag": "dag",
        "data": "data",
        "executor": "executor",
        "fail_fast": "failFast",
        "host_aliases": "hostAliases",
        "init_containers": "initContainers",
        "inputs": "inputs",
        "memoize": "memoize",
        "metadata": "metadata",
        "metrics": "metrics",
        "name": "name",
        "node_selector": "nodeSelector",
        "outputs": "outputs",
        "parallelism": "parallelism",
        "pod_spec_patch": "podSpecPatch",
        "priority": "priority",
        "priority_class_name": "priorityClassName",
        "resource": "resource",
        "retry_strategy": "retryStrategy",
        "scheduler_name": "schedulerName",
        "script": "script",
        "security_context": "securityContext",
        "service_account_name": "serviceAccountName",
        "sidecars": "sidecars",
        "steps": "steps",
        "suspend": "suspend",
        "synchronization": "synchronization",
        "timeout": "timeout",
        "tolerations": "tolerations",
        "volumes": "volumes",
    },
)
class Template:
    def __init__(
        self,
        *,
        active_deadline_seconds: typing.Optional[_IntOrString_f14b6057] = None,
        affinity: typing.Optional[_Affinity_a7d59e98] = None,
        archive_location: typing.Optional[ArtifactLocation] = None,
        automount_service_account_token: typing.Optional[builtins.bool] = None,
        container: typing.Optional[_Container_7c687a93] = None,
        container_set: typing.Optional[ContainerSetTemplate] = None,
        daemon: typing.Optional[builtins.bool] = None,
        dag: typing.Optional[DAGTemplate] = None,
        data: typing.Optional[Data] = None,
        executor: typing.Optional[ExecutorConfig] = None,
        fail_fast: typing.Optional[builtins.bool] = None,
        host_aliases: typing.Optional[typing.Sequence[_HostAlias_82563da2]] = None,
        init_containers: typing.Optional[typing.Sequence["UserContainer"]] = None,
        inputs: typing.Optional[Inputs] = None,
        memoize: typing.Optional[Memoize] = None,
        metadata: typing.Optional[Metadata] = None,
        metrics: typing.Optional[Metrics] = None,
        name: typing.Optional[builtins.str] = None,
        node_selector: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        outputs: typing.Optional[Outputs] = None,
        parallelism: typing.Optional[jsii.Number] = None,
        pod_spec_patch: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        priority_class_name: typing.Optional[builtins.str] = None,
        resource: typing.Optional[ResourceTemplate] = None,
        retry_strategy: typing.Optional[RetryStrategy] = None,
        scheduler_name: typing.Optional[builtins.str] = None,
        script: typing.Optional[ScriptTemplate] = None,
        security_context: typing.Optional[_PodSecurityContext_c3a517d7] = None,
        service_account_name: typing.Optional[builtins.str] = None,
        sidecars: typing.Optional[typing.Sequence["UserContainer"]] = None,
        steps: typing.Optional[typing.Sequence[typing.Sequence["WorkflowStep"]]] = None,
        suspend: typing.Optional[SuspendTemplate] = None,
        synchronization: typing.Optional[Synchronization] = None,
        timeout: typing.Optional[builtins.str] = None,
        tolerations: typing.Optional[typing.Sequence[_Toleration_aec52105]] = None,
        volumes: typing.Optional[typing.Sequence[_Volume_05ce2014]] = None,
    ) -> None:
        '''
        :param active_deadline_seconds: 
        :param affinity: 
        :param archive_location: 
        :param automount_service_account_token: 
        :param container: 
        :param container_set: 
        :param daemon: 
        :param dag: 
        :param data: 
        :param executor: 
        :param fail_fast: 
        :param host_aliases: 
        :param init_containers: 
        :param inputs: 
        :param memoize: 
        :param metadata: 
        :param metrics: 
        :param name: 
        :param node_selector: 
        :param outputs: 
        :param parallelism: 
        :param pod_spec_patch: 
        :param priority: 
        :param priority_class_name: 
        :param resource: 
        :param retry_strategy: 
        :param scheduler_name: 
        :param script: 
        :param security_context: 
        :param service_account_name: 
        :param sidecars: 
        :param steps: 
        :param suspend: 
        :param synchronization: 
        :param timeout: 
        :param tolerations: 
        :param volumes: 
        '''
        if isinstance(affinity, dict):
            affinity = _Affinity_a7d59e98(**affinity)
        if isinstance(archive_location, dict):
            archive_location = ArtifactLocation(**archive_location)
        if isinstance(container, dict):
            container = _Container_7c687a93(**container)
        if isinstance(container_set, dict):
            container_set = ContainerSetTemplate(**container_set)
        if isinstance(dag, dict):
            dag = DAGTemplate(**dag)
        if isinstance(data, dict):
            data = Data(**data)
        if isinstance(executor, dict):
            executor = ExecutorConfig(**executor)
        if isinstance(inputs, dict):
            inputs = Inputs(**inputs)
        if isinstance(memoize, dict):
            memoize = Memoize(**memoize)
        if isinstance(metadata, dict):
            metadata = Metadata(**metadata)
        if isinstance(metrics, dict):
            metrics = Metrics(**metrics)
        if isinstance(outputs, dict):
            outputs = Outputs(**outputs)
        if isinstance(resource, dict):
            resource = ResourceTemplate(**resource)
        if isinstance(retry_strategy, dict):
            retry_strategy = RetryStrategy(**retry_strategy)
        if isinstance(script, dict):
            script = ScriptTemplate(**script)
        if isinstance(security_context, dict):
            security_context = _PodSecurityContext_c3a517d7(**security_context)
        if isinstance(suspend, dict):
            suspend = SuspendTemplate(**suspend)
        if isinstance(synchronization, dict):
            synchronization = Synchronization(**synchronization)
        self._values: typing.Dict[str, typing.Any] = {}
        if active_deadline_seconds is not None:
            self._values["active_deadline_seconds"] = active_deadline_seconds
        if affinity is not None:
            self._values["affinity"] = affinity
        if archive_location is not None:
            self._values["archive_location"] = archive_location
        if automount_service_account_token is not None:
            self._values["automount_service_account_token"] = automount_service_account_token
        if container is not None:
            self._values["container"] = container
        if container_set is not None:
            self._values["container_set"] = container_set
        if daemon is not None:
            self._values["daemon"] = daemon
        if dag is not None:
            self._values["dag"] = dag
        if data is not None:
            self._values["data"] = data
        if executor is not None:
            self._values["executor"] = executor
        if fail_fast is not None:
            self._values["fail_fast"] = fail_fast
        if host_aliases is not None:
            self._values["host_aliases"] = host_aliases
        if init_containers is not None:
            self._values["init_containers"] = init_containers
        if inputs is not None:
            self._values["inputs"] = inputs
        if memoize is not None:
            self._values["memoize"] = memoize
        if metadata is not None:
            self._values["metadata"] = metadata
        if metrics is not None:
            self._values["metrics"] = metrics
        if name is not None:
            self._values["name"] = name
        if node_selector is not None:
            self._values["node_selector"] = node_selector
        if outputs is not None:
            self._values["outputs"] = outputs
        if parallelism is not None:
            self._values["parallelism"] = parallelism
        if pod_spec_patch is not None:
            self._values["pod_spec_patch"] = pod_spec_patch
        if priority is not None:
            self._values["priority"] = priority
        if priority_class_name is not None:
            self._values["priority_class_name"] = priority_class_name
        if resource is not None:
            self._values["resource"] = resource
        if retry_strategy is not None:
            self._values["retry_strategy"] = retry_strategy
        if scheduler_name is not None:
            self._values["scheduler_name"] = scheduler_name
        if script is not None:
            self._values["script"] = script
        if security_context is not None:
            self._values["security_context"] = security_context
        if service_account_name is not None:
            self._values["service_account_name"] = service_account_name
        if sidecars is not None:
            self._values["sidecars"] = sidecars
        if steps is not None:
            self._values["steps"] = steps
        if suspend is not None:
            self._values["suspend"] = suspend
        if synchronization is not None:
            self._values["synchronization"] = synchronization
        if timeout is not None:
            self._values["timeout"] = timeout
        if tolerations is not None:
            self._values["tolerations"] = tolerations
        if volumes is not None:
            self._values["volumes"] = volumes

    @builtins.property
    def active_deadline_seconds(self) -> typing.Optional[_IntOrString_f14b6057]:
        result = self._values.get("active_deadline_seconds")
        return typing.cast(typing.Optional[_IntOrString_f14b6057], result)

    @builtins.property
    def affinity(self) -> typing.Optional[_Affinity_a7d59e98]:
        result = self._values.get("affinity")
        return typing.cast(typing.Optional[_Affinity_a7d59e98], result)

    @builtins.property
    def archive_location(self) -> typing.Optional[ArtifactLocation]:
        result = self._values.get("archive_location")
        return typing.cast(typing.Optional[ArtifactLocation], result)

    @builtins.property
    def automount_service_account_token(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("automount_service_account_token")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def container(self) -> typing.Optional[_Container_7c687a93]:
        result = self._values.get("container")
        return typing.cast(typing.Optional[_Container_7c687a93], result)

    @builtins.property
    def container_set(self) -> typing.Optional[ContainerSetTemplate]:
        result = self._values.get("container_set")
        return typing.cast(typing.Optional[ContainerSetTemplate], result)

    @builtins.property
    def daemon(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("daemon")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def dag(self) -> typing.Optional[DAGTemplate]:
        result = self._values.get("dag")
        return typing.cast(typing.Optional[DAGTemplate], result)

    @builtins.property
    def data(self) -> typing.Optional[Data]:
        result = self._values.get("data")
        return typing.cast(typing.Optional[Data], result)

    @builtins.property
    def executor(self) -> typing.Optional[ExecutorConfig]:
        result = self._values.get("executor")
        return typing.cast(typing.Optional[ExecutorConfig], result)

    @builtins.property
    def fail_fast(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("fail_fast")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def host_aliases(self) -> typing.Optional[typing.List[_HostAlias_82563da2]]:
        result = self._values.get("host_aliases")
        return typing.cast(typing.Optional[typing.List[_HostAlias_82563da2]], result)

    @builtins.property
    def init_containers(self) -> typing.Optional[typing.List["UserContainer"]]:
        result = self._values.get("init_containers")
        return typing.cast(typing.Optional[typing.List["UserContainer"]], result)

    @builtins.property
    def inputs(self) -> typing.Optional[Inputs]:
        result = self._values.get("inputs")
        return typing.cast(typing.Optional[Inputs], result)

    @builtins.property
    def memoize(self) -> typing.Optional[Memoize]:
        result = self._values.get("memoize")
        return typing.cast(typing.Optional[Memoize], result)

    @builtins.property
    def metadata(self) -> typing.Optional[Metadata]:
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[Metadata], result)

    @builtins.property
    def metrics(self) -> typing.Optional[Metrics]:
        result = self._values.get("metrics")
        return typing.cast(typing.Optional[Metrics], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_selector(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("node_selector")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def outputs(self) -> typing.Optional[Outputs]:
        result = self._values.get("outputs")
        return typing.cast(typing.Optional[Outputs], result)

    @builtins.property
    def parallelism(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("parallelism")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def pod_spec_patch(self) -> typing.Optional[builtins.str]:
        result = self._values.get("pod_spec_patch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def priority_class_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("priority_class_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource(self) -> typing.Optional[ResourceTemplate]:
        result = self._values.get("resource")
        return typing.cast(typing.Optional[ResourceTemplate], result)

    @builtins.property
    def retry_strategy(self) -> typing.Optional[RetryStrategy]:
        result = self._values.get("retry_strategy")
        return typing.cast(typing.Optional[RetryStrategy], result)

    @builtins.property
    def scheduler_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("scheduler_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def script(self) -> typing.Optional[ScriptTemplate]:
        result = self._values.get("script")
        return typing.cast(typing.Optional[ScriptTemplate], result)

    @builtins.property
    def security_context(self) -> typing.Optional[_PodSecurityContext_c3a517d7]:
        result = self._values.get("security_context")
        return typing.cast(typing.Optional[_PodSecurityContext_c3a517d7], result)

    @builtins.property
    def service_account_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("service_account_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sidecars(self) -> typing.Optional[typing.List["UserContainer"]]:
        result = self._values.get("sidecars")
        return typing.cast(typing.Optional[typing.List["UserContainer"]], result)

    @builtins.property
    def steps(self) -> typing.Optional[typing.List[typing.List["WorkflowStep"]]]:
        result = self._values.get("steps")
        return typing.cast(typing.Optional[typing.List[typing.List["WorkflowStep"]]], result)

    @builtins.property
    def suspend(self) -> typing.Optional[SuspendTemplate]:
        result = self._values.get("suspend")
        return typing.cast(typing.Optional[SuspendTemplate], result)

    @builtins.property
    def synchronization(self) -> typing.Optional[Synchronization]:
        result = self._values.get("synchronization")
        return typing.cast(typing.Optional[Synchronization], result)

    @builtins.property
    def timeout(self) -> typing.Optional[builtins.str]:
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tolerations(self) -> typing.Optional[typing.List[_Toleration_aec52105]]:
        result = self._values.get("tolerations")
        return typing.cast(typing.Optional[typing.List[_Toleration_aec52105]], result)

    @builtins.property
    def volumes(self) -> typing.Optional[typing.List[_Volume_05ce2014]]:
        result = self._values.get("volumes")
        return typing.cast(typing.Optional[typing.List[_Volume_05ce2014]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Template(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.TemplateRef",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_scope": "clusterScope",
        "name": "name",
        "template": "template",
    },
)
class TemplateRef:
    def __init__(
        self,
        *,
        cluster_scope: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cluster_scope: 
        :param name: 
        :param template: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if cluster_scope is not None:
            self._values["cluster_scope"] = cluster_scope
        if name is not None:
            self._values["name"] = name
        if template is not None:
            self._values["template"] = template

    @builtins.property
    def cluster_scope(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("cluster_scope")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template(self) -> typing.Optional[builtins.str]:
        result = self._values.get("template")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TemplateRef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.TransformationStep",
    jsii_struct_bases=[],
    name_mapping={"expression": "expression"},
)
class TransformationStep:
    def __init__(self, *, expression: builtins.str) -> None:
        '''
        :param expression: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "expression": expression,
        }

    @builtins.property
    def expression(self) -> builtins.str:
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TransformationStep(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.UpdateCronWorkflowRequest",
    jsii_struct_bases=[],
    name_mapping={
        "cron_workflow": "cronWorkflow",
        "name": "name",
        "namespace": "namespace",
    },
)
class UpdateCronWorkflowRequest:
    def __init__(
        self,
        *,
        cron_workflow: typing.Optional[CronWorkflow] = None,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cron_workflow: 
        :param name: 
        :param namespace: 
        '''
        if isinstance(cron_workflow, dict):
            cron_workflow = CronWorkflow(**cron_workflow)
        self._values: typing.Dict[str, typing.Any] = {}
        if cron_workflow is not None:
            self._values["cron_workflow"] = cron_workflow
        if name is not None:
            self._values["name"] = name
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def cron_workflow(self) -> typing.Optional[CronWorkflow]:
        result = self._values.get("cron_workflow")
        return typing.cast(typing.Optional[CronWorkflow], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UpdateCronWorkflowRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.UserContainer",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "args": "args",
        "command": "command",
        "env": "env",
        "env_from": "envFrom",
        "image": "image",
        "image_pull_policy": "imagePullPolicy",
        "lifecycle": "lifecycle",
        "liveness_probe": "livenessProbe",
        "mirror_volume_mounts": "mirrorVolumeMounts",
        "ports": "ports",
        "readiness_probe": "readinessProbe",
        "resources": "resources",
        "security_context": "securityContext",
        "startup_probe": "startupProbe",
        "stdin": "stdin",
        "stdin_once": "stdinOnce",
        "termination_message_path": "terminationMessagePath",
        "termination_message_policy": "terminationMessagePolicy",
        "tty": "tty",
        "volume_devices": "volumeDevices",
        "volume_mounts": "volumeMounts",
        "working_dir": "workingDir",
    },
)
class UserContainer:
    def __init__(
        self,
        *,
        name: builtins.str,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        env: typing.Optional[typing.Sequence[_EnvVar_1741b5ed]] = None,
        env_from: typing.Optional[typing.Sequence[_EnvFromSource_35bf044a]] = None,
        image: typing.Optional[builtins.str] = None,
        image_pull_policy: typing.Optional[builtins.str] = None,
        lifecycle: typing.Optional[_Lifecycle_780bc732] = None,
        liveness_probe: typing.Optional[_Probe_6e8f94fa] = None,
        mirror_volume_mounts: typing.Optional[builtins.bool] = None,
        ports: typing.Optional[typing.Sequence[_ContainerPort_1a56bbf5]] = None,
        readiness_probe: typing.Optional[_Probe_6e8f94fa] = None,
        resources: typing.Optional[_ResourceRequirements_892d16ec] = None,
        security_context: typing.Optional[_SecurityContext_a4b1b9fb] = None,
        startup_probe: typing.Optional[_Probe_6e8f94fa] = None,
        stdin: typing.Optional[builtins.bool] = None,
        stdin_once: typing.Optional[builtins.bool] = None,
        termination_message_path: typing.Optional[builtins.str] = None,
        termination_message_policy: typing.Optional[builtins.str] = None,
        tty: typing.Optional[builtins.bool] = None,
        volume_devices: typing.Optional[typing.Sequence[_VolumeDevice_aae53ff5]] = None,
        volume_mounts: typing.Optional[typing.Sequence[_VolumeMount_366b43c7]] = None,
        working_dir: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: 
        :param args: 
        :param command: 
        :param env: 
        :param env_from: 
        :param image: 
        :param image_pull_policy: 
        :param lifecycle: 
        :param liveness_probe: 
        :param mirror_volume_mounts: 
        :param ports: 
        :param readiness_probe: 
        :param resources: 
        :param security_context: 
        :param startup_probe: 
        :param stdin: 
        :param stdin_once: 
        :param termination_message_path: 
        :param termination_message_policy: 
        :param tty: 
        :param volume_devices: 
        :param volume_mounts: 
        :param working_dir: 
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _Lifecycle_780bc732(**lifecycle)
        if isinstance(liveness_probe, dict):
            liveness_probe = _Probe_6e8f94fa(**liveness_probe)
        if isinstance(readiness_probe, dict):
            readiness_probe = _Probe_6e8f94fa(**readiness_probe)
        if isinstance(resources, dict):
            resources = _ResourceRequirements_892d16ec(**resources)
        if isinstance(security_context, dict):
            security_context = _SecurityContext_a4b1b9fb(**security_context)
        if isinstance(startup_probe, dict):
            startup_probe = _Probe_6e8f94fa(**startup_probe)
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }
        if args is not None:
            self._values["args"] = args
        if command is not None:
            self._values["command"] = command
        if env is not None:
            self._values["env"] = env
        if env_from is not None:
            self._values["env_from"] = env_from
        if image is not None:
            self._values["image"] = image
        if image_pull_policy is not None:
            self._values["image_pull_policy"] = image_pull_policy
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if liveness_probe is not None:
            self._values["liveness_probe"] = liveness_probe
        if mirror_volume_mounts is not None:
            self._values["mirror_volume_mounts"] = mirror_volume_mounts
        if ports is not None:
            self._values["ports"] = ports
        if readiness_probe is not None:
            self._values["readiness_probe"] = readiness_probe
        if resources is not None:
            self._values["resources"] = resources
        if security_context is not None:
            self._values["security_context"] = security_context
        if startup_probe is not None:
            self._values["startup_probe"] = startup_probe
        if stdin is not None:
            self._values["stdin"] = stdin
        if stdin_once is not None:
            self._values["stdin_once"] = stdin_once
        if termination_message_path is not None:
            self._values["termination_message_path"] = termination_message_path
        if termination_message_policy is not None:
            self._values["termination_message_policy"] = termination_message_policy
        if tty is not None:
            self._values["tty"] = tty
        if volume_devices is not None:
            self._values["volume_devices"] = volume_devices
        if volume_mounts is not None:
            self._values["volume_mounts"] = volume_mounts
        if working_dir is not None:
            self._values["working_dir"] = working_dir

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.List[_EnvVar_1741b5ed]]:
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.List[_EnvVar_1741b5ed]], result)

    @builtins.property
    def env_from(self) -> typing.Optional[typing.List[_EnvFromSource_35bf044a]]:
        result = self._values.get("env_from")
        return typing.cast(typing.Optional[typing.List[_EnvFromSource_35bf044a]], result)

    @builtins.property
    def image(self) -> typing.Optional[builtins.str]:
        result = self._values.get("image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_pull_policy(self) -> typing.Optional[builtins.str]:
        result = self._values.get("image_pull_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_Lifecycle_780bc732]:
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_Lifecycle_780bc732], result)

    @builtins.property
    def liveness_probe(self) -> typing.Optional[_Probe_6e8f94fa]:
        result = self._values.get("liveness_probe")
        return typing.cast(typing.Optional[_Probe_6e8f94fa], result)

    @builtins.property
    def mirror_volume_mounts(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("mirror_volume_mounts")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ports(self) -> typing.Optional[typing.List[_ContainerPort_1a56bbf5]]:
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.List[_ContainerPort_1a56bbf5]], result)

    @builtins.property
    def readiness_probe(self) -> typing.Optional[_Probe_6e8f94fa]:
        result = self._values.get("readiness_probe")
        return typing.cast(typing.Optional[_Probe_6e8f94fa], result)

    @builtins.property
    def resources(self) -> typing.Optional[_ResourceRequirements_892d16ec]:
        result = self._values.get("resources")
        return typing.cast(typing.Optional[_ResourceRequirements_892d16ec], result)

    @builtins.property
    def security_context(self) -> typing.Optional[_SecurityContext_a4b1b9fb]:
        result = self._values.get("security_context")
        return typing.cast(typing.Optional[_SecurityContext_a4b1b9fb], result)

    @builtins.property
    def startup_probe(self) -> typing.Optional[_Probe_6e8f94fa]:
        result = self._values.get("startup_probe")
        return typing.cast(typing.Optional[_Probe_6e8f94fa], result)

    @builtins.property
    def stdin(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("stdin")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stdin_once(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("stdin_once")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def termination_message_path(self) -> typing.Optional[builtins.str]:
        result = self._values.get("termination_message_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def termination_message_policy(self) -> typing.Optional[builtins.str]:
        result = self._values.get("termination_message_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tty(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("tty")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def volume_devices(self) -> typing.Optional[typing.List[_VolumeDevice_aae53ff5]]:
        result = self._values.get("volume_devices")
        return typing.cast(typing.Optional[typing.List[_VolumeDevice_aae53ff5]], result)

    @builtins.property
    def volume_mounts(self) -> typing.Optional[typing.List[_VolumeMount_366b43c7]]:
        result = self._values.get("volume_mounts")
        return typing.cast(typing.Optional[typing.List[_VolumeMount_366b43c7]], result)

    @builtins.property
    def working_dir(self) -> typing.Optional[builtins.str]:
        result = self._values.get("working_dir")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserContainer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.ValueFrom",
    jsii_struct_bases=[],
    name_mapping={
        "default": "default",
        "event": "event",
        "expression": "expression",
        "jq_filter": "jqFilter",
        "json_path": "jsonPath",
        "parameter": "parameter",
        "path": "path",
        "supplied": "supplied",
    },
)
class ValueFrom:
    def __init__(
        self,
        *,
        default: typing.Optional[builtins.str] = None,
        event: typing.Optional[builtins.str] = None,
        expression: typing.Optional[builtins.str] = None,
        jq_filter: typing.Optional[builtins.str] = None,
        json_path: typing.Optional[builtins.str] = None,
        parameter: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        supplied: typing.Optional[SuppliedValueFrom] = None,
    ) -> None:
        '''
        :param default: 
        :param event: 
        :param expression: 
        :param jq_filter: 
        :param json_path: 
        :param parameter: 
        :param path: 
        :param supplied: 
        '''
        if isinstance(supplied, dict):
            supplied = SuppliedValueFrom(**supplied)
        self._values: typing.Dict[str, typing.Any] = {}
        if default is not None:
            self._values["default"] = default
        if event is not None:
            self._values["event"] = event
        if expression is not None:
            self._values["expression"] = expression
        if jq_filter is not None:
            self._values["jq_filter"] = jq_filter
        if json_path is not None:
            self._values["json_path"] = json_path
        if parameter is not None:
            self._values["parameter"] = parameter
        if path is not None:
            self._values["path"] = path
        if supplied is not None:
            self._values["supplied"] = supplied

    @builtins.property
    def default(self) -> typing.Optional[builtins.str]:
        result = self._values.get("default")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event(self) -> typing.Optional[builtins.str]:
        result = self._values.get("event")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expression(self) -> typing.Optional[builtins.str]:
        result = self._values.get("expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jq_filter(self) -> typing.Optional[builtins.str]:
        result = self._values.get("jq_filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def json_path(self) -> typing.Optional[builtins.str]:
        result = self._values.get("json_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter(self) -> typing.Optional[builtins.str]:
        result = self._values.get("parameter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def supplied(self) -> typing.Optional[SuppliedValueFrom]:
        result = self._values.get("supplied")
        return typing.cast(typing.Optional[SuppliedValueFrom], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ValueFrom(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.Version",
    jsii_struct_bases=[],
    name_mapping={
        "build_date": "buildDate",
        "compiler": "compiler",
        "git_commit": "gitCommit",
        "git_tag": "gitTag",
        "git_tree_state": "gitTreeState",
        "go_version": "goVersion",
        "platform": "platform",
        "version": "version",
    },
)
class Version:
    def __init__(
        self,
        *,
        build_date: builtins.str,
        compiler: builtins.str,
        git_commit: builtins.str,
        git_tag: builtins.str,
        git_tree_state: builtins.str,
        go_version: builtins.str,
        platform: builtins.str,
        version: builtins.str,
    ) -> None:
        '''
        :param build_date: 
        :param compiler: 
        :param git_commit: 
        :param git_tag: 
        :param git_tree_state: 
        :param go_version: 
        :param platform: 
        :param version: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "build_date": build_date,
            "compiler": compiler,
            "git_commit": git_commit,
            "git_tag": git_tag,
            "git_tree_state": git_tree_state,
            "go_version": go_version,
            "platform": platform,
            "version": version,
        }

    @builtins.property
    def build_date(self) -> builtins.str:
        result = self._values.get("build_date")
        assert result is not None, "Required property 'build_date' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def compiler(self) -> builtins.str:
        result = self._values.get("compiler")
        assert result is not None, "Required property 'compiler' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def git_commit(self) -> builtins.str:
        result = self._values.get("git_commit")
        assert result is not None, "Required property 'git_commit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def git_tag(self) -> builtins.str:
        result = self._values.get("git_tag")
        assert result is not None, "Required property 'git_tag' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def git_tree_state(self) -> builtins.str:
        result = self._values.get("git_tree_state")
        assert result is not None, "Required property 'git_tree_state' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def go_version(self) -> builtins.str:
        result = self._values.get("go_version")
        assert result is not None, "Required property 'go_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def platform(self) -> builtins.str:
        result = self._values.get("platform")
        assert result is not None, "Required property 'platform' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Version(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.VolumeClaimGC",
    jsii_struct_bases=[],
    name_mapping={"strategy": "strategy"},
)
class VolumeClaimGC:
    def __init__(self, *, strategy: typing.Optional[builtins.str] = None) -> None:
        '''
        :param strategy: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if strategy is not None:
            self._values["strategy"] = strategy

    @builtins.property
    def strategy(self) -> typing.Optional[builtins.str]:
        result = self._values.get("strategy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VolumeClaimGC(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.Workflow",
    jsii_struct_bases=[],
    name_mapping={
        "metadata": "metadata",
        "spec": "spec",
        "api_version": "apiVersion",
        "kind": "kind",
        "status": "status",
    },
)
class Workflow:
    def __init__(
        self,
        *,
        metadata: _ObjectMeta_77a65d46,
        spec: "WorkflowSpec",
        api_version: typing.Optional[builtins.str] = None,
        kind: typing.Optional[builtins.str] = None,
        status: typing.Optional["WorkflowStatus"] = None,
    ) -> None:
        '''
        :param metadata: 
        :param spec: 
        :param api_version: 
        :param kind: 
        :param status: 
        '''
        if isinstance(metadata, dict):
            metadata = _ObjectMeta_77a65d46(**metadata)
        if isinstance(spec, dict):
            spec = WorkflowSpec(**spec)
        if isinstance(status, dict):
            status = WorkflowStatus(**status)
        self._values: typing.Dict[str, typing.Any] = {
            "metadata": metadata,
            "spec": spec,
        }
        if api_version is not None:
            self._values["api_version"] = api_version
        if kind is not None:
            self._values["kind"] = kind
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def metadata(self) -> _ObjectMeta_77a65d46:
        result = self._values.get("metadata")
        assert result is not None, "Required property 'metadata' is missing"
        return typing.cast(_ObjectMeta_77a65d46, result)

    @builtins.property
    def spec(self) -> "WorkflowSpec":
        result = self._values.get("spec")
        assert result is not None, "Required property 'spec' is missing"
        return typing.cast("WorkflowSpec", result)

    @builtins.property
    def api_version(self) -> typing.Optional[builtins.str]:
        result = self._values.get("api_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kind(self) -> typing.Optional[builtins.str]:
        result = self._values.get("kind")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional["WorkflowStatus"]:
        result = self._values.get("status")
        return typing.cast(typing.Optional["WorkflowStatus"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Workflow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.WorkflowCreateRequest",
    jsii_struct_bases=[],
    name_mapping={
        "create_options": "createOptions",
        "instance_id": "instanceID",
        "namespace": "namespace",
        "server_dry_run": "serverDryRun",
        "workflow": "workflow",
    },
)
class WorkflowCreateRequest:
    def __init__(
        self,
        *,
        create_options: typing.Optional[_CreateOptions_33e095be] = None,
        instance_id: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        server_dry_run: typing.Optional[builtins.bool] = None,
        workflow: typing.Optional[Workflow] = None,
    ) -> None:
        '''
        :param create_options: 
        :param instance_id: 
        :param namespace: 
        :param server_dry_run: 
        :param workflow: 
        '''
        if isinstance(create_options, dict):
            create_options = _CreateOptions_33e095be(**create_options)
        if isinstance(workflow, dict):
            workflow = Workflow(**workflow)
        self._values: typing.Dict[str, typing.Any] = {}
        if create_options is not None:
            self._values["create_options"] = create_options
        if instance_id is not None:
            self._values["instance_id"] = instance_id
        if namespace is not None:
            self._values["namespace"] = namespace
        if server_dry_run is not None:
            self._values["server_dry_run"] = server_dry_run
        if workflow is not None:
            self._values["workflow"] = workflow

    @builtins.property
    def create_options(self) -> typing.Optional[_CreateOptions_33e095be]:
        result = self._values.get("create_options")
        return typing.cast(typing.Optional[_CreateOptions_33e095be], result)

    @builtins.property
    def instance_id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("instance_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_dry_run(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("server_dry_run")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def workflow(self) -> typing.Optional[Workflow]:
        result = self._values.get("workflow")
        return typing.cast(typing.Optional[Workflow], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowCreateRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.WorkflowDeleteResponse",
    jsii_struct_bases=[],
    name_mapping={},
)
class WorkflowDeleteResponse:
    def __init__(self) -> None:
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowDeleteResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.WorkflowEventBinding",
    jsii_struct_bases=[],
    name_mapping={
        "metadata": "metadata",
        "spec": "spec",
        "api_version": "apiVersion",
        "kind": "kind",
    },
)
class WorkflowEventBinding:
    def __init__(
        self,
        *,
        metadata: _ObjectMeta_77a65d46,
        spec: "WorkflowEventBindingSpec",
        api_version: typing.Optional[builtins.str] = None,
        kind: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param metadata: 
        :param spec: 
        :param api_version: 
        :param kind: 
        '''
        if isinstance(metadata, dict):
            metadata = _ObjectMeta_77a65d46(**metadata)
        if isinstance(spec, dict):
            spec = WorkflowEventBindingSpec(**spec)
        self._values: typing.Dict[str, typing.Any] = {
            "metadata": metadata,
            "spec": spec,
        }
        if api_version is not None:
            self._values["api_version"] = api_version
        if kind is not None:
            self._values["kind"] = kind

    @builtins.property
    def metadata(self) -> _ObjectMeta_77a65d46:
        result = self._values.get("metadata")
        assert result is not None, "Required property 'metadata' is missing"
        return typing.cast(_ObjectMeta_77a65d46, result)

    @builtins.property
    def spec(self) -> "WorkflowEventBindingSpec":
        result = self._values.get("spec")
        assert result is not None, "Required property 'spec' is missing"
        return typing.cast("WorkflowEventBindingSpec", result)

    @builtins.property
    def api_version(self) -> typing.Optional[builtins.str]:
        result = self._values.get("api_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kind(self) -> typing.Optional[builtins.str]:
        result = self._values.get("kind")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowEventBinding(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.WorkflowEventBindingList",
    jsii_struct_bases=[],
    name_mapping={
        "items": "items",
        "metadata": "metadata",
        "api_version": "apiVersion",
        "kind": "kind",
    },
)
class WorkflowEventBindingList:
    def __init__(
        self,
        *,
        items: typing.Sequence[WorkflowEventBinding],
        metadata: _ListMeta_fcb8bed2,
        api_version: typing.Optional[builtins.str] = None,
        kind: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param items: 
        :param metadata: 
        :param api_version: 
        :param kind: 
        '''
        if isinstance(metadata, dict):
            metadata = _ListMeta_fcb8bed2(**metadata)
        self._values: typing.Dict[str, typing.Any] = {
            "items": items,
            "metadata": metadata,
        }
        if api_version is not None:
            self._values["api_version"] = api_version
        if kind is not None:
            self._values["kind"] = kind

    @builtins.property
    def items(self) -> typing.List[WorkflowEventBinding]:
        result = self._values.get("items")
        assert result is not None, "Required property 'items' is missing"
        return typing.cast(typing.List[WorkflowEventBinding], result)

    @builtins.property
    def metadata(self) -> _ListMeta_fcb8bed2:
        result = self._values.get("metadata")
        assert result is not None, "Required property 'metadata' is missing"
        return typing.cast(_ListMeta_fcb8bed2, result)

    @builtins.property
    def api_version(self) -> typing.Optional[builtins.str]:
        result = self._values.get("api_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kind(self) -> typing.Optional[builtins.str]:
        result = self._values.get("kind")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowEventBindingList(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.WorkflowEventBindingSpec",
    jsii_struct_bases=[],
    name_mapping={"event": "event", "submit": "submit"},
)
class WorkflowEventBindingSpec:
    def __init__(self, *, event: Event, submit: typing.Optional[Submit] = None) -> None:
        '''
        :param event: 
        :param submit: 
        '''
        if isinstance(event, dict):
            event = Event(**event)
        if isinstance(submit, dict):
            submit = Submit(**submit)
        self._values: typing.Dict[str, typing.Any] = {
            "event": event,
        }
        if submit is not None:
            self._values["submit"] = submit

    @builtins.property
    def event(self) -> Event:
        result = self._values.get("event")
        assert result is not None, "Required property 'event' is missing"
        return typing.cast(Event, result)

    @builtins.property
    def submit(self) -> typing.Optional[Submit]:
        result = self._values.get("submit")
        return typing.cast(typing.Optional[Submit], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowEventBindingSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.WorkflowLintRequest",
    jsii_struct_bases=[],
    name_mapping={"namespace": "namespace", "workflow": "workflow"},
)
class WorkflowLintRequest:
    def __init__(
        self,
        *,
        namespace: typing.Optional[builtins.str] = None,
        workflow: typing.Optional[Workflow] = None,
    ) -> None:
        '''
        :param namespace: 
        :param workflow: 
        '''
        if isinstance(workflow, dict):
            workflow = Workflow(**workflow)
        self._values: typing.Dict[str, typing.Any] = {}
        if namespace is not None:
            self._values["namespace"] = namespace
        if workflow is not None:
            self._values["workflow"] = workflow

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workflow(self) -> typing.Optional[Workflow]:
        result = self._values.get("workflow")
        return typing.cast(typing.Optional[Workflow], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowLintRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.WorkflowList",
    jsii_struct_bases=[],
    name_mapping={
        "items": "items",
        "metadata": "metadata",
        "api_version": "apiVersion",
        "kind": "kind",
    },
)
class WorkflowList:
    def __init__(
        self,
        *,
        items: typing.Sequence[Workflow],
        metadata: _ListMeta_fcb8bed2,
        api_version: typing.Optional[builtins.str] = None,
        kind: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param items: 
        :param metadata: 
        :param api_version: 
        :param kind: 
        '''
        if isinstance(metadata, dict):
            metadata = _ListMeta_fcb8bed2(**metadata)
        self._values: typing.Dict[str, typing.Any] = {
            "items": items,
            "metadata": metadata,
        }
        if api_version is not None:
            self._values["api_version"] = api_version
        if kind is not None:
            self._values["kind"] = kind

    @builtins.property
    def items(self) -> typing.List[Workflow]:
        result = self._values.get("items")
        assert result is not None, "Required property 'items' is missing"
        return typing.cast(typing.List[Workflow], result)

    @builtins.property
    def metadata(self) -> _ListMeta_fcb8bed2:
        result = self._values.get("metadata")
        assert result is not None, "Required property 'metadata' is missing"
        return typing.cast(_ListMeta_fcb8bed2, result)

    @builtins.property
    def api_version(self) -> typing.Optional[builtins.str]:
        result = self._values.get("api_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kind(self) -> typing.Optional[builtins.str]:
        result = self._values.get("kind")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowList(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.WorkflowResubmitRequest",
    jsii_struct_bases=[],
    name_mapping={"memoized": "memoized", "name": "name", "namespace": "namespace"},
)
class WorkflowResubmitRequest:
    def __init__(
        self,
        *,
        memoized: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param memoized: 
        :param name: 
        :param namespace: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if memoized is not None:
            self._values["memoized"] = memoized
        if name is not None:
            self._values["name"] = name
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def memoized(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("memoized")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowResubmitRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.WorkflowResumeRequest",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "namespace": "namespace",
        "node_field_selector": "nodeFieldSelector",
    },
)
class WorkflowResumeRequest:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        node_field_selector: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: 
        :param namespace: 
        :param node_field_selector: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if namespace is not None:
            self._values["namespace"] = namespace
        if node_field_selector is not None:
            self._values["node_field_selector"] = node_field_selector

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_field_selector(self) -> typing.Optional[builtins.str]:
        result = self._values.get("node_field_selector")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowResumeRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.WorkflowRetryRequest",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "namespace": "namespace",
        "node_field_selector": "nodeFieldSelector",
        "restart_successful": "restartSuccessful",
    },
)
class WorkflowRetryRequest:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        node_field_selector: typing.Optional[builtins.str] = None,
        restart_successful: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param name: 
        :param namespace: 
        :param node_field_selector: 
        :param restart_successful: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if namespace is not None:
            self._values["namespace"] = namespace
        if node_field_selector is not None:
            self._values["node_field_selector"] = node_field_selector
        if restart_successful is not None:
            self._values["restart_successful"] = restart_successful

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_field_selector(self) -> typing.Optional[builtins.str]:
        result = self._values.get("node_field_selector")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def restart_successful(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("restart_successful")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowRetryRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.WorkflowSetRequest",
    jsii_struct_bases=[],
    name_mapping={
        "message": "message",
        "name": "name",
        "namespace": "namespace",
        "node_field_selector": "nodeFieldSelector",
        "output_parameters": "outputParameters",
        "phase": "phase",
    },
)
class WorkflowSetRequest:
    def __init__(
        self,
        *,
        message: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        node_field_selector: typing.Optional[builtins.str] = None,
        output_parameters: typing.Optional[builtins.str] = None,
        phase: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param message: 
        :param name: 
        :param namespace: 
        :param node_field_selector: 
        :param output_parameters: 
        :param phase: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if message is not None:
            self._values["message"] = message
        if name is not None:
            self._values["name"] = name
        if namespace is not None:
            self._values["namespace"] = namespace
        if node_field_selector is not None:
            self._values["node_field_selector"] = node_field_selector
        if output_parameters is not None:
            self._values["output_parameters"] = output_parameters
        if phase is not None:
            self._values["phase"] = phase

    @builtins.property
    def message(self) -> typing.Optional[builtins.str]:
        result = self._values.get("message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_field_selector(self) -> typing.Optional[builtins.str]:
        result = self._values.get("node_field_selector")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_parameters(self) -> typing.Optional[builtins.str]:
        result = self._values.get("output_parameters")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def phase(self) -> typing.Optional[builtins.str]:
        result = self._values.get("phase")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowSetRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.WorkflowSpec",
    jsii_struct_bases=[],
    name_mapping={
        "active_deadline_seconds": "activeDeadlineSeconds",
        "affinity": "affinity",
        "arguments": "arguments",
        "artifact_repository_ref": "artifactRepositoryRef",
        "automount_service_account_token": "automountServiceAccountToken",
        "dns_config": "dnsConfig",
        "dns_policy": "dnsPolicy",
        "entrypoint": "entrypoint",
        "executor": "executor",
        "host_aliases": "hostAliases",
        "host_network": "hostNetwork",
        "image_pull_secrets": "imagePullSecrets",
        "metrics": "metrics",
        "node_selector": "nodeSelector",
        "on_exit": "onExit",
        "parallelism": "parallelism",
        "pod_disruption_budget": "podDisruptionBudget",
        "pod_gc": "podGC",
        "pod_metadata": "podMetadata",
        "pod_priority": "podPriority",
        "pod_priority_class_name": "podPriorityClassName",
        "pod_spec_patch": "podSpecPatch",
        "priority": "priority",
        "retry_strategy": "retryStrategy",
        "scheduler_name": "schedulerName",
        "security_context": "securityContext",
        "service_account_name": "serviceAccountName",
        "shutdown": "shutdown",
        "suspend": "suspend",
        "synchronization": "synchronization",
        "template_defaults": "templateDefaults",
        "templates": "templates",
        "tolerations": "tolerations",
        "ttl_strategy": "ttlStrategy",
        "volume_claim_gc": "volumeClaimGC",
        "volume_claim_templates": "volumeClaimTemplates",
        "volumes": "volumes",
        "workflow_template_ref": "workflowTemplateRef",
    },
)
class WorkflowSpec:
    def __init__(
        self,
        *,
        active_deadline_seconds: typing.Optional[jsii.Number] = None,
        affinity: typing.Optional[_Affinity_a7d59e98] = None,
        arguments: typing.Optional[Arguments] = None,
        artifact_repository_ref: typing.Optional[ArtifactRepositoryRef] = None,
        automount_service_account_token: typing.Optional[builtins.bool] = None,
        dns_config: typing.Optional[_PodDnsConfig_4c2fa008] = None,
        dns_policy: typing.Optional[builtins.str] = None,
        entrypoint: typing.Optional[builtins.str] = None,
        executor: typing.Optional[ExecutorConfig] = None,
        host_aliases: typing.Optional[typing.Sequence[_HostAlias_82563da2]] = None,
        host_network: typing.Optional[builtins.bool] = None,
        image_pull_secrets: typing.Optional[typing.Sequence[_LocalObjectReference_cdc737d6]] = None,
        metrics: typing.Optional[Metrics] = None,
        node_selector: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        on_exit: typing.Optional[builtins.str] = None,
        parallelism: typing.Optional[jsii.Number] = None,
        pod_disruption_budget: typing.Optional[_PodDisruptionBudgetSpec_8bcdde1e] = None,
        pod_gc: typing.Optional[PodGC] = None,
        pod_metadata: typing.Optional[Metadata] = None,
        pod_priority: typing.Optional[jsii.Number] = None,
        pod_priority_class_name: typing.Optional[builtins.str] = None,
        pod_spec_patch: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        retry_strategy: typing.Optional[RetryStrategy] = None,
        scheduler_name: typing.Optional[builtins.str] = None,
        security_context: typing.Optional[_PodSecurityContext_c3a517d7] = None,
        service_account_name: typing.Optional[builtins.str] = None,
        shutdown: typing.Optional[builtins.str] = None,
        suspend: typing.Optional[builtins.bool] = None,
        synchronization: typing.Optional[Synchronization] = None,
        template_defaults: typing.Optional[Template] = None,
        templates: typing.Optional[typing.Sequence[Template]] = None,
        tolerations: typing.Optional[typing.Sequence[_Toleration_aec52105]] = None,
        ttl_strategy: typing.Optional[TTLStrategy] = None,
        volume_claim_gc: typing.Optional[VolumeClaimGC] = None,
        volume_claim_templates: typing.Optional[typing.Sequence[_KubePersistentVolumeClaimProps_f5d98fb6]] = None,
        volumes: typing.Optional[typing.Sequence[_Volume_05ce2014]] = None,
        workflow_template_ref: typing.Optional["WorkflowTemplateRef"] = None,
    ) -> None:
        '''
        :param active_deadline_seconds: 
        :param affinity: 
        :param arguments: 
        :param artifact_repository_ref: 
        :param automount_service_account_token: 
        :param dns_config: 
        :param dns_policy: 
        :param entrypoint: 
        :param executor: 
        :param host_aliases: 
        :param host_network: 
        :param image_pull_secrets: 
        :param metrics: 
        :param node_selector: 
        :param on_exit: 
        :param parallelism: 
        :param pod_disruption_budget: 
        :param pod_gc: 
        :param pod_metadata: 
        :param pod_priority: 
        :param pod_priority_class_name: 
        :param pod_spec_patch: 
        :param priority: 
        :param retry_strategy: 
        :param scheduler_name: 
        :param security_context: 
        :param service_account_name: 
        :param shutdown: 
        :param suspend: 
        :param synchronization: 
        :param template_defaults: 
        :param templates: 
        :param tolerations: 
        :param ttl_strategy: 
        :param volume_claim_gc: 
        :param volume_claim_templates: 
        :param volumes: 
        :param workflow_template_ref: 
        '''
        if isinstance(affinity, dict):
            affinity = _Affinity_a7d59e98(**affinity)
        if isinstance(arguments, dict):
            arguments = Arguments(**arguments)
        if isinstance(artifact_repository_ref, dict):
            artifact_repository_ref = ArtifactRepositoryRef(**artifact_repository_ref)
        if isinstance(dns_config, dict):
            dns_config = _PodDnsConfig_4c2fa008(**dns_config)
        if isinstance(executor, dict):
            executor = ExecutorConfig(**executor)
        if isinstance(metrics, dict):
            metrics = Metrics(**metrics)
        if isinstance(pod_disruption_budget, dict):
            pod_disruption_budget = _PodDisruptionBudgetSpec_8bcdde1e(**pod_disruption_budget)
        if isinstance(pod_gc, dict):
            pod_gc = PodGC(**pod_gc)
        if isinstance(pod_metadata, dict):
            pod_metadata = Metadata(**pod_metadata)
        if isinstance(retry_strategy, dict):
            retry_strategy = RetryStrategy(**retry_strategy)
        if isinstance(security_context, dict):
            security_context = _PodSecurityContext_c3a517d7(**security_context)
        if isinstance(synchronization, dict):
            synchronization = Synchronization(**synchronization)
        if isinstance(template_defaults, dict):
            template_defaults = Template(**template_defaults)
        if isinstance(ttl_strategy, dict):
            ttl_strategy = TTLStrategy(**ttl_strategy)
        if isinstance(volume_claim_gc, dict):
            volume_claim_gc = VolumeClaimGC(**volume_claim_gc)
        if isinstance(workflow_template_ref, dict):
            workflow_template_ref = WorkflowTemplateRef(**workflow_template_ref)
        self._values: typing.Dict[str, typing.Any] = {}
        if active_deadline_seconds is not None:
            self._values["active_deadline_seconds"] = active_deadline_seconds
        if affinity is not None:
            self._values["affinity"] = affinity
        if arguments is not None:
            self._values["arguments"] = arguments
        if artifact_repository_ref is not None:
            self._values["artifact_repository_ref"] = artifact_repository_ref
        if automount_service_account_token is not None:
            self._values["automount_service_account_token"] = automount_service_account_token
        if dns_config is not None:
            self._values["dns_config"] = dns_config
        if dns_policy is not None:
            self._values["dns_policy"] = dns_policy
        if entrypoint is not None:
            self._values["entrypoint"] = entrypoint
        if executor is not None:
            self._values["executor"] = executor
        if host_aliases is not None:
            self._values["host_aliases"] = host_aliases
        if host_network is not None:
            self._values["host_network"] = host_network
        if image_pull_secrets is not None:
            self._values["image_pull_secrets"] = image_pull_secrets
        if metrics is not None:
            self._values["metrics"] = metrics
        if node_selector is not None:
            self._values["node_selector"] = node_selector
        if on_exit is not None:
            self._values["on_exit"] = on_exit
        if parallelism is not None:
            self._values["parallelism"] = parallelism
        if pod_disruption_budget is not None:
            self._values["pod_disruption_budget"] = pod_disruption_budget
        if pod_gc is not None:
            self._values["pod_gc"] = pod_gc
        if pod_metadata is not None:
            self._values["pod_metadata"] = pod_metadata
        if pod_priority is not None:
            self._values["pod_priority"] = pod_priority
        if pod_priority_class_name is not None:
            self._values["pod_priority_class_name"] = pod_priority_class_name
        if pod_spec_patch is not None:
            self._values["pod_spec_patch"] = pod_spec_patch
        if priority is not None:
            self._values["priority"] = priority
        if retry_strategy is not None:
            self._values["retry_strategy"] = retry_strategy
        if scheduler_name is not None:
            self._values["scheduler_name"] = scheduler_name
        if security_context is not None:
            self._values["security_context"] = security_context
        if service_account_name is not None:
            self._values["service_account_name"] = service_account_name
        if shutdown is not None:
            self._values["shutdown"] = shutdown
        if suspend is not None:
            self._values["suspend"] = suspend
        if synchronization is not None:
            self._values["synchronization"] = synchronization
        if template_defaults is not None:
            self._values["template_defaults"] = template_defaults
        if templates is not None:
            self._values["templates"] = templates
        if tolerations is not None:
            self._values["tolerations"] = tolerations
        if ttl_strategy is not None:
            self._values["ttl_strategy"] = ttl_strategy
        if volume_claim_gc is not None:
            self._values["volume_claim_gc"] = volume_claim_gc
        if volume_claim_templates is not None:
            self._values["volume_claim_templates"] = volume_claim_templates
        if volumes is not None:
            self._values["volumes"] = volumes
        if workflow_template_ref is not None:
            self._values["workflow_template_ref"] = workflow_template_ref

    @builtins.property
    def active_deadline_seconds(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("active_deadline_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def affinity(self) -> typing.Optional[_Affinity_a7d59e98]:
        result = self._values.get("affinity")
        return typing.cast(typing.Optional[_Affinity_a7d59e98], result)

    @builtins.property
    def arguments(self) -> typing.Optional[Arguments]:
        result = self._values.get("arguments")
        return typing.cast(typing.Optional[Arguments], result)

    @builtins.property
    def artifact_repository_ref(self) -> typing.Optional[ArtifactRepositoryRef]:
        result = self._values.get("artifact_repository_ref")
        return typing.cast(typing.Optional[ArtifactRepositoryRef], result)

    @builtins.property
    def automount_service_account_token(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("automount_service_account_token")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def dns_config(self) -> typing.Optional[_PodDnsConfig_4c2fa008]:
        result = self._values.get("dns_config")
        return typing.cast(typing.Optional[_PodDnsConfig_4c2fa008], result)

    @builtins.property
    def dns_policy(self) -> typing.Optional[builtins.str]:
        result = self._values.get("dns_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def entrypoint(self) -> typing.Optional[builtins.str]:
        result = self._values.get("entrypoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def executor(self) -> typing.Optional[ExecutorConfig]:
        result = self._values.get("executor")
        return typing.cast(typing.Optional[ExecutorConfig], result)

    @builtins.property
    def host_aliases(self) -> typing.Optional[typing.List[_HostAlias_82563da2]]:
        result = self._values.get("host_aliases")
        return typing.cast(typing.Optional[typing.List[_HostAlias_82563da2]], result)

    @builtins.property
    def host_network(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("host_network")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def image_pull_secrets(
        self,
    ) -> typing.Optional[typing.List[_LocalObjectReference_cdc737d6]]:
        result = self._values.get("image_pull_secrets")
        return typing.cast(typing.Optional[typing.List[_LocalObjectReference_cdc737d6]], result)

    @builtins.property
    def metrics(self) -> typing.Optional[Metrics]:
        result = self._values.get("metrics")
        return typing.cast(typing.Optional[Metrics], result)

    @builtins.property
    def node_selector(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("node_selector")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def on_exit(self) -> typing.Optional[builtins.str]:
        result = self._values.get("on_exit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parallelism(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("parallelism")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def pod_disruption_budget(
        self,
    ) -> typing.Optional[_PodDisruptionBudgetSpec_8bcdde1e]:
        result = self._values.get("pod_disruption_budget")
        return typing.cast(typing.Optional[_PodDisruptionBudgetSpec_8bcdde1e], result)

    @builtins.property
    def pod_gc(self) -> typing.Optional[PodGC]:
        result = self._values.get("pod_gc")
        return typing.cast(typing.Optional[PodGC], result)

    @builtins.property
    def pod_metadata(self) -> typing.Optional[Metadata]:
        result = self._values.get("pod_metadata")
        return typing.cast(typing.Optional[Metadata], result)

    @builtins.property
    def pod_priority(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("pod_priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def pod_priority_class_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("pod_priority_class_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pod_spec_patch(self) -> typing.Optional[builtins.str]:
        result = self._values.get("pod_spec_patch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retry_strategy(self) -> typing.Optional[RetryStrategy]:
        result = self._values.get("retry_strategy")
        return typing.cast(typing.Optional[RetryStrategy], result)

    @builtins.property
    def scheduler_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("scheduler_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_context(self) -> typing.Optional[_PodSecurityContext_c3a517d7]:
        result = self._values.get("security_context")
        return typing.cast(typing.Optional[_PodSecurityContext_c3a517d7], result)

    @builtins.property
    def service_account_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("service_account_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shutdown(self) -> typing.Optional[builtins.str]:
        result = self._values.get("shutdown")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suspend(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("suspend")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def synchronization(self) -> typing.Optional[Synchronization]:
        result = self._values.get("synchronization")
        return typing.cast(typing.Optional[Synchronization], result)

    @builtins.property
    def template_defaults(self) -> typing.Optional[Template]:
        result = self._values.get("template_defaults")
        return typing.cast(typing.Optional[Template], result)

    @builtins.property
    def templates(self) -> typing.Optional[typing.List[Template]]:
        result = self._values.get("templates")
        return typing.cast(typing.Optional[typing.List[Template]], result)

    @builtins.property
    def tolerations(self) -> typing.Optional[typing.List[_Toleration_aec52105]]:
        result = self._values.get("tolerations")
        return typing.cast(typing.Optional[typing.List[_Toleration_aec52105]], result)

    @builtins.property
    def ttl_strategy(self) -> typing.Optional[TTLStrategy]:
        result = self._values.get("ttl_strategy")
        return typing.cast(typing.Optional[TTLStrategy], result)

    @builtins.property
    def volume_claim_gc(self) -> typing.Optional[VolumeClaimGC]:
        result = self._values.get("volume_claim_gc")
        return typing.cast(typing.Optional[VolumeClaimGC], result)

    @builtins.property
    def volume_claim_templates(
        self,
    ) -> typing.Optional[typing.List[_KubePersistentVolumeClaimProps_f5d98fb6]]:
        result = self._values.get("volume_claim_templates")
        return typing.cast(typing.Optional[typing.List[_KubePersistentVolumeClaimProps_f5d98fb6]], result)

    @builtins.property
    def volumes(self) -> typing.Optional[typing.List[_Volume_05ce2014]]:
        result = self._values.get("volumes")
        return typing.cast(typing.Optional[typing.List[_Volume_05ce2014]], result)

    @builtins.property
    def workflow_template_ref(self) -> typing.Optional["WorkflowTemplateRef"]:
        result = self._values.get("workflow_template_ref")
        return typing.cast(typing.Optional["WorkflowTemplateRef"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.WorkflowStatus",
    jsii_struct_bases=[],
    name_mapping={
        "artifact_repository_ref": "artifactRepositoryRef",
        "compressed_nodes": "compressedNodes",
        "conditions": "conditions",
        "estimated_duration": "estimatedDuration",
        "finished_at": "finishedAt",
        "message": "message",
        "nodes": "nodes",
        "offload_node_status_version": "offloadNodeStatusVersion",
        "outputs": "outputs",
        "persistent_volume_claim_specs": "persistentVolumeClaimSpecs",
        "phase": "phase",
        "progress": "progress",
        "resources_duration": "resourcesDuration",
        "started_at": "startedAt",
        "stored_templates": "storedTemplates",
        "stored_workflow_template_spec": "storedWorkflowTemplateSpec",
        "synchronization": "synchronization",
    },
)
class WorkflowStatus:
    def __init__(
        self,
        *,
        artifact_repository_ref: typing.Optional[ArtifactRepositoryRefStatus] = None,
        compressed_nodes: typing.Optional[builtins.str] = None,
        conditions: typing.Optional[typing.Sequence[Condition]] = None,
        estimated_duration: typing.Optional[jsii.Number] = None,
        finished_at: typing.Optional[datetime.datetime] = None,
        message: typing.Optional[builtins.str] = None,
        nodes: typing.Optional[typing.Mapping[builtins.str, NodeStatus]] = None,
        offload_node_status_version: typing.Optional[builtins.str] = None,
        outputs: typing.Optional[Outputs] = None,
        persistent_volume_claim_specs: typing.Optional[typing.Sequence[_Volume_05ce2014]] = None,
        phase: typing.Optional[builtins.str] = None,
        progress: typing.Optional[builtins.str] = None,
        resources_duration: typing.Optional[typing.Mapping[builtins.str, jsii.Number]] = None,
        started_at: typing.Optional[datetime.datetime] = None,
        stored_templates: typing.Optional[typing.Mapping[builtins.str, Template]] = None,
        stored_workflow_template_spec: typing.Optional[WorkflowSpec] = None,
        synchronization: typing.Optional[SynchronizationStatus] = None,
    ) -> None:
        '''
        :param artifact_repository_ref: 
        :param compressed_nodes: 
        :param conditions: 
        :param estimated_duration: 
        :param finished_at: 
        :param message: 
        :param nodes: 
        :param offload_node_status_version: 
        :param outputs: 
        :param persistent_volume_claim_specs: 
        :param phase: 
        :param progress: 
        :param resources_duration: 
        :param started_at: 
        :param stored_templates: 
        :param stored_workflow_template_spec: 
        :param synchronization: 
        '''
        if isinstance(artifact_repository_ref, dict):
            artifact_repository_ref = ArtifactRepositoryRefStatus(**artifact_repository_ref)
        if isinstance(outputs, dict):
            outputs = Outputs(**outputs)
        if isinstance(stored_workflow_template_spec, dict):
            stored_workflow_template_spec = WorkflowSpec(**stored_workflow_template_spec)
        if isinstance(synchronization, dict):
            synchronization = SynchronizationStatus(**synchronization)
        self._values: typing.Dict[str, typing.Any] = {}
        if artifact_repository_ref is not None:
            self._values["artifact_repository_ref"] = artifact_repository_ref
        if compressed_nodes is not None:
            self._values["compressed_nodes"] = compressed_nodes
        if conditions is not None:
            self._values["conditions"] = conditions
        if estimated_duration is not None:
            self._values["estimated_duration"] = estimated_duration
        if finished_at is not None:
            self._values["finished_at"] = finished_at
        if message is not None:
            self._values["message"] = message
        if nodes is not None:
            self._values["nodes"] = nodes
        if offload_node_status_version is not None:
            self._values["offload_node_status_version"] = offload_node_status_version
        if outputs is not None:
            self._values["outputs"] = outputs
        if persistent_volume_claim_specs is not None:
            self._values["persistent_volume_claim_specs"] = persistent_volume_claim_specs
        if phase is not None:
            self._values["phase"] = phase
        if progress is not None:
            self._values["progress"] = progress
        if resources_duration is not None:
            self._values["resources_duration"] = resources_duration
        if started_at is not None:
            self._values["started_at"] = started_at
        if stored_templates is not None:
            self._values["stored_templates"] = stored_templates
        if stored_workflow_template_spec is not None:
            self._values["stored_workflow_template_spec"] = stored_workflow_template_spec
        if synchronization is not None:
            self._values["synchronization"] = synchronization

    @builtins.property
    def artifact_repository_ref(self) -> typing.Optional[ArtifactRepositoryRefStatus]:
        result = self._values.get("artifact_repository_ref")
        return typing.cast(typing.Optional[ArtifactRepositoryRefStatus], result)

    @builtins.property
    def compressed_nodes(self) -> typing.Optional[builtins.str]:
        result = self._values.get("compressed_nodes")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def conditions(self) -> typing.Optional[typing.List[Condition]]:
        result = self._values.get("conditions")
        return typing.cast(typing.Optional[typing.List[Condition]], result)

    @builtins.property
    def estimated_duration(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("estimated_duration")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def finished_at(self) -> typing.Optional[datetime.datetime]:
        result = self._values.get("finished_at")
        return typing.cast(typing.Optional[datetime.datetime], result)

    @builtins.property
    def message(self) -> typing.Optional[builtins.str]:
        result = self._values.get("message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nodes(self) -> typing.Optional[typing.Mapping[builtins.str, NodeStatus]]:
        result = self._values.get("nodes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, NodeStatus]], result)

    @builtins.property
    def offload_node_status_version(self) -> typing.Optional[builtins.str]:
        result = self._values.get("offload_node_status_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def outputs(self) -> typing.Optional[Outputs]:
        result = self._values.get("outputs")
        return typing.cast(typing.Optional[Outputs], result)

    @builtins.property
    def persistent_volume_claim_specs(
        self,
    ) -> typing.Optional[typing.List[_Volume_05ce2014]]:
        result = self._values.get("persistent_volume_claim_specs")
        return typing.cast(typing.Optional[typing.List[_Volume_05ce2014]], result)

    @builtins.property
    def phase(self) -> typing.Optional[builtins.str]:
        result = self._values.get("phase")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def progress(self) -> typing.Optional[builtins.str]:
        result = self._values.get("progress")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resources_duration(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, jsii.Number]]:
        result = self._values.get("resources_duration")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, jsii.Number]], result)

    @builtins.property
    def started_at(self) -> typing.Optional[datetime.datetime]:
        result = self._values.get("started_at")
        return typing.cast(typing.Optional[datetime.datetime], result)

    @builtins.property
    def stored_templates(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, Template]]:
        result = self._values.get("stored_templates")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, Template]], result)

    @builtins.property
    def stored_workflow_template_spec(self) -> typing.Optional[WorkflowSpec]:
        result = self._values.get("stored_workflow_template_spec")
        return typing.cast(typing.Optional[WorkflowSpec], result)

    @builtins.property
    def synchronization(self) -> typing.Optional[SynchronizationStatus]:
        result = self._values.get("synchronization")
        return typing.cast(typing.Optional[SynchronizationStatus], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.WorkflowStep",
    jsii_struct_bases=[],
    name_mapping={
        "arguments": "arguments",
        "continue_on": "continueOn",
        "name": "name",
        "on_exit": "onExit",
        "template": "template",
        "template_ref": "templateRef",
        "when": "when",
        "with_items": "withItems",
        "with_param": "withParam",
        "with_sequence": "withSequence",
    },
)
class WorkflowStep:
    def __init__(
        self,
        *,
        arguments: typing.Optional[Arguments] = None,
        continue_on: typing.Optional[ContinueOn] = None,
        name: typing.Optional[builtins.str] = None,
        on_exit: typing.Optional[builtins.str] = None,
        template: typing.Optional[builtins.str] = None,
        template_ref: typing.Optional[TemplateRef] = None,
        when: typing.Optional[builtins.str] = None,
        with_items: typing.Optional[typing.Sequence[typing.Any]] = None,
        with_param: typing.Optional[builtins.str] = None,
        with_sequence: typing.Optional[Sequence] = None,
    ) -> None:
        '''
        :param arguments: 
        :param continue_on: 
        :param name: 
        :param on_exit: 
        :param template: 
        :param template_ref: 
        :param when: 
        :param with_items: 
        :param with_param: 
        :param with_sequence: 
        '''
        if isinstance(arguments, dict):
            arguments = Arguments(**arguments)
        if isinstance(continue_on, dict):
            continue_on = ContinueOn(**continue_on)
        if isinstance(template_ref, dict):
            template_ref = TemplateRef(**template_ref)
        if isinstance(with_sequence, dict):
            with_sequence = Sequence(**with_sequence)
        self._values: typing.Dict[str, typing.Any] = {}
        if arguments is not None:
            self._values["arguments"] = arguments
        if continue_on is not None:
            self._values["continue_on"] = continue_on
        if name is not None:
            self._values["name"] = name
        if on_exit is not None:
            self._values["on_exit"] = on_exit
        if template is not None:
            self._values["template"] = template
        if template_ref is not None:
            self._values["template_ref"] = template_ref
        if when is not None:
            self._values["when"] = when
        if with_items is not None:
            self._values["with_items"] = with_items
        if with_param is not None:
            self._values["with_param"] = with_param
        if with_sequence is not None:
            self._values["with_sequence"] = with_sequence

    @builtins.property
    def arguments(self) -> typing.Optional[Arguments]:
        result = self._values.get("arguments")
        return typing.cast(typing.Optional[Arguments], result)

    @builtins.property
    def continue_on(self) -> typing.Optional[ContinueOn]:
        result = self._values.get("continue_on")
        return typing.cast(typing.Optional[ContinueOn], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def on_exit(self) -> typing.Optional[builtins.str]:
        result = self._values.get("on_exit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template(self) -> typing.Optional[builtins.str]:
        result = self._values.get("template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template_ref(self) -> typing.Optional[TemplateRef]:
        result = self._values.get("template_ref")
        return typing.cast(typing.Optional[TemplateRef], result)

    @builtins.property
    def when(self) -> typing.Optional[builtins.str]:
        result = self._values.get("when")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def with_items(self) -> typing.Optional[typing.List[typing.Any]]:
        result = self._values.get("with_items")
        return typing.cast(typing.Optional[typing.List[typing.Any]], result)

    @builtins.property
    def with_param(self) -> typing.Optional[builtins.str]:
        result = self._values.get("with_param")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def with_sequence(self) -> typing.Optional[Sequence]:
        result = self._values.get("with_sequence")
        return typing.cast(typing.Optional[Sequence], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowStep(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.WorkflowStopRequest",
    jsii_struct_bases=[],
    name_mapping={
        "message": "message",
        "name": "name",
        "namespace": "namespace",
        "node_field_selector": "nodeFieldSelector",
    },
)
class WorkflowStopRequest:
    def __init__(
        self,
        *,
        message: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        node_field_selector: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param message: 
        :param name: 
        :param namespace: 
        :param node_field_selector: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if message is not None:
            self._values["message"] = message
        if name is not None:
            self._values["name"] = name
        if namespace is not None:
            self._values["namespace"] = namespace
        if node_field_selector is not None:
            self._values["node_field_selector"] = node_field_selector

    @builtins.property
    def message(self) -> typing.Optional[builtins.str]:
        result = self._values.get("message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_field_selector(self) -> typing.Optional[builtins.str]:
        result = self._values.get("node_field_selector")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowStopRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.WorkflowSubmitRequest",
    jsii_struct_bases=[],
    name_mapping={
        "namespace": "namespace",
        "resource_kind": "resourceKind",
        "resource_name": "resourceName",
        "submit_options": "submitOptions",
    },
)
class WorkflowSubmitRequest:
    def __init__(
        self,
        *,
        namespace: typing.Optional[builtins.str] = None,
        resource_kind: typing.Optional[builtins.str] = None,
        resource_name: typing.Optional[builtins.str] = None,
        submit_options: typing.Optional[SubmitOpts] = None,
    ) -> None:
        '''
        :param namespace: 
        :param resource_kind: 
        :param resource_name: 
        :param submit_options: 
        '''
        if isinstance(submit_options, dict):
            submit_options = SubmitOpts(**submit_options)
        self._values: typing.Dict[str, typing.Any] = {}
        if namespace is not None:
            self._values["namespace"] = namespace
        if resource_kind is not None:
            self._values["resource_kind"] = resource_kind
        if resource_name is not None:
            self._values["resource_name"] = resource_name
        if submit_options is not None:
            self._values["submit_options"] = submit_options

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_kind(self) -> typing.Optional[builtins.str]:
        result = self._values.get("resource_kind")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("resource_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def submit_options(self) -> typing.Optional[SubmitOpts]:
        result = self._values.get("submit_options")
        return typing.cast(typing.Optional[SubmitOpts], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowSubmitRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.WorkflowSuspendRequest",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "namespace": "namespace"},
)
class WorkflowSuspendRequest:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: 
        :param namespace: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowSuspendRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.WorkflowTemplate",
    jsii_struct_bases=[],
    name_mapping={
        "metadata": "metadata",
        "spec": "spec",
        "api_version": "apiVersion",
        "kind": "kind",
    },
)
class WorkflowTemplate:
    def __init__(
        self,
        *,
        metadata: _ObjectMeta_77a65d46,
        spec: "WorkflowTemplateSpec",
        api_version: typing.Optional[builtins.str] = None,
        kind: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param metadata: 
        :param spec: 
        :param api_version: 
        :param kind: 
        '''
        if isinstance(metadata, dict):
            metadata = _ObjectMeta_77a65d46(**metadata)
        if isinstance(spec, dict):
            spec = WorkflowTemplateSpec(**spec)
        self._values: typing.Dict[str, typing.Any] = {
            "metadata": metadata,
            "spec": spec,
        }
        if api_version is not None:
            self._values["api_version"] = api_version
        if kind is not None:
            self._values["kind"] = kind

    @builtins.property
    def metadata(self) -> _ObjectMeta_77a65d46:
        result = self._values.get("metadata")
        assert result is not None, "Required property 'metadata' is missing"
        return typing.cast(_ObjectMeta_77a65d46, result)

    @builtins.property
    def spec(self) -> "WorkflowTemplateSpec":
        result = self._values.get("spec")
        assert result is not None, "Required property 'spec' is missing"
        return typing.cast("WorkflowTemplateSpec", result)

    @builtins.property
    def api_version(self) -> typing.Optional[builtins.str]:
        result = self._values.get("api_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kind(self) -> typing.Optional[builtins.str]:
        result = self._values.get("kind")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowTemplate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.WorkflowTemplateCreateRequest",
    jsii_struct_bases=[],
    name_mapping={
        "create_options": "createOptions",
        "namespace": "namespace",
        "template": "template",
    },
)
class WorkflowTemplateCreateRequest:
    def __init__(
        self,
        *,
        create_options: typing.Optional[_CreateOptions_33e095be] = None,
        namespace: typing.Optional[builtins.str] = None,
        template: typing.Optional[WorkflowTemplate] = None,
    ) -> None:
        '''
        :param create_options: 
        :param namespace: 
        :param template: 
        '''
        if isinstance(create_options, dict):
            create_options = _CreateOptions_33e095be(**create_options)
        if isinstance(template, dict):
            template = WorkflowTemplate(**template)
        self._values: typing.Dict[str, typing.Any] = {}
        if create_options is not None:
            self._values["create_options"] = create_options
        if namespace is not None:
            self._values["namespace"] = namespace
        if template is not None:
            self._values["template"] = template

    @builtins.property
    def create_options(self) -> typing.Optional[_CreateOptions_33e095be]:
        result = self._values.get("create_options")
        return typing.cast(typing.Optional[_CreateOptions_33e095be], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template(self) -> typing.Optional[WorkflowTemplate]:
        result = self._values.get("template")
        return typing.cast(typing.Optional[WorkflowTemplate], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowTemplateCreateRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.WorkflowTemplateDeleteResponse",
    jsii_struct_bases=[],
    name_mapping={},
)
class WorkflowTemplateDeleteResponse:
    def __init__(self) -> None:
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowTemplateDeleteResponse(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.WorkflowTemplateLintRequest",
    jsii_struct_bases=[],
    name_mapping={
        "create_options": "createOptions",
        "namespace": "namespace",
        "template": "template",
    },
)
class WorkflowTemplateLintRequest:
    def __init__(
        self,
        *,
        create_options: typing.Optional[_CreateOptions_33e095be] = None,
        namespace: typing.Optional[builtins.str] = None,
        template: typing.Optional[WorkflowTemplate] = None,
    ) -> None:
        '''
        :param create_options: 
        :param namespace: 
        :param template: 
        '''
        if isinstance(create_options, dict):
            create_options = _CreateOptions_33e095be(**create_options)
        if isinstance(template, dict):
            template = WorkflowTemplate(**template)
        self._values: typing.Dict[str, typing.Any] = {}
        if create_options is not None:
            self._values["create_options"] = create_options
        if namespace is not None:
            self._values["namespace"] = namespace
        if template is not None:
            self._values["template"] = template

    @builtins.property
    def create_options(self) -> typing.Optional[_CreateOptions_33e095be]:
        result = self._values.get("create_options")
        return typing.cast(typing.Optional[_CreateOptions_33e095be], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template(self) -> typing.Optional[WorkflowTemplate]:
        result = self._values.get("template")
        return typing.cast(typing.Optional[WorkflowTemplate], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowTemplateLintRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.WorkflowTemplateList",
    jsii_struct_bases=[],
    name_mapping={
        "items": "items",
        "metadata": "metadata",
        "api_version": "apiVersion",
        "kind": "kind",
    },
)
class WorkflowTemplateList:
    def __init__(
        self,
        *,
        items: typing.Sequence[WorkflowTemplate],
        metadata: _ListMeta_fcb8bed2,
        api_version: typing.Optional[builtins.str] = None,
        kind: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param items: 
        :param metadata: 
        :param api_version: 
        :param kind: 
        '''
        if isinstance(metadata, dict):
            metadata = _ListMeta_fcb8bed2(**metadata)
        self._values: typing.Dict[str, typing.Any] = {
            "items": items,
            "metadata": metadata,
        }
        if api_version is not None:
            self._values["api_version"] = api_version
        if kind is not None:
            self._values["kind"] = kind

    @builtins.property
    def items(self) -> typing.List[WorkflowTemplate]:
        result = self._values.get("items")
        assert result is not None, "Required property 'items' is missing"
        return typing.cast(typing.List[WorkflowTemplate], result)

    @builtins.property
    def metadata(self) -> _ListMeta_fcb8bed2:
        result = self._values.get("metadata")
        assert result is not None, "Required property 'metadata' is missing"
        return typing.cast(_ListMeta_fcb8bed2, result)

    @builtins.property
    def api_version(self) -> typing.Optional[builtins.str]:
        result = self._values.get("api_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kind(self) -> typing.Optional[builtins.str]:
        result = self._values.get("kind")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowTemplateList(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.WorkflowTemplateRef",
    jsii_struct_bases=[],
    name_mapping={"cluster_scope": "clusterScope", "name": "name"},
)
class WorkflowTemplateRef:
    def __init__(
        self,
        *,
        cluster_scope: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cluster_scope: 
        :param name: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if cluster_scope is not None:
            self._values["cluster_scope"] = cluster_scope
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def cluster_scope(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("cluster_scope")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowTemplateRef(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.WorkflowTemplateSpec",
    jsii_struct_bases=[],
    name_mapping={
        "active_deadline_seconds": "activeDeadlineSeconds",
        "affinity": "affinity",
        "arguments": "arguments",
        "artifact_repository_ref": "artifactRepositoryRef",
        "automount_service_account_token": "automountServiceAccountToken",
        "dns_config": "dnsConfig",
        "dns_policy": "dnsPolicy",
        "entrypoint": "entrypoint",
        "executor": "executor",
        "host_aliases": "hostAliases",
        "host_network": "hostNetwork",
        "image_pull_secrets": "imagePullSecrets",
        "metrics": "metrics",
        "node_selector": "nodeSelector",
        "on_exit": "onExit",
        "parallelism": "parallelism",
        "pod_disruption_budget": "podDisruptionBudget",
        "pod_gc": "podGC",
        "pod_metadata": "podMetadata",
        "pod_priority": "podPriority",
        "pod_priority_class_name": "podPriorityClassName",
        "pod_spec_patch": "podSpecPatch",
        "priority": "priority",
        "retry_strategy": "retryStrategy",
        "scheduler_name": "schedulerName",
        "security_context": "securityContext",
        "service_account_name": "serviceAccountName",
        "shutdown": "shutdown",
        "suspend": "suspend",
        "synchronization": "synchronization",
        "template_defaults": "templateDefaults",
        "templates": "templates",
        "tolerations": "tolerations",
        "ttl_strategy": "ttlStrategy",
        "volume_claim_gc": "volumeClaimGC",
        "volume_claim_templates": "volumeClaimTemplates",
        "volumes": "volumes",
        "workflow_metadata": "workflowMetadata",
        "workflow_template_ref": "workflowTemplateRef",
    },
)
class WorkflowTemplateSpec:
    def __init__(
        self,
        *,
        active_deadline_seconds: typing.Optional[jsii.Number] = None,
        affinity: typing.Optional[_Affinity_a7d59e98] = None,
        arguments: typing.Optional[Arguments] = None,
        artifact_repository_ref: typing.Optional[ArtifactRepositoryRef] = None,
        automount_service_account_token: typing.Optional[builtins.bool] = None,
        dns_config: typing.Optional[_PodDnsConfig_4c2fa008] = None,
        dns_policy: typing.Optional[builtins.str] = None,
        entrypoint: typing.Optional[builtins.str] = None,
        executor: typing.Optional[ExecutorConfig] = None,
        host_aliases: typing.Optional[typing.Sequence[_HostAlias_82563da2]] = None,
        host_network: typing.Optional[builtins.bool] = None,
        image_pull_secrets: typing.Optional[typing.Sequence[_LocalObjectReference_cdc737d6]] = None,
        metrics: typing.Optional[Metrics] = None,
        node_selector: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        on_exit: typing.Optional[builtins.str] = None,
        parallelism: typing.Optional[jsii.Number] = None,
        pod_disruption_budget: typing.Optional[_PodDisruptionBudgetSpec_8bcdde1e] = None,
        pod_gc: typing.Optional[PodGC] = None,
        pod_metadata: typing.Optional[Metadata] = None,
        pod_priority: typing.Optional[jsii.Number] = None,
        pod_priority_class_name: typing.Optional[builtins.str] = None,
        pod_spec_patch: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        retry_strategy: typing.Optional[RetryStrategy] = None,
        scheduler_name: typing.Optional[builtins.str] = None,
        security_context: typing.Optional[_PodSecurityContext_c3a517d7] = None,
        service_account_name: typing.Optional[builtins.str] = None,
        shutdown: typing.Optional[builtins.str] = None,
        suspend: typing.Optional[builtins.bool] = None,
        synchronization: typing.Optional[Synchronization] = None,
        template_defaults: typing.Optional[Template] = None,
        templates: typing.Optional[typing.Sequence[Template]] = None,
        tolerations: typing.Optional[typing.Sequence[_Toleration_aec52105]] = None,
        ttl_strategy: typing.Optional[TTLStrategy] = None,
        volume_claim_gc: typing.Optional[VolumeClaimGC] = None,
        volume_claim_templates: typing.Optional[typing.Sequence[_PersistentVolumeClaimSpec_fc09a257]] = None,
        volumes: typing.Optional[typing.Sequence[_Volume_05ce2014]] = None,
        workflow_metadata: typing.Optional[_ObjectMeta_77a65d46] = None,
        workflow_template_ref: typing.Optional[WorkflowTemplateRef] = None,
    ) -> None:
        '''
        :param active_deadline_seconds: 
        :param affinity: 
        :param arguments: 
        :param artifact_repository_ref: 
        :param automount_service_account_token: 
        :param dns_config: 
        :param dns_policy: 
        :param entrypoint: 
        :param executor: 
        :param host_aliases: 
        :param host_network: 
        :param image_pull_secrets: 
        :param metrics: 
        :param node_selector: 
        :param on_exit: 
        :param parallelism: 
        :param pod_disruption_budget: 
        :param pod_gc: 
        :param pod_metadata: 
        :param pod_priority: 
        :param pod_priority_class_name: 
        :param pod_spec_patch: 
        :param priority: 
        :param retry_strategy: 
        :param scheduler_name: 
        :param security_context: 
        :param service_account_name: 
        :param shutdown: 
        :param suspend: 
        :param synchronization: 
        :param template_defaults: 
        :param templates: 
        :param tolerations: 
        :param ttl_strategy: 
        :param volume_claim_gc: 
        :param volume_claim_templates: 
        :param volumes: 
        :param workflow_metadata: 
        :param workflow_template_ref: 
        '''
        if isinstance(affinity, dict):
            affinity = _Affinity_a7d59e98(**affinity)
        if isinstance(arguments, dict):
            arguments = Arguments(**arguments)
        if isinstance(artifact_repository_ref, dict):
            artifact_repository_ref = ArtifactRepositoryRef(**artifact_repository_ref)
        if isinstance(dns_config, dict):
            dns_config = _PodDnsConfig_4c2fa008(**dns_config)
        if isinstance(executor, dict):
            executor = ExecutorConfig(**executor)
        if isinstance(metrics, dict):
            metrics = Metrics(**metrics)
        if isinstance(pod_disruption_budget, dict):
            pod_disruption_budget = _PodDisruptionBudgetSpec_8bcdde1e(**pod_disruption_budget)
        if isinstance(pod_gc, dict):
            pod_gc = PodGC(**pod_gc)
        if isinstance(pod_metadata, dict):
            pod_metadata = Metadata(**pod_metadata)
        if isinstance(retry_strategy, dict):
            retry_strategy = RetryStrategy(**retry_strategy)
        if isinstance(security_context, dict):
            security_context = _PodSecurityContext_c3a517d7(**security_context)
        if isinstance(synchronization, dict):
            synchronization = Synchronization(**synchronization)
        if isinstance(template_defaults, dict):
            template_defaults = Template(**template_defaults)
        if isinstance(ttl_strategy, dict):
            ttl_strategy = TTLStrategy(**ttl_strategy)
        if isinstance(volume_claim_gc, dict):
            volume_claim_gc = VolumeClaimGC(**volume_claim_gc)
        if isinstance(workflow_metadata, dict):
            workflow_metadata = _ObjectMeta_77a65d46(**workflow_metadata)
        if isinstance(workflow_template_ref, dict):
            workflow_template_ref = WorkflowTemplateRef(**workflow_template_ref)
        self._values: typing.Dict[str, typing.Any] = {}
        if active_deadline_seconds is not None:
            self._values["active_deadline_seconds"] = active_deadline_seconds
        if affinity is not None:
            self._values["affinity"] = affinity
        if arguments is not None:
            self._values["arguments"] = arguments
        if artifact_repository_ref is not None:
            self._values["artifact_repository_ref"] = artifact_repository_ref
        if automount_service_account_token is not None:
            self._values["automount_service_account_token"] = automount_service_account_token
        if dns_config is not None:
            self._values["dns_config"] = dns_config
        if dns_policy is not None:
            self._values["dns_policy"] = dns_policy
        if entrypoint is not None:
            self._values["entrypoint"] = entrypoint
        if executor is not None:
            self._values["executor"] = executor
        if host_aliases is not None:
            self._values["host_aliases"] = host_aliases
        if host_network is not None:
            self._values["host_network"] = host_network
        if image_pull_secrets is not None:
            self._values["image_pull_secrets"] = image_pull_secrets
        if metrics is not None:
            self._values["metrics"] = metrics
        if node_selector is not None:
            self._values["node_selector"] = node_selector
        if on_exit is not None:
            self._values["on_exit"] = on_exit
        if parallelism is not None:
            self._values["parallelism"] = parallelism
        if pod_disruption_budget is not None:
            self._values["pod_disruption_budget"] = pod_disruption_budget
        if pod_gc is not None:
            self._values["pod_gc"] = pod_gc
        if pod_metadata is not None:
            self._values["pod_metadata"] = pod_metadata
        if pod_priority is not None:
            self._values["pod_priority"] = pod_priority
        if pod_priority_class_name is not None:
            self._values["pod_priority_class_name"] = pod_priority_class_name
        if pod_spec_patch is not None:
            self._values["pod_spec_patch"] = pod_spec_patch
        if priority is not None:
            self._values["priority"] = priority
        if retry_strategy is not None:
            self._values["retry_strategy"] = retry_strategy
        if scheduler_name is not None:
            self._values["scheduler_name"] = scheduler_name
        if security_context is not None:
            self._values["security_context"] = security_context
        if service_account_name is not None:
            self._values["service_account_name"] = service_account_name
        if shutdown is not None:
            self._values["shutdown"] = shutdown
        if suspend is not None:
            self._values["suspend"] = suspend
        if synchronization is not None:
            self._values["synchronization"] = synchronization
        if template_defaults is not None:
            self._values["template_defaults"] = template_defaults
        if templates is not None:
            self._values["templates"] = templates
        if tolerations is not None:
            self._values["tolerations"] = tolerations
        if ttl_strategy is not None:
            self._values["ttl_strategy"] = ttl_strategy
        if volume_claim_gc is not None:
            self._values["volume_claim_gc"] = volume_claim_gc
        if volume_claim_templates is not None:
            self._values["volume_claim_templates"] = volume_claim_templates
        if volumes is not None:
            self._values["volumes"] = volumes
        if workflow_metadata is not None:
            self._values["workflow_metadata"] = workflow_metadata
        if workflow_template_ref is not None:
            self._values["workflow_template_ref"] = workflow_template_ref

    @builtins.property
    def active_deadline_seconds(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("active_deadline_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def affinity(self) -> typing.Optional[_Affinity_a7d59e98]:
        result = self._values.get("affinity")
        return typing.cast(typing.Optional[_Affinity_a7d59e98], result)

    @builtins.property
    def arguments(self) -> typing.Optional[Arguments]:
        result = self._values.get("arguments")
        return typing.cast(typing.Optional[Arguments], result)

    @builtins.property
    def artifact_repository_ref(self) -> typing.Optional[ArtifactRepositoryRef]:
        result = self._values.get("artifact_repository_ref")
        return typing.cast(typing.Optional[ArtifactRepositoryRef], result)

    @builtins.property
    def automount_service_account_token(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("automount_service_account_token")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def dns_config(self) -> typing.Optional[_PodDnsConfig_4c2fa008]:
        result = self._values.get("dns_config")
        return typing.cast(typing.Optional[_PodDnsConfig_4c2fa008], result)

    @builtins.property
    def dns_policy(self) -> typing.Optional[builtins.str]:
        result = self._values.get("dns_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def entrypoint(self) -> typing.Optional[builtins.str]:
        result = self._values.get("entrypoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def executor(self) -> typing.Optional[ExecutorConfig]:
        result = self._values.get("executor")
        return typing.cast(typing.Optional[ExecutorConfig], result)

    @builtins.property
    def host_aliases(self) -> typing.Optional[typing.List[_HostAlias_82563da2]]:
        result = self._values.get("host_aliases")
        return typing.cast(typing.Optional[typing.List[_HostAlias_82563da2]], result)

    @builtins.property
    def host_network(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("host_network")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def image_pull_secrets(
        self,
    ) -> typing.Optional[typing.List[_LocalObjectReference_cdc737d6]]:
        result = self._values.get("image_pull_secrets")
        return typing.cast(typing.Optional[typing.List[_LocalObjectReference_cdc737d6]], result)

    @builtins.property
    def metrics(self) -> typing.Optional[Metrics]:
        result = self._values.get("metrics")
        return typing.cast(typing.Optional[Metrics], result)

    @builtins.property
    def node_selector(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        result = self._values.get("node_selector")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def on_exit(self) -> typing.Optional[builtins.str]:
        result = self._values.get("on_exit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parallelism(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("parallelism")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def pod_disruption_budget(
        self,
    ) -> typing.Optional[_PodDisruptionBudgetSpec_8bcdde1e]:
        result = self._values.get("pod_disruption_budget")
        return typing.cast(typing.Optional[_PodDisruptionBudgetSpec_8bcdde1e], result)

    @builtins.property
    def pod_gc(self) -> typing.Optional[PodGC]:
        result = self._values.get("pod_gc")
        return typing.cast(typing.Optional[PodGC], result)

    @builtins.property
    def pod_metadata(self) -> typing.Optional[Metadata]:
        result = self._values.get("pod_metadata")
        return typing.cast(typing.Optional[Metadata], result)

    @builtins.property
    def pod_priority(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("pod_priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def pod_priority_class_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("pod_priority_class_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pod_spec_patch(self) -> typing.Optional[builtins.str]:
        result = self._values.get("pod_spec_patch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retry_strategy(self) -> typing.Optional[RetryStrategy]:
        result = self._values.get("retry_strategy")
        return typing.cast(typing.Optional[RetryStrategy], result)

    @builtins.property
    def scheduler_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("scheduler_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_context(self) -> typing.Optional[_PodSecurityContext_c3a517d7]:
        result = self._values.get("security_context")
        return typing.cast(typing.Optional[_PodSecurityContext_c3a517d7], result)

    @builtins.property
    def service_account_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("service_account_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shutdown(self) -> typing.Optional[builtins.str]:
        result = self._values.get("shutdown")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suspend(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("suspend")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def synchronization(self) -> typing.Optional[Synchronization]:
        result = self._values.get("synchronization")
        return typing.cast(typing.Optional[Synchronization], result)

    @builtins.property
    def template_defaults(self) -> typing.Optional[Template]:
        result = self._values.get("template_defaults")
        return typing.cast(typing.Optional[Template], result)

    @builtins.property
    def templates(self) -> typing.Optional[typing.List[Template]]:
        result = self._values.get("templates")
        return typing.cast(typing.Optional[typing.List[Template]], result)

    @builtins.property
    def tolerations(self) -> typing.Optional[typing.List[_Toleration_aec52105]]:
        result = self._values.get("tolerations")
        return typing.cast(typing.Optional[typing.List[_Toleration_aec52105]], result)

    @builtins.property
    def ttl_strategy(self) -> typing.Optional[TTLStrategy]:
        result = self._values.get("ttl_strategy")
        return typing.cast(typing.Optional[TTLStrategy], result)

    @builtins.property
    def volume_claim_gc(self) -> typing.Optional[VolumeClaimGC]:
        result = self._values.get("volume_claim_gc")
        return typing.cast(typing.Optional[VolumeClaimGC], result)

    @builtins.property
    def volume_claim_templates(
        self,
    ) -> typing.Optional[typing.List[_PersistentVolumeClaimSpec_fc09a257]]:
        result = self._values.get("volume_claim_templates")
        return typing.cast(typing.Optional[typing.List[_PersistentVolumeClaimSpec_fc09a257]], result)

    @builtins.property
    def volumes(self) -> typing.Optional[typing.List[_Volume_05ce2014]]:
        result = self._values.get("volumes")
        return typing.cast(typing.Optional[typing.List[_Volume_05ce2014]], result)

    @builtins.property
    def workflow_metadata(self) -> typing.Optional[_ObjectMeta_77a65d46]:
        result = self._values.get("workflow_metadata")
        return typing.cast(typing.Optional[_ObjectMeta_77a65d46], result)

    @builtins.property
    def workflow_template_ref(self) -> typing.Optional[WorkflowTemplateRef]:
        result = self._values.get("workflow_template_ref")
        return typing.cast(typing.Optional[WorkflowTemplateRef], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowTemplateSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.WorkflowTemplateUpdateRequest",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "namespace": "namespace", "template": "template"},
)
class WorkflowTemplateUpdateRequest:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
        template: typing.Optional[WorkflowTemplate] = None,
    ) -> None:
        '''
        :param name: 
        :param namespace: 
        :param template: 
        '''
        if isinstance(template, dict):
            template = WorkflowTemplate(**template)
        self._values: typing.Dict[str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if namespace is not None:
            self._values["namespace"] = namespace
        if template is not None:
            self._values["template"] = template

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template(self) -> typing.Optional[WorkflowTemplate]:
        result = self._values.get("template")
        return typing.cast(typing.Optional[WorkflowTemplate], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowTemplateUpdateRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.WorkflowTerminateRequest",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "namespace": "namespace"},
)
class WorkflowTerminateRequest:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: 
        :param namespace: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowTerminateRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.WorkflowWatchEvent",
    jsii_struct_bases=[],
    name_mapping={"object": "object", "type": "type"},
)
class WorkflowWatchEvent:
    def __init__(
        self,
        *,
        object: typing.Optional[Workflow] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param object: 
        :param type: 
        '''
        if isinstance(object, dict):
            object = Workflow(**object)
        self._values: typing.Dict[str, typing.Any] = {}
        if object is not None:
            self._values["object"] = object
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def object(self) -> typing.Optional[Workflow]:
        result = self._values.get("object")
        return typing.cast(typing.Optional[Workflow], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowWatchEvent(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@opencdk8s/cdk8s-argoworkflow-resources.ZipStrategy",
    jsii_struct_bases=[],
    name_mapping={},
)
class ZipStrategy:
    def __init__(self) -> None:
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ZipStrategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ArchiveStrategy",
    "ArchivedWorkflowDeletedResponse",
    "ArgoWorkflowClusterWorkflowTemplate",
    "ArgoWorkflowCronWorkflow",
    "ArgoWorkflowWorkflowTemplate",
    "Arguments",
    "Artifact",
    "ArtifactLocation",
    "ArtifactPaths",
    "ArtifactRepositoryRef",
    "ArtifactRepositoryRefStatus",
    "ArtifactoryArtifact",
    "Backoff",
    "Cache",
    "ClusterWorkflowTemplate",
    "ClusterWorkflowTemplateDeleteResponse",
    "ClusterWorkflowTemplateLintRequest",
    "ClusterWorkflowTemplateList",
    "ClusterWorkflowTemplateUpdateRequest",
    "Condition",
    "ContainerNode",
    "ContainerSetTemplate",
    "ContinueOn",
    "Counter",
    "CreateCronWorkflowRequest",
    "CreateS3BucketOptions",
    "CronWorkflow",
    "CronWorkflowDeletedResponse",
    "CronWorkflowList",
    "CronWorkflowResumeRequest",
    "CronWorkflowSpec",
    "CronWorkflowStatus",
    "CronWorkflowSuspendRequest",
    "DAGTask",
    "DAGTemplate",
    "Data",
    "DataSource",
    "Event",
    "EventResponse",
    "ExecutorConfig",
    "GCSArtifact",
    "Gauge",
    "GetUserInfoResponse",
    "GitArtifact",
    "GoogleProtobufAny",
    "GrpcGatewayRuntimeError",
    "GrpcGatewayRuntimeStreamError",
    "HDFSArtifact",
    "HTTPArtifact",
    "Header",
    "Histogram",
    "InfoResponse",
    "Inputs",
    "Link",
    "LintCronWorkflowRequest",
    "LogEntry",
    "MemoizationStatus",
    "Memoize",
    "Metadata",
    "MetricLabel",
    "Metrics",
    "Mutex",
    "MutexHolding",
    "MutexStatus",
    "NodeStatus",
    "NodeSynchronizationStatus",
    "NoneStrategy",
    "OSSArtifact",
    "Outputs",
    "Parameter",
    "PodGC",
    "Prometheus",
    "RawArtifact",
    "ResourceTemplate",
    "RetryAffinity",
    "RetryNodeAntiAffinity",
    "RetryStrategy",
    "S3Artifact",
    "ScriptTemplate",
    "SemaphoreHolding",
    "SemaphoreRef",
    "SemaphoreStatus",
    "Sequence",
    "Submit",
    "SubmitOpts",
    "SuppliedValueFrom",
    "SuspendTemplate",
    "Synchronization",
    "SynchronizationStatus",
    "TTLStrategy",
    "TarStrategy",
    "Template",
    "TemplateRef",
    "TransformationStep",
    "UpdateCronWorkflowRequest",
    "UserContainer",
    "ValueFrom",
    "Version",
    "VolumeClaimGC",
    "Workflow",
    "WorkflowCreateRequest",
    "WorkflowDeleteResponse",
    "WorkflowEventBinding",
    "WorkflowEventBindingList",
    "WorkflowEventBindingSpec",
    "WorkflowLintRequest",
    "WorkflowList",
    "WorkflowResubmitRequest",
    "WorkflowResumeRequest",
    "WorkflowRetryRequest",
    "WorkflowSetRequest",
    "WorkflowSpec",
    "WorkflowStatus",
    "WorkflowStep",
    "WorkflowStopRequest",
    "WorkflowSubmitRequest",
    "WorkflowSuspendRequest",
    "WorkflowTemplate",
    "WorkflowTemplateCreateRequest",
    "WorkflowTemplateDeleteResponse",
    "WorkflowTemplateLintRequest",
    "WorkflowTemplateList",
    "WorkflowTemplateRef",
    "WorkflowTemplateSpec",
    "WorkflowTemplateUpdateRequest",
    "WorkflowTerminateRequest",
    "WorkflowWatchEvent",
    "ZipStrategy",
    "k8s",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import k8s
