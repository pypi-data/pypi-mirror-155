from pathlib import Path, PurePath
import os
import platform
import subprocess


def get_surface_dict(pdb_filename, n_atoms, use_precomputed=False):
    """ Returns a dict of dicts based on atom numbers (input file must have
        unique atom numbers), containing surface area in contact between
        pairs of atoms.
    """
    if not os.path.isfile(pdb_filename):
        raise ValueError("This file does not exist: {}".format(pdb_filename))
    vcon_file = pdb_filename + ".vcon"
    if not (use_precomputed and os.path.isfile(vcon_file)):
        vcon_file = run_vcon(pdb_filename, n_atoms)
    sd = dict()
    with open(vcon_file) as f:
        lines = f.readlines()
    for line in lines:
        ll = line.split()
        from_atom = int(ll[0])
        to_atom = int(ll[1])
        if from_atom != to_atom:
            surf = float(ll[-1])
            if from_atom not in sd:
                sd[from_atom] = dict()
            sd[from_atom][to_atom] = surf
    if not use_precomputed:
        os.remove(vcon_file)
    return sd


def run_vcon(pdb_filename, n_atoms, tried_compiling_once=False):
    """ Runs Vcontacts using compiled executable. Produces a .pdb.vcon file.
    """
    execpath = Path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vcontacts'))
    execnames = [x for x in execpath.glob("vcon")]

    out_filename = pdb_filename + ".vcon"

    if len(execnames) == 0:
        if not tried_compiling_once:
            try_to_compile_vcon(execpath)
            return run_vcon(pdb_filename, n_atoms, tried_compiling_once=True)
        else:
            raise ValueError("There was a problem with the automatic compilation of Vcontacts. See the " +
                             "Troubleshooting section of the NRGTEN online documentation (nrgten.readthedocs.io)")
    elif len(execnames) > 1:
        raise ValueError("Somehow, there are more than one Vcontacts executables. This should never happen...")

    vcon_exec = execnames[0]
    subprocess.run([str(vcon_exec), pdb_filename, out_filename], check=True)
    return out_filename


def try_to_compile_vcon(execpath):
    """ Workaround for compiling the Vcontacts executable. The reason for using this instead of Extension directly in the setup.py script is that Extension works on
        Unix-like systems but is looking for some type of Cython/Python.h bindings when compiled on Windows (to enable
        importing the extension as a Python module), whereas the Vcontacts original code is just pure C that is kind of
        tangled and full of global variables. This is safer to ensure proper execution and the only drawback arises
        if the package is installed system-wide and the user does not have the permission to compile upon the first
        execution.
    """
    libpath = PurePath(execpath)
    op_system = platform.system()
    args = []
    if op_system == "Windows":
        args = ['cl.exe', str(libpath.joinpath('Vcontacts.c')), '-o', str(libpath.joinpath('vcon'))]
    elif op_system == "Darwin" or op_system == "Linux":
        args = ['gcc', str(libpath.joinpath('Vcontacts.c')), '-o', str(libpath.joinpath('vcon')), '-lm']
    else:
        raise ValueError("Unrecognized operating system: {0}".format(op_system))
    subprocess.run(args)



if __name__ == "__main__":
    print(get_surface_dict("vcontacts/mir125aWT_1_d-0017.pdb", 10))


