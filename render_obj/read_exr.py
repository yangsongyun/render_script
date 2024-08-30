import OpenEXR
import Imath
import numpy as np

# 要读取的 .exr 文件路径
exr_file_path = r'C:\Users\ysy18801056971\Desktop\ml-neilf-gpu\ml-neilf-main\code\data\chinese\inputs\depth_maps\000000.exr'

# 检查文件是否存在
if not OpenEXR.isOpenExrFile(exr_file_path):
    raise RuntimeError(f"The file {exr_file_path} is not a valid .exr file")

# 打开 EXR 文件
exr_file = OpenEXR.InputFile(exr_file_path)

# 获取文件的数据窗口大小（宽度与高度）
dw = exr_file.header()['dataWindow']
size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)

# 定义要读取的图片通道
pt = Imath.PixelType(Imath.PixelType.FLOAT)
str_channels = [ 'G']  # 比如，对于 RGB 图像

# 读取通道数据
channels = [exr_file.channel(c, pt) for c in str_channels]

# 将数据转换为 Numpy 数组
channels_np = [np.frombuffer(c, dtype=np.float32) for c in channels]
channels_np = [np.reshape(c, (size[1], size[0])) for c in channels_np]  # 重新排列成图片格式

# 将多个通道合并成一个 Numpy 数组 (如果是单通道，这一步就不需要)
exr_np = np.stack(channels_np, axis=-1)

# 现在 exr_np 是一个包含图片数据的 Numpy 数组
print(exr_np.shape)