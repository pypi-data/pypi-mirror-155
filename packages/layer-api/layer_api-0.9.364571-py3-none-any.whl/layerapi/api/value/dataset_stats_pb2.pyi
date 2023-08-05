"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class DatasetStats(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    class Histogram(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        class Bucket(google.protobuf.message.Message):
            DESCRIPTOR: google.protobuf.descriptor.Descriptor
            VALUE_FIELD_NUMBER: builtins.int
            COUNT_FIELD_NUMBER: builtins.int
            value: typing.Text
            count: builtins.int
            def __init__(self,
                *,
                value: typing.Text = ...,
                count: builtins.int = ...,
                ) -> None: ...
            def ClearField(self, field_name: typing_extensions.Literal["count",b"count","value",b"value"]) -> None: ...

        class Percentiles(google.protobuf.message.Message):
            DESCRIPTOR: google.protobuf.descriptor.Descriptor
            P25_FIELD_NUMBER: builtins.int
            P50_FIELD_NUMBER: builtins.int
            P75_FIELD_NUMBER: builtins.int
            p25: builtins.int
            p50: builtins.int
            p75: builtins.int
            def __init__(self,
                *,
                p25: builtins.int = ...,
                p50: builtins.int = ...,
                p75: builtins.int = ...,
                ) -> None: ...
            def ClearField(self, field_name: typing_extensions.Literal["p25",b"p25","p50",b"p50","p75",b"p75"]) -> None: ...

        NAME_FIELD_NUMBER: builtins.int
        BUCKETS_FIELD_NUMBER: builtins.int
        PERCENTILES_FIELD_NUMBER: builtins.int
        name: typing.Text
        @property
        def buckets(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___DatasetStats.Histogram.Bucket]: ...
        @property
        def percentiles(self) -> global___DatasetStats.Histogram.Percentiles: ...
        def __init__(self,
            *,
            name: typing.Text = ...,
            buckets: typing.Optional[typing.Iterable[global___DatasetStats.Histogram.Bucket]] = ...,
            percentiles: typing.Optional[global___DatasetStats.Histogram.Percentiles] = ...,
            ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["percentiles",b"percentiles"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["buckets",b"buckets","name",b"name","percentiles",b"percentiles"]) -> None: ...

    class Column(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        class Value(google.protobuf.message.Message):
            DESCRIPTOR: google.protobuf.descriptor.Descriptor
            LONG_VALUE_FIELD_NUMBER: builtins.int
            DOUBLE_VALUE_FIELD_NUMBER: builtins.int
            long_value: builtins.int
            double_value: builtins.float
            def __init__(self,
                *,
                long_value: builtins.int = ...,
                double_value: builtins.float = ...,
                ) -> None: ...
            def HasField(self, field_name: typing_extensions.Literal["double_value",b"double_value","long_value",b"long_value","value",b"value"]) -> builtins.bool: ...
            def ClearField(self, field_name: typing_extensions.Literal["double_value",b"double_value","long_value",b"long_value","value",b"value"]) -> None: ...
            def WhichOneof(self, oneof_group: typing_extensions.Literal["value",b"value"]) -> typing.Optional[typing_extensions.Literal["long_value","double_value"]]: ...

        class TopK(google.protobuf.message.Message):
            DESCRIPTOR: google.protobuf.descriptor.Descriptor
            class Item(google.protobuf.message.Message):
                DESCRIPTOR: google.protobuf.descriptor.Descriptor
                VALUE_FIELD_NUMBER: builtins.int
                COUNT_FIELD_NUMBER: builtins.int
                value: typing.Text
                count: builtins.int
                def __init__(self,
                    *,
                    value: typing.Text = ...,
                    count: builtins.int = ...,
                    ) -> None: ...
                def ClearField(self, field_name: typing_extensions.Literal["count",b"count","value",b"value"]) -> None: ...

            ITEMS_FIELD_NUMBER: builtins.int
            @property
            def items(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___DatasetStats.Column.TopK.Item]: ...
            def __init__(self,
                *,
                items: typing.Optional[typing.Iterable[global___DatasetStats.Column.TopK.Item]] = ...,
                ) -> None: ...
            def ClearField(self, field_name: typing_extensions.Literal["items",b"items"]) -> None: ...

        NAME_FIELD_NUMBER: builtins.int
        NULL_COUNT_FIELD_NUMBER: builtins.int
        NOT_NULL_COUNT_FIELD_NUMBER: builtins.int
        MIN_FIELD_NUMBER: builtins.int
        MAX_FIELD_NUMBER: builtins.int
        MEAN_FIELD_NUMBER: builtins.int
        STD_FIELD_NUMBER: builtins.int
        UNIQUE_COUNT_APPROX_FIELD_NUMBER: builtins.int
        TOP_K_APPROX_FIELD_NUMBER: builtins.int
        name: typing.Text
        null_count: builtins.int
        not_null_count: builtins.int
        @property
        def min(self) -> global___DatasetStats.Column.Value: ...
        @property
        def max(self) -> global___DatasetStats.Column.Value: ...
        @property
        def mean(self) -> global___DatasetStats.Column.Value: ...
        @property
        def std(self) -> global___DatasetStats.Column.Value: ...
        unique_count_approx: builtins.int
        @property
        def top_k_approx(self) -> global___DatasetStats.Column.TopK: ...
        def __init__(self,
            *,
            name: typing.Text = ...,
            null_count: builtins.int = ...,
            not_null_count: builtins.int = ...,
            min: typing.Optional[global___DatasetStats.Column.Value] = ...,
            max: typing.Optional[global___DatasetStats.Column.Value] = ...,
            mean: typing.Optional[global___DatasetStats.Column.Value] = ...,
            std: typing.Optional[global___DatasetStats.Column.Value] = ...,
            unique_count_approx: builtins.int = ...,
            top_k_approx: typing.Optional[global___DatasetStats.Column.TopK] = ...,
            ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["max",b"max","mean",b"mean","min",b"min","std",b"std","top_k_approx",b"top_k_approx"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["max",b"max","mean",b"mean","min",b"min","name",b"name","not_null_count",b"not_null_count","null_count",b"null_count","std",b"std","top_k_approx",b"top_k_approx","unique_count_approx",b"unique_count_approx"]) -> None: ...

    ROW_COUNT_FIELD_NUMBER: builtins.int
    HISTOGRAMS_FIELD_NUMBER: builtins.int
    SIZE_IN_BYTES_FIELD_NUMBER: builtins.int
    COLUMNS_FIELD_NUMBER: builtins.int
    row_count: builtins.int
    @property
    def histograms(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___DatasetStats.Histogram]: ...
    size_in_bytes: builtins.int
    @property
    def columns(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___DatasetStats.Column]: ...
    def __init__(self,
        *,
        row_count: builtins.int = ...,
        histograms: typing.Optional[typing.Iterable[global___DatasetStats.Histogram]] = ...,
        size_in_bytes: builtins.int = ...,
        columns: typing.Optional[typing.Iterable[global___DatasetStats.Column]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["columns",b"columns","histograms",b"histograms","row_count",b"row_count","size_in_bytes",b"size_in_bytes"]) -> None: ...
global___DatasetStats = DatasetStats
