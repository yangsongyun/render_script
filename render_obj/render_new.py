import random
import numpy as np
import time
import math
import configparser
import os
import argparse
import pandas as pd
import shutil
import gen_camera_location


# 输入：.npy .hdr .obj .tga
# 输出：渲染图片文件夹
#这个文件主要用于新的渲染方式，能够渲染物体不变，但是相机改变位置

def createDir(dirpath):
    import os
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    return dirpath
def unzipfile(filepath,work_dir):
    save_path = os.path.join(work_dir,"obj")
    if os.path.exists(save_path):
        # 删除目录及其中的所有内容
        shutil.rmtree(save_path)
        print(f"The directory '{save_path}' has been removed.")
    shutil.unpack_archive(filepath, save_path, 'zip')
    entries = os.listdir(save_path)
    obj_name = ""
    path_list = []
    for filename in entries:
        if filename[-3:] == "jpg":
            obj_name = filename[:-4]

    forewords = ["8bit_T_","T_"]
    for word in forewords:
        exsits, filepath = if_path_exsist(save_path,obj_name,word,"")
        if exsits:
            return obj_name, filepath


    return "lack_texture", path_list

def euler_to_rotation_matrix(euler_angles):
    """
    通过欧拉角(以弧度为单位)生成旋转矩阵。
    按照Z-Y-X顺序（首先绕X轴旋转，然后绕Y轴，最后绕Z轴）。
    """
    roll, pitch, yaw = euler_angles

    R_x = np.array([[1, 0, 0],
                    [0, np.cos(roll), -np.sin(roll)],
                    [0, np.sin(roll), np.cos(roll)]])

    R_y = np.array([[np.cos(pitch), 0, np.sin(pitch)],
                    [0, 1, 0],
                    [-np.sin(pitch), 0, np.cos(pitch)]])

    R_z = np.array([[np.cos(yaw), -np.sin(yaw), 0],
                    [np.sin(yaw), np.cos(yaw), 0],
                    [0, 0, 1]])

    R = np.dot(R_z, np.dot(R_y, R_x))
    #R = np.dot(R_z, np.dot(R_x, R_y))
    #对于colmap的坐标系转换，y轴反向，然后z轴反向，
    colmap_R = np.array([[1,0, 0],
                    [0, -1, 0],
                    [0, 0, -1]])
    R = np.dot(R,colmap_R)
    return R

def create_c2w_matrix(position, euler_angles):
    """
    根据位置和欧拉角生成4x4的变换矩阵。
    注意，这个生成的是c2w矩阵
    """
    R = euler_to_rotation_matrix(euler_angles)
    T = np.zeros((4, 4))
    #c2w = np.linalg.inv(R)
    T[:3, :3] = R
    T[:3, 3] = position
    T[3, 3] = 1.0
    return T

def if_path_exsist(save_path,obj_name,foreword,backword):
    if not os.path.exists(os.path.join(save_path,obj_name+'.fbx')):
        print(obj_name+'.fbx')
        return False,[]
    roughness_path = os.path.join(save_path, foreword+obj_name+"_Roughness_8K.png")
    metallic_path = os.path.join(save_path, foreword+obj_name+"_Metallic_8k.png")
    albedo_path = os.path.join(save_path, foreword+obj_name + "_Albedo_8k.png")
    if not os.path.exists(roughness_path):
        return False,[]
    if not os.path.exists(metallic_path):
        return False,[]
    if not os.path.exists(albedo_path):
        return False,[]

    return True,[roughness_path,metallic_path,albedo_path]

