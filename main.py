from typing import List
import pathlib
import tkinter as tk
from tkinter import filedialog
from collections import defaultdict
import hashlib
import uuid

root = tk.Tk()
root.withdraw()


def is_valid_directory(directory: pathlib.Path):
    return directory.exists() and (directory != "" or directory is not None)


def get_parent_directory():
    parent_directory = pathlib.Path(filedialog.askdirectory())

    if not is_valid_directory(parent_directory):
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


def create_duplicates_subfolder(
    parent_directory: pathlib.Path, dupes_subfolder: pathlib.Path
):
    compound_path = parent_directory.joinpath(dupes_subfolder)

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


def delete_duplicate_files(md5_dictionary: defaultdict):
    for _, value in md5_dictionary.items():
        duplicates = value[1:]
        if len(duplicates) > 0:
            for duplicate in duplicates:
                duplicate.unlink()


def delete_or_cut(parent_directory: pathlib.Path):
    delete_or_not = input(
        "Delete files (default) or enter folder name to cut duplicates into: "
    )

    if delete_or_not == "":
        return delete_or_not
    else:
        duplicates_folder = parent_directory.joinpath(delete_or_not)

        try:
            duplicates_folder.mkdir()
            return duplicates_folder
        except FileExistsError:
            print("Folder already exists, input a unique file name.")
            delete_or_not(parent_directory)
        except:
            print(
                "Could not create folder. Check folder name for invalid characters, or file creation permissions."
            )
            delete_or_not(parent_directory)


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
    dupe_dir = delete_or_cut(parent_directory)
    dupe_dict = create_md5_dictionary(all_files)

    if dupe_dir != "":
        dupes_folder = create_duplicates_subfolder(parent_directory, dupe_dir)
        move_duplicate_files(dupe_dict, dupes_folder)
    else:
        delete_duplicate_files(dupe_dict)


if __name__ == "__main__":
    main()
