from os import walk, path


def get_folder_names(filepath="."):
    if not path.exists(filepath):
        raise Exception("Invalid path")
    return [name for name in next(walk(filepath))[1]]
