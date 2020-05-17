import pandas as pd
from sklearn import metrics
import numpy as np

import DoubanData.tools as tool
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier


def split_data():
    data = pd.read_csv("train.csv")
    train, test = train_test_split(
        data,
        test_size=0.2,
        random_state=20
    )
    tool.truncatefile("train_data.csv")
    tool.truncatefile("test_data.csv")
    train.to_csv("train_data.csv", index="None")
    test.to_csv("test_data.csv", index="None")
    return train, test


class Model(object):
    def __init__(self, lr, ne, md):
        self.lr = lr
        self.ne = ne
        self.md = md
        self.train_data, self.test_data = split_data()
        self.gbdt = self._train_model()

    def _train_model(self):
        label = "click"
        feature = [x for x in self.train_data.columns if x not in [label]]
        x_train = self.train_data[feature]
        y_train = self.train_data[label]
        gbdt = GradientBoostingClassifier(learning_rate=self.lr, n_estimators=self.ne, max_depth=self.md)
        gbdt.fit(x_train, y_train)
        return gbdt

    def test_model(self):
        label = "click"
        feature = [x for x in self.train_data.columns if x not in [label]]
        x_test = self.test_data[feature]
        y_test = self.test_data[label]
        y_pred = self.gbdt.predict_proba(x_test)
        new_y_pred = list()
        cnt = 0
        for pred in y_pred:
            if pred[1] < 0.5:
                cnt = cnt + 1
            new_y_pred.append(1 if pred[1] > 0.5 else 0)
        print(cnt)
        mse = metrics.mean_squared_error(y_test, new_y_pred)
        print("MSE: %.4f" % mse)
        accuracy = metrics.accuracy_score(y_test.values, new_y_pred)
        print("Accuracy : %.4g" % accuracy)
        auc = metrics.roc_auc_score(y_test.values, new_y_pred)
        print("AUC Score : %.4g" % auc)


if __name__ == "__main__":
    for i in np.arange(10, 90, 1):
        print(i/100)
        model = Model(lr=i/100, ne=80, md=3)
        model.test_model()
    # model = Model()
    # model.test_model()

