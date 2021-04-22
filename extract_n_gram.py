"""
此部分写：
n-gram特征提取
"""
import os
import subprocess
import pandas as pd
from infrastructure.fileutils import DataFile
from infrastructure.mydict import MyDict
from infrastructure.ware import Ware


def disassemble(fromPath, toPath, num, start=0):
    files = os.listdir(fromPath)
    files = files[start:num]
    total = len(files)
    for i, file in enumerate(files):
        fullFromPath = os.path.join(fromPath, file)
        fullToPath = os.path.join(toPath, file)
        command = "apktool d " + fullFromPath + " -o " + fullToPath
        subprocess.call(command, shell=True)
        print("已反汇编", i + 1, "个APK应用")
        print("百分比为:", (i + 1) * 100 / total, "%")


def extract_raw_opcode_features(rootdir, isMalware, opcode_csv_root):
    opcode_csv_filepath = DataFile(opcode_csv_root)
    wares = os.listdir(rootdir)
    total = len(wares)
    for i, ware in enumerate(wares):
        warePath = os.path.join(rootdir, ware)
        ware = Ware(warePath, isMalware)
        ware.opcode_extract(opcode_csv_filepath)
        print("已提取", i + 1, "个APK文件特征")
        print("百分比为:", (i + 1) * 100 / total, "%")
    opcode_csv_filepath.close()


def n_gram(n, mDict, origin_data, opcode_feature):
    for i, opcode in enumerate(opcode_feature):
        mDict.newLayer()
        if not type(opcode) == list:
            continue
        for method in opcode:
            length = len(method)
            if length < n:
                continue
            for start in range(length - (n - 1)):
                end = start + n
                mDict.mark(method[start:end])
        print("已完成", i + 1, "个APK")
        print("百分比为:", (i + 1) * 100 / len(opcode_feature), "%")
    result = mDict.dict
    pd.DataFrame(result, index=origin_data.index) \
        .to_csv("./" + str(n) + "_gram.csv", index=False)


# def extract_n_gram(benign_root, malware_root, benign_smalis_root, malware_smalis_root,
#                    opcode_csv_root, mDict, origin_data, opcode_feature, n=4):
#     disassemble(benign_root, ".\\smalis\\benign", 180)
#     disassemble(malware_root, ".\\smalis\\malware", 180)
#     extract_raw_opcode_features(benign_smalis_root, 0, opcode_csv_root)
#     extract_raw_opcode_features(malware_smalis_root, 1, opcode_csv_root)
#     n_gram(n, mDict, origin_data, opcode_feature)


# 测试
if __name__ == '__main__':
    # 良性APK文件目录
    benign_root = "./dataset/benign"
    # 恶意APK文件目录
    malware_root = "./dataset/malware"
    # 良性软件反汇编目录
    benign_smalis_root = "./smalis/benign"
    # 恶性软件反汇编目录
    malware_smalis_root = "./smalis/malware"
    # 还未进行n_gram的最初数据集的位置
    opcode_csv_root = "./raw_opcode.csv"
    # 封装的Dict
    mDict = MyDict()
    disassemble(benign_root, ".\\smalis\\benign", 180)
    disassemble(malware_root, ".\\smalis\\malware", 180)
    # 追加提取原始特征
    extract_raw_opcode_features(benign_smalis_root, 0, opcode_csv_root)
    extract_raw_opcode_features(malware_smalis_root, 1, opcode_csv_root)
    # 读取原始数据集
    origin_data = pd.read_csv("raw_opcode.csv")
    # 分割n_gram，得到指令集
    opcode_feature = origin_data["Feature"].str.split("|")
    n_gram(4, mDict, origin_data, opcode_feature)
