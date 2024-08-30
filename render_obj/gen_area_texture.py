import cv2
import cv2.aruco as aruco
import tqdm
import os
from PIL import Image
def createDir(dirpath):
    import os
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)

    return dirpath

def create_marker(dict, dir, numMarkder, resolution):

    createDir(dir)
    # aruco_dict = aruco.Dictionary(aruco.DICT_6X6_50)
    aruco_dict = aruco.getPredefinedDictionary(dict)
    # Generate each marker
    for i in tqdm.trange(numMarkder):
        # Generate the marker
        marker_image = aruco.generateImageMarker(aruco_dict, i, resolution)
        # Save the marker to a file
        cv2.imwrite("{}/{}.png".format(dir, i), marker_image)

def gen_texture_paths_csv(dir,subdir,numMarkder):
    save_path = os.path.join(dir, 'texture_paths.csv')
    with open(save_path, 'w') as f:

        for i in range(numMarkder):
            area_path = os.path.join(subdir, '{}.png'.format(i))
            f.write(f'{area_path} \n')

def gen(base_dir):
    dir = os.path.join(base_dir, 'supp/area_texture')
    subdir = os.path.join(base_dir,"supp/area_texture")
    dict = aruco.DICT_6X6_1000
    numMarkder = 101
    resolution = 256
    # create_marker(dict, dir, numMarkder, resolution)
    gen_texture_paths_csv(dir,subdir,numMarkder)
    #img = Image.new('RGB', (256, 256), color='black')
    #img.save(os.path.join(subdir, '0.png'))

if __name__ =='__main__':
    gen()


