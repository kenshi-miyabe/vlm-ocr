# エラーメッセージをファイルに記録する関数
import os

# txtファイルを書き込む関数
def write_text_file(file_path, content):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"ファイルを{file_path}に書き込みました。")
    except Exception as e:
        log_error(f"エラーが発生しました: {e}")

def log_error(error_message, file_name="error.txt"):
    """
    エラーメッセージを指定されたファイルに追記する関数。

    Parameters:
        error_message (str): ログとして記録するエラーメッセージ。
        file_name (str): エラーログを記録するファイル名（デフォルトは 'error.txt'）。
    """
    
    print(error_message)

    try:
        with open(file_name, "a", encoding="utf-8") as file:
            file.write(error_message + "\n")
        print(f"エラーが{file_name}に記録されました。")
    except Exception as e:
        print(f"エラーログの記録に失敗しました: {e}")
    
    return error_message

# dir内のstrで終わるファイルすべてにfuncを適用する関数
def repeat_func_in_dir(dir, str, func):
    """
    指定されたディレクトリ内の指定された文字列で終わるファイルに指定された関数を繰り返し適用する関数。

    Parameters:
        dir (str): ファイルを検索するディレクトリのパス。
        func (function): 適用する関数。
        str (str): ファイル名の末尾に含まれる文字列。

    Returns:
        None
    """
    try:
        for file_name in sorted(os.listdir(dir)):
            if file_name.endswith(str):
                file_path = os.path.join(dir, file_name)
                print(f"{file_path}を処理中")
                func(file_path)
    except Exception as e:
        log_error(f"エラーが発生しました: {e}")