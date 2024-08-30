import os


def gen_texture_path(folder_path):
    # 替换为你的文件夹路径

    # 列出文件夹中的所有文件和文件夹
    files_and_folders = os.listdir(folder_path)

    # 只列出文件，排除文件夹
    files = [f for f in files_and_folders if not os.path.isfile(os.path.join(folder_path, f))]

    print(files)
    print(len(files))
    save_path = os.path.join(folder_path, 'texture.csv')
    with open(save_path, 'w') as f:
        for name in files:
            f.write(f'{name} \n')


if __name__ =='__main__':
    folder_path = r"./textures"
    gen_texture_path(folder_path)
