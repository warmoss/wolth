import os
import shutil
import zipfile


def read_lines(filename):
    if not os.path.isfile(filename):
        return None
    with open(filename, "r") as f:
        return f.readlines()


def read_all(filename):
    if not os.path.isfile(filename):
        return None
    with open(filename, "r") as f:
        return "".join(f.readlines())


def write_all(filename, data, mode="w"):
    with open(filename, mode) as f:
        f.write(data)


def path_join(*path_parts: str):
    return os.path.join(*path_parts)


def exists(target):
    return os.path.exists(target)


def rmdirs(target):
    if os.path.exists(target):
        shutil.rmtree(target)


def mkdirs(target):
    os.makedirs(target, exist_ok=True)


def remove(filename):
    os.remove(filename)


def unzip(filename: str, extract_to: str):
    with zipfile.ZipFile(filename, "r") as zip_ref:
        zip_ref.extractall(extract_to)
