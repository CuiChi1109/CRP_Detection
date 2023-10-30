# import os
# import json
from ocr_call import *
# import ast
# from tqdm import tqdm

# result = {}
# dir = './dataset/val_imgs'
# with open("./dataset/val_coords.txt", 'r') as f:
#     for line in tqdm(f.readlines()):
#         img_name, coord, com_type, is_cred = line.split('\t')
#         img_name += '.png'
#         bounding_box = ast.literal_eval(coord)
#         img_path = os.path.join(dir, img_name)
#         ocr_result = ocr_crop_image(img_path, bounding_box)

#         if img_name not in list(result.keys()):
#             result[img_name] = []
#         result[img_name].append({
#             'bounding_box' : coord,
#             "type": com_type,
#             "text": ocr_result
#             # "label": is_cred,
#         })

# with open("./dataset/val_coord.json", 'w') as f:
#     json.dump(result, f, indent=4)

import os
import ast
import json
from tqdm import tqdm

def save_to_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

result = {}

with open('/Users/cuichi/dissertation/ocr/dataset/val_coord_temp.json', 'r') as f:
    result = json.load(f)

dir = './dataset/val_imgs'
save_interval = 50  # 例如每处理50张图片就保存一次
count = 0
flag = 0

with open("./dataset/val_coords.txt", 'r') as f:
    for line in tqdm(f.readlines()):
        img_name, coord, com_type, is_cred = line.split('\t')
        img_name += '.png'
        if img_name == "secret-toy.png":
            flag = 1
        if flag == 0:
            continue
        bounding_box = ast.literal_eval(coord)
        img_path = os.path.join(dir, img_name)
        ocr_result = ocr_crop_image(img_path, bounding_box)

        if img_name not in list(result.keys()):
            result[img_name] = []
        result[img_name].append({
            'bounding_box': coord,
            "type": com_type,
            "text": ocr_result
            # "label": is_cred,
        })

        count += 1
        if count % save_interval == 0:
            save_to_json(result, "./dataset/val_coord_temp.json")  # 保存到一个临时文件，防止中断后覆盖原始文件

# 最后将所有的结果保存到最终的 JSON 文件
save_to_json(result, "./dataset/val_coord.json")
