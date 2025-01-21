from PIL import Image

# 画像を開く
image = Image.open("./student_answers/20250121_001_page1_image1.png")

width, height = 9892, 14016

# 切り抜く領域の座標を指定 (左, 上, 右, 下)
crop_box = (0, int(height*3.85/29.7), width, int(height*4.75/29.7))  # 学生番号，氏名

# 切り抜き
cropped_image = image.crop(crop_box)

# 切り抜いた画像を保存
cropped_image.save("./student_answers/cropped_image.png")

# 結果を表示 (必要に応じて)
cropped_image.show()
