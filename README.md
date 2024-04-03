# xTB MD
Molecular Dynamics with xTB 

# Running simulations:
## Parameters:  
- --method (choose between gfn1 and gfn2 xTB)
- --task (md or opt) for Molecular Dynamics or Optimization
- --structure data/example_molecule.xyz (name of the structure in data/ folder)
- --N_steps 1000 (Number of steps)
- --pbc (use this argument if structure is periodic)
- --cell 10 10 10 (unit cell size)
- --T 800 (temperature in K)
## Outputs:
- Saved in `results/` folder 
- initial structure
- final structure
- log file
- trajectories in .traj and .extxyz formats

## Example:
- Optimization: `python main.py --task opt --structure data/example_molecule.xyz`
- Molecular Dynamics: `python main.py --task md --structure data/example_molecule.xyz --pbc --cell 10 10 10 --N_steps 1000`

