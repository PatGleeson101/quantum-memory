# 1D quantum Gradient Echo Memory equations with XMDS2

## Usage
1. `root/bin: xmds2 ../src/my-sim.xmds`. This compiles the XMDS file to the `bin/` directory.
2. `root: ./run.sh ./instances/my-instance.toml`. The TOML file should specify the name of the compiled binary (e.g. `my-sim`), and any arguments to be passed. If an argument is specified as a list, a separate simulation will be run for each value. For example:
```
simulate="jesse-double-gaussian"

[arguments]
pulsewidth=[0.5, 1.0, 1.2, 1.4]
bandwidth=4
tswitch=8

# Unspecified arguments will be left as default.
```

Output will appear in a sibling folder to `my-instance.toml`.

## TODO:
- allow run.py to autocompile xmds files to the `bin` directory if `-c` flag given. This makes it easier to get binaries in the right place (so they can be gitignored).
