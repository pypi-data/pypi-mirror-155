from google.protobuf.empty_pb2 import Empty

import ai.h2o.featurestore.api.v1.RecommendationProtoApi_pb2 as RecommendationApi


class Classifiers:
    def __init__(self, stub):
        self._stub = stub

    def list(self) -> [str]:
        request = Empty()
        response = self._stub.ListRecommendationClassifiers(request)
        return [classifier.name for classifier in response.classifiers]

    def create(self, name: str) -> None:
        request = RecommendationApi.CreateRecommendationClassifierRequest()
        request.classifier_name = name
        self._stub.CreateRecommendationClassifier(request)

    def __repr__(self):
        return "Recommendation classifiers"
