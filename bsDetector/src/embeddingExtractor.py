import numpy as np


class AveragingEmbeddingExtractor:

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

assert np.array_equal(AveragingEmbeddingExtractor(None).aggregate(embeddings), [[0.5, 1, 0], [0, 1, 1]])
assert np.array_equal(AveragingEmbeddingExtractor(None).aggregate(embeddings2), [[0.5, 1, 0], [0, 1, 1]])
