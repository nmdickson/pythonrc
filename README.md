Use this package by setting something like
```bash
export PYTHONSTARTUP="{...}/pythonrc/src.py"
```
in your `.bashrc` login file.

This package simply imports various commonly used (by me) packages and sets up a few helpful functions and variables, upon starting up python (e.g. starting a python shell through `python`).

You should actually install the package (e.g. `pipx install {...}/pythonrc`), but it will try to make it work if you only set `PYTHONSTARTUP` too.

If any required 3rd-party libraries (e.g. numpy, matplotlib) fail to import, this will error and not all goodies will be loaded.
