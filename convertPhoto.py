import os
import zipfile
from PIL import Image
import pillow_avif
import shutil
import threading
from alive_progress import alive_bar
from rich import print as print
from rich.console import Console
from rich.prompt import Prompt, Confirm, IntPrompt
console = Console(color_system='256', style=None)

def unzip(filePath):
    with console.status(f"[bold yellow]正在解压[{filePath}]的ZIP存档[/]"):
        with zipfile.ZipFile(filePath, 'r') as z:
            save_path = filePath.replace('.zip', '')
            z.extractall(save_path)
            rename_file(save_path)
            z.close()
    print("\n" + f"[bold green][:white_check_mark:]已解压[{filePath}]的ZIP存档[/]")

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

def convert_to_avif(image_file):
    img = Image.open(image_file)
    img.save(image_file.replace('.jpg', '.avif'), 'AVIF', quality=85, subsampling='4:2:0')
    img.close()
    remove_file(image_file)

def remove_file(image_file):
    os.remove(image_file)

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
    print("\n" + f"[bold green][:white_check_mark:]已转换[{dir_path}]的图片格式[/]")

def remove_dir(dir_path):
    shutil.rmtree(dir_path)
    
def main():
    files = os.listdir("D:\manga\download")
    for file in files:
        file_path = os.path.join("D:\manga\download", file)
        if file_path.endswith('.zip'):
            unzip(file_path)
            remove_file(file_path)
            file_path = file_path.replace('.zip', '')
            convert_by_sorting(file_path)
            zip(file_path)
            remove_dir(file_path)

main()