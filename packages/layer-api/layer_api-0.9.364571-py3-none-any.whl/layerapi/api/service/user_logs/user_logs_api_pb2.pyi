"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import layerapi.api.entity.user_log_line_pb2
import layerapi.api.ids_pb2
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class GetPipelineRunLogsRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    RUN_ID_FIELD_NUMBER: builtins.int
    CONTINUATION_TOKEN_FIELD_NUMBER: builtins.int
    @property
    def run_id(self) -> api.ids_pb2.RunId: ...
    continuation_token: typing.Text
    def __init__(self,
        *,
        run_id: typing.Optional[api.ids_pb2.RunId] = ...,
        continuation_token: typing.Text = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["run_id",b"run_id"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["continuation_token",b"continuation_token","run_id",b"run_id"]) -> None: ...
global___GetPipelineRunLogsRequest = GetPipelineRunLogsRequest

class GetPipelineRunLogsResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    LOG_LINES_FIELD_NUMBER: builtins.int
    CONTINUATION_TOKEN_FIELD_NUMBER: builtins.int
    @property
    def log_lines(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[api.entity.user_log_line_pb2.UserLogLine]: ...
    continuation_token: typing.Text
    def __init__(self,
        *,
        log_lines: typing.Optional[typing.Iterable[api.entity.user_log_line_pb2.UserLogLine]] = ...,
        continuation_token: typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["continuation_token",b"continuation_token","log_lines",b"log_lines"]) -> None: ...
global___GetPipelineRunLogsResponse = GetPipelineRunLogsResponse

class GetPipelineRunLogsPerEntityRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    RUN_ID_FIELD_NUMBER: builtins.int
    DATASET_NAME_FIELD_NUMBER: builtins.int
    MODEL_NAME_FIELD_NUMBER: builtins.int
    CONTINUATION_TOKEN_FIELD_NUMBER: builtins.int
    @property
    def run_id(self) -> api.ids_pb2.RunId: ...
    dataset_name: typing.Text
    model_name: typing.Text
    continuation_token: typing.Text
    def __init__(self,
        *,
        run_id: typing.Optional[api.ids_pb2.RunId] = ...,
        dataset_name: typing.Text = ...,
        model_name: typing.Text = ...,
        continuation_token: typing.Text = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["run_id",b"run_id"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["continuation_token",b"continuation_token","dataset_name",b"dataset_name","model_name",b"model_name","run_id",b"run_id"]) -> None: ...
global___GetPipelineRunLogsPerEntityRequest = GetPipelineRunLogsPerEntityRequest

class GetPipelineRunLogsPerEntityResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    LOG_LINES_FIELD_NUMBER: builtins.int
    CONTINUATION_TOKEN_FIELD_NUMBER: builtins.int
    @property
    def log_lines(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[api.entity.user_log_line_pb2.UserLogLine]: ...
    continuation_token: typing.Text
    def __init__(self,
        *,
        log_lines: typing.Optional[typing.Iterable[api.entity.user_log_line_pb2.UserLogLine]] = ...,
        continuation_token: typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["continuation_token",b"continuation_token","log_lines",b"log_lines"]) -> None: ...
global___GetPipelineRunLogsPerEntityResponse = GetPipelineRunLogsPerEntityResponse

class GetPipelineRunLogsStreamingRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    RUN_ID_FIELD_NUMBER: builtins.int
    @property
    def run_id(self) -> api.ids_pb2.RunId: ...
    def __init__(self,
        *,
        run_id: typing.Optional[api.ids_pb2.RunId] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["run_id",b"run_id"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["run_id",b"run_id"]) -> None: ...
global___GetPipelineRunLogsStreamingRequest = GetPipelineRunLogsStreamingRequest

class GetPipelineRunLogsStreamingResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    LOG_LINES_FIELD_NUMBER: builtins.int
    @property
    def log_lines(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[api.entity.user_log_line_pb2.UserLogLine]: ...
    def __init__(self,
        *,
        log_lines: typing.Optional[typing.Iterable[api.entity.user_log_line_pb2.UserLogLine]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["log_lines",b"log_lines"]) -> None: ...
global___GetPipelineRunLogsStreamingResponse = GetPipelineRunLogsStreamingResponse
