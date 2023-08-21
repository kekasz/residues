import argparse
from os import system as terminal
from find_pdb import f_nppdb, f_ppdb
from find_invalid import f_invalid

protonated_files = []
invalid_molecules = []
invalid_bond_cases = []
lines = []


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--protonate',
        action='store',
        nargs='?',
        type=str,
        const=''
    )
    parser.add_argument(
        '--select',
        action='store',
        nargs='?',
        type=str,
        const=''
    )
    parser.add_argument(
        '--find',
        action='store',
        nargs='?',
        type=str,
        const=''
    )
    return parser


def protonate(path):
    for file in path:
        terminal(f'/home/l/pycharmprojects/residues/protonisation/bin/pdb2pqr30 --noopt --nodebump '
        # terminal(f'/root/protonation/bin/pdb2pqr30 --noopt --nodebump '
                 f'--pdb-output {file[:-4]}_protonated.pdb {file} {file[:-4]}_protonated.pqr --titration-state-method '
                 f'propka --with-ph 7.2; rm {file[:-4]}_protonated.pqr')
        protonated_files.append(file[:-4] + 'protonated.pdb')


def find(path):
    b = 0
    a = len(path)
    for file in path:
        invalid = f_invalid(file)
        if invalid:
            lines.append(invalid[3])
            invalid_molecules.append(invalid[0:2])
            for case in invalid[2]:
                invalid_bond_cases.append(case)
        b += 1
        print(f'{b}/{a}')


def main():
    selected_files = []
    args = build_parser().parse_args()

    if args.select:
        if args.select == '':
            if args.protonate:
                print('You do not need to use --select for automatic selection when you use --protonate as well.')
            else:
                print('Please provide a path to the directory to be searched.')
        elif not args.find:
            selected_files = f_nppdb(args.select)
        else:
            selected_files = f_ppdb(args.select)

    if args.protonate:
        if args.protonate == '':
            if selected_files:
                protonate(selected_files)
            else:
                print('Please provide a path to the PDBs\' to be protonated directory, to a single file or use '
                      '--select')
        else:
            protonate(f_nppdb(args.protonate))

    if args.find:
        if args.find == '':
            if protonated_files:
                find(protonated_files)
            elif selected_files:
                find(selected_files)
            else:
                print('Please provide a path to the PDBs\' to be examined directory, to a single file or use --select.')
        else:
            find(f_ppdb(args.find))

        if invalid_molecules:
            print('\n------------------------------------------------RESULTS'
                  ':------------------------------------------------\n')
            types = set()
            types_count = dict()
            for case in invalid_bond_cases:
                a = len(types)
                types.add(case)
                if len(types) > a:
                    types_count[case] = 1
                else:
                    types_count[case] += 1
            for case, times in types_count.items():
                print(f'Times of {case} found: {times}.')

            for line in lines:
                print(line)


if __name__ == '__main__':
    main()
