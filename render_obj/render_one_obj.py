import random
import numpy as np
import time
import math
import configparser
import os
import argparse
import pandas as pd


# 输入：.npy .hdr .obj .tga
# 输出：渲染图片文件夹


def createDir(dirpath):
    import os
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    return dirpath


def renderMultiInput(object_num, hdri_set, camera_poses_file, base_dir, texture_dir, camera_view):
    # base_dir = args.base_dir
    # texture_dir = args.texture_dir
    pose_max =3
    light_num = 35
    output_base_dir = os.path.join(base_dir, 'result')
    ini_basic_path = os.path.join(base_dir, 'config/templete.ini')
    ini_used_path = os.path.join(base_dir, 'config/current.ini')
    render_script_path = os.path.join(base_dir, 'render_engine.py')
    para_dir = os.path.join(base_dir, 'supp')
    led_path = os.path.join(para_dir, 'light_euler_1000.csv')
    obj_pose_path = os.path.join(para_dir, 'pose_euler_1000.csv')

    df_camera_pose = pd.read_csv(obj_pose_path, header=None)
    df_led = pd.read_csv(led_path)


    ini = configparser.ConfigParser()
    ini.optionxform = str
    ini.read(ini_basic_path)
    print(ini_basic_path)

    ini['settings']['working_dir'] = para_dir
    ini['settings']['out_dir'] = output_base_dir
    createDir(output_base_dir)
    ini['light']['energy'] = '{}'.format(3)  # 光强统一设置为3


    # ini texture:随机在3022个材质里面选择一份材质，并且更新材质的名称
    # object_texture_list = np.loadcsv(os.path.join(texture_dir,r"texture.csv"), delimiter=',',dtype=str)
    object_texture_list = [x for x in os.listdir(texture_dir) if '.csv' not in x]
    texture_num = len(object_texture_list)

    # random.sample(range(0,object_num-1))
    for shape_name in [object_num]:  # set epoch
        # shape_name = str(random.randint(0,object_num-1))
        # shape_name = '24'
        shape_name = str(shape_name)
        texture_name = object_texture_list[0]

        roughness_path = os.path.join(texture_dir, texture_name, texture_name + '_roughness.tga')
        if os.path.exists(roughness_path):
            ini['sample']['roughness_texture'] = roughness_path
        else:
            del ini['sample']['roughness_texture']

        metallic_path = os.path.join(texture_dir, texture_name, texture_name + '_metallic.tga')
        if os.path.exists(metallic_path):
            ini['sample']['metallic_texture'] = metallic_path
        else:
            del ini['sample']['metallic_texture']

        specular_path = os.path.join(texture_dir, texture_name, texture_name + '_specular.tga')
        if os.path.exists(specular_path):
            ini['sample']['specular_texture'] = specular_path
        else:
            del ini['sample']['specular_texture']
        # 如果没有找到颜色贴图，那么使用diffuse贴图代替颜色贴图
        color_path = os.path.join(texture_dir, texture_name, texture_name + '_baseColor.tga')
        diffuse_path = os.path.join(texture_dir, texture_name, texture_name + '_diffuse.tga')
        if os.path.exists(color_path):
            ini['sample']['color_texture'] = color_path
        elif os.path.exists(diffuse_path):
            ini['sample']['color_texture'] = diffuse_path
        else:
            del ini['sample']['color_texture']

        print("the texture name is " + texture_name)

        ini['settings']['object_file'] = 'obj_data/{}.obj'.format(shape_name)
        # load texture
        # ini['rendering']['use_hdri'] = hdri_name
        ini['rendering']['use_hdri'] = "None"
        # np.savetxt(camera_pose_file_name_i, camera_poses_path, delimiter=',')
        filename_str = '{}_{}'.format(shape_name, texture_name)

        for pose_id in range(0, pose_max):
            new_folder_path = os.path.join(output_base_dir,str(shape_name), filename_str, str(pose_id))
            createDir(new_folder_path)
            row_data = df_camera_pose.iloc[pose_id:pose_id + 1]  # 提取数据并将其转换为二维结构便于后续
            pose_file_name_i = os.path.join(new_folder_path, 'pose_cash.csv')
            row_data.to_csv(pose_file_name_i, index=False, header=False)  # 将这 1 行数据写入新的 CSV 文件
            ini['object']['object_directions_file'] = pose_file_name_i  # 使用当前指定pose文件
            # 获取随机BRDF
            # df = pd.read_csv(BRDF_csv_path, header=None)  # 读取BRDF材料索引文件
            # 获取随机光照文件
            # df = pd.read_csv(LED_path)
            sampled_df = df_led.sample(n=light_num)  # 随机选取light_num+1个光源
            LEDs_file_name_i = os.path.join('light_positions_of_{}_pose_{}.csv'.format(shape_name, pose_id + 1))
            light_dir_path = os.path.join(new_folder_path, LEDs_file_name_i)
            sampled_df.to_csv(light_dir_path, index=False)  # 将 light_num+1 行数据写入新的 CSV 文件
            # 基础渲染配置

            ini['light']['light_directions_file'] = light_dir_path  # 使用随机选择的 light_num+ 1个光源位置文件
            ini['settings']['filename_str'] = os.path.join(filename_str, str(pose_id))
            with open(ini_used_path, 'w') as f:
                ini.write(f)

            os.system("blender -b -P {} {} ".format(render_script_path, ini_used_path))
            print("blender -b -P {} {} ".format(render_script_path, ini_used_path))


if __name__ == '__main__':

    object_num = '25'
    hdri_set = ["hdri-54.hdr"]
    camera_poses_file = "NERO_camera.npy"

    renderMultiInput(object_num, 1, 1, r'C:\Users\ysy18801056971\cartoon_cut',
                     r'C:\Users\ysy18801056971\Desktop\texture',2)

# 3dmodels/datasets/sdm_mat/Animal-alien_cell_growth.zip/