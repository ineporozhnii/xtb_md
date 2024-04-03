import os
import ase
import time
from tblite.ase import TBLite
from ase.io.trajectory import Trajectory
from utils import traj_to_extxyz
from ase.md.langevin import Langevin
from ase import units

def xtb_md(method: str = None, 
           structure: ase.Atoms = None, 
           file_extension: str = None, 
           output_name: str = None,
           output_dir: str = '',
           step: float = 1.0,
           T: float = 300.0,
           N_steps: int = 10000) -> (float, float, int):


    os.makedirs(f'results/{output_dir}{output_name}_{method}_{int(T)}K', exist_ok=True)
    
    structure.write(f'results/{output_dir}{output_name}_{method}_{int(T)}K/{output_name}_init{file_extension}')
    
    if method == 'gfn1':
        calc = TBLite(method="GFN1-xTB", max_iterations=1000, verbosity=0)
    elif method == 'gfn2':
        calc = TBLite(method="GFN2-xTB", max_iterations=1000, verbosity=0) 

    structure.calc = calc

    dyn = Langevin(structure, step * units.fs, temperature_K = T * units.kB, friction=0.01, logfile=f'results/{output_dir}{output_name}_{method}_{int(T)}K/{output_name}.log')

    traj = Trajectory(f'results/{output_dir}{output_name}_{method}_{int(T)}K/{output_name}.traj', 'w', structure)
    dyn.attach(traj.write, interval=1)

    t_start = time.time()
    dyn.run(N_steps)
    t_end = time.time()
    run_time = t_end - t_start

    traj_to_extxyz(f'results/{output_dir}{output_name}_{method}_{int(T)}K/{output_name}')

    return run_time
