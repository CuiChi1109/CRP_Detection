# from eval import copy_image
import shutil
import os
def count_labels(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # 初始化字典来存储统计结果
    image_list = []
    label_counts = {'credential':[], 'noncredential':[]}

    for line in lines:
        # 从每一行获取文件名和标签
        parts = line.strip().split('\t')
        file_name = parts[0]
        label = parts[-1]

        # 更新字典的计数
        if file_name not in image_list:
            image_list.append(file_name)
            label_counts[label].append(file_name)

    return label_counts

if __name__ == "__main__":
    file_path = './dataset/val_coords.txt'  # 将此处的路径替换为您的txt文件的路径
    result = count_labels(file_path)
    print(result)

    for image in os.listdir('./dataset/val_imgs'):
        if image[:-4] in result['credential']:
            shutil.copy('./dataset/val_imgs/'+image, './dataset/val_credential/'+image)
        else:
            shutil.copy('./dataset/val_imgs/'+image, './dataset/val_noncredential/'+image)
    # for file_name, counts in result.items():
    #     print(f"文件名: {file_name}")
    #     for label, count in counts.items():
    #         print(f"标签 {label} 出现次数: {count}")
    #     print("------")


# import os
# import shutil
# for image_name in os.listdir('./dataset/Legitimate1000/600_legitimate'):
#     img_path = os.path.join('./dataset/Legitimate1000/600_legitimate', image_name, 'shot.png')
#     print(img_path, image_name)
#     shutil.copy(img_path, './dataset/begin/'+image_name+'.png')