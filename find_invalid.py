from rdkit import Chem
from real_atom_types import real_ats_types
from os.path import basename


def f_invalid(path):
    # Returns name of the molecule, invalid residues and types of invalid atoms.
    invalid_residues = set()
    invalid_atom_types = []
    residues_with_type = dict()
    molecule = Chem.MolFromPDBFile(path,
                                   removeHs=False,
                                   sanitize=False
                                   )
    atoms_bonded = {
        atom.GetIdx(): [str(atom.GetSymbol()) + '/', atom.GetPDBResidueInfo().GetResidueNumber()] for atom in
        molecule.GetAtoms()
    }
    for bond in molecule.GetBonds():
        atom1 = bond.GetBeginAtom()
        atom2 = bond.GetEndAtom()
        atoms_bonded[atom1.GetIdx()][0] += atom2.GetSymbol()
        atoms_bonded[atom2.GetIdx()][0] += atom1.GetSymbol()
    for atom, atom_bonded in atoms_bonded.items():
        atom_bonded[0] = atom_bonded[0][:2] + ''.join(sorted(atom_bonded[0][2:]))
        if not (atom_bonded[0] in real_ats_types):
            invalid_residues.add(atom_bonded[1])
            invalid_atom_types.append(atom_bonded[0])
            if atom_bonded[1] in residues_with_type.keys():
                residues_with_type[atom_bonded[1]].append(atom_bonded[0])
            else:
                residues_with_type[atom_bonded[1]] = [atom_bonded[0]]

    if len(invalid_residues) == 0:
        return 0
    else:
        line = f'In {basename(path)[3:-27]}, we found: '
        a = len(residues_with_type.keys())
        for residue in residues_with_type.keys():
            a -= 1
            line += f'{residue} with '
            b = len(residues_with_type[residue])
            for typ in residues_with_type[residue]:
                b -= 1
                if a > 0 or b > 0:
                    line += f'{typ}, '
                else:
                    line += f'{typ}.'
            if a > 0:
                line += '\n                     '
        return basename(path)[3:-27], invalid_residues, invalid_atom_types, line
