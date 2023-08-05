"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import layerapi.api.value.logged_data_type_pb2
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import google.protobuf.timestamp_pb2
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class LoggedData(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    class EpochedDataEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.int
        value: typing.Text
        def __init__(self,
            *,
            key: builtins.int = ...,
            value: typing.Text = ...,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["key",b"key","value",b"value"]) -> None: ...

    class DataWithEpoch(google.protobuf.message.Message):
        """This is added as GraphQL doesn't support map type. This comment will be removed when epoched_data above is removed."""
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        EPOCH_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        epoch: builtins.int
        value: typing.Text
        def __init__(self,
            *,
            epoch: builtins.int = ...,
            value: typing.Text = ...,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["epoch",b"epoch","value",b"value"]) -> None: ...

    UNIQUE_TAG_FIELD_NUMBER: builtins.int
    TYPE_FIELD_NUMBER: builtins.int
    CREATED_TIME_FIELD_NUMBER: builtins.int
    UPDATED_TIME_FIELD_NUMBER: builtins.int
    TEXT_FIELD_NUMBER: builtins.int
    URL_FIELD_NUMBER: builtins.int
    EPOCHED_DATA_FIELD_NUMBER: builtins.int
    ALL_EPOCHED_DATA_FIELD_NUMBER: builtins.int
    unique_tag: typing.Text
    type: api.value.logged_data_type_pb2.LoggedDataType.ValueType
    @property
    def created_time(self) -> google.protobuf.timestamp_pb2.Timestamp: ...
    @property
    def updated_time(self) -> google.protobuf.timestamp_pb2.Timestamp: ...
    text: typing.Text
    url: typing.Text
    @property
    def epoched_data(self) -> google.protobuf.internal.containers.ScalarMap[builtins.int, typing.Text]:
        """TODO: map is not a supported type for GraphQL. Remove this."""
        pass
    @property
    def all_epoched_data(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___LoggedData.DataWithEpoch]: ...
    def __init__(self,
        *,
        unique_tag: typing.Text = ...,
        type: api.value.logged_data_type_pb2.LoggedDataType.ValueType = ...,
        created_time: typing.Optional[google.protobuf.timestamp_pb2.Timestamp] = ...,
        updated_time: typing.Optional[google.protobuf.timestamp_pb2.Timestamp] = ...,
        text: typing.Text = ...,
        url: typing.Text = ...,
        epoched_data: typing.Optional[typing.Mapping[builtins.int, typing.Text]] = ...,
        all_epoched_data: typing.Optional[typing.Iterable[global___LoggedData.DataWithEpoch]] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["created_time",b"created_time","data",b"data","text",b"text","updated_time",b"updated_time","url",b"url"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["all_epoched_data",b"all_epoched_data","created_time",b"created_time","data",b"data","epoched_data",b"epoched_data","text",b"text","type",b"type","unique_tag",b"unique_tag","updated_time",b"updated_time","url",b"url"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["data",b"data"]) -> typing.Optional[typing_extensions.Literal["text","url"]]: ...
global___LoggedData = LoggedData
