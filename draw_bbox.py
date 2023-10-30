from utility import *
import os
import argparse

def draw_bbox(img_name):

    with open('./dataset/val_coord.json', 'r') as f:
        d = json.load(f)

    # for img_name in list(d.keys())[:1]:
    bds, bounding_box_list = [], []
    coms = d[img_name]
    for com in coms:
        bds.append(com['bounding_box'])

    for box in bds:
        box = box[1: -1]
        tmp = list(map(int, box.split(',')))
        # new_box = [tmp[0], tmp[1], tmp[0]+tmp[2], tmp[1]+tmp[3]]
        new_box = [tmp[0], tmp[1], tmp[2], tmp[3]]
        bounding_box_list.append(new_box)
    img_path = os.path.join('./dataset/val_imgs', img_name)

    try:
        draw_bounding_box(img_path, bounding_box_list)
    except Exception as e:
        print(e)
        # continue

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--image_name', type=str, help='image_name ', required=True)
    args = parser.parse_args()
    draw_bbox(args.image_name)


if __name__ == '__main__':
    main()
