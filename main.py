import argparse
from utils import validate_input, get_structure
from molecular_dynamics import xtb_md
from optimization import xtb_optim

def main(args: argparse.Namespace) -> None:
    if not validate_input(args=args):
        return 
    
    structure, file_extension, output_name = get_structure(args.structure, args.pbc, args.cell)
    n_atoms = len(structure)

    if args.task == 'md':
        run_time = xtb_md(args.method, structure, file_extension, output_name, T=args.T, N_steps=args.N_steps)

        print(
            f"""\t------------------------------------------------
            |              MD run completed!               |
            ------------------------------------------------""")
        print(f'\t* MD Time: {run_time:.2f} s, MD Time: {run_time/60:.2f} min')
        print(f'\t* MD Steps: {args.N_steps}')
        print(f'\t* N Atoms: {n_atoms}')

    elif args.task == 'opt':
        energy, opt_time, n_steps = xtb_optim(args.method, structure, file_extension, output_name)

        print(
        f"""\t------------------------------------------------
        |           Optimization completed!            |
        ------------------------------------------------""")
        print(f'\t* Energy: {energy:.3f} kcal/mol')
        print(f'\t* Optim Time: {opt_time:.2f} s, Optim Time: {opt_time/60:.2f} min')
        print(f'\t* Optim Steps: {n_steps}')
        print(f'\t* N Atoms: {n_atoms}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--method", choices=['gfn1', 'gfn2'], default='gfn1', help="Select xTB method for structure optimization.")
    parser.add_argument("--task", choices=['md', 'opt'], default='md', help="Select task (Molecular Dynamics or Optimization). Default: md")
    parser.add_argument("--structure", default=None, help="Provide a structure for optimization.")
    parser.add_argument("--pbc", action='store_true', help="Select if structure is periodic. Default: False")
    parser.add_argument("--cell", nargs='+', type=float, default=None, help="Provide periodic cell (-cell a b c). Default: None")
    parser.add_argument("--T", type=float, default=300.0, help="Provide temperature in K. Default: 300.0 K")
    parser.add_argument("--N_steps", type=int, default=10000, help="Provide number of MD steps. Default: 10,000")
    args = parser.parse_args()

    main(args)

