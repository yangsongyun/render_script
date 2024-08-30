import os.path

import render_new
import random
def set_ramdon_hdr():
    hdr_num = random.randint(1,916)
    hdr_name = "hdri-"+str(hdr_num)+".hdr"
    hdr_path = os.path.join(r'C:\Users\ysy18801056971\Desktop\HDRI',hdr_name)
    return hdr_path

def render_locate():
    continue_render = True
    all_zip = []
    work_dir = r'C:\Users\ysy18801056971\cartoon_cut'
    log_path = os.path.join(work_dir,"finish_obj.txt")
    zip_paths = r'C:\Users\ysy18801056971\cartoon_cut\supp\obj_path.txt'
    texture_dir = os.path.join(work_dir,'obj')
    with open(zip_paths, 'r') as file:
        for line in file:
            all_zip.append(line.strip())


    if continue_render :
        finish_render = []
        with open(log_path, 'r') as file:
            for line in file:
                finish_render.append(line.strip())
        all_zip = all_zip[len(finish_render):]
        print("you have render {} object,now continue...".format(len(finish_render)))
        print("there are {} left".format(len(all_zip)))
        print(all_zip)


    for zip_path in all_zip:
        print(zip_path)
        hdr_path = set_ramdon_hdr()
        obj_name,path_list = render_new.unzipfile(zip_path, work_dir)
        orign_path= zip_path.split('\\')[-1]
        if obj_name in ["no_mesh", "no_roughness", "no_Metallic","no_Albedo","lack_texture"]:
            with open(log_path,'a') as file:
                file.write('lack_texture'+zip_path+'\n')
        else:
            render_new.renderMultiInput(obj_name, work_dir, texture_dir, hdr_path, orign_path, path_list)
            with open(log_path,'a') as file:
                file.write(zip_path+'\n')

def see_rendered_object():
    finish=[]
    finish_number=0
    work_dir = r'C:\Users\ysy18801056971\cartoon_cut'
    log_path = os.path.join(work_dir,"finish_obj.txt")
    with open(log_path, 'r') as file:
        for line in file:
            finish.append(line.strip())
    for path in finish:
        if not path[:4] == 'lack':
            finish_number = finish_number+1
    print("you have render {} objects".format(finish_number))



if __name__ == '__main__':


    see_rendered_object()

    render_locate()
