"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import layerapi.api.entity.dataset_build_pb2
import layerapi.api.ids_pb2
import builtins
import google.protobuf.descriptor
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class StartBuildDatasetByPathRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    PATH_FIELD_NUMBER: builtins.int
    path: typing.Text
    def __init__(self,
        *,
        path: typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["path",b"path"]) -> None: ...
global___StartBuildDatasetByPathRequest = StartBuildDatasetByPathRequest

class StartBuildDatasetByPathResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    DATASET_BUILD_ID_FIELD_NUMBER: builtins.int
    @property
    def dataset_build_id(self) -> api.ids_pb2.DatasetBuildId: ...
    def __init__(self,
        *,
        dataset_build_id: typing.Optional[api.ids_pb2.DatasetBuildId] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["dataset_build_id",b"dataset_build_id"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["dataset_build_id",b"dataset_build_id"]) -> None: ...
global___StartBuildDatasetByPathResponse = StartBuildDatasetByPathResponse

class GetBuildDatasetStatusRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    DATASET_BUILD_ID_FIELD_NUMBER: builtins.int
    @property
    def dataset_build_id(self) -> api.ids_pb2.DatasetBuildId: ...
    def __init__(self,
        *,
        dataset_build_id: typing.Optional[api.ids_pb2.DatasetBuildId] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["dataset_build_id",b"dataset_build_id"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["dataset_build_id",b"dataset_build_id"]) -> None: ...
global___GetBuildDatasetStatusRequest = GetBuildDatasetStatusRequest

class GetBuildDatasetStatusResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    DATASET_BUILD_ID_FIELD_NUMBER: builtins.int
    DATASET_BUILD_STATUS_FIELD_NUMBER: builtins.int
    @property
    def dataset_build_id(self) -> api.ids_pb2.DatasetBuildId: ...
    @property
    def dataset_build_status(self) -> api.entity.dataset_build_pb2.DatasetBuild.BuildStatusInfo: ...
    def __init__(self,
        *,
        dataset_build_id: typing.Optional[api.ids_pb2.DatasetBuildId] = ...,
        dataset_build_status: typing.Optional[api.entity.dataset_build_pb2.DatasetBuild.BuildStatusInfo] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["dataset_build_id",b"dataset_build_id","dataset_build_status",b"dataset_build_status"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["dataset_build_id",b"dataset_build_id","dataset_build_status",b"dataset_build_status"]) -> None: ...
global___GetBuildDatasetStatusResponse = GetBuildDatasetStatusResponse

class CancelBuildDatasetRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    DATASET_BUILD_ID_FIELD_NUMBER: builtins.int
    @property
    def dataset_build_id(self) -> api.ids_pb2.DatasetBuildId: ...
    def __init__(self,
        *,
        dataset_build_id: typing.Optional[api.ids_pb2.DatasetBuildId] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["dataset_build_id",b"dataset_build_id"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["dataset_build_id",b"dataset_build_id"]) -> None: ...
global___CancelBuildDatasetRequest = CancelBuildDatasetRequest

class CancelBuildDatasetResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    DATASET_BUILD_ID_FIELD_NUMBER: builtins.int
    @property
    def dataset_build_id(self) -> api.ids_pb2.DatasetBuildId: ...
    def __init__(self,
        *,
        dataset_build_id: typing.Optional[api.ids_pb2.DatasetBuildId] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["dataset_build_id",b"dataset_build_id"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["dataset_build_id",b"dataset_build_id"]) -> None: ...
global___CancelBuildDatasetResponse = CancelBuildDatasetResponse
