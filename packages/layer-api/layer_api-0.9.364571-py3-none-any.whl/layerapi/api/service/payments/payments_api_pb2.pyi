"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import layerapi.api.entity.billing_info_pb2
import layerapi.api.entity.payment_info_pb2
import layerapi.api.ids_pb2
import layerapi.api.value.payment_status_type_pb2
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class CreateStripeCustomerRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    EMAIL_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    ORGANIZATION_ID_FIELD_NUMBER: builtins.int
    email: typing.Text
    name: typing.Text
    @property
    def organization_id(self) -> api.ids_pb2.OrganizationId: ...
    def __init__(self,
        *,
        email: typing.Text = ...,
        name: typing.Text = ...,
        organization_id: typing.Optional[api.ids_pb2.OrganizationId] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["organization_id",b"organization_id"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["email",b"email","name",b"name","organization_id",b"organization_id"]) -> None: ...
global___CreateStripeCustomerRequest = CreateStripeCustomerRequest

class CreateStripeCustomerResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    MESSAGE_FIELD_NUMBER: builtins.int
    message: typing.Text
    def __init__(self,
        *,
        message: typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["message",b"message"]) -> None: ...
global___CreateStripeCustomerResponse = CreateStripeCustomerResponse

class GetStripeSetupIntentIdRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    def __init__(self,
        ) -> None: ...
global___GetStripeSetupIntentIdRequest = GetStripeSetupIntentIdRequest

class GetStripeSetupIntentIdResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    STRIPE_SETUP_INTENT_ID_FIELD_NUMBER: builtins.int
    @property
    def stripe_setup_intent_id(self) -> api.ids_pb2.StripeSetupIntentId: ...
    def __init__(self,
        *,
        stripe_setup_intent_id: typing.Optional[api.ids_pb2.StripeSetupIntentId] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["stripe_setup_intent_id",b"stripe_setup_intent_id"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["stripe_setup_intent_id",b"stripe_setup_intent_id"]) -> None: ...
global___GetStripeSetupIntentIdResponse = GetStripeSetupIntentIdResponse

class SaveStripePaymentMethodIdRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    STRIPE_PAYMENT_METHOD_ID_FIELD_NUMBER: builtins.int
    @property
    def stripe_payment_method_id(self) -> api.ids_pb2.StripePaymentMethodId: ...
    def __init__(self,
        *,
        stripe_payment_method_id: typing.Optional[api.ids_pb2.StripePaymentMethodId] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["stripe_payment_method_id",b"stripe_payment_method_id"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["stripe_payment_method_id",b"stripe_payment_method_id"]) -> None: ...
global___SaveStripePaymentMethodIdRequest = SaveStripePaymentMethodIdRequest

class SaveStripePaymentMethodIdResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    BILLING_INFO_FIELD_NUMBER: builtins.int
    @property
    def billing_info(self) -> api.entity.billing_info_pb2.BillingInfo: ...
    def __init__(self,
        *,
        billing_info: typing.Optional[api.entity.billing_info_pb2.BillingInfo] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["billing_info",b"billing_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["billing_info",b"billing_info"]) -> None: ...
global___SaveStripePaymentMethodIdResponse = SaveStripePaymentMethodIdResponse

class GetStripeBillingInfoRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    STRIPE_PAYMENT_METHOD_ID_FIELD_NUMBER: builtins.int
    @property
    def stripe_payment_method_id(self) -> api.ids_pb2.StripePaymentMethodId: ...
    def __init__(self,
        *,
        stripe_payment_method_id: typing.Optional[api.ids_pb2.StripePaymentMethodId] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["stripe_payment_method_id",b"stripe_payment_method_id"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["stripe_payment_method_id",b"stripe_payment_method_id"]) -> None: ...
global___GetStripeBillingInfoRequest = GetStripeBillingInfoRequest

class GetStripeBillingInfoResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    BILLING_INFO_FIELD_NUMBER: builtins.int
    @property
    def billing_info(self) -> api.entity.billing_info_pb2.BillingInfo: ...
    def __init__(self,
        *,
        billing_info: typing.Optional[api.entity.billing_info_pb2.BillingInfo] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["billing_info",b"billing_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["billing_info",b"billing_info"]) -> None: ...
global___GetStripeBillingInfoResponse = GetStripeBillingInfoResponse

class GetStripePaymentMethodIdRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    def __init__(self,
        ) -> None: ...
global___GetStripePaymentMethodIdRequest = GetStripePaymentMethodIdRequest

class GetStripePaymentMethodIdResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    STRIPE_PAYMENT_METHOD_ID_FIELD_NUMBER: builtins.int
    @property
    def stripe_payment_method_id(self) -> api.ids_pb2.StripePaymentMethodId: ...
    def __init__(self,
        *,
        stripe_payment_method_id: typing.Optional[api.ids_pb2.StripePaymentMethodId] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["stripe_payment_method_id",b"stripe_payment_method_id"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["stripe_payment_method_id",b"stripe_payment_method_id"]) -> None: ...
global___GetStripePaymentMethodIdResponse = GetStripePaymentMethodIdResponse

class DeleteStripePaymentMethodRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    def __init__(self,
        ) -> None: ...
global___DeleteStripePaymentMethodRequest = DeleteStripePaymentMethodRequest

class DeleteStripePaymentMethodResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    MESSAGE_FIELD_NUMBER: builtins.int
    message: typing.Text
    def __init__(self,
        *,
        message: typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["message",b"message"]) -> None: ...
global___DeleteStripePaymentMethodResponse = DeleteStripePaymentMethodResponse

class GetStripePaymentsListRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    def __init__(self,
        ) -> None: ...
global___GetStripePaymentsListRequest = GetStripePaymentsListRequest

class GetStripePaymentsListResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    PAYMENTS_FIELD_NUMBER: builtins.int
    @property
    def payments(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[api.entity.payment_info_pb2.PaymentInfo]: ...
    def __init__(self,
        *,
        payments: typing.Optional[typing.Iterable[api.entity.payment_info_pb2.PaymentInfo]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["payments",b"payments"]) -> None: ...
global___GetStripePaymentsListResponse = GetStripePaymentsListResponse

class UpdateStripeBillingInfoRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    BILLING_INFO_FIELD_NUMBER: builtins.int
    @property
    def billing_info(self) -> api.entity.billing_info_pb2.BillingInfo: ...
    def __init__(self,
        *,
        billing_info: typing.Optional[api.entity.billing_info_pb2.BillingInfo] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["billing_info",b"billing_info"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["billing_info",b"billing_info"]) -> None: ...
global___UpdateStripeBillingInfoRequest = UpdateStripeBillingInfoRequest

class UpdateStripeBillingInfoResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    MESSAGE_FIELD_NUMBER: builtins.int
    message: typing.Text
    def __init__(self,
        *,
        message: typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["message",b"message"]) -> None: ...
global___UpdateStripeBillingInfoResponse = UpdateStripeBillingInfoResponse

class GetLastPaymentInfoRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    def __init__(self,
        ) -> None: ...
global___GetLastPaymentInfoRequest = GetLastPaymentInfoRequest

class GetLastPaymentInfoResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    PAYMENT_STATUS_FIELD_NUMBER: builtins.int
    ERROR_MESSAGE_FIELD_NUMBER: builtins.int
    payment_status: api.value.payment_status_type_pb2.PaymentStatusType.ValueType
    error_message: typing.Text
    def __init__(self,
        *,
        payment_status: api.value.payment_status_type_pb2.PaymentStatusType.ValueType = ...,
        error_message: typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["error_message",b"error_message","payment_status",b"payment_status"]) -> None: ...
global___GetLastPaymentInfoResponse = GetLastPaymentInfoResponse
