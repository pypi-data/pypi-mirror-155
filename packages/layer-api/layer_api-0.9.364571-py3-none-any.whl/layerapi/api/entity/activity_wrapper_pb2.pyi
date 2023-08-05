"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import layerapi.api.ids_pb2
import builtins
import google.protobuf.descriptor
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class ActivityWrapper(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    DATASET_BUILD_ID_FIELD_NUMBER: builtins.int
    MODEL_TRAIN_ID_FIELD_NUMBER: builtins.int
    @property
    def dataset_build_id(self) -> api.ids_pb2.DatasetBuildId: ...
    @property
    def model_train_id(self) -> api.ids_pb2.ModelTrainId: ...
    def __init__(self,
        *,
        dataset_build_id: typing.Optional[api.ids_pb2.DatasetBuildId] = ...,
        model_train_id: typing.Optional[api.ids_pb2.ModelTrainId] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["dataset_build_id",b"dataset_build_id","model_train_id",b"model_train_id","value",b"value"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["dataset_build_id",b"dataset_build_id","model_train_id",b"model_train_id","value",b"value"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["value",b"value"]) -> typing.Optional[typing_extensions.Literal["dataset_build_id","model_train_id"]]: ...
global___ActivityWrapper = ActivityWrapper
