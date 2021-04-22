import csv


def load_txt(data_path):
    data = []
    with open(data_path,'r') as f:
        for line in f.readlines():
            line = line.strip()
            data.append(line)
    return data

def load_csv(data_path):
    data = []
    with open(data_path) as f:
        readCSV = csv.reader(f,delimiter=',')
        for row in readCSV:
            for i in range(len(row)):
                if row[i] == '1':
                    row[i] = 1
                else:
                    row[i] = 0
            data.append(row)
    return data