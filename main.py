from typing import List
import pathlib
import tkinter as tk
from tkinter import filedialog
from collections import defaultdict
import hashlib
import uuid

root = tk.Tk()
root.withdraw()


def get_parent_directory():
    parent_directory = pathlib.Path(filedialog.askdirectory())

    if not parent_directory.exists():
        print("Path doesn't exist, try again.")
        get_parent_directory()
    else:
        return parent_directory


def get_children(parent_directory: pathlib.Path):
    children = []

    for child in parent_directory.iterdir():
        children.append(child)

    return children


def get_list_of_all_files(parent_directory: pathlib.Path):
    return filter(pathlib.Path.is_file, parent_directory.rglob("*"))


def create_md5_dictionary(files: List[pathlib.Path]):
    md5_dict = defaultdict(list)

    for file in files:
        with open(file, "rb") as filecontents:
            md5_sum = hashlib.md5(filecontents.read()).hexdigest()

            md5_dict[md5_sum].append(file)

    return md5_dict


def create_duplicates_subfolder(parent_directory: pathlib.Path):
    compound_path = parent_directory.joinpath("duplicates")

    compound_path.mkdir(parents=False, exist_ok=True)

    return compound_path


def move_duplicate_files(md5_dictionary: defaultdict, duplicates_path: pathlib.Path):
    for _, value in md5_dictionary.items():
        duplicates = value[1:]
        if len(duplicates) > 0:
            for duplicate in duplicates:
                source = duplicate
                destination = duplicates_path.joinpath(
                    str(uuid.uuid4()) + "-" + source.name
                )
                source.replace(destination)


def main():
    parent_directory = get_parent_directory()
    children = get_children(parent_directory)

    print("Parent Directory:", parent_directory)
    print("Sample of children: ")
    for child in children[:5]:
        print(child)
    correct_dir = input("Correct directory? y/n: ")
    if not correct_dir == "y":
        return

    all_files = get_list_of_all_files(parent_directory)
    dupe_dict = create_md5_dictionary(all_files)
    dupes_folder = create_duplicates_subfolder(parent_directory)

    move_duplicate_files(dupe_dict, dupes_folder)


if __name__ == "__main__":
    main()
