import fitz  # PyMuPDF
from PIL import Image, ImageEnhance # Pillow
import os
import mylib

def convert_pdf_to_jpg(file_name, contrast_ratio=3.0):
    # ファイル拡張子を確認
    if not file_name.endswith('.pdf'):
        mylib.log_error("エラー: PDFファイルを指定してください．")
        return

    # PDFを開く
    pdf_document = fitz.open(file_name)
    output_files = []

    # 各ページを画像に変換
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        pix = page.get_pixmap()  # ピクセルデータを取得

        # 一時的な画像ファイルに保存
        temp_file = f"temp_page{page_number + 1}.png"
        pix.save(temp_file)

        # PILで画像を開き、コントラストを調整
        with Image.open(temp_file) as img:
            enhancer = ImageEnhance.Contrast(img)
            enhanced_img = enhancer.enhance(contrast_ratio)  # コントラスト倍率（例: 2.0で2倍）
            
            # JPGとして保存
            output_file = f"{os.path.splitext(file_name)[0]}_page{page_number + 1}.jpg"
            enhanced_img.save(output_file, format='JPEG')
            output_files.append(output_file)
        
        # 一時ファイルを削除
        os.remove(temp_file)

    pdf_document.close()

    print("以下のJPGファイルが作成されました：")
    for output_file in output_files:
        print(output_file)

def extract_images_from_pdf(pdf_path, output_folder):
    # PDFの元のファイル名（拡張子を除いた部分）を取得
    pdf_base_name = os.path.splitext(os.path.basename(pdf_path))[0]

    # PDFを開く
    pdf_document = fitz.open(pdf_path)

    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        images = page.get_images(full=True)  # ページ内のすべての画像を取得

        for img_index, img in enumerate(images):
            xref = img[0]  # 画像オブジェクトの参照
            base_image = pdf_document.extract_image(xref)  # 画像データを抽出
            image_bytes = base_image["image"]  # バイナリデータ
            image_ext = base_image["ext"]  # 拡張子（例: jpg, png）

            # 保存ファイル名を作成
            output_path = os.path.join(
                output_folder, 
                f"{pdf_base_name}_page{page_number + 1}_image{img_index + 1}.{image_ext}"
            )
                        
            # ファイルに保存
            with open(output_path, "wb") as output_file:
                output_file.write(image_bytes)
                print(f"画像を保存しました：{output_path}")

    pdf_document.close()

# 例: extract_images_from_pdf("input.pdf", "output_images")

def resize_image(input_path, output_path, new_size, dpi):
    """
    Args:
        input_path (str): 元の画像ファイルのパス．
        output_path (str): リサイズ後の画像を保存するパス．
        new_size (tuple): 最大サイズ (幅, 高さ) をピクセル単位で指定．
        dpi (tuple): DPI (dots per inch) を指定．

    Returns:
        None
    """
    try:
        # 画像を開く
        with Image.open(input_path) as img:
            print(f"元のモード: {img.mode}, サイズ: {img.size}, DPI: {img.info.get('dpi', '未指定')}")

            # リサイズ
            img = img.resize(new_size)

            # リサイズ後の画像を保存
            img.save(output_path, dpi=dpi, compress_level=0, optimize=True)
            print(f"リサイズ後の画像を保存しました: {output_path}")
            print(f"リサイズ後のモード: {img.mode}, リサイズ後のサイズ: {img.size}, DPI: {dpi}")

    except Exception as e:
        print(f"エラーが発生しました: {e}")

def resize_image_with_aspect_ratio(input_path, output_path, max_pixels, dpi=72):
    try:
        # 画像を開く
        with Image.open(input_path) as img:
            print(f"元のモード: {img.mode}, サイズ: {img.size}, DPI: {img.info.get('dpi', '未指定')}")

            # 元の画像サイズを取得
            original_width, original_height = img.size

            # アスペクト比を計算
            aspect_ratio = original_width / original_height

            # リサイズ後のサイズを計算
            if original_width * original_height > max_pixels:
                scale_factor = (max_pixels / (original_width * original_height)) ** 0.5
                new_width = int(original_width * scale_factor)
                new_height = int(original_height * scale_factor)
            else:
                new_width, new_height = original_width, original_height

            new_size = (new_width, new_height)

            # リサイズ
            img = img.resize(new_size, Image.LANCZOS)

            # リサイズ後の画像を保存
            img.save(output_path, dpi=(dpi, dpi), compress_level=0, optimize=True)
            print(f"リサイズ後の画像を保存しました: {output_path}")
            print(f"リサイズ後のモード: {img.mode}, リサイズ後のサイズ: {img.size}, DPI: {dpi}")

    except Exception as e:
        print(f"エラーが発生しました: {e}")

# 使用例
#input_image = "large_image.jpg"  # 入力画像パス
#output_image = "resized_image.jpg"  # 出力画像パス
#max_dimensions = (1024, 1024)  # 最大幅と高さ
#resize_image_with_aspect_ratio(input_image, output_image, max_dimensions)



if __name__ == "__main__":
    #input_file = input("PDFファイル名を入力してください：")
    #dir = "./student_answers/"
    #path = "./student_answers/20250121.pdf"
    #extract_images_from_pdf(path, dir)

    input_path = "./student_answers/20250121_page1_image1_1.png"
    output_path = "./student_answers/20250121_page1_image1_1_small.png"
#    max_pixels = 28 * 28 * 1280
    max_pixels = 28 * 28 * 512
    resize_image_with_aspect_ratio(input_path, output_path, max_pixels, dpi=72)
