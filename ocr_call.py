from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import os
import json
import argparse
from PIL import Image

def get_ocr_client():
    subscription_key = os.environ["OCR_API_KEY"]
    endpoint ='https://ocr-test-cuichi-1.cognitiveservices.azure.com/'
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
    return computervision_client

def ocr(image_path):
    computervision_client = get_ocr_client()
    with open(image_path, "rb") as image_stream:
        ocr_result = computervision_client.recognize_printed_text_in_stream(image_stream)
    return ocr_result

def ocr_webpages(img_dir, json_file):
    print(img_dir, json_file)
    result_list = {}
    for image in os.listdir(img_dir):
        img_path = os.path.join(img_dir, image)
        try:
            ocr_result = ocr(img_path)
        except Exception as e:
            print(e)
            continue
        # image_result = {'region':{}}
        region_data = {}
        for region in ocr_result.regions:

            line_text_list = []
            for line in region.lines:
                line_text = " ".join([word.text for word in line.words])
                line_text_list.append(line_text)
            region_data[region.bounding_box] = '\n'.join(line_text_list)
        result_list[image] = region_data
    with open(json_file, "w") as outfile:
        json.dump(result_list, outfile, indent=4)


def check_bounding_box(bounding_box):
    x1, y1, x2, y2 = bounding_box
    if x2 - x1 < 50 or y2 - y1 < 50:
        return 0
    return 1


'''
    give a image_path and a bounding box of the cropped image
    return the ocr result about the cropped image
'''
def ocr_crop_image(image_path, bounding_box):
    # bounding_box should be a tuple (left, upper, right, lower)

    if not check_bounding_box(bounding_box):
        # print("image is too small")
        return ""

    with Image.open(image_path) as image:
        cropped_image = image.crop(bounding_box)
        cropped_image_path = "cropped_image.png"
        cropped_image.save(cropped_image_path)

    # Now you have a cropped image, proceed with OCR
    computervision_client = get_ocr_client()
    with open(cropped_image_path, "rb") as image_stream:
        try:
            ocr_result = computervision_client.recognize_printed_text_in_stream(image_stream)
        except Exception as e:
            print(e)
            return ""
    # Delete the cropped image after OCR is done
    os.remove(cropped_image_path)
    texts = []
    for region in ocr_result.regions:
        for line in region.lines:
            line_text = " ".join([word.text for word in line.words])
            texts.append(line_text)

    total_text = '\n'.join(texts)
    return total_text

# img_dir = 'imgs'
# json_file = 'ocr_result.json'
# ocr_webpages(img_dir, json_file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_dir', type=str, help='path to the image dir ', required=True)
    parser.add_argument('-o', '--output_file', type=str, help='path to the output file')
    args = parser.parse_args()
    if args.output_file:
        json_file = args.output_file
    else:
        json_file = 'ocr_result.json'

    ocr_webpages(args.input_dir, json_file)

if __name__ == '__main__':
    main()