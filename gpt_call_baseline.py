import openai
import json
from utility import *
from tqdm import tqdm
import time
import argparse
import os

openai.api_key = os.environ["OPENAI_API_KEY"]

PROM_SIMPLE = "You are an assistant, helping people with identifying phishing websites. \
                            Given the words extracted from the webpage, please tell the user if the webpage is credential-requiring or not. \
                            Please just give a score from 1-10, 1 is not credential, 10 is credential. Remember give nothing except a number. \
                            For example, if a webpage ask user about username and password, you should score it 10"
PROM_COMPLEX = "You are a web programmer and security expert working on detecting phishing website. Now you have a task about figuring out whether a webpage is a credential-requiring page(CRP) or not. To complete this task, follow these sub-tasks: \
                Explicit: Analyze whether the webpage want users to give out sensitive information such as username, email, password, and credit card number.\
                Implicit: Analyze whether there is any button or link that linked to an explicit CRP.\
                Submit your findings as JSON-formatted output with the following keys: \
                CRP_score: int (indicates CRP on scale of 1-10) \
                CRP_type: int (0 for non-CRP,  1 for implicit, 2 for explicit) \
                Phishing_score: int (indicates phishing risk on scale of 1-10) \
                Noted, the text may not always be accurate. \
                Example of credential-requiring: \
                Having inputs fields about username, password, credit card number or buttons to login \
                Offer unexpected rewards \
                Informing the user of a missing package or additional payment required \
                Displaying fake security warnings \
                This is the text extracted from screenshots of webpages. \ "

class GPTConversationalAgent:
    def __init__(self, model, prompts=PROM_SIMPLE):
        self.messages = [
            {
                "role": "system",
                "content": prompts
            }
        ]
        self.model = model

    def call_gpt(self, text, image=None):
        if image != None:
            print(f'Call gpt on {image}')
        self.messages.append({"role": "user", "content": text})
        completion = openai.ChatCompletion.create(
            model=self.model,
            # model='gpt-4',
            messages=self.messages,
            temperature=0.0
        )
        response = completion.choices[0].message.content
        # self.messages.append({"role": "assistant", "content": response})
        self.messages.pop()     # delete the user ask
        return response

# 创建一个GPTConversationalAgent的实例

def gpt_pred(input_file, output_file, input_dir, model="gpt-3.5-turbo"):
    agent = GPTConversationalAgent(model, prompts=PROM_COMPLEX)

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
    parser.add_argument('-c', '--ocr_result', type=str, help='path to the ocr result json ', required=True)
    parser.add_argument('-o', '--output_file', type=str, help='path to the output file', required=True)
    parser.add_argument('-i', '--input_dir', type=str, help='path to the ocr result json ', required=True)
    args = parser.parse_args()
    gpt_pred(args.ocr_result, args.output_file, args.input_dir)

if __name__ == '__main__':
    main()
