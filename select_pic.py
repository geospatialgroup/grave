import os
import shutil

# 设置文件夹路径
image_folder = '/mnt/xlusb/广东省/jpg/1'  # 图片文件夹路径
txt_folder = '/mnt/xlusb/广东省/detect/1/exp2/labels'      # txt 文件夹路径
output_folder = ('/home/xulei/pick_gd_pic/source_pic')  # 输出文件夹路径

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 获取 txt 文件名（不包括扩展名）
txt_files = [f.replace('.txt', '') for f in os.listdir(txt_folder) if f.endswith('.txt')]

# 获取图片文件
image_files = os.listdir(image_folder)

# 遍历每个 txt 文件，检查是否有对应的图片
for txt_file in txt_files:
    print(txt_file)
    # 根据 txt 文件名查找对应的图片文件
    for image_file in image_files:
        # 假设图片名与 txt 文件名一致（包括扩展名）
        if image_file.startswith(txt_file):
            # 找到匹配的图片，复制到输出文件夹
            src_path = os.path.join(image_folder, image_file)
            dst_path = os.path.join(output_folder, image_file)
            shutil.copy(src_path, dst_path)
            print(f"复制文件: {image_file}")

print("完成所有图片筛选并复制!")
