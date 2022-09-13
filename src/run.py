# Run a compiled xmds2 program with specified arguments
import toml
import glob
import os
from os.path import dirname, abspath, splitext
import subprocess
import sys
import itertools

# Directory containing this script and compiled simulation binaries
source_dir = dirname(abspath(__file__))
# Path to config toml file for simulation to be run
config_file = abspath(sys.argv[1])
# Output directory is a sibling of the config file, with the same name.
# This convention also avoids two configs overwriting each other's output.
output_dir = splitext(config_file)[0]
os.makedirs(output_dir, exist_ok=True)
#basename('/some/path/to/file.txt') -> 'file.txt' #handy to know

# Read the toml file
with open(config_file, 'r') as f:
  config = toml.loads(f.read())
  # config object has format
  """
  { 
    "keyname": 47,
    "sectionname": {"key1": 56.7, "key2": "stringvalue"},
  }
  """

# Identify which simulation to run, and any arguments
bin_dir = os.path.join(source_dir, "../bin/")
exec_path = os.path.join(bin_dir, config["simulate"])
if "arguments" in config:
  args = config["arguments"]
else:
  args = {}

# Arguments may be specified as a list, indicating to run the simulation once
# for each value. If multiple arguments are lists, every combination is run.
# TODO: Might make more sense for multiple lists to be paired, not producted.
dynamic_argnames = []
dynamic_argvalues = []

shell_staticargs = []
for (arg, value) in args.items():
  if type(value) == list:
    dynamic_argnames.append(arg)
    dynamic_argvalues.append([str(x) for x in value])
  else:
    shell_staticargs.extend([f"--{arg}", str(value)])

print(f"Static arguments: {shell_staticargs}")
# If running a single simulation, leave the output filename alone.
if len(dynamic_argnames) == 0:
  subprocess.run([exec_path, *shell_staticargs], cwd = output_dir)
else:
  argprefixes = [f"--{arg}" for arg in dynamic_argnames]

  for combo in itertools.product(*dynamic_argvalues):
    shell_dynamicargs = [val for pair in zip(argprefixes, combo) for val in pair]
    print(f"Dynamic args: {shell_dynamicargs}")
    subprocess.run([exec_path, *shell_staticargs, *shell_dynamicargs], cwd = output_dir)
    #If running multiple simulations, use the distinguishing variable(s) as the filenames. Do this be renaming the most recently-created files.
    all_h5 = glob.glob(os.path.join(output_dir, '*.h5'))
    all_xsil = glob.glob(os.path.join(output_dir, '*.xsil'))
    new_h5 = max(all_h5, key=os.path.getctime)
    new_xsil = max(all_xsil, key=os.path.getctime)
    name = os.path.join(output_dir, ".".join([f"{arg}={val}" for (arg, val) in zip(dynamic_argnames, combo)]))
    os.rename(new_h5, f"{name}.h5")
    os.rename(new_xsil, f"{name}.xsil")
