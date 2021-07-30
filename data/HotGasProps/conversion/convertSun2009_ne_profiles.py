from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

input_filename = "../raw/Sun2009_ne_profiles.txt"

output_directory = "../"
output_filename = "Sun09_ne_profiles.hdf5"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

data = np.loadtxt(input_filename)
# we discard the last two rows, since they are outside r500
x = unyt.unyt_array(10.0 ** data[:-2, 0], unyt.dimensionless)
y = unyt.unyt_array(10.0 ** data[:-2, 1], unyt.cm ** (-3))
yerr = unyt.unyt_array(10.0 ** data[:-2, 2:].T, unyt.cm ** (-3))

# Meta-data
comment = "No comment"
citation = "Sun et al. (2009)"
bibcode = "2009ApJ...693.1142S"
name = "Electron density profiles for 43 nearby galaxy groups"
plot_as = "points"
redshift = 0.0

# Write everything
processed = ObservationalData()
processed.associate_x(
    x, scatter=None, comoving=False, description="$r/r_{500,\mathrm{hse}}$"
)
processed.associate_y(y, scatter=yerr, comoving=False, description="$n_e$")
processed.associate_citation(citation, bibcode)
processed.associate_name(name)
processed.associate_comment(comment)
processed.associate_redshift(redshift)
processed.associate_plot_as(plot_as)
processed.associate_cosmology(cosmology)

output_path = f"{output_directory}/{output_filename}"

if os.path.exists(output_path):
    os.remove(output_path)

processed.write(filename=output_path)
