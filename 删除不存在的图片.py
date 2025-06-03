import os

# 设置文件夹路径
image_folder = 'G:\目标检测\结果\detect\exp'  # 图片文件夹路径
txt_folder = r'G:\目标检测\结果\所有结果\广东省\detect\1\exp\labels'      # txt 文件夹路径

# 获取 txt 文件的文件名（不包括扩展名）
txt_files = [f.replace('.txt', '') for f in os.listdir(txt_folder) if f.endswith('.txt')]

image_files = [os.path.splitext(f)[0] for f in os.listdir(image_folder)]

# 遍历图片文件
for image_file in image_files:
    # 如果图片的文件名不在 txt 文件名列表中
    if image_file not in txt_files:
        # 获取图片原始文件扩展名
        original_extension = next(
            (os.path.splitext(f)[1] for f in os.listdir(image_folder) if os.path.splitext(f)[0] == image_file), None)

        if original_extension:
            # 构造图片文件的完整路径
            image_path = os.path.join(image_folder, image_file + original_extension)
            try:
                # 删除图片文件
                os.remove(image_path)
                print(f"已删除图片: {image_file + original_extension}")
            except Exception as e:
                print(f"删除失败: {image_file + original_extension}, 错误信息: {e}")

print("操作完成!")