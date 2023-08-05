"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import abc
import layerapi.api.service.modeltraining.model_training_worker_api_pb2
import grpc

class ModelTrainingWorkerAPIStub:
    def __init__(self, channel: grpc.Channel) -> None: ...
    StartExecution: grpc.UnaryUnaryMultiCallable[
        api.service.modeltraining.model_training_worker_api_pb2.StartExecutionRequest,
        api.service.modeltraining.model_training_worker_api_pb2.StartExecutionResponse]

    StartHyperparameterTuningExecution: grpc.UnaryUnaryMultiCallable[
        api.service.modeltraining.model_training_worker_api_pb2.StartHyperparameterTuningExecutionRequest,
        api.service.modeltraining.model_training_worker_api_pb2.StartHyperparameterTuningExecutionResponse]


class ModelTrainingWorkerAPIServicer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def StartExecution(self,
        request: api.service.modeltraining.model_training_worker_api_pb2.StartExecutionRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modeltraining.model_training_worker_api_pb2.StartExecutionResponse: ...

    @abc.abstractmethod
    def StartHyperparameterTuningExecution(self,
        request: api.service.modeltraining.model_training_worker_api_pb2.StartHyperparameterTuningExecutionRequest,
        context: grpc.ServicerContext,
    ) -> api.service.modeltraining.model_training_worker_api_pb2.StartHyperparameterTuningExecutionResponse: ...


def add_ModelTrainingWorkerAPIServicer_to_server(servicer: ModelTrainingWorkerAPIServicer, server: grpc.Server) -> None: ...
