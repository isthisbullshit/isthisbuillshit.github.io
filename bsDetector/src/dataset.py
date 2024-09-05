import numpy as np


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

