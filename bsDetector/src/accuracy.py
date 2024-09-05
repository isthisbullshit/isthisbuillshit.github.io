class Accuracy():

    def measure(self, predictions, labels):
        correct = 0
        for prediction, label in zip(predictions, labels):
            if prediction == label:
                correct += 1
        return correct / len(predictions)


assert Accuracy().measure([0, 1, 1], [0, 1, 1]) == 1
assert Accuracy().measure([0, 1], [1, 1]) == 0.5
