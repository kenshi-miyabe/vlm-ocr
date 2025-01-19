import mylib
import pdf_to_jpg
import image_to_text

# 学生の解答用紙ファイルのディレクトリ設定
dir_students = './student_answers'
# pdfファイルをjpgに変換
mylib.repeat_func_in_dir(dir_students, ".pdf", pdf_to_jpg.convert_pdf_to_jpg)

# 画像からテキストを抽出
# モデルを設定
#"""
arg_list = [
    {'model_path': "mlx-community/pixtral-12b-4bit", 'model_name': "Pixtral-0", 'type': "mlx", 'max_tokens': 5000, 'temp': 0.4}, #0.94
    {'model_path': "mlx-community/Qwen2-VL-7B-Instruct-8bit", 'model_name': "Qwen-0", 'type': "mlx", 'max_tokens': 5000, 'temp': 0.4}, #0.76
]
#"""

# promptを設定
prompt = """
**Prompt:**  
Please extract all texts from the provided image.
- The background of the image is white, and the text is primarily handwritten in black ink.  
- Structure your extraction into two parts if applicable: **Header** and **Main text**.
If the **Header** section is not present, extract only the **Main text**.

### Instructions for Extraction
1. **Header** (if present)
 Extract the header section of the image in the specified format below. Replace `?????` with the corresponding text extracted from the image.
 
   ```
   # Header
   学生番号 (Student's ID): ?????
   氏名 (Name): ?????
   所属 (Department): 学部 (Faculty) ????? 学科 (Department) ?????
   科目 (Subject): ?????
   教員名 (Teacher): ?????
   年・組・番号 (Class): ?? 年 (Grade) ?? 組 (Class) ?? 番 (Number)
   日付 (Date): ?? 年 (Year) ?? 月 (Month) ?? 日 (Day)
   ```

2. **Main text**  
Extract the main body of the text in **markdown format**. Use `TeX math` syntax for mathematical expressions. Replace `?????` with the corresponding content extracted from the image.

   ```
   # Main text
   ?????
   ```
"""

# 画像内容をテキストに出力
mylib.repeat_func_in_dir(dir_students, ".jpg", lambda path: image_to_text.process_list(arg_list, prompt, path))
