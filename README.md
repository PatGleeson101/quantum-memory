# 1D Optical Gradient Echo Memory exploration with XMDS2
This repo includes [XMDS2](http://www.xmds.org) source code and simulation instances for numerical exploration of optical Gradient Echo Memory (GEM) in a room-temperature gas cloud. These make use of a custom helper tool for managing multiple XMDS2 simulations and different combinations of parameters.

Different schemes and phenomena are visualised in the included Jupyter notebook (python).

XMDS2 source files are based on the original `1DGEM2L.xmds` file. You can see the group's repository here: [https://github.com/lemni1/Quantum-Memory-Simulations].

## License
[MIT](LICENCE)

## Usage
> See [Convenient Flags](#Convenient-flags) for how to autocompile and/or run all simulations at once.

For a single instance:
1. `root-dir/bin: xmds2 ../src/my-sim.xmds`. This compiles the XMDS file to the `bin/` directory.
2. `root-dir: ./run.sh path/to/my-instance.toml`. You may need to first make `run.sh` executable using `chmod`. 

An instance `.toml` file specifies the name of the compiled binary to be run (e.g. `my-sim-name`), and any arguments to be passed. Output(s) will appear in a sibling folder to `my-instance.toml`, named `my-instance`. Existing instance files have been placed in `./instances`.

If no arguments are specified as lists, this will contain the output (`.h5` and `.xsil` file pair) of a single simulation, with filename specified in the `.xmds` source. Otherwise, a separate simulation will be run for every combination of list-specified arguments, and the output files of each will be renamed to indicate this combination. Unspecified arguments will be set to their default, and neither unspecified nor single-valued arguments will be included in the
output file name (which is convenient when a simulation takes many
parameters).

### Example TOML:
```
simulate="double-gaussian"

[arguments]
pulsewidth=[0.5, 1.5]
pulsesep=[2,4]
bandwidth=4
tswitch=8
tin=4
```
This runs four simulations, one for each combination of `pulsewidth` and `pulsesep`.

### Convenient flags
To automatically (re)compile the appropriate `.xmds` file to the `bin` directory before simulating, add the `-c` flag:
```
root-dir: ./run.sh ./instances/my-instance.toml -c
```
For autocompiling to work, the name of the source file and executable binary must match, except for the `.xmds` extension.

To run all `.toml` files in a directory, specify the directory name and then the `-a` flag:
```
root-dir: ./run.sh ./instances/ -a
```

Using `-c` with `-a` will run all instances, (re)compiling all necessary simulations.

## Installing XMDS2 on a Mac
The XMDS Homebrew formula (described [here](http://www.xmds.org/installation.html#mac-os-x-installation)) **does not work** on my machine as of 2022. Instead, I successfully followed the [manual install instructions](http://www.xmds.org/installation.html#manual-installation-from-source). Below is a brief overview, which may need to be adjusted for different machines and is described more thoroughly in the instructions.

Ensure you have Python 3 and a C++ compiler. The compiler `clang` can be obtained (amongst other things) by installing the XCode developer tools:
```
xcode-select --install
```
Download the [XMDS2 source](https://sourceforge.net/projects/xmds/) and move the unzipped directory to `~/.xmds-3.1.0`. In the next step, Homebrew is convenient for installing required libraries:
```
brew install hdf5 fftw open-mpi
pip3 install h5py lxml numpy (optional)
brew install gsl (optional)
cd ~/.xmds-3.1.0
sudo ./setup.py develop
```
You will likely need to add `~/.xmds-3.1.0/bin/` to your `PATH` and give the contained files execute permission using `chmod`. I am then able to run `xmds2 --help` in terminal.

## Notes
The two advantages of storing the XMDS-generated C and binary files in a separate `bin/` directory are:
1. Allow them to be `.gitignore`d.
2. Avoid cluttering the `src/` directory.

### To-do
- add a `-r` flag to remove old files from the output directory.
