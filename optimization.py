import os
import ase
import time
from ase.optimize import BFGS
from tblite.ase import TBLite
from ase.io.trajectory import Trajectory
from utils import traj_to_extxyz

def xtb_optim(method: str = None, 
              structure: ase.Atoms = None, 
              file_extension: str = None, 
              output_name: str = None,
              output_dir: str = '') -> (float, float, int):
    
    os.makedirs(f'results/{output_dir}{output_name}_{method}_optim', exist_ok=True)
    
    structure.write(f'results/{output_dir}{output_name}_{method}_optim/{output_name}_init{file_extension}')

    if method == 'gfn1':
        calc = TBLite(method="GFN1-xTB", max_iterations=1000, verbosity=0)
    elif method == 'gfn2':
        calc = TBLite(method="GFN2-xTB", max_iterations=1000, verbosity=0) 

    structure.calc = calc

    opt = BFGS(structure, trajectory=f'results/{output_dir}{output_name}_{method}_optim/{output_name}.traj', maxstep=0.05)

    t_start = time.time()
    opt.run(fmax=0.015, steps=2500)
    t_end = time.time()
    opt_time = t_end - t_start

    structure.write(f'results/{output_dir}{output_name}_{method}_optim/{output_name}_final{file_extension}')
    traj_to_extxyz(f'results/{output_dir}{output_name}_{method}_optim/{output_name}')
    n_steps = len(Trajectory(f'results/{output_dir}{output_name}_{method}_optim/{output_name}.traj'))
    energy = structure.get_total_energy() * 23.060
    return energy, opt_time, n_steps