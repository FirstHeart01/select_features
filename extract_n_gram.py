"""
此部分写：
n-gram特征提取
TF-IDF文档频率的计算
"""
import os
import subprocess
import pandas as pd
from infrastructure.fileutils import DataFile
from infrastructure.mydict import MyDict
from infrastructure.ware import Ware

# 良性APK文件目录
benign_root = r"D:\AndroidMalware\benign"
# 恶意APK文件目录
malware_root = r"D:\AndroidMalware\malware"
# 良性软件反汇编目录
benign_smalis_root = "./smalis/benign"
# 恶性软件反汇编目录
malware_smalis_root = "./smalis/malware"
# 还未进行n_gram的最初数据集
opcode_csv_filepath = DataFile("./raw_opcode.csv")


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


def extract_raw_opcode_features(rootdir, isMalware):
    wares = os.listdir(rootdir)
    total = len(wares)
    for i, ware in enumerate(wares):
        warePath = os.path.join(rootdir, ware)
        ware = Ware(warePath, isMalware)
        ware.opcode_extract(opcode_csv_filepath)
        print("已提取", i + 1, "个APK文件特征")
        print("百分比为:", (i + 1) * 100 / total, "%")


# 封装的Dict
mDict = MyDict()
# 读取原始n_gram数据集
origin_data = pd.read_csv("raw_opcode.csv")
# 分割n_gram，得到指令集
opcode_feature = origin_data["Feature"].str.split("|")
total = len(opcode_feature)


def n_gram(n):
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
        print("百分比为:", (i + 1) * 100 / total, "%")
    result = mDict.dict
    pd.DataFrame(result, index=origin_data.index) \
        .to_csv("./" + str(n) + "_gram.csv", index=False)


def extract_n_gram(n=4):
    disassemble(benign_root, ".\\smalis\\benign", 600)
    disassemble(malware_root, ".\\smalis\\malware", 600)
    extract_raw_opcode_features(benign_smalis_root, 0)
    extract_raw_opcode_features(malware_smalis_root, 1)
    opcode_csv_filepath.close()
    n_gram(n)


# 测试
if __name__ == '__main__':
    disassemble(benign_root, ".\\smalis\\benign", 600)
    disassemble(malware_root, ".\\smalis\\malware", 600)
    extract_raw_opcode_features(benign_smalis_root, 0)
    extract_raw_opcode_features(malware_smalis_root, 1)
    opcode_csv_filepath.close()
    n_gram(4)
