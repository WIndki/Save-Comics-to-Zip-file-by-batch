import os
import json
from rich import print as print
from rich.console import Console
from setting import setting
from zip import zipfun
from list import get_manga_list, create_manga_list_json
from remove_cache import remove_download_cache
RUNNING_DIR, SAVE_DIR, DOWNLOAD_DIR = setting()

console = Console(color_system='256', style=None)


def main():
    if os.path.exists(f"{RUNNING_DIR}/manga_list.json"):
        manga_list = json.load(open(f"{RUNNING_DIR}/manga_list.json", 'r', encoding='utf-8'))
        total = len(manga_list)
        manga_list_update = get_manga_list(DOWNLOAD_DIR)
        new_total = len(manga_list_update) + total
        for manga in manga_list_update:
            manga_list.append(manga)
    else:
        create_manga_list_json(DOWNLOAD_DIR)
        manga_list = json.load(open(f"{RUNNING_DIR}/manga_list.json", 'r', encoding='utf-8'))
        total = 0
        new_total = len(manga_list)
    if new_total == 0:
        print(f"[yellow]没有新的下载[/]")
        return
    else:
        print(f"[yellow]发现{new_total-total}个新的下载[/]")
        input("按回车键开始压缩...")
    for manga in (manga_list[total:]) :
        if manga["isZiped"] == "false":
            zipfun(manga["name"],DOWNLOAD_DIR,SAVE_DIR,manga["isWaifu2x"])
            manga["isZiped"] = "true"
    with open(f"{RUNNING_DIR}/manga_list.json", 'w', encoding='utf-8') as f:
        json.dump(manga_list, f, ensure_ascii=False, indent=4)
    for manga in (manga_list) :
        remove_download_cache(manga["name"])
    print(f"[green]压缩完成[/]")

if __name__ == "__main__":
    main()
    input("按回车键退出...")
