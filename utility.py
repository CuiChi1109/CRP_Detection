from PIL import Image, ImageDraw
import json

def draw_bounding_box(image_path, bounding_box_list):
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    for box in bounding_box_list:
        # bounding_box_list中的每个box应该是一个元组或列表，格式为(left, top, right, bottom)
        draw.rectangle(box, outline="red", width=2)

    img = img.convert('RGB')

    # 显示图像（这将在默认的图像查看器中打开图像）
    # img.show()

    # 如果你想保存带有边界框的新图像，可以使用以下代码：
    img_name = image_path[:-4]
    img.save('result.jpg')

# 使用函数
def get_bounding_box_list(image_name, json_file):
    with open(json_file, 'r') as f:
        ocr_result = json.load(f)

    img_result = ocr_result[image_name]
    bounding_box_list = []
    box_list = list(img_result.keys())
    for box in box_list:
        tmp = list(map(int, box.split(',')))
        new_box = [tmp[0], tmp[1], tmp[0]+tmp[2], tmp[1]+tmp[3]]
        bounding_box_list.append(new_box)
    return bounding_box_list

def get_text(image_name, json_file):
    with open(json_file, 'r') as f:
        ocr_result = json.load(f)

    img_result = ocr_result[image_name]
    text_list = list(img_result.values())
    total_text = '\n'.join(text_list)
    return total_text


# bounding_box_list = get_bounding_box_list('coupontrak.com_[2022_12_20]_0.png', 'ocr_result.json')
# # print(bounding_box_list)
# image_path = 'imgs/coupontrak.com_[2022_12_20]_0.png'
# # draw_bounding_box(image_path, bounding_box_list)
# text = get_text('coupontrak.com_[2022_12_20]_0.png', 'ocr_result.json')
# print(text)
