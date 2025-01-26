import os

# 照片所在目录
photo_directory = input("请输入照片所在目录的路径：")  # 用户输入照片目录

# 检查目录是否存在
if not os.path.exists(photo_directory):
    print(f"目录不存在: {photo_directory}")
else:
    # 获取目录中的所有图片文件
    photos = [f for f in os.listdir(photo_directory) if f.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]

    # 获取每个文件的创建时间
    photos_with_time = []
    for photo in photos:
        photo_path = os.path.join(photo_directory, photo)
        creation_time = os.path.getctime(photo_path)
        photos_with_time.append((photo, creation_time))

    # 按照创建时间排序
    photos_with_time.sort(key=lambda x: x[1])

    # 重命名文件
    for index, (photo, _) in enumerate(photos_with_time):
        new_name = f"{index + 1}{os.path.splitext(photo)[1]}"  # 保留原文件后缀
        old_path = os.path.join(photo_directory, photo)
        new_path = os.path.join(photo_directory, new_name)
        os.rename(old_path, new_path)
        print(f"已将 {photo} 重命名为 {new_name}")

    print("重命名完成！")