import os
import shutil

# 设置源文件夹和目标文件夹路径
source_folder = '/mnt/xlusb/广东省/jpg/12'  # 替换为源文件夹的实际路径
destination_folder = '/home/xulei/gd_12'  # 替换为目标文件夹的实际路径

# 创建目标文件夹（如果目标文件夹不存在的话）
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# 遍历源文件夹，查找符合条件的文件
for filename in os.listdir(source_folder):

    if filename.endswith('.jpg'):
        # 获取文件名的数字部分（去掉文件扩展名）
        try:
            file_number = int(filename.split('.')[0])
        except ValueError:
            # 如果文件名的数字部分无法转换为整数，则跳过该文件
            continue

        # 如果文件名在范围内，复制文件
        if 11998000 <= file_number <= 12000000:
            # 创建源文件和目标文件的完整路径
            source_file = os.path.join(source_folder, filename)
            destination_file = os.path.join(destination_folder, filename)

            # 复制文件
            shutil.copy(source_file, destination_file)
            print(f'复制文件: {filename}')

print("文件复制完成！")
