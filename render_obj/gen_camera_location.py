#这个文件生成随机的相机位姿，决定的向量是alpha与gamma，beta（作为y轴的旋转角度，默认为0）当alpha>90的时候，此时应该让alpha+=180,beta+=180使得图片的正面是朝上的

import numpy as np
import pandas as pd
import random

def euler_to_rotation_matrix(rx, ry, rz):

    # 将角度转换为弧度
    # roll_rad = np.radians(rx)
    # pitch_rad = np.radians(ry)
    # yaw_rad = np.radians(rz)


    roll_rad = rx
    pitch_rad = ry
    yaw_rad = rz

    # 求解偏航、俯仰和滚转的旋转矩阵
    Rz_yaw = np.array([
        [np.cos(yaw_rad), -np.sin(yaw_rad), 0],
        [np.sin(yaw_rad),  np.cos(yaw_rad), 0],
        [0,                0,               1]
    ])

    Ry_pitch = np.array([
        [np.cos(pitch_rad),  0, np.sin(pitch_rad)],
        [0,                  1, 0],
        [-np.sin(pitch_rad), 0, np.cos(pitch_rad)]
    ])

    Rx_roll = np.array([
        [1, 0,                0],
        [0, np.cos(roll_rad), -np.sin(roll_rad)],
        [0, np.sin(roll_rad),  np.cos(roll_rad)]
    ])

    # 计算最终的旋转矩阵
    rotation_matrix = Rz_yaw @ Ry_pitch @ Rx_roll
    #在blender返回渲染的时候，应该使用角度制




    return rotation_matrix

def cal_camera_position(rx, ry, rz, distance=4):
    '''该方法用于计算相机应该在的位置，此时我们默认相机朝向为原点方向。方便物体总是能被找到'''
    rot_matrix = euler_to_rotation_matrix(rx, ry, rz)
    origin = [0,0,distance]
    position = rot_matrix@origin
    return position

def gen_position(dense ,if_rand=True,if_up=False, neg=False):
    '''该方法通过密度生成不同的相机位姿，使用角度表示，密度表示在一个平面内部最多有多少台相机
    if_rand:表示是否随机生成位姿（小范围滑动）
    if_up:表示相机是否只在水平面上alpha<90
    '''
    position=[]
    distance = np.pi*2/dense#表示不同的相机相隔的弧度
    vert_number = int(np.ceil(dense/4))+1
    vert_samples = np.linspace(0, np.pi/2, vert_number)
    for vert_rad in vert_samples:
        length = np.pi*2*np.sin(vert_rad)
        hori_number = int(np.ceil(length/distance))+1
        samples_1 = np.linspace(0, np.pi*2, hori_number)
        samples_1 = samples_1[:-1]
        for hori in samples_1:
            position.append([vert_rad,hori,0])
    position.insert(0,[0,0,0])
    #position = position[:-dense]
    np_position = np.array(position)
    np_position = np_position-np.array([1.57,0,0])
    all_position = np_position
    if neg:
        neg_position = np_position+np.array([np.pi,0,0])
        all_position = np.concatenate((np_position, neg_position), axis=0)
        all_position = all_position[:-4,:]


    print('you have get {} number samples'.format(len(all_position)))
    print(all_position)
    return all_position


def gen_position_deer(dense ,if_rand=True,if_up=False):
    '''该方法通过密度生成不同的相机位姿，使用角度表示，密度表示在一个平面内部最多有多少台相机
    if_rand:表示是否随机生成位姿（小范围滑动）
    if_up:表示相机是否只在水平面上alpha<90
    '''
    position=[]
    distance = np.pi*2/dense#表示不同的相机相隔的弧度
    vert_number = int(np.ceil(dense/4))+1
    vert_samples = np.linspace(0, np.pi/2, vert_number)
    for vert_rad in vert_samples:
        length = np.pi*2*np.sin(vert_rad)
        hori_number = int(np.ceil(length/distance))+1
        samples_1 = np.linspace(0, np.pi*2, hori_number)
        samples_1 = samples_1[:-1]
        for hori in samples_1:
            position.append([vert_rad,hori,0])
    position.insert(0,[0,0,0])
    position = position[:-dense]
    np_position = np.array(position)
    np_position = np_position-np.array([1.57,0,0])
    position = np_position
    print('you have get {} number samples'.format(len(position)))
    print(position)
    return position
def save_camera_rad(dense=4, neg=False):
    camera_rad = gen_position(dense=dense, neg=neg)
    # 将Numpy数组转换为pandas DataFrame
    df = pd.DataFrame(camera_rad)
    # 将DataFrame写入CSV文件，包括列头
    np.savetxt("./supp/camera_pose.csv", df, delimiter=",", fmt='%.3f')
    return len(camera_rad)

def gen_light_by_camera(camera_rad,n=10,range=2, rand=True, fix=False):
    '''这个方法是通过相机的角度生成光线的角度，避免光线照到背面，在初始化中，物体的光线方向为+z
    camera_rad：[1,3]数组
    n：生成光线的数量
    range:光线的范围（以相机为中心）'''
    if fix:
        return camera_rad
    if rand:
        alpha,_,gamma = camera_rad
        rand_rx = (np.random.rand(n)-0.5)*range+alpha
        rand_rz = (np.random.rand(n)-0.5)*range+gamma
        rand_ry = np.zeros(n)
        light_rad = np.vstack((rand_rx,rand_ry,rand_rz)).T
    else:
        return [[0,0,0]]
    return light_rad

def get_all_light_dir():
    '''这个方法用于整合所有的光线，此时'''
    return

def gen_obj_pose(base,max_eluer,dense=10):
    # 这个方法用于生成物体的pose，用于模仿我拥有一个旋转的系统，固定的相机
    # 弧度制
    # 输入：偏置角度（初始的时候物体的旋转角度）
    #      最大旋转角度（有的时候我不需要物体旋转360度）
    #      旋转密度（最后输出的数组大小[n,3]）
    obj_pose = np.zeros((dense,3))
    rad = max_eluer/dense
    for i in range(dense):
        obj_pose[i] = base
        obj_pose[i,2] = obj_pose[i,2] + rad*i

    return obj_pose

if __name__ == '__main__':
    save_camera_rad(dense=20)






