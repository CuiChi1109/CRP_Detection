# eval performance of gpt result

import os
import json
import shutil
import argparse

IMG_DIR = './dataset/small_test'
def copy_image(img, dir):
    img_path = os.path.join(IMG_DIR, img)
    shutil.copy(img_path, dir)

'''
mode: binary_crp, multilabel_crp, binary_phishing
'''

def eval(file, threshold, store_fail_dir=None):
    gt_dict = {}
    pred_dict = {}
    with open('./dataset/2000_gt.json', 'r') as f:
        gt_dict = json.load(f)
    with open(file, 'r') as f:
        pred_dict = json.load(f)

    tp, tn, fp, fn, fail = 0, 0, 0, 0, 0
    for img in pred_dict.keys():
        try:
            pred = json.loads(pred_dict[img])['CRP_type']
            # print(pred)
            # pred = int(pred_dict[img])
        except:
            # print(img, gt_dict[img], pred_dict[img])
            fail += 1
            # print(img)
            continue
        # pred = 1 if pred == 1
        # try:
        #     gt = 1 if gt_dict[img] > 0
        # except Exception as e:
        #     print(e)
        #     continue
        # if gt == 2:
        #     continue
        gt = gt_dict[img]
        # print(img, gt, pred)
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
                # copy_image(img, './fn_8_gpt35')
                fn += 1
            # print(img, gt_dict[img], pred_dict[img])
            if store_fail_dir is not None:
                copy_image(img, store_fail_dir)
    total = tp+tn+fp+fn+fail
    print(f'accuracy={(tp+tn)/total}, tp={tp}, tn={tn}, fp={fp}, fn={fn}, fail={fail}')
# print(tp, tn, fp, fn)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', type=str, help='path to the gpt result json ', required=True)
    parser.add_argument('-t', '--threshold', type=int, help='threshold of the score ', default=8)
    parser.add_argument('-d', '--failed_dir', type=str)
    # parser.add_argument('-m', '--mode', type=str, help='mode of the eval')
    args = parser.parse_args()
    if args.failed_dir:
        fail_dir = args.failed_dir
    else:
        fail_dir = None
    eval(args.input_file, args.threshold, store_fail_dir=fail_dir)

if __name__ == '__main__':
    main()