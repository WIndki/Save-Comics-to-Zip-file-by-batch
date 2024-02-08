import os
import json
from rich.prompt import Prompt
from rich import print as print
DEFAULT_DIR = os.getcwd()
#导入设置
def import_setting():
    if os.path.exists(f"{os.getcwd()}/setting.json"):
        setting = json.load(open(f"{DEFAULT_DIR}/setting.json", 'r', encoding='utf-8'))
        global RUNNING_DIR, SAVE_DIR, DOWNLOAD_DIR
        RUNNING_DIR = setting["RUNNING_DIR"]
        SAVE_DIR = setting["SAVE_DIR"]
        DOWNLOAD_DIR = setting["DOWNLOAD_DIR"]
    else:
        print(f"[bold red]未找到setting.json文件，请手动输入运行目录、保存目录、下载目录[/]")
        input_setting()
        setting = {
            "RUNNING_DIR": RUNNING_DIR,
            "SAVE_DIR": SAVE_DIR,
            "DOWNLOAD_DIR": DOWNLOAD_DIR
        }
        with open(f"{DEFAULT_DIR}/setting.json", 'w', encoding='utf-8') as f:
            json.dump(setting, f, ensure_ascii=False, indent=4)
        print(f"[bold green][:white_check_mark:]设置已保存[/]")
#输入设置
def input_setting():
    global RUNNING_DIR, SAVE_DIR, DOWNLOAD_DIR
    RUNNING_DIR = Prompt.ask("请输入运行目录", default=DEFAULT_DIR)
    SAVE_DIR = Prompt.ask("请输入保存目录", default=DEFAULT_DIR+"/download")
    DOWNLOAD_DIR = Prompt.ask("请输入下载目录", default=DEFAULT_DIR+"/commies")

#setting函数
def setting():
    import_setting()
    return RUNNING_DIR, SAVE_DIR, DOWNLOAD_DIR
