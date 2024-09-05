import xgboost


class ProbabilisticClassifier:
    def predict_probability(self, embeddings):
        raise NotImplementedError
    def fit(self, embeddings, labels):
        raise NotImplementedError
    def save_model(self, directory):
        raise NotImplementedError
    def load_model(self, directory):
        raise NotImplementedError

class XGBoostClassifier(ProbabilisticClassifier):

    def __init__(self):
        self.xgboostclassifier = xgboost.XGBClassifier()

    def predict_probability(self, embeddings):
        return [ x[1] for x in self.xgboostclassifier.predict_proba(embeddings)]

    def fit(self, embeddings, labels):
        self.xgboostclassifier.fit(embeddings, labels)

    def save_model(self, directory):
        self.xgboostclassifier.save_model(directory)

    def load_model(self, directory):
        self.xgboostclassifier.load_model(directory)
