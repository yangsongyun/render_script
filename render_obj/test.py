import os
import numpy as np
from render_new import  unzipfile
def get_file_paths(directory):
    file_paths = []  # 用于存储所有文件的绝对路径
    for root, directories, files in os.walk(directory):
        for filename in files:
            if filename[-3:] =='zip':
                filepath = os.path.join(root, filename)
                file_paths.append(os.path.abspath(filepath))
    return file_paths

# 调用函数并传入您的目录路径
folder_path = r'D:\好的材质'  # 替换为您的目录路径
all_file_paths = get_file_paths(folder_path)
output_file = r'C:\Users\ysy18801056971\cartoon_cut\supp\obj_path.txt'
with open(output_file, 'w') as file:
    for path in all_file_paths:
        file.write(path + '\n')  # 写入路径并换行

with open(output_file, 'r') as file:
    for line in file:
        print(line.strip())  # 使用strip()方法去除每行末尾的换行符


print("找到材质数量。。。")
print(len(all_file_paths))

def filter(all_file_paths):
    useful_file =[]
    useful_file_path = r'C:\Users\ysy18801056971\cartoon_cut\supp\useful_path.txt'
    for directory in all_file_paths:

        obj_name,_ = unzipfile(directory, r'D:\cartoon_cut')
        print(obj_name)
        if not obj_name == "lack_texture":
            useful_file.append(directory)
    with open(useful_file_path, 'w') as file:
        for path in useful_file:
            file.write(path + '\n')  # 写入路径并换行
    print(len(useful_file))
filter(all_file_paths=all_file_paths)