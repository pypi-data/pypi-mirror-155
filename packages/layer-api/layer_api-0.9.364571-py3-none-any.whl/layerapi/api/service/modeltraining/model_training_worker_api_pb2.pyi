"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import layerapi.api.ids_pb2
import layerapi.api.value.aws_credentials_pb2
import layerapi.api.value.s3_path_pb2
import builtins
import google.protobuf.descriptor
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class StartExecutionRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    TRAIN_ID_FIELD_NUMBER: builtins.int
    BASE_URI_FIELD_NUMBER: builtins.int
    ACCESS_TOKEN_FIELD_NUMBER: builtins.int
    MODEL_NAME_FIELD_NUMBER: builtins.int
    MODEL_VERSION_FIELD_NUMBER: builtins.int
    SOURCE_ENTRYPOINT_FIELD_NUMBER: builtins.int
    SOURCE_ARCHIVE_NAME_FIELD_NUMBER: builtins.int
    CREDENTIALS_FIELD_NUMBER: builtins.int
    S3_PATH_FIELD_NUMBER: builtins.int
    DEPENDENCY_FILENAME_FIELD_NUMBER: builtins.int
    @property
    def train_id(self) -> api.ids_pb2.ModelTrainId: ...
    base_uri: typing.Text
    access_token: typing.Text
    model_name: typing.Text
    model_version: typing.Text
    source_entrypoint: typing.Text
    source_archive_name: typing.Text
    @property
    def credentials(self) -> api.value.aws_credentials_pb2.AwsCredentials: ...
    @property
    def s3_path(self) -> api.value.s3_path_pb2.S3Path: ...
    dependency_filename: typing.Text
    def __init__(self,
        *,
        train_id: typing.Optional[api.ids_pb2.ModelTrainId] = ...,
        base_uri: typing.Text = ...,
        access_token: typing.Text = ...,
        model_name: typing.Text = ...,
        model_version: typing.Text = ...,
        source_entrypoint: typing.Text = ...,
        source_archive_name: typing.Text = ...,
        credentials: typing.Optional[api.value.aws_credentials_pb2.AwsCredentials] = ...,
        s3_path: typing.Optional[api.value.s3_path_pb2.S3Path] = ...,
        dependency_filename: typing.Text = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["credentials",b"credentials","s3_path",b"s3_path","train_id",b"train_id"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["access_token",b"access_token","base_uri",b"base_uri","credentials",b"credentials","dependency_filename",b"dependency_filename","model_name",b"model_name","model_version",b"model_version","s3_path",b"s3_path","source_archive_name",b"source_archive_name","source_entrypoint",b"source_entrypoint","train_id",b"train_id"]) -> None: ...
global___StartExecutionRequest = StartExecutionRequest

class StartExecutionResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    SUCCESS_FIELD_NUMBER: builtins.int
    DETAIL_FIELD_NUMBER: builtins.int
    success: builtins.bool
    detail: typing.Text
    def __init__(self,
        *,
        success: builtins.bool = ...,
        detail: typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["detail",b"detail","success",b"success"]) -> None: ...
global___StartExecutionResponse = StartExecutionResponse

class StartHyperparameterTuningExecutionRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    HYPERPARAMETER_TUNING_ID_FIELD_NUMBER: builtins.int
    BASE_URI_FIELD_NUMBER: builtins.int
    ACCESS_TOKEN_FIELD_NUMBER: builtins.int
    MODEL_NAME_FIELD_NUMBER: builtins.int
    MODEL_VERSION_FIELD_NUMBER: builtins.int
    SOURCE_ENTRYPOINT_FIELD_NUMBER: builtins.int
    SOURCE_ARCHIVE_NAME_FIELD_NUMBER: builtins.int
    CREDENTIALS_FIELD_NUMBER: builtins.int
    S3_PATH_FIELD_NUMBER: builtins.int
    DEPENDENCY_FILENAME_FIELD_NUMBER: builtins.int
    @property
    def hyperparameter_tuning_id(self) -> api.ids_pb2.HyperparameterTuningId: ...
    base_uri: typing.Text
    access_token: typing.Text
    model_name: typing.Text
    model_version: typing.Text
    source_entrypoint: typing.Text
    source_archive_name: typing.Text
    @property
    def credentials(self) -> api.value.aws_credentials_pb2.AwsCredentials: ...
    @property
    def s3_path(self) -> api.value.s3_path_pb2.S3Path: ...
    dependency_filename: typing.Text
    def __init__(self,
        *,
        hyperparameter_tuning_id: typing.Optional[api.ids_pb2.HyperparameterTuningId] = ...,
        base_uri: typing.Text = ...,
        access_token: typing.Text = ...,
        model_name: typing.Text = ...,
        model_version: typing.Text = ...,
        source_entrypoint: typing.Text = ...,
        source_archive_name: typing.Text = ...,
        credentials: typing.Optional[api.value.aws_credentials_pb2.AwsCredentials] = ...,
        s3_path: typing.Optional[api.value.s3_path_pb2.S3Path] = ...,
        dependency_filename: typing.Text = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["credentials",b"credentials","hyperparameter_tuning_id",b"hyperparameter_tuning_id","s3_path",b"s3_path"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["access_token",b"access_token","base_uri",b"base_uri","credentials",b"credentials","dependency_filename",b"dependency_filename","hyperparameter_tuning_id",b"hyperparameter_tuning_id","model_name",b"model_name","model_version",b"model_version","s3_path",b"s3_path","source_archive_name",b"source_archive_name","source_entrypoint",b"source_entrypoint"]) -> None: ...
global___StartHyperparameterTuningExecutionRequest = StartHyperparameterTuningExecutionRequest

class StartHyperparameterTuningExecutionResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    SUCCESS_FIELD_NUMBER: builtins.int
    DETAIL_FIELD_NUMBER: builtins.int
    success: builtins.bool
    detail: typing.Text
    def __init__(self,
        *,
        success: builtins.bool = ...,
        detail: typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["detail",b"detail","success",b"success"]) -> None: ...
global___StartHyperparameterTuningExecutionResponse = StartHyperparameterTuningExecutionResponse
