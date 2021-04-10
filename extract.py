"""
建立一个Extract对象
直接提取所有特征
"""
import extract_statistic_features as Statistic
import extract_n_gram as NGram

class Extract:
    def __init__(self, N = 4):
        self.N = N
        return

    def __call__(self, a):
        self.features = []
        self.features.extend(Statistic.extract(a))
        self.features.extend(NGram.extract_n_gram())
        return
