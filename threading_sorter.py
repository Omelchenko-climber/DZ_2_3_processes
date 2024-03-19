from threading import Thread
from time import time
from pathlib import Path
import shutil
import sys
import re


CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

EXTANSIONS = {
    'images': ['JPEG', 'PNG', 'JPG', 'SVG'],
    'video': ['AVI', 'MP4', 'MOV', 'MKV'],
    'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
    'audio': ['MP3', 'OGG', 'WAV', 'AMR'],
    'archives': ['ZIP', 'GZ', 'TAR'],
    'unknown_extansions': []
}


def get_folders_list(folder_path: str) -> list:
    if isinstance(folder_path, str) and folder_path.startswith('"'):
        folder_path = folder_path.strip('"')
    folder_path = Path(folder_path)
    subfolders = []
    subfolders.append(folder_path)

    for obj in folder_path.iterdir():
        if obj.is_dir():
            subfolders.extend(get_folders_list(obj))

    return subfolders


def handle_file(folder_path: Path, output_folder: str):
    if output_folder.startswith('"'):
        output_folder = output_folder.strip('"')
    known_extension = False
    output_folder = Path(output_folder)
    counter = 0
    for obj in folder_path.iterdir():
        if obj.is_file():
            counter += 1
            ext = obj.suffix.upper()[1:]
            normalize_obj = normalize_name(obj)
            for key, value in EXTANSIONS.items():
                if ext in value:
                    known_extension = True
                    new_path = output_folder /key /ext
                    copy_file(obj, new_path)
                    break

            if not known_extension:
                new_path = output_folder /'unknown_extansions' /ext
                copy_file(obj, new_path)

    print(folder_path.name, counter, sep='  ***   ')


def copy_file(file_path: Path, copy_path: Path):
    try:
        copy_path.mkdir(exist_ok=True, parents=True)
        shutil.copyfile(file_path, copy_path / normalize_name(file_path).name)
    except OSError as err:
        print(err)


def normalize_name(path_to_file: Path) -> Path:
    name = path_to_file.name.split('.')
    name[0] = re.sub(r'\W', '_', name[0].translate(TRANS))
    new_name = '.'.join(name)
    list_path = str(path_to_file).split('\\')
    list_path[-1] = new_name
    new_path = Path('/'.join(list_path))
    return new_path


if __name__ == '__main__':
    path_to_folder = input('Enter path to folder you want to sort: ')
    output_folder = input('Enter path to folder where you want to creat sorted folders: ')

    subfolders = get_folders_list(path_to_folder)
    threads = []

    # time_before = time()
    # for folder in subfolders:
    #     handle_file(folder, output_folder)

    time_before = time()
    for folder in subfolders:
        thread = Thread(target=handle_file, args=(folder, output_folder, ))
        thread.start()
        threads.append(thread)

    [thread.join() for thread in threads]

    print(f'It lasted {time() - time_before:0.4} sec!')
    print('You can delete your trash. Done!')
