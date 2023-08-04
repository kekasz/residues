import argparse
import os
from find_pdb import f_pdb, f_ppdb
from find_invalid import f_invalid


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--protonate',
        action='store',
        nargs='?',
        type=str,
        const=str(os.getcwd())
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
    args = parser.parse_args()

    selection = []
    protonation = []

    if isinstance(args.select, str):
        if args.select == '':
            if isinstance(args.protonate, str):
                print('You do not need to use --select for automatic selection when you use --protonate as well.')
            else:
                print('Please provide a path to the directory to be searched.')
        elif not isinstance(args.find, str):
            selection = f_pdb(args.select)
        else:
            selection = f_ppdb(args.select)

    if isinstance(args.protonate, str):
        if args.protonate == '':
            if len(selection) != 0:
                for file in selection:
                    os.system(f'{file} ; do pdb2pqr30 --noopt --nodebump --pdb-output "${{x:0:-4}}"_protonated.pdb '
                              f'$x "${{x:0:-4}}"_protonated.pqr --titration-state-method propka --with-ph 7.2 ; rm '
                              f'"${{x:0:-4}}"_protonated.pqr ; done')
                    protonation.append(file[:-4] + 'protonated.pdb')
            else:
                print('Please provide a path to the PDBs\' to be protonated directory, to a single file or use '
                      '--select')
        else:
            for file in f_pdb(args.protonate):
                os.system(f'{file} ; do pdb2pqr30 --noopt --nodebump --pdb-output "${{'
                          f'x:0:-4}}"_protonated.pdb $x "${{x:0:-4}}"_protonated.pqr --titration-state-method propka '
                          f'--with-ph 7.2 ; rm "${{x:0:-4}}"_protonated.pqr ; done')
                protonation.append(file[:-4] + 'protonated.pdb')

    if isinstance(args.find, str):
        invalid_molecules = []
        invalid_bond_types = []
        b = 0
        if args.find == '':
            if len(selection) != 0:
                a = len(selection)
                for file in selection:
                    invalid = f_invalid(file)
                    if invalid != 0:
                        invalid_molecules.append(invalid[0:2])
                        for case in invalid[2]:
                            invalid_bond_types.append(case)
                    b += 1
                    print(f'{b}/{a}')
            elif len(protonation) != 0:
                a = len(protonation)
                for file in protonation:
                    invalid = f_invalid(file)
                    if invalid != 0:
                        invalid_molecules.append(invalid[0:2])
                        for case in invalid[2]:
                            invalid_bond_types.append(case)
                    b += 1
                    print(f'{b}/{a}')
            else:
                print('Please provide a path to the PDBs\' to be examined directory, to a single file or use --select.')
        else:
            files = f_ppdb(args.find)
            a = len(files)
            for file in files:
                invalid = f_invalid(file)
                if invalid != 0:
                    invalid_molecules.append(invalid[0:2])
                    for case in invalid[2]:
                        invalid_bond_types.append(case)
                b += 1
                print(f'{b}/{a}')

        if len(invalid_molecules) != 0:
            for molecule in invalid_molecules:
                print(f'In protein {molecule[0]}, we have found these invalid residues: {molecule[1]}.')
            cases = set()
            cases_count = dict()
            for case in invalid_bond_types:
                a = len(cases)
                cases.add(case)
                if len(cases) > a:
                    cases_count[case] = 1
                else:
                    cases_count[case] += 1
            for case, times in cases_count.items():
                print(f'Times of {case} found: {times}.')


if __name__ == '__main__':
    main()
