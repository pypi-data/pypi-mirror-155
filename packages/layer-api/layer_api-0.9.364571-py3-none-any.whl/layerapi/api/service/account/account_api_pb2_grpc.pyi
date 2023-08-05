"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import abc
import layerapi.api.service.account.account_api_pb2
import grpc

class AccountAPIStub:
    def __init__(self, channel: grpc.Channel) -> None: ...
    GetAccountViewByName: grpc.UnaryUnaryMultiCallable[
        api.service.account.account_api_pb2.GetAccountViewByNameRequest,
        api.service.account.account_api_pb2.GetAccountViewByNameResponse]

    GetAccountViewById: grpc.UnaryUnaryMultiCallable[
        api.service.account.account_api_pb2.GetAccountViewByIdRequest,
        api.service.account.account_api_pb2.GetAccountViewByIdResponse]

    GetMyAccountView: grpc.UnaryUnaryMultiCallable[
        api.service.account.account_api_pb2.GetMyAccountViewRequest,
        api.service.account.account_api_pb2.GetMyAccountViewResponse]

    CreateAccount: grpc.UnaryUnaryMultiCallable[
        api.service.account.account_api_pb2.CreateAccountRequest,
        api.service.account.account_api_pb2.CreateAccountResponse]

    CreateApiKey: grpc.UnaryUnaryMultiCallable[
        api.service.account.account_api_pb2.CreateApiKeyRequest,
        api.service.account.account_api_pb2.CreateApiKeyResponse]

    ToggleDatasetLikeByMyAccount: grpc.UnaryUnaryMultiCallable[
        api.service.account.account_api_pb2.ToggleDatasetLikeByMyAccountRequest,
        api.service.account.account_api_pb2.ToggleDatasetLikeByMyAccountResponse]

    GetDatasetLikedByMyAccount: grpc.UnaryUnaryMultiCallable[
        api.service.account.account_api_pb2.GetDatasetLikedByMyAccountRequest,
        api.service.account.account_api_pb2.GetDatasetLikedByMyAccountResponse]

    ToggleModelLikeByMyAccount: grpc.UnaryUnaryMultiCallable[
        api.service.account.account_api_pb2.ToggleModelLikeByMyAccountRequest,
        api.service.account.account_api_pb2.ToggleModelLikeByMyAccountResponse]

    GetModelLikedByMyAccount: grpc.UnaryUnaryMultiCallable[
        api.service.account.account_api_pb2.GetModelLikedByMyAccountRequest,
        api.service.account.account_api_pb2.GetModelLikedByMyAccountResponse]

    ToggleProjectLikeByMyAccount: grpc.UnaryUnaryMultiCallable[
        api.service.account.account_api_pb2.ToggleProjectLikeByMyAccountRequest,
        api.service.account.account_api_pb2.ToggleProjectLikeByMyAccountResponse]

    GetProjectLikedByMyAccount: grpc.UnaryUnaryMultiCallable[
        api.service.account.account_api_pb2.GetProjectLikedByMyAccountRequest,
        api.service.account.account_api_pb2.GetProjectLikedByMyAccountResponse]


class AccountAPIServicer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def GetAccountViewByName(self,
        request: api.service.account.account_api_pb2.GetAccountViewByNameRequest,
        context: grpc.ServicerContext,
    ) -> api.service.account.account_api_pb2.GetAccountViewByNameResponse: ...

    @abc.abstractmethod
    def GetAccountViewById(self,
        request: api.service.account.account_api_pb2.GetAccountViewByIdRequest,
        context: grpc.ServicerContext,
    ) -> api.service.account.account_api_pb2.GetAccountViewByIdResponse: ...

    @abc.abstractmethod
    def GetMyAccountView(self,
        request: api.service.account.account_api_pb2.GetMyAccountViewRequest,
        context: grpc.ServicerContext,
    ) -> api.service.account.account_api_pb2.GetMyAccountViewResponse: ...

    @abc.abstractmethod
    def CreateAccount(self,
        request: api.service.account.account_api_pb2.CreateAccountRequest,
        context: grpc.ServicerContext,
    ) -> api.service.account.account_api_pb2.CreateAccountResponse: ...

    @abc.abstractmethod
    def CreateApiKey(self,
        request: api.service.account.account_api_pb2.CreateApiKeyRequest,
        context: grpc.ServicerContext,
    ) -> api.service.account.account_api_pb2.CreateApiKeyResponse: ...

    @abc.abstractmethod
    def ToggleDatasetLikeByMyAccount(self,
        request: api.service.account.account_api_pb2.ToggleDatasetLikeByMyAccountRequest,
        context: grpc.ServicerContext,
    ) -> api.service.account.account_api_pb2.ToggleDatasetLikeByMyAccountResponse: ...

    @abc.abstractmethod
    def GetDatasetLikedByMyAccount(self,
        request: api.service.account.account_api_pb2.GetDatasetLikedByMyAccountRequest,
        context: grpc.ServicerContext,
    ) -> api.service.account.account_api_pb2.GetDatasetLikedByMyAccountResponse: ...

    @abc.abstractmethod
    def ToggleModelLikeByMyAccount(self,
        request: api.service.account.account_api_pb2.ToggleModelLikeByMyAccountRequest,
        context: grpc.ServicerContext,
    ) -> api.service.account.account_api_pb2.ToggleModelLikeByMyAccountResponse: ...

    @abc.abstractmethod
    def GetModelLikedByMyAccount(self,
        request: api.service.account.account_api_pb2.GetModelLikedByMyAccountRequest,
        context: grpc.ServicerContext,
    ) -> api.service.account.account_api_pb2.GetModelLikedByMyAccountResponse: ...

    @abc.abstractmethod
    def ToggleProjectLikeByMyAccount(self,
        request: api.service.account.account_api_pb2.ToggleProjectLikeByMyAccountRequest,
        context: grpc.ServicerContext,
    ) -> api.service.account.account_api_pb2.ToggleProjectLikeByMyAccountResponse: ...

    @abc.abstractmethod
    def GetProjectLikedByMyAccount(self,
        request: api.service.account.account_api_pb2.GetProjectLikedByMyAccountRequest,
        context: grpc.ServicerContext,
    ) -> api.service.account.account_api_pb2.GetProjectLikedByMyAccountResponse: ...


def add_AccountAPIServicer_to_server(servicer: AccountAPIServicer, server: grpc.Server) -> None: ...
