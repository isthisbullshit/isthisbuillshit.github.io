from transformers import pipeline
import xgboost
import os

from model.embeddingExtractor import PipelineAveragingEmbeddingExtractor


class Algorithm:
    def __init__(self, embedding_extractor: PipelineAveragingEmbeddingExtractor, classifier):
        self.embedding_extractor = embedding_extractor
        self.classifier = classifier

    def train(self, inputs, labels):
        embeddings = self.embedding_extractor.get_embeddings(inputs)
        self.classifier.fit(embeddings, labels)

    def predict(self, inputs):
        embeddings = self.embedding_extractor.get_embeddings(inputs)
        return self.classifier.predict(embeddings)

    def save_to_directory(self, directory):
        os.makedirs(directory, exist_ok=True)
        self.embedding_extractor.save_to_directory(f"{directory}/extractor")
        if isinstance(self.classifier, xgboost.XGBClassifier):
            self.classifier.save_model(f"{directory}/classifier_xgboost.ubj")

def runExperiment(algorithm, dataset, metrics):
    algorithm.train(dataset.train_inputs(), dataset.train_labels())
    measureQuality(algorithm, dataset, metrics)


def measureQuality(algorithm, dataset, metrics):
    predictions = algorithm.predict(dataset.test_inputs())
    print(f"accuracy is {metrics.measure(predictions, dataset.test_labels())}")

def load_embedding_extractor(directory) -> PipelineAveragingEmbeddingExtractor:
    return PipelineAveragingEmbeddingExtractor(pipeline("feature-extraction",directory))

def load_algorithm_from_directory(directory):
    extractor_directory = f"{directory}/extractor"
    extractor = load_embedding_extractor(extractor_directory)
    classifier = xgboost.XGBClassifier()
    classifier.load_model(f"{directory}/classifier_xgboost.ubj")
    return Algorithm(extractor, classifier)
        
