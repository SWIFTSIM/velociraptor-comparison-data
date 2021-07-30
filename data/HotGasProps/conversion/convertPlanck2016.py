from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

input_filename = "../raw/Planck_tSZ.csv"

output_directory = "../"
output_filename = "Planck16_data.hdf5"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

data = np.loadtxt(input_filename, skiprows=1, delimiter=",")
x = unyt.unyt_array(10.0 ** data[:, 0], unyt.Msun)
y = unyt.unyt_array(data[:, 1], unyt.Mpc ** 2)
yerr = unyt.unyt_array(data[:, 2:].T, unyt.Mpc ** 2)

# Meta-data
comment = "No comment"
citation = "Planck Collaboration XXIV (2016)"
bibcode = "2016A&A...594A..27P"
name = "Local Sunyaev-Zeldovich sources"
plot_as = "points"
redshift = 0.0

# Write everything
processed = ObservationalData()
processed.associate_x(
    x, scatter=None, comoving=False, description="$M_{500,\mathrm{hse}}$"
)
processed.associate_y(
    y,
    scatter=yerr,
    comoving=True,
    description="$\mathrm{log}_{10} (\mathrm{E}(z)^{-2/3} Y_\mathrm{SZ, hse}(<5r_{500}) D_A^2$",
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
