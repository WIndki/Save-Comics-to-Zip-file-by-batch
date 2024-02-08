import os
import json
import time
from setting import setting
RUNNING_DIR, SAVE_DIR, DOWNLOAD_DIR = setting()
#获取文件夹下漫画列表
def get_manga_list(download_path):
    manga_list = []
    manga_name_list = os.listdir(download_path)
    for manga_name in manga_name_list:
        isWaifu2x = "original"
        if os.path.exists(f"{download_path}/{manga_name}/waifu2x"):
            isWaifu2x = "waifu2x"
        manga_list.append(
            {
            "name":manga_name,
            "TotalChapter":len(os.listdir(f"{download_path}/{manga_name}/{isWaifu2x}")),
            "isWaifu2x": isWaifu2x,
            "isZiped": "false",
            "download_path": f"{download_path}/{manga_name}/{isWaifu2x}",
            "save_file": f"{SAVE_DIR}/{manga_name}.zip",
            "add_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            }
        )
    return manga_list

#生成漫画列表json
def create_manga_list_json(download_path):
    manga_list = get_manga_list(download_path)
    with open(f"{RUNNING_DIR}/manga_list.json", 'w', encoding='utf-8') as f:
        json.dump(manga_list, f, ensure_ascii=False, indent=4)
    print(f"[bold green][:white_check_mark:]已生成漫画列表[/]")
    return None