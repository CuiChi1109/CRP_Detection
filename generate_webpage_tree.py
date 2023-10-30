
import os
from PIL import Image
from ocr_call import *
import ast

def parse_bounding_box(bbox_str):
    x1, y1, x2, y2 = map(int, bbox_str.strip("()").split(","))
    return x1, y1, x2, y2

def is_contrain(block_bbox, item_bbox):
    ox1, oy1, ox2, oy2 = parse_bounding_box(block_bbox)
    ix1, iy1, ix2, iy2 = parse_bounding_box(item_bbox)
    if ox1 == ix1 and oy1 == iy1 and ox2 == ix2 and oy2 == ix2:
        return 0
    return ox1 <= ix1 and oy1 <= iy1 and ox2 >= ix2 and oy2 >= iy2


def generate_webpage_tree_single(com_list):

    delete_items = []
    for i in range(len(com_list)):
        com = com_list[i]
        if com['type'] == 'block':      # when components block
            for j in range(len(com_list)):
                if i == j:              # is blcok it self
                    continue
                item = com_list[j]
                if is_contrain(com['bounding_box'], item['bounding_box']):  # check if contain
                    # print(i, j)
                    if 'item' not in list(com.keys()):
                        com['item'] = []
                    com['item'].append(item)
                    delete_items.append(item)

        com_list[i] = com               # update com

    for item in delete_items:
        try:
            com_list.remove(item)
        except Exception as e:
            continue

    return com_list



def generate_webpage_tree_all(json_file):
    tree_dict = {}
    with open(json_file) as f:
        ocr_result = json.load(f)
    for image_name in list(ocr_result.keys()):
        if image_name in ['M & T Bank Coporation+2020-09-01-13`14`34.png',
                          'Made-In-China+2020-05-24-15`29`02.png',
                          'Mastercard International Incorporated+2020-05-27-17`14`49.png',
                          "Mastercard International Incorporated+2020-08-09-00`52`17.png",
                          "Mastercard International Incorporated+2020-09-12-12`01`42.png",
                          "Match+2019-08-05-13`41`48.png",
                          "Match+2019-08-06-14`22`57.png",
                          "Match+2019-08-19-10`41`53.png"]:
            continue
        if 'Match' in image_name:
            continue
        try:
            tree_dict[image_name] = generate_webpage_tree_single(ocr_result[image_name])
        except:
            continue
    with open('./dataset/val_com_tree.json', 'w') as f:
        json.dump(tree_dict, f, indent=4)

generate_webpage_tree_all('./dataset/val_coord.json')