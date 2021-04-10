"""
n_gram特征检测
"""

from sklearn.ensemble import RandomForestClassifier as RF
from sklearn.model_selection import cross_val_score
import pandas as pd


train_feature = pd.read_csv('./4_gram.csv')
data = pd.read_csv('./raw_opcode.csv')
labels = data['isMalware']


train_feature = train_feature.iloc[:,:].values
# RF模型
srf = RF(n_estimators=500, n_jobs=-1)
# 十倍交叉检验
clf_s = cross_val_score(srf, train_feature, labels, cv=10)