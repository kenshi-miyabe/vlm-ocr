import os
from PIL import Image

def crop_image(img_path, output_path, crop_box):
    with Image.open(img_path) as img:
        # 切り抜き
        cropped_image = img.crop(crop_box)
        # 保存
        cropped_image.save(output_path)
        # 結果を表示 (必要に応じて)
        #cropped_image.show()

height_cm = 29.67
width,height = 3288, 4672
#width, height = 9892, 14016

# 切り抜く領域の座標を指定 (左, 上, 右, 下)
crop_box_list = []
#crop_box = (0, int(height*3.85/height_cm), width, int(height*4.75/height_cm))  # 学生番号，氏名
crop_box = (0, int(height*4.25/height_cm), width, int(height*5.25/height_cm))  # 学生番号，氏名
crop_box_list.append(crop_box)
crop_box = (0, int(height*5.25/height_cm), width, int(height*6.2/height_cm))  # 所属，科目，教員名
crop_box_list.append(crop_box)
crop_box = (0, int(height*6.2/29.7), width, int(height*7.15/29.7))  # 年組番号日付
crop_box_list.append(crop_box)
len_crop_box = len(crop_box_list)

path = "./student_answers/20250115a_page1_image1.png"
for i in range(len_crop_box):
    # 画像を開く
    output_path = os.path.splitext(path)[0] + "_" + str(i) + ".png"
    crop_box = crop_box_list[i]
    crop_image(path, output_path, crop_box)


