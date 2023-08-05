"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import layerapi.api.entity.activity_wrapper_pb2
import builtins
import google.protobuf.descriptor
import google.protobuf.message
import google.protobuf.timestamp_pb2
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class FabricActivity(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    ACTIVITY_WRAPPER_FIELD_NUMBER: builtins.int
    FABRIC_FIELD_NUMBER: builtins.int
    REPORTED_START_TIME_FIELD_NUMBER: builtins.int
    REPORTED_END_TIME_FIELD_NUMBER: builtins.int
    @property
    def activity_wrapper(self) -> api.entity.activity_wrapper_pb2.ActivityWrapper: ...
    fabric: typing.Text
    @property
    def reported_start_time(self) -> google.protobuf.timestamp_pb2.Timestamp: ...
    @property
    def reported_end_time(self) -> google.protobuf.timestamp_pb2.Timestamp: ...
    def __init__(self,
        *,
        activity_wrapper: typing.Optional[api.entity.activity_wrapper_pb2.ActivityWrapper] = ...,
        fabric: typing.Text = ...,
        reported_start_time: typing.Optional[google.protobuf.timestamp_pb2.Timestamp] = ...,
        reported_end_time: typing.Optional[google.protobuf.timestamp_pb2.Timestamp] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["activity_wrapper",b"activity_wrapper","reported_end_time",b"reported_end_time","reported_start_time",b"reported_start_time"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["activity_wrapper",b"activity_wrapper","fabric",b"fabric","reported_end_time",b"reported_end_time","reported_start_time",b"reported_start_time"]) -> None: ...
global___FabricActivity = FabricActivity