def renderMultiInput(object_name, base_dir, hdr_dir,path_list, test=True, rand=False, dense=20):

    #light_num = 2
    #该方法用于生成相机位姿，在半圆/圆内作均匀采样
    pose_max = gen_camera_location.save_camera_rad(dense=dense, neg=True)
    #pose_max = 1
    #该方法用于生成物体位姿
    base = np.array([0, 0, 0])
    obj_euler = gen_camera_location.gen_obj_pose(base, 0.3, 1)
    pose_pd = pd.DataFrame(obj_euler)
    pose_file_name_i = os.path.join("./supp", 'pose_cash.csv')
    pose_pd.to_csv(pose_file_name_i, index=False, header=False)  # 将这 1 行数据写入新的 CSV 文件

    #pose_max = 1
    output_base_dir = os.path.join(base_dir, 'result')
    ini_basic_path = os.path.join(base_dir, 'config/templete.ini')
    ini_used_path = os.path.join(base_dir, 'config/current.ini')
    render_script_path = os.path.join(base_dir, 'render_engine.py')
    para_dir = os.path.join(base_dir, 'supp')

    ini = configparser.ConfigParser()
    ini.optionxform = str
    ini.read(ini_basic_path)
    #  路径配置
    ini['settings']['working_dir'] = os.path.join(base_dir, 'obj')
    ini['settings']['out_dir'] = output_base_dir
    createDir(output_base_dir)
    #是否测试，由于某些方法不需要一些图像，因此能够添加测试减少其他的图像渲染
    if test:
        ini['object_custom']['test'] = 'True'
    #光源大小配置
    ini['light']['energy'] = '{}'.format(1000)  # 光强统一设置为5

    #物体与材质配置
    ini['sample']['roughness_texture'] = path_list[0]
    ini['sample']['metallic_texture'] = path_list[1]
    ini['sample']['color_texture'] = path_list[2]
    ini['settings']['object_file'] = object_name+'.fbx'

    obj_pose_path = os.path.join(para_dir, 'camera_pose.csv')
    df_obj_pose = pd.read_csv(obj_pose_path, header=None)

    filename_str = '{}'.format(object_name)
    #hdri设置
    hdri_set = [hdr_dir]

    for hdri in hdri_set:
        #初始化hdri做多hdr渲染
        ini['rendering']['use_hdri'] = hdri
        if hdri=="None":
            hdr_out = os.path.join(output_base_dir,"no_hdr")
        else:
            hdr_out = os.path.join(output_base_dir, "hdr")
        ini['settings']['out_dir'] = hdr_out
        for pose_id in range(0, pose_max):
            new_folder_path = os.path.join(hdr_out, filename_str, str(pose_id))
            createDir(new_folder_path)
            row_data = df_obj_pose.iloc[pose_id:pose_id + 1]  # 提取数据并将其转换为二维结构便于后续
            ini['object']['object_directions_file'] = pose_file_name_i  # 使用当前指定pose文件
            # 获取随机BRDF
            # df = pd.read_csv(BRDF_csv_path, header=None)  # 读取BRDF材料索引文件
            np_row = np.array(row_data)[0]
            camera_location = gen_camera_location.cal_camera_position(np_row[0], np_row[1], np_row[2])
            #sampled = gen_camera_location.gen_light_by_camera(row_data, n=light_num, rand=rand, fix=False)
            sampled = camera_location[np.newaxis,:]
            LEDs_file_name_i = os.path.join('light_positions_of_{}_pose_{}.csv'.format(object_name, pose_id + 1))
            light_dir_path = os.path.join(new_folder_path, LEDs_file_name_i)
            # sampled.to_csv(light_dir_path, index=False)  # 将 light_num+1 行数据写入新的 CSV 文件
            np.savetxt(light_dir_path,sampled, delimiter=",", fmt='%.3f')
            # 基础渲染配置
            ini['camera']['location'] = ', '.join(str(i) for i in camera_location)
            ini['camera']['rotation'] = ', '.join(str(i) for i in np_row)#存入的是角度制
            ini['light']['light_directions_file'] = light_dir_path  # 使用随机选择的 light_num+ 1个光源位置文件
            ini['settings']['filename_str'] = os.path.join(str(pose_id))
            #ini['settings']['zip_path'] = orign_path
            with open(ini_used_path, 'w') as f:
                ini.write(f)
            os.system("blender -b -P {} {} ".format(render_script_path, ini_used_path, test))
            print("blender -b -P {} {} ".format(render_script_path, ini_used_path))


if __name__ == '__main__':

    zipfile = r'C:\Users\bupty\Desktop\code\data_set\chicken.zip'
    obj_name,path_list = unzipfile(zipfile,r'C:\Users\bupty\Desktop\code\render_obj')
    if not obj_name == "lack_texture":
        print(obj_name)
        print(path_list)
        renderMultiInput(obj_name,r'C:\Users\bupty\Desktop\code\render_obj',r'C:\Users\bupty\Desktop\code\render_obj\supp\hdri-54.hdr',path_list)
