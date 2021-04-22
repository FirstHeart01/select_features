from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
import pandas as pd
import numpy as np
import utils

# train_feature = pd.read_csv('./4_gram.csv')
# data = pd.read_csv('./raw_opcode.csv')
# labels = data['isMalware']

RandomForest = RandomForestClassifier(random_state=0, n_estimators=450)
SVC = SVC(kernel='rbf', probability=True, gamma='auto')
KNN = KNeighborsClassifier()
GaussianNB = GaussianNB()
DT = tree.DecisionTreeClassifier()


# state: 存储选取特征的下标
# data_path：处理好后的带有标签的特征数据集
# classifier：分类器，默认为SVC
# return：模型正确率
def get_accuracy_sorce(state, data_path, classifier=SVC):
    # count为选取特征个数。
    count = len(state)
    # data从csv文件中读取
    data = utils.load_csv(data_path)
    # len(data)减去1,防止标签被删除
    for i in reversed(range(len(data)-1)):
        # 如果第i个特征没有选取,data中第i列全部删除
        if i not in state:
            for index in range(len(data)):
                del data[index][i]
    if count == 0:
        return 0
    # data数据中的最后一列是标签
    label = np.array(data)[:, -1]
    # 取出data除最后一列的所有特征数据
    data = np.array(data)[:, :-1]
    return classify(data, label, classifier)

def classify(data, label, classifier):
    x_train, x_test, y_train, y_test = train_test_split(data, label, test_size=0.2, random_state=0)
    classifier.fit(x_train, y_train)

    y_predict = classifier.predict(x_test)
    result = metrics.accuracy_score(y_test, y_predict)
    return result


# 十倍交叉检验
# clf_s = cross_val_score(RandomForest, train_feature, labels, cv=10)
