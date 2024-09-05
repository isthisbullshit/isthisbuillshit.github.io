from transformers import pipeline
import xgboost
import os

from probabilisticClassifier import ProbabilisticClassifier, XGBoostClassifier
from embeddingExtractor import AveragingEmbeddingExtractor


class Algorithm:
    def __init__(self, embedding_extractor: AveragingEmbeddingExtractor, classifier: ProbabilisticClassifier):
        self.embedding_extractor = embedding_extractor
        self.classifier = classifier

    def train(self, inputs, labels):
        embeddings = self.embedding_extractor.get_embeddings(inputs)
        self.classifier.fit(embeddings, labels)

    def predict_probability(self, inputs):
        embeddings = self.embedding_extractor.get_embeddings(inputs)
        return self.classifier.predict_probability(embeddings)

    def save_to_directory(self, directory):
        os.makedirs(directory, exist_ok=True)
        self.embedding_extractor.save_to_directory(f"{directory}/extractor")
        if isinstance(self.classifier, xgboost.XGBClassifier):
            self.classifier.save_model(f"{directory}/classifier_xgboost.ubj")

def runExperiment(algorithm, dataset, metrics):
    algorithm.train(dataset.train_inputs(), dataset.train_labels())
    measureQuality(algorithm, dataset, metrics)


def measureQuality(algorithm, dataset, metrics):
    predictions = algorithm.predict_probability(dataset.test_inputs())
    print(f"accuracy is {metrics.measure(predictions, dataset.test_labels())}")

def load_embedding_extractor(directory) -> AveragingEmbeddingExtractor:
    return AveragingEmbeddingExtractor(pipeline("feature-extraction", directory))

def load_algorithm_from_directory(directory):
    extractor_directory = f"{directory}/extractor"
    extractor = load_embedding_extractor(extractor_directory)
    classifier = XGBoostClassifier()
    classifier.load_model(f"{directory}/classifier_xgboost.ubj")
    return Algorithm(extractor, classifier)
        
