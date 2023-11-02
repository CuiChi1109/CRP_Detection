import json
import argparse
def merge_json(file1, file2, output_file):
    with open(file1) as f1, open(file2) as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)

    merged_data = {**data1, **data2}

    with open(output_file, 'w') as f:
        json.dump(merged_data, f, indent=4)

def main(file1, file2, output_file):
    merge_json(file1, file2, output_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file1', type=str, help='file1', required=True)
    parser.add_argument('--file2', type=str, help='file2 ', required=True)
    parser.add_argument('-o', '--output', type=str, help='output file ', default='merged.json')
    args = parser.parse_args()
    main(args.file1, args.file2, args.output)