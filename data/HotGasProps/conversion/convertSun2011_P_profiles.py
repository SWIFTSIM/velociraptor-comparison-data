from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

input_filename = "../raw/Sun2011_P_profiles.txt"

output_directory = "../"
output_filename = "Sun11_P_profiles.hdf5"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

data = np.loadtxt(input_filename)
x = unyt.unyt_array(10.0 ** data[:, 0], unyt.dimensionless)
y = unyt.unyt_array(10.0 ** data[:, 1], unyt.dimensionless)
yerr = np.zeros((2, data.shape[0]))
yerr[0, :] = 10.0 ** (data[:, 1] - data[:, 2])
yerr[1, :] = 10.0 ** (data[:, 3] - data[:, 1])
yerr = unyt.unyt_array(yerr, unyt.dimensionless)

# Meta-data
comment = "No comment"
citation = "Sun et al. (2011)"
bibcode = "2011ApJ...727L..49S"
name = "Pressure profiles for 43 nearby galaxy groups"
plot_as = "points"
redshift = 0.0

# Write everything
processed = ObservationalData()
processed.associate_x(
    x, scatter=None, comoving=False, description="$r/r_{500,\mathrm{hse}}$"
)
processed.associate_y(
    y, scatter=yerr, comoving=False, description="$P/P_{500,\mathrm{hse}}$"
)
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
