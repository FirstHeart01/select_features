"""
提取APK文件的静态特征：
permission
intent
activity
string
api
......
"""

from androguard.misc import AnalyzeAPK


def extract(a):
    features = []
    features.extend(extract_package(a))
    features.extend(extract_permission(a))
    features.extend(extract_activities(a))
    features.extend(extract_services(a))
    features.extend(extract_receivers(a))
    features.extend(extract_providers(a))
    features.extend(extract_attr_features(a))
    features.extend(extract_strings())
    return features


def extract_package(a):
    features = []
    package_name = a.get_package()
    features.append(package_name)
    return features


def extract_permission(a):
    features = []
    perms = a.get_permissions()
    perms.sort()
    permsList = list(a.permission_module.keys())
    for perm in permsList:
        if perm in perms:
            features.append(1)
        else:
            features.append(0)
    return features


# 需要指定提取哪些activities。
# 以下的特征都需要从数据集样本中提取特征选取数量最多的前多少个特征制成一个列表，放到constants中
# 然后再像上面权限一样提取特征。
# 否则每个样本的特征维度不一样
def extract_activities(a):
    features = []
    activities = a.get_activities()
    for activity in activities:
        intent_filters = a.get_intent_filters('activity', activity)
        if 'action' in intent_filters:
            for intent in intent_filters['action']:
                features.append(intent)
        if 'category' in intent_filters:
            for category in intent_filters['category']:
                features.append(category)
    return features


def extract_services(a):
    features = []
    return features


def extract_receivers(a):
    features = []
    return features


def extract_providers(a):
    features = []
    return features


def extract_attr_features(a):
    features = []
    return features


def extract_strings(dx):
    features = []
    strings = dx.get_strings()
    features.append(len(strings))
    return features


# 看一下字符串的个数
if __name__ == '__main__':
    filepath = "D:/AndroidMalware/benign/app-debug2.apk"
    a, d, dx = AnalyzeAPK(filepath)
    strings = dx.get_strings()
    for i in strings:
        print("{}\n".format(i))
