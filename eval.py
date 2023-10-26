# eval performance of gpt result

import os
import json
import shutil
import argparse

IMG_DIR = 'val_imgs'
def copy_image(img, dir):
    img_path = os.path.join(IMG_DIR, img)
    shutil.copy(img_path, dir)

def eval(file, threshold):
    gt_dict = {}
    pred_dict = {}
    with open('val_img_gt.json', 'r') as f:
        gt_dict = json.load(f)
    with open(file, 'r') as f:
        pred_dict = json.load(f)

    tp, tn, fp, fn, fail = 0, 0, 0, 0, 0
    for img in pred_dict.keys():
        try:
            pred = int(pred_dict[img])
        except:
            fail += 1
            # print(img)
            continue
        pred = 1 if pred > threshold else 0
        try:
            gt = gt_dict[img]
        except Exception as e:
            print(e)
            continue
        if gt == pred:
            if gt == 1:
                tp += 1
            else:
                tn += 1
        else:

            if gt == 0:

                fp += 1
            else:
                # print(img, gt, pred_dict[img])
                copy_image(img, './fn_8_gpt35')
                fn += 1

    total = tp+tn+fp+fn
    print(f'accuracy={(tp+tn)/total}, tp={tp}, tn={tn}, fp={fp}, fn={fn}, fail={fail}')
# print(tp, tn, fp, fn)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', type=str, help='path to the ocr result json ', required=True)
    parser.add_argument('-t', '--threshold', type=int, help='threshold of the score ', default=8)
    args = parser.parse_args()
    eval(args.input_file, args.threshold)

if __name__ == '__main__':
    main()