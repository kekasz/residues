from os import listdir
from os.path import isfile, isdir, join


def is_nppdb(path):
    if path[-4:] == '.pdb' and not path[-14:] == 'protonated.pdb' and not isfile(path[:-4] + '_protonated.pdb'):
        return path
    else:
        return False


def is_ppdb(path):
    if path[-14:] == 'protonated.pdb':
        return path
    else:
        return False


def main(path, function):
    if isfile(path):
        if function(path):
            return [path]
        else:
            if function == is_ppdb:
                print('The file you entered is not a protonated PDB file.')
            if function == is_nppdb:
                print('The file you entered is not a non-protonated PDB file.')
    elif isdir(path):
        files = []
        for item in listdir(path):
            full_path = join(path, item)
            if function(full_path):
                files.append(full_path)
            else:
                continue
        return files
    else:
        print('You have not entered neither a valid directory nor a valid file.')


def f_nppdb(path) -> list:
    return main(path, is_nppdb)


def f_ppdb(path) -> list:
    return main(path, is_ppdb)
