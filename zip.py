import os
import zipfile
from rich import print as print
from rich.console import Console
from rich.prompt import Prompt, Confirm, IntPrompt
console = Console(color_system='256', style=None)

# 压缩zip
def zipfun(manga_name,download_path,save_path,zipmode):
    if not os.path.exists(f"{download_path}/{manga_name}/{zipmode}"):
        print(f"[bold red][:cross_mark:]没有找到[{manga_name}]的下载文件夹[/]")
        return
    z = zipfile.ZipFile(f"{save_path}/{manga_name}.zip", 'w', zipfile.ZIP_DEFLATED)
    #with console.status(f"[bold yellow]正在保存[{manga_name}]为ZIP存档[/]"):
    for dirpath, dirnames, filenames in os.walk(f"{download_path}/{manga_name}/{zipmode}"):
        fpath = dirpath.replace(f"{download_path}/{manga_name}/{zipmode}", '')
        fpath = fpath and fpath + os.sep or ''
        for filename in filenames:
            z.write(os.path.join(dirpath, filename), fpath + filename)
    z.close()
    print(f"[bold green][:white_check_mark:]已将[{manga_name}]保存为ZIP存档[/]")