import mylib
import pdf_to_image
import image_to_text

# 学生の解答用紙ファイルのディレクトリ設定
dir_students = './student_answers'
#mylib.repeat_func_in_dir(dir_students, ".pdf", pdf_to_jpg.convert_pdf_to_jpg)
# ScanSnapで取り込んだpdfファイルから画像を抽出
#mylib.repeat_func_in_dir(dir_students, ".pdf", lambda path: pdf_to_image.extract_images_from_pdf(path, dir_students))
#new_size = (724, 1024)
#new_size = (1448, 2048) #4分くらい
#new_size = (1810, 2560) #メモリオーバー
#dpi = (96.012, 96.012)
#mylib.repeat_func_in_dir(dir_students, ".png", lambda path: pdf_to_image.resize_image(path, path, new_size, dpi))
#new_size = (512, 512)
max_pixels = 28 * 28 * 1280
mylib.repeat_func_in_dir(dir_students, ".png", lambda path: pdf_to_image.resize_image_with_aspect_ratio(path, path, max_pixels))


# 画像からテキストを抽出
# モデルを設定
#"""
arg_list = [
#    {'model_path': "mlx-community/QVQ-72B-Preview-4bit", 'model_name': "QVQ", 'type': "mlx", 'max_tokens': 15000, 'temp': 0},
#    {'model_path': "mlx-community/Qwen2-VL-72B-Instruct-4bit", 'model_name': "Qwen-72B-0", 'type': "mlx", 'max_tokens': 500, 'temp': 0.4},
#    {'model_path': "mlx-community/pixtral-12b-4bit", 'model_name': "Pixtral-0", 'type': "mlx", 'max_tokens': 5000, 'temp': 0.4},
    {'model_path': "mlx-community/Qwen2-VL-7B-Instruct-8bit", 'model_name': "Qwen-0", 'type': "mlx", 'max_tokens': 500, 'temp': 0.4},
]
#"""

# promptを設定
prompt = """
**Prompt:**  
Please extract all texts from the provided image, accurately and completely.
The background of the image is white, and the text is primarily handwritten in black ink, mainly in Japanese.
Structure your extraction into two parts if applicable: **Header** and **Main text**.
If the **Header** section is not present, extract only the **Main text**.

1. **Header** (if present)
Extract the header section of the image in the specified format below.
Replace `?????` with the corresponding text extracted from the image.

=====
# Header
学生番号 (Student's ID): ?????
氏名 (Name): ?????
所属 (Department): 学部 (Faculty) ????? 学科 (Department) ?????
科目 (Subject): ?????
教員名 (Teacher): ?????
年・組・番号 (Class): ?? 年 (Grade) ?? 組 (Class) ?? 番 (Number)
日付 (Date): ?? 年 (Year) ?? 月 (Month) ?? 日 (Day)
=====

2. **Main text**  
Extract the main body of the text in **markdown format**.
Use `TeX math` syntax for mathematical expressions. For example: '$y=x^2$'.
Replace `?????` with the corresponding content extracted from the image.

=====
# Main text
?????
=====

Note: Accurately extract only what is written.
"""

# 画像内容をテキストに出力
mylib.repeat_func_in_dir(dir_students, ".png", lambda path: image_to_text.process_list(arg_list, prompt, path))
