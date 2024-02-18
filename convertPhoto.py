import os
import zipfile
from PIL import Image
import pillow_avif
import shutil
import threading
import json
from alive_progress import alive_bar
from rich import print as print
from rich.console import Console
from rich.prompt import Prompt, Confirm, IntPrompt
console = Console(color_system='256', style=None)

#解压缩函数
def unzip(filePath):
    with console.status(f"[bold yellow]正在解压[{filePath}]的ZIP存档[/]"):
        with zipfile.ZipFile(filePath, 'r') as z:
            save_path = filePath.replace('.zip', '')
            z.extractall(save_path)
            rename_file(save_path)
            z.close()

#重命名函数，避免中文乱码,可复用
def rename_file(file_path):
    os.chdir(file_path)
    for file in os.listdir('.'):
        try:
            new_name = file.encode('cp437').decode('gbk')
            os.rename(file, new_name)
        except:
            pass

        if os.path.isdir(file):
            rename_file(file)
            os.chdir('..')
    os.chdir('..')

#压缩函数
def zip(dir_path):
    zip_file = dir_path + 'av1' + '.zip'
    dir_list = os.listdir(dir_path)
    manga_name = os.path.basename(dir_path)
    for dir in dir_list:
        if dir == manga_name :
            dir_path = os.path.join(dir_path, manga_name)
    z = zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED)
    with console.status(f"[bold yellow]正在保存[{manga_name}]为ZIP存档[/]"):
        for dirpath, dirnames, filenames in os.walk(f"{dir_path}"):
            fpath = dirpath.replace(f"{dir_path}", '')
            fpath = fpath and fpath + os.sep or ''
            for filename in filenames:
                z.write(os.path.join(dirpath, filename), fpath + filename)
    z.close()

#转换为avif格式
def convert_to_avif(image_file):
    img = Image.open(image_file)
    img.save(image_file.replace('.jpg', '.avif'), 'AVIF', quality=85, subsampling='4:2:0')
    img.close()
    remove_file(image_file)

#删除文件，调用os.remove
def remove_file(image_file):
    os.remove(image_file)

#删除文件夹，调用shutil.rmtree
def remove_dir(dir_path):
    shutil.rmtree(dir_path)

#多线程转换图片格式
def convert_by_sorting(dir_path):
    with console.status(f"[bold yellow]正在转换[{dir_path}]的图片格式[/]"):
        threads = [] 
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.endswith('.jpg'):
                    task = threading.Thread(target=convert_to_avif, args=(os.path.join(root, file),))
                    threads.append(task)
                    if len(threads) > 10 or len(threads) == len(files) - 1:
                        for task in threads:
                            task.start()
                        for task in threads:
                            task.join()
                        threads = []
                    #convert_to_avif(os.path.join(root, file))
                    #remove_file(os.path.join(root, file))
    print(f"[bold green][:white_check_mark:]已转换[{dir_path}]的图片格式[/]")

#首次运行时的配置
def first_run():
    default=os.getcwd()
    manga_path = Prompt.ask("请输入你的漫画存档路径", default=default)
    output_path = Prompt.ask("请输入你的输出路径", default=default)
    config = {
        "manga_path": manga_path,
        "output_path": output_path
    }
    with open(os.path.join(default,'config.json'), 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

#导入配置文件
def import_config():
    config_path = os.path.join(os.getcwd(), 'config.json')
    if not os.path.exists(config_path):
        first_run()
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config

def main():
    config = import_config()
    files = os.listdir(config['manga_path'])
    print(f"[yellow]共发现有{len(files)}个文件[/]")
    input("按下回车键开始处理")
    for file in files:
        file_path = os.path.join(config['manga_path'], file)
        if file_path.endswith('.zip') and not file_path.endswith('av1.zip'):
            try:
                unzip(file_path)
                remove_file(file_path)
                file_path = file_path.replace('.zip', '')
                convert_by_sorting(file_path)
                zip(file_path)
                remove_dir(file_path)
            except Exception as e:
                print(f"[bold red][:x:]处理[{file_path}]失败[/]<{e}>")
                with open('error.log', 'a') as f:
                    f.write(f"处理{file_path}失败\n")
                pass

if __name__ == '__main__':
    main()