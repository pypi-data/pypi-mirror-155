"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import abc
import layerapi.api.service.modelcatalog.model_catalog_api_pb2
import grpc

class ModelCatalogAPIStub:
    def __init__(self, channel: grpc.Channel) -> None: ...
    GetModel: grpc.UnaryUnaryMultiCallable[
        api.service.modelcatalog.model_catalog_api_pb2.GetModelRequest,
        api.service.modelcatalog.model_catalog_api_pb2.GetModelResponse]

    GetModels: grpc.UnaryUnaryMultiCallable[
        api.service.modelcatalog.model_catalog_api_pb2.GetModelsRequest,
        api.service.modelcatalog.model_catalog_api_pb2.GetModelsResponse]

    GetModelByPath: grpc.UnaryUnaryMultiCallable[
        api.service.modelcatalog.model_catalog_api_pb2.GetModelByPathRequest,
        api.service.modelcatalog.model_catalog_api_pb2.GetModelByPathResponse]

    UpdateModel: grpc.UnaryUnaryMultiCallable[
        api.service.modelcatalog.model_catalog_api_pb2.UpdateModelRequest,
        api.service.modelcatalog.model_catalog_api_pb2.UpdateModelResponse]

    GetModelVersion: grpc.UnaryUnaryMultiCallable[
        api.service.modelcatalog.model_catalog_api_pb2.GetModelVersionRequest,
        api.service.modelcatalog.model_catalog_api_pb2.GetModelVersionResponse]

    GetModelVersionIdByName: grpc.UnaryUnaryMultiCallable[
        api.service.modelcatalog.model_catalog_api_pb2.GetModelVersionIdByNameRequest,
        api.service.modelcatalog.model_catalog_api_pb2.GetModelVersionIdByNameResponse]

    GetModelTrain: grpc.UnaryUnaryMultiCallable[
        api.service.modelcatalog.model_catalog_api_pb2.GetModelTrainRequest,
        api.service.modelcatalog.model_catalog_api_pb2.GetModelTrainResponse]

    LoadModelTrainDataByPath: grpc.UnaryUnaryMultiCallable[
        api.service.modelcatalog.model_catalog_api_pb2.LoadModelTrainDataByPathRequest,
        api.service.modelcatalog.model_catalog_api_pb2.LoadModelTrainDataByPathResponse]

    GetModelVersions: grpc.UnaryUnaryMultiCallable[
        api.service.modelcatalog.model_catalog_api_pb2.GetModelVersionsRequest,
        api.service.modelcatalog.model_catalog_api_pb2.GetModelVersionsResponse]

    GetModelTrains: grpc.UnaryUnaryMultiCallable[
        api.service.modelcatalog.model_catalog_api_pb2.GetModelTrainsRequest,
        api.service.modelcatalog.model_catalog_api_pb2.GetModelTrainsResponse]

    UpdateModelTrainDescription: grpc.UnaryUnaryMultiCallable[
        api.service.modelcatalog.model_catalog_api_pb2.UpdateModelTrainDescriptionRequest,
        api.service.modelcatalog.model_catalog_api_pb2.UpdateModelTrainDescriptionResponse]

    CreateModelTrain: grpc.UnaryUnaryMultiCallable[
        api.service.modelcatalog.model_catalog_api_pb2.CreateModelTrainRequest,
        api.service.modelcatalog.model_catalog_api_pb2.CreateModelTrainResponse]

    CreateModelTrainFromVersionId: grpc.UnaryUnaryMultiCallable[
        api.service.modelcatalog.model_catalog_api_pb2.CreateModelTrainFromVersionIdRequest,
        api.service.modelcatalog.model_catalog_api_pb2.CreateModelTrainFromVersionIdResponse]

    StartModelTrain: grpc.UnaryUnaryMultiCallable[
        api.service.modelcatalog.model_catalog_api_pb2.StartModelTrainRequest,
        api.service.modelcatalog.model_catalog_api_pb2.StartModelTrainResponse]

    GetModelTrainStorageConfiguration: grpc.UnaryUnaryMultiCallable[
        api.service.modelcatalog.model_catalog_api_pb2.GetModelTrainStorageConfigurationRequest,
        api.service.modelcatalog.model_catalog_api_pb2.GetModelTrainStorageConfigurationResponse]

    CompleteModelTrain: grpc.UnaryUnaryMultiCallable[
        api.service.modelcatalog.model_catalog_api_pb2.CompleteModelTrainRequest,
        api.service.modelcatalog.model_catalog_api_pb2.CompleteModelTrainResponse]

    SetDefaultModelTrain: grpc.UnaryUnaryMultiCallable[
        api.service.modelcatalog.model_catalog_api_pb2.SetDefaultModelTrainRequest,
        api.service.modelcatalog.model_catalog_api_pb2.SetDefaultModelTrainResponse]

    CreateModelVersion: grpc.UnaryUnaryMultiCallable[
        api.service.modelcatalog.model_catalog_api_pb2.CreateModelVersionRequest,
        api.service.modelcatalog.model_catalog_api_pb2.CreateModelVersionResponse]

    SetDefaultModelVersion: grpc.UnaryUnaryMultiCallable[
        api.service.modelcatalog.model_catalog_api_pb2.SetDefaultModelVersionRequest,
        api.service.modelcatalog.model_catalog_api_pb2.SetDefaultModelVersionResponse]

    UpdateModelTrainStatus: grpc.UnaryUnaryMultiCallable[
        api.service.modelcatalog.model_catalog_api_pb2.UpdateModelTrainStatusRequest,
        api.service.modelcatalog.model_catalog_api_pb2.UpdateModelTrainStatusResponse]

    SetHyperparameterTuningId: grpc.UnaryUnaryMultiCallable[
        api.service.modelcatalog.model_catalog_api_pb2.SetHyperparameterTuningIdRequest,
        api.service.modelcatalog.model_catalog_api_pb2.SetHyperparameterTuningIdResponse]

    StoreTrainingMetadata: grpc.UnaryUnaryMultiCallable[
        api.service.modelcatalog.model_catalog_api_pb2.StoreTrainingMetadataRequest,
        api.service.modelcatalog.model_catalog_api_pb2.StoreTrainingMetadataResponse]

    GetTrainingMetadata: grpc.UnaryUnaryMultiCallable[
        api.service.modelcatalog.model_catalog_api_pb2.GetTrainingMetadataRequest,
        api.service.modelcatalog.model_catalog_api_pb2.GetTrainingMetadataResponse]

    RemoveAllModelsByProjectId: grpc.UnaryUnaryMultiCallable[
        api.service.modelcatalog.model_catalog_api_pb2.RemoveAllModelsByProjectIdRequest,
        api.service.modelcatalog.model_catalog_api_pb2.RemoveAllModelsByProjectIdResponse]

    GetModelTrainByPath: grpc.UnaryUnaryMultiCallable[
        api.service.modelcatalog.model_catalog_api_pb2.GetModelTrainByPathRequest,
        api.service.modelcatalog.model_catalog_api_pb2.GetModelTrainByPathResponse]

    IncrementModelLikes: grpc.UnaryUnaryMultiCallable[
        api.service.modelcatalog.model_catalog_api_pb2.IncrementModelLikesRequest,
        api.service.modelcatalog.model_catalog_api_pb2.IncrementModelLikesResponse]

    DecrementModelLikes: grpc.UnaryUnaryMultiCallable[
        api.service.modelcatalog.model_catalog_api_pb2.DecrementModelLikesRequest,
        api.service.modelcatalog.model_catalog_api_pb2.DecrementModelLikesResponse]


