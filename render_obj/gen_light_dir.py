'''改写这个文件，首先生成一堆基于z = -4的点，然后在[-4,4]中随机采样x与y的值，使得该点的光源方向在45度以内
然后利用求取的点的坐标计算出需要更新的x与z的旋转角度，此时我们假设y的旋转角度为0'''


import random
import numpy as np

def cal_degree(dir):
    x = dir[0]
    y = dir[1]
    z = dir[2]
    xy = np.sqrt(np.square(x) + np.square(y))
    xdegree = np.arctan(xy / z) + np.pi
    ydegree = 0
    if x >= 0:
        if y >= 0:
            zdegree = np.pi - np.arcsin(x / xy)
        else:
            zdegree = np.arcsin(x / xy)

    else:
        if y >= 0:
            zdegree = np.pi - np.arcsin(x / xy)
        else:
            zdegree = np.arcsin(x / xy)
    csv = [xdegree,ydegree,zdegree]
    return csv

x = []
y = []
for i in range(1000):
    x_sample = random.uniform(-4, 4)
    y_sample = random.uniform(-4, 4)
    x.append(x_sample)
    y.append(y_sample)
x=np.reshape(x,[1000,1])
y=np.reshape(y,[1000,1])
z = np.ones([1000,1])*4
csv= np.concatenate((x,y,z),axis=1)
np.savetxt("./supp/light_dir_1000.csv", csv, delimiter=",")
degree_csv = []
for i in range(len(csv)):
    degree = cal_degree(csv[i])
    degree_csv.append(degree)
np.savetxt("./supp/light_euler_1000.csv", degree_csv, delimiter=",")

