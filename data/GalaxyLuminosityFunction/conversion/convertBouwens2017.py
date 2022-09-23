from velociraptor.observations.objects import ObservationalData

import unyt
import os
import sys
import csv
import numpy as np

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

# Cosmology
h_sim = cosmology.h

output_filename = "Bouwens_2017.hdf5"
output_directory = "../"

# Both in log
Muv = unyt.unyt_array(
    [
        -20.75,
        -20.25,
        -19.75,
        -19.25,
        -18.75,
        -18.25,
        -17.75,
        -17.25,
        -16.75,
        -16.25,
        -15.75,
        -15.25,
        -14.75,
        -14.25,
        -13.75,
        -13.25,
        -12.75,
    ],
    "dimensionless",
)

phi = unyt.unyt_array(
    [
        0.0002,
        0.0009,
        0.0007,
        0.0018,
        0.0036,
        0.0060,
        0.0071,
        0.0111,
        0.0170,
        0.0142,
        0.0415,
        0.0599,
        0.0817,
        0.1052,
        0.1275,
        0.1464,
        0.1584,
    ],
    "Mpc**-3",
).to("Mpc**-3")
phi_err = unyt.unyt_array(
    [
        [0.0002, 0.0002],
        [0.0004, 0.0004],
        [0.0004, 0.0004],
        [0.0006, 0.0006],
        [0.0009, 0.0009],
        [0.0012, 0.0012],
        [0.0014, 0.0066],
        [0.0022, 0.0102],
        [0.0039, 0.0165],
        [0.0054, 0.0171],
        [0.0069, 0.0354],
        [0.0106, 0.0757],
        [0.0210, 0.1902],
        [0.0434, 0.5414],
        [0.0747, 1.6479],
        [0.1077, 5.4369],
        [0.1343, 19.8047],
    ],
    "Mpc**-3",
).to("Mpc**-3").T


if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# Meta-data
comment = (
    "UV luminosity function from Hubble Frontier Fields, at z=6. "
    "Data obtained assuming h=0.7, from Table 5."
)
citation = "Bouwens et al. (2017)"
bibcode = "2017ApJ...843..129B"
name = "UV Luminosity Function (1500A)"
plot_as = "points"
redshift = 6
h = h_sim

# Write everything
processed = ObservationalData()
processed.associate_x(
    Muv, scatter=None, comoving=True, description="Galaxy UV Luminosity"
)
processed.associate_y(
    phi, scatter=phi_err, comoving=True, description="Number per mag per cMpc^3"
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
