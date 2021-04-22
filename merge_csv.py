import csv

# n_gram_csv = open("4_gram.csv","r")
# n_gram_info = csv.reader(n_gram_csv)

# 此文件是测试合并两个csv文件的
# 跟permission.csv文件一模一样
permission_copy_csv = open("permissions_copy.csv")
permission_copy_info = csv.reader(permission_copy_csv)

permission_csv = open("permissions.csv")
permission_info = csv.reader(permission_csv)

feature1 = []
feature2 = []

for info in permission_copy_info:
    feature1.append(info)
for info in permission_info:
    feature2.append(info)

with open("data.csv", "w", newline='') as f:
    writer = csv.writer(f)
    for index in range(len(feature2)):
        feature1[index].extend(feature2[index])
        writer.writerow(feature1[index])