class ModelCatalogAPIServicer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def GetModel(self,
        request: api.service.modelcatalog.model_catalog_api_pb2.GetModelRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modelcatalog.model_catalog_api_pb2.GetModelResponse: ...

    @abc.abstractmethod
    def GetModels(self,
        request: api.service.modelcatalog.model_catalog_api_pb2.GetModelsRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modelcatalog.model_catalog_api_pb2.GetModelsResponse: ...

    @abc.abstractmethod
    def GetModelByPath(self,
        request: api.service.modelcatalog.model_catalog_api_pb2.GetModelByPathRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modelcatalog.model_catalog_api_pb2.GetModelByPathResponse: ...

    @abc.abstractmethod
    def UpdateModel(self,
        request: api.service.modelcatalog.model_catalog_api_pb2.UpdateModelRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modelcatalog.model_catalog_api_pb2.UpdateModelResponse: ...

    @abc.abstractmethod
    def GetModelVersion(self,
        request: api.service.modelcatalog.model_catalog_api_pb2.GetModelVersionRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modelcatalog.model_catalog_api_pb2.GetModelVersionResponse: ...

    @abc.abstractmethod
    def GetModelVersionIdByName(self,
        request: api.service.modelcatalog.model_catalog_api_pb2.GetModelVersionIdByNameRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modelcatalog.model_catalog_api_pb2.GetModelVersionIdByNameResponse: ...

    @abc.abstractmethod
    def GetModelTrain(self,
        request: api.service.modelcatalog.model_catalog_api_pb2.GetModelTrainRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modelcatalog.model_catalog_api_pb2.GetModelTrainResponse: ...

    @abc.abstractmethod
    def LoadModelTrainDataByPath(self,
        request: api.service.modelcatalog.model_catalog_api_pb2.LoadModelTrainDataByPathRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modelcatalog.model_catalog_api_pb2.LoadModelTrainDataByPathResponse: ...

    @abc.abstractmethod
    def GetModelVersions(self,
        request: api.service.modelcatalog.model_catalog_api_pb2.GetModelVersionsRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modelcatalog.model_catalog_api_pb2.GetModelVersionsResponse: ...

    @abc.abstractmethod
    def GetModelTrains(self,
        request: api.service.modelcatalog.model_catalog_api_pb2.GetModelTrainsRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modelcatalog.model_catalog_api_pb2.GetModelTrainsResponse: ...

    @abc.abstractmethod
    def UpdateModelTrainDescription(self,
        request: api.service.modelcatalog.model_catalog_api_pb2.UpdateModelTrainDescriptionRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modelcatalog.model_catalog_api_pb2.UpdateModelTrainDescriptionResponse: ...

    @abc.abstractmethod
    def CreateModelTrain(self,
        request: api.service.modelcatalog.model_catalog_api_pb2.CreateModelTrainRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modelcatalog.model_catalog_api_pb2.CreateModelTrainResponse: ...

    @abc.abstractmethod
    def CreateModelTrainFromVersionId(self,
        request: api.service.modelcatalog.model_catalog_api_pb2.CreateModelTrainFromVersionIdRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modelcatalog.model_catalog_api_pb2.CreateModelTrainFromVersionIdResponse: ...

    @abc.abstractmethod
    def StartModelTrain(self,
        request: api.service.modelcatalog.model_catalog_api_pb2.StartModelTrainRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modelcatalog.model_catalog_api_pb2.StartModelTrainResponse: ...

    @abc.abstractmethod
    def GetModelTrainStorageConfiguration(self,
        request: api.service.modelcatalog.model_catalog_api_pb2.GetModelTrainStorageConfigurationRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modelcatalog.model_catalog_api_pb2.GetModelTrainStorageConfigurationResponse: ...

    @abc.abstractmethod
    def CompleteModelTrain(self,
        request: api.service.modelcatalog.model_catalog_api_pb2.CompleteModelTrainRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modelcatalog.model_catalog_api_pb2.CompleteModelTrainResponse: ...

    @abc.abstractmethod
    def SetDefaultModelTrain(self,
        request: api.service.modelcatalog.model_catalog_api_pb2.SetDefaultModelTrainRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modelcatalog.model_catalog_api_pb2.SetDefaultModelTrainResponse: ...

    @abc.abstractmethod
    def CreateModelVersion(self,
        request: api.service.modelcatalog.model_catalog_api_pb2.CreateModelVersionRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modelcatalog.model_catalog_api_pb2.CreateModelVersionResponse: ...

    @abc.abstractmethod
    def SetDefaultModelVersion(self,
        request: api.service.modelcatalog.model_catalog_api_pb2.SetDefaultModelVersionRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modelcatalog.model_catalog_api_pb2.SetDefaultModelVersionResponse: ...

    @abc.abstractmethod
    def UpdateModelTrainStatus(self,
        request: api.service.modelcatalog.model_catalog_api_pb2.UpdateModelTrainStatusRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modelcatalog.model_catalog_api_pb2.UpdateModelTrainStatusResponse: ...

    @abc.abstractmethod
    def SetHyperparameterTuningId(self,
        request: api.service.modelcatalog.model_catalog_api_pb2.SetHyperparameterTuningIdRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modelcatalog.model_catalog_api_pb2.SetHyperparameterTuningIdResponse: ...

    @abc.abstractmethod
    def StoreTrainingMetadata(self,
        request: api.service.modelcatalog.model_catalog_api_pb2.StoreTrainingMetadataRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modelcatalog.model_catalog_api_pb2.StoreTrainingMetadataResponse: ...

    @abc.abstractmethod
    def GetTrainingMetadata(self,
        request: api.service.modelcatalog.model_catalog_api_pb2.GetTrainingMetadataRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modelcatalog.model_catalog_api_pb2.GetTrainingMetadataResponse: ...

    @abc.abstractmethod
    def RemoveAllModelsByProjectId(self,
        request: api.service.modelcatalog.model_catalog_api_pb2.RemoveAllModelsByProjectIdRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modelcatalog.model_catalog_api_pb2.RemoveAllModelsByProjectIdResponse: ...

    @abc.abstractmethod
    def GetModelTrainByPath(self,
        request: api.service.modelcatalog.model_catalog_api_pb2.GetModelTrainByPathRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modelcatalog.model_catalog_api_pb2.GetModelTrainByPathResponse: ...

    @abc.abstractmethod
    def IncrementModelLikes(self,
        request: api.service.modelcatalog.model_catalog_api_pb2.IncrementModelLikesRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modelcatalog.model_catalog_api_pb2.IncrementModelLikesResponse: ...

    @abc.abstractmethod
    def DecrementModelLikes(self,
        request: api.service.modelcatalog.model_catalog_api_pb2.DecrementModelLikesRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modelcatalog.model_catalog_api_pb2.DecrementModelLikesResponse: ...


def add_ModelCatalogAPIServicer_to_server(servicer: ModelCatalogAPIServicer, server: grpc.Server) -> None: ...
