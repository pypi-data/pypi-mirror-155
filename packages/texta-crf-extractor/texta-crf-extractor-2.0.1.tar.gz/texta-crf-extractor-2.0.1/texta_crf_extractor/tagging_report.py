from sklearn.metrics import confusion_matrix, precision_score, recall_score, roc_curve, auc, f1_score
import json

class TaggingReport:

    def __init__(self, y_test: list, y_pred: list, classes: list, average: str = "macro"):
        self.average = average
        self.classes = classes

        # flatten y
        y_pred = [j for sub in y_pred for j in sub]
        y_test = [j for sub in y_test for j in sub]

        self.precision = precision_score(y_test, y_pred, average=self.average)
        self.f1_score = f1_score(y_test, y_pred, average=self.average)
        self.confusion = confusion_matrix(y_test, y_pred)
        self.recall = recall_score(y_test, y_pred, average=self.average)

    def to_dict(self):
        return {
            "f1_score": round(self.f1_score, 5),
            "precision": round(self.precision, 5),
            "recall": round(self.recall, 5),
            "confusion_matrix": self.confusion.tolist(),
            "classes": self.classes
        }
