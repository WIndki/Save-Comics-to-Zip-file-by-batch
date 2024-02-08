import shutil
import os
from rich import print as print
from rich.console import Console
from setting import setting
console = Console(color_system='256', style=None)
DOWNLOAD_DIR = setting()[2]
def remove_download_cache(manga_name):
    manga_dir = f"{DOWNLOAD_DIR}/{manga_name}"
    if os.path.exists(manga_dir):
        shutil.rmtree(manga_dir)
        print(f"[bold green][:white_check_mark:]已删除{manga_dir}下载缓存[/]")