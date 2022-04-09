# import pandas as pd
import csv
import datetime


def saveToFile(array):
    # [('1', '1', '1', '1', '1'), ('1', '1', '2', '3', '4'), ...] 二维数组
    # 对应  ("id", "service", "money", "card_number", "name", "phone", "project",\
    #            "shop_guide", "teacher", "financial", "remarks1", "collect_money", "remarks2") 
    path = "D:\\backup_data_" + datetime.datetime.now().strftime('%Y%m%d') + ".csv"
    # a = [1,2,3]
    # b = [4,5,6]
    # with open(path, "w", newline='') as csvfile: 
    #     writer = csv.writer(csvfile)
    #      #先写入columns_name
    #     writer.writerow(["index","a_name","b_name"])
    #     writer.writerow(a)
    #     writer.writerow(b)
    columns = ["id", "service", "money", "card_number", "name", "phone", "project", \
               "shop_guide", "teacher", "financial", "remarks1", "collect_money", "remarks2"]
    with open(path, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(columns)
        writer.writerows(array)
    print("已导出到" + path)
    re = {
        'code': 0,
        'message': "已导出到" + path
    }
    return re


def loadFromFile():
    pass


if __name__ == "__main__":
    saveToFile(None)
