import tempfile
import unittest

import xgboost

from algorithm import Algorithm, load_algorithm_from_directory, PipelineAveragingEmbeddingExtractor, Dataset
from transformers import pipeline
import dataset


class TestStringMethods(unittest.TestCase):

    def test_algorithm_save_load(self):
        ds = Dataset([("a",0), ("b",1), ("c",0)], [1,1,1])
        the_pipe = PipelineAveragingEmbeddingExtractor(pipeline(
            "feature-extraction", "../model/extractor"
        ))
        algo = Algorithm(the_pipe, xgboost.XGBClassifier())

        algo.train(ds.train_inputs(), ds.train_labels())

        with tempfile.TemporaryDirectory() as td:
            algo.save_to_directory(td)
            load_algorithm_from_directory(td)

