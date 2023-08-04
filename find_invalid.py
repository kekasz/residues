from rdkit import Chem
from real_atom_types import real_ats_types
from os.path import basename


def f_invalid(path):
    # Function for selection of invalid atoms
    invalid_residues = set()
    invalid_atom_types = []
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
    if len(invalid_residues) == 0:
        return 0
    else:
        print(invalid_residues)
        return basename(path)[3:-27], invalid_residues, invalid_atom_types
