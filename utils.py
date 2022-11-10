import json
import datetime

# JSONを読み込んでdataとして返す関数
def json_load():
    json_read = open("pkm.json", "r")
    data = json.load(json_read)
    json_read.close()
    return data

# dataを引数としてJSONに書き込む関数
def json_write(data):
    json_write = open("pkm.json", "w")
    json.dump(data, json_write, indent=4, ensure_ascii=False)
    json_write.close()

# dataを引数としてバックアップを出力する関数
def json_backup(data):
    time = datetime.datetime.now()
    json_backup = open(time.strftime('%Y-%m-%d-%H-%M-%S') + ".json", "w")
    json.dump(data, json_backup, indent=4, ensure_ascii=False)
    json_backup.close()

# data内に一致するkeyが無ければ1を返す関数
def key_check(data, key):
    flag = 1
    for k in data.keys():
        if k == key:
            flag = 0
    return flag

# data内に一致するvalueが無ければ1を返す関数
def value_check(data, value):
    flag = 1
    for v in data.values():
        if v == value:
            flag = 0
    return flag

# keyをvalueに変換する関数
def key_to_value(data, key):
    if not key_check(data, key):
        return data[key]
    else:
        return key

# valueをkeyに変換する関数
def value_to_key(data, value):
    if not value_check(data, value):
        for k, v in data.items():
            if v == value:
                return k
    else:
        return value

# 順位によるptを決定する関数
def pt_rate(player, stack):
    if player <= 4:
        if stack <= 2000:
            return [3, 1]
        elif stack <= 10000:
            return [4, 2]
        else:
            return [5, 2]
    elif player <= 6:
        if stack <= 2000:
            return [5, 3, 1]
        elif stack <= 10000:
            return [6, 4, 2]
        else:
            return [7, 4, 2]
    elif player <= 9:
        if stack <= 2000:
            return [8, 5, 3, 1]
        elif stack <= 10000:
            return [9, 6, 4, 2]
        else:
            return [11, 7, 4, 2]
    elif player <= 12:
        if stack <= 2000:
            return [12, 8, 5, 3, 1]
        elif stack <= 10000:
            return [13, 9, 6, 4, 2]
        else:
            return [15, 11, 7, 4, 2]
    else:
        if stack <= 2000:
            return [17, 12, 8, 5, 3, 1]
        elif stack <= 10000:
            return [19, 13, 9, 6, 4, 2]
        else:
            return [21, 15, 11, 7, 4, 2]
