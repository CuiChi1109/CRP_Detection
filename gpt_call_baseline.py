from gpt_api import *
from utility import *
from tqdm import tqdm
import time
import argparse
import os



# 创建一个GPTConversationalAgent的实例

def gpt_pred(input_file, output_file, input_dir, model, prompt_type):
    agent = GPTConversationalAgent(model=model, prompts=prompts_dict[prompt_type])

    # with open(input_file, 'r') as f:
    #     ocr_result = json.load(f)

    for image in tqdm(os.listdir(input_dir)):
        try:
            with open(output_file, 'r') as f:
                result = json.load(f)
        except:
            result = {}

        if image in list(result.keys()):
            continue

        try:
            ocr_text = get_text(image, input_file)
        except:
            print(f"No {image} in ocr result!")
            continue

        while True:
            try:
                gpt_pred = agent.call_gpt(ocr_text, image)
                result[image] = gpt_pred  # 更新结果字典
                time.sleep(0.3)
                with open(output_file, 'w') as f:
                    json.dump(result, f, indent=4)
                    print("Save to json")
            except Exception as e:
                print("Error occured")
                if e == openai.error.RateLimitError:
                    print(f"Rate limit reached. Saving progress and waiting for 1 seconds.")

                    # 保存当前的结果到JSON文件
                    with open(output_file, 'w') as f:
                        json.dump(result, f, indent=4)

                    # 等待所需的时间
                    time.sleep(10)

                    # 重新加载结果字典
                    with open(output_file, 'r') as f:
                        result = json.load(f)
                else:
                    print("This is another error", e)

                    break

                continue  # 重新尝试API调用
            break  # 如果成功，跳出循环

    # 保存最终的结果到JSON文件
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=4)




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--ocr_result', type=str, help='path to the ocr result json ', default='ocr_result/total_ocr_result.json')
    parser.add_argument('-o', '--output_file', type=str, help='path to the output file')
    parser.add_argument('-i', '--input_dir', type=str, help='path to the image dir ', required=True)
    parser.add_argument('-m', '--model', type=str, help='model name', default="gpt-3.5-turbo")
    parser.add_argument('-p', '--prompt_type', type=str, help='prompt_type', default='simple')
    args = parser.parse_args()

    if not args.output_file:
        sub_input_dir = args.input_dir.split('/')[-1]
        args.output_file = f'gpt_result/{sub_input_dir}_{args.model}_{args.prompt_type}.json'

    gpt_pred(args.ocr_result, args.output_file, args.input_dir, args.model, args.prompt_type)

if __name__ == '__main__':
    main()
