import transformers
import torch
import algorithm
import xgboost

from accuracy import Accuracy
from dataset import data, split

model_id = "HuggingFaceTB/SmolLM-135M"

smolLM_135_pipeline = transformers.pipeline(
    "feature-extraction", model="HuggingFaceTB/SmolLM-135M", model_kwargs={"torch_dtype": torch.bfloat16}, device_map="auto",
)

theXGboostEmbeddingExtractorAlgorithm = algorithm.Algorithm(algorithm.PipelineAveragingEmbeddingExtractor(smolLM_135_pipeline), xgboost.XGBClassifier())
algorithm.runExperiment(theXGboostEmbeddingExtractorAlgorithm, algorithm.Dataset(data, split), Accuracy())
algorithm.measureQuality(theXGboostEmbeddingExtractorAlgorithm, algorithm.Dataset(data, split), Accuracy())

theXGboostEmbeddingExtractorAlgorithm.save_to_directory("model")

t = algorithm.load_algorithm_from_directory("model")
algorithm.measureQuality(theXGboostEmbeddingExtractorAlgorithm, algorithm.Dataset(data, split), Accuracy())
