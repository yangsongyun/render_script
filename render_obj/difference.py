import OpenEXR
import Imath
import numpy as np
from PIL import Image
def read_exr(filename):
    """ 读取 EXR 文件并转换为 NumPy 数组 """
    exr_file = OpenEXR.InputFile(filename)
    dw = exr_file.header()['dataWindow']
    size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)

    # 读取 RGB 通道
    FLOAT = Imath.PixelType(Imath.PixelType.FLOAT)
    (r_str, g_str, b_str) = exr_file.channels("RGB", FLOAT)
    r = np.frombuffer(r_str, dtype=np.float32)
    g = np.frombuffer(g_str, dtype=np.float32)
    b = np.frombuffer(b_str, dtype=np.float32)
    r.shape = (size[1], size[0])  # 注意尺寸顺序
    g.shape = (size[1], size[0])
    b.shape = (size[1], size[0])
    return np.stack((r, g, b), axis=-1)

# 读取两个 EXR 文件
image1 = read_exr(r"C:\Users\ysy\Desktop\RenderWithBlender\result\18\18_hdri-54.hdr_glass1.1\view_001\002.exr")
image2 = read_exr(r"C:\Users\ysy\Desktop\RenderWithBlender\result\18\18_hdri-54.hdr_glass1.1\view_001\006.exr")

# 计算差异
difference = image1 - image2

# 可以根据需要处理差异，例如保存差异图像或进一步分析

def save_image(array, filename):
    """ 保存 NumPy 数组为图像文件 """
    # 将差异值缩放到 0-255 并转换为整数
    print(array.min())
    print(array.max() - array.min())
    array = (array - array.min()) / (array.max() - array.min())
    array = (array * 255).astype('uint8')

    # 转换为 PIL 图像并保存
    image = Image.fromarray(array, 'RGB')
    image.save(filename)

# 保存 difference 数组为图像
save_image(difference, 'difference_image.png')