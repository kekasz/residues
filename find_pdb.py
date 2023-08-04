# from glob import glob
#
# def f_ppdb(directory):
#     path_name = f'{directory}/*protonated.pdb'
#     return glob(pathname=path_name)

from os import listdir
from os.path import isfile, isdir, join


def f_pdb(path) -> list:
    if isfile(path):
        if path[-4:] == '.pdb':
            return [path]
        else:
            print('The file you entered is not a PDB file.')
    elif isdir(path):
        files = []
        for item in listdir(path):
            full_path = join(path, item)
            if isfile(full_path) and item[-4:] == '.pdb':
                files.append(full_path)
            else:
                continue
        return files
    else:
        print('You have not entered neither a valid directory nor a valid file.')


def f_ppdb(path) -> list:
    if isfile(path):
        if path[-14:] == 'protonated.pdb':
            return [path]
        else:
            print('The file you entered is not a protonated PDB file.')
    elif isdir(path):
        files = []
        for item in listdir(path):
            full_path = join(path, item)
            if isfile(full_path) and item[-14:] == 'protonated.pdb':
                files.append(full_path)
            else:
                continue
        return files
    else:
        print('You have not entered neither a valid directory nor a valid file.')
