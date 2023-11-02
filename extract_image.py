import os
import shutil
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_dir', type=str, help='path to the srs dir ', required=True)
    parser.add_argument('-d', '--dst_dir', type=str, help='path to the dst dir', required=True)
    args = parser.parse_args()

    for image_name in os.listdir(args.input_dir):
        img_path = os.path.join(args.input_dir, image_name, 'shot.png')
        dst_img_path = os.path.join(args.dst_dir, image_name+'.png')
        print(img_path, image_name)
        shutil.copy(img_path, dst_img_path)

if __name__ == '__main__':
    main()