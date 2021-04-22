"""
提取APK文件的静态特征：
permission
intent
activity
string
api
......
"""
import csv
import os

from androguard.core.bytecodes.apk import APK
from androguard.misc import AnalyzeAPK

import utils

permsList = utils.load_txt("default_permissions.txt")


def extract(a):
    features = []
    # features.extend(extract_package(a))
    features.extend(extract_permission(a))
    # features.extend(extract_activities(a))
    # features.extend(extract_services(a))
    # features.extend(extract_receivers(a))
    # features.extend(extract_providers(a))
    # features.extend(extract_attr_features(a))
    # features.extend(extract_strings())
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
    print(len(a.permission_module.keys()))
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


def feature_to_csv(rootdir, isMalware):
    data = []
    data_path = "./permissions.csv"
    files = os.listdir(rootdir)
    for f in files:
        features = []
        try:
            features.extend(extract(APK(rootdir+"/"+f)))
        except Exception as e:
            print("ERROR: {} {}".format(f, e))
        features.append(isMalware)
        data.append(features)
    with open(data_path, 'a+', newline='') as f:
        writer = csv.writer(f)
        for i in range(len(data)):
            if data[i]:
                writer.writerow(data[i])


if __name__ == '__main__':
    BENIGN_PATH = "./dataset/benign"
    MALWARE_PATH = "./dataset/malware"
    print("————————————————————正在处理良性样本————————————————————————")
    feature_to_csv(BENIGN_PATH, 0)
    print("————————————————————良性样本处理完毕————————————————————————")
    print("————————————————————正在处理恶意样本————————————————————————")
    feature_to_csv(MALWARE_PATH, 1)
    print("————————————————————恶意样本处理完毕————————————————————————")
