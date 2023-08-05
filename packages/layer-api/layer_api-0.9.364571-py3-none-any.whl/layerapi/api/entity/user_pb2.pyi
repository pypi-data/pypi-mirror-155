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

class User(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    ID_FIELD_NUMBER: builtins.int
    EMAIL_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    FIRST_NAME_FIELD_NUMBER: builtins.int
    LAST_NAME_FIELD_NUMBER: builtins.int
    ORGANIZATION_ID_FIELD_NUMBER: builtins.int
    PICTURE_URL_FIELD_NUMBER: builtins.int
    @property
    def id(self) -> api.ids_pb2.UserId: ...
    email: typing.Text
    name: typing.Text
    first_name: typing.Text
    last_name: typing.Text
    @property
    def organization_id(self) -> api.ids_pb2.OrganizationId: ...
    picture_url: typing.Text
    def __init__(self,
        *,
        id: typing.Optional[api.ids_pb2.UserId] = ...,
        email: typing.Text = ...,
        name: typing.Text = ...,
        first_name: typing.Text = ...,
        last_name: typing.Text = ...,
        organization_id: typing.Optional[api.ids_pb2.OrganizationId] = ...,
        picture_url: typing.Text = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["id",b"id","organization_id",b"organization_id"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["email",b"email","first_name",b"first_name","id",b"id","last_name",b"last_name","name",b"name","organization_id",b"organization_id","picture_url",b"picture_url"]) -> None: ...
global___User = User
