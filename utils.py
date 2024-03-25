import os.path
import argparse
import ase.io
from pathlib import Path
import subprocess

def validate_input(args: argparse.Namespace) -> bool:
    if not os.path.isfile(args.structure):
        print('Error: Provided structure file does not exist')
        return False
    
    if not (args.structure.endswith('.xyz') or args.structure.endswith('.cif')):
        print('Error: Please, provide structure file in xyz or cif format')
        return False
    
    if args.pbc and args.cell is None:
        print('Error: Please, provide cell parameters using --cell a b c')
        return False
    
    if args.cell is not None and len(args.cell) != 3:
        print('Error: Please, provide 3 cell parameters')
        return False

    return True


def get_structure(structure_file: str = None, 
                  pbc: bool = False, 
                  cell: list = None) -> (ase.Atoms, str):

    structure = ase.io.read(structure_file)
    structure.set_pbc(pbc)
    if pbc: 
        structure.cell = cell

    output_name = Path(structure_file).stem
    _, file_extension = os.path.splitext(structure_file)
    
    return structure, file_extension, output_name


def traj_to_extxyz(traj_file: str = None) -> None:
    command = f'ase convert {traj_file}.traj {traj_file}.extxyz'
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
