import os
import mylib

import codecs
import mlx.core as mx
from mlx_vlm.prompt_utils import apply_chat_template
from mlx_vlm.utils import generate, get_model_path, load, load_config, load_image_processor

import ollama

# 画像ファイルをテキストに変換する関数
def process_images_with_prompt(model_path, image_paths, prompt, max_tokens=500, temp=0):
    """
    モデル名、画像ファイルリスト、プロンプトを受け取り、出力テキストを返す関数。

    Args:
        model_path (str): 使用するモデルのパス。
        image_paths (list of str): 入力画像のファイルパスのリスト。
        prompt (str): モデルに与えるプロンプト。

    Returns:
        str: モデルからの出力テキスト。
    """
    # モデルとプロセッサをロード
    model_path = get_model_path(model_path)
#    model, processor = load(model_path, lazy=False, trust_remote_code=True)
#    processor.eos_token_id = 1
    model, processor = load(model_path, lazy=False)
    config = load_config(model_path)

    # チャットテンプレートを適用
    #prompt = codecs.decode(prompt, "unicode_escape")
    #print(prompt)
    formatted_prompt = apply_chat_template(
        processor, config, prompt, num_images=len(image_paths)
    )
    #print(formatted_prompt)
    # 出力を生成
    output = generate(model=model, processor=processor, prompt=formatted_prompt, image=image_paths, max_tokens=max_tokens, temp=temp, verbose=False)
    
    return output

def process_images_with_prompt_ollama(model_path, image_paths, prompt, max_tokens=500, temp=0):
    """
    モデル名、画像ファイルリスト、プロンプトを受け取り、出力テキストを返す関数。

    Args:
        model_path (str): 使用するモデルのパス。
        image_paths (list of str): 入力画像のファイルパスのリスト。
        prompt (str): モデルに与えるプロンプト。

    Returns:
        str: モデルからの出力テキスト。
    """
    #response = ollama.chat(model=model_path, options={"temperature":temp, "num_predict":max_tokens}, messages=[
    response = ollama.chat(model=model_path,  messages=[
        {
            'role': 'user',
            'content': prompt,
#            'images': image_paths
        }
    ])
    
    return response['message']['content']

def process_images_to_txt(model_info, prompt, image_path):
    model_path = model_info['model_path']
    model_name = model_info['model_name']
    model_type = model_info['type']
    max_tokens = model_info['max_tokens']
    temp = model_info['temp']
    if model_type == "mlx":
        print(f"{model_name}で{image_path}を処理中")
        output = process_images_with_prompt(model_path, [image_path], prompt, max_tokens, temp)
    elif model_type == "ollama":
        print(f"{model_name}で{image_path}を処理中")
        output = process_images_with_prompt_ollama(model_path, [image_path], prompt, max_tokens, temp)
    else :
        print("Error: unknown model type.")
        return

    # テキストファイルに出力
    base, ext = os.path.splitext(image_path)
    txt_path = base + "-" + model_name + ".txt"
    mylib.write_text_file(txt_path, output)


def process_list(arg_list, prompt, image_path):
    for model_info in arg_list:
        process_images_to_txt(model_info, prompt, image_path)

if __name__ == "__main__":
    # モデル名、画像パス、プロンプトを設定
    #model_info = {'model_path': "mlx-community/pixtral-12b-4bit", 'model_name': "Pixtral-0", 'type': "mlx", 'max_tokens': 500, 'temp': 0.4}
    model_info =  {'model_path': "mlx-community/Qwen2-VL-7B-Instruct-8bit", 'model_name': "Qwen-0", 'type': "mlx", 'max_tokens': 500, 'temp': 0.4}
    #model_info =  {'model_path': "minicpm-v", 'model_name': "minicpm-v", 'type': "ollama", 'max_tokens': 500, 'temp': 0.4}

    image_paths = ["./student_answers/20250121_0.png"]
    #image_paths = []
    prompt = "白地に黒で日本語手書きで学生番号と氏名が書いてあります．両方正確に読み取って．"
    prompt0 = "白地に黒で日本語手書きで学部，学科，科目，教員名が書いてあります．すべて正確に読み取って．"
    prompt0 = "年，組，番，年，月，日が手書きで書いてあります．すべて読み取って．"
    prompt0 = """
Extract 学部(Faculty), 学科(Department), 科目(Subject), and 教員名(Teacher) from the image.
"""
    prompt0 = """
Extract 年(Grade), 組(Class), 番号(Number) and 年(year), 月(Month), 日(Day) from the image.
"""
    #prompt = codecs.decode(prompt, "unicode_escape")


    # 関数を呼び出して結果を取得
    output = process_images_with_prompt(model_info['model_path'], image_paths, prompt)
    #output = process_images_with_prompt_ollama(model_info['model_path'], image_paths, prompt)

    # 出力を表示
    print("出力結果:")
    print(output)
