class Accuracy():

    def measure(self, predictions, labels):
        correct = 0
        for prediction, label in zip(predictions, labels):
            if prediction == label:
                correct += 1
        return correct / len(predictions)


assert Accuracy().measure([0, 1, 1], [0, 1, 1]) == 1
assert Accuracy().measure([0, 1], [1, 1]) == 0.5


class Dataset:
    def __init__(self, dataset, split):
        self.dataset = dataset
        self.split = split

    def train_inputs(self):
        return [self.dataset[idx][0] for idx, val in enumerate(self.split) if val]

    def train_labels(self):
        return [self.dataset[idx][1] for idx, val in enumerate(self.split) if val]

    def test_inputs(self):
        return [self.dataset[idx][0] for idx, val in enumerate(self.split) if not val]

    def test_labels(self):
        return [self.dataset[idx][1] for idx, val in enumerate(self.split) if not val]


test_data = [
    ("a", 0),
    ("b", 0),
    ("c", False),
    ("d", 0),
]

assert np.array_equal(Dataset(test_data, [True, True, False, False]).train_inputs(), ["a", "b"])
assert np.array_equal(Dataset(test_data, [True, True, False, False]).train_labels(), [0, 0])


class PipelineAveragingEmbeddingExtractor:

    def __init__(self, pipeline):
        self.pipeline = pipeline

    def get_embeddings(self, inputs):
        return self.aggregate(self.pipeline(inputs))

    def aggregate(self, encodings):
        encoding_arrays = [np.array(x, ndmin=4) for x in encodings]
        return np.array([x.mean(axis=x.ndim - 2).reshape(-1) for x in encoding_arrays])

    def save_to_directory(self, location):
        self.pipeline.save_pretrained(location)


embeddings = [
    [[0, 1, 0], [1, 1, 0]],
    [[0, 1, 1]],
]

embeddings2 = [
    [[[0, 1, 0], [1, 1, 0]]],
    [[0, 1, 1]],
]

assert np.array_equal(PipelineAveragingEmbeddingExtractor(None).aggregate(embeddings), [[0.5, 1, 0], [0, 1, 1]])
assert np.array_equal(PipelineAveragingEmbeddingExtractor(None).aggregate(embeddings2), [[0.5, 1, 0], [0, 1, 1]])


class Algorithm:
    def __init__(self, embedding_extractor, classifier):
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
    predictions = algorithm.predict(dataset.test_inputs())
    # print(list(zip(dataset.test_inputs(), predictions, dataset.test_labels())))
    print(f"accuracy is {metrics.measure(predictions, dataset.test_labels())}")

