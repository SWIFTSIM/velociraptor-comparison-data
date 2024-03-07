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

output_filename = "Rosdahl_2022.hdf5"
output_directory = "../"

m1500 = unyt.unyt_array(
    [
        -10.54522294293518,
        -11.520940547416828,
        -12.521216058558023,
        -13.509841870210444,
        -14.486664920628982,
        -15.511328269824048,
        -16.476603661917217,
        -17.46568865880496,
        -18.46664444436886,
        -19.47987918326253,
        -20.468675063520624,
        -21.481348576015566,
        -22.47082473069636,
    ],
    "dimensionless",
)

phi = unyt.unyt_array(
    [
        0.6138955952987115,
        0.885073650339456,
        0.7151673317890972,
        0.47438937430197553,
        0.29079706052311677,
        0.1502120187088852,
        0.06985105008941557,
        0.032479847770387114,
        0.015504938059272316,
        0.005541122703335031,
        0.003222418933625186,
        0.0017777954989803807,
        0.0006107926883337623,
    ],
    "Mpc**-3",
)

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# Meta-data
comment = (
    "UV luminosity function (1500A) for SPHINX20, extracted from the paper "
    "at redshift z=5. Intrinsic, with no dust/etc. absorption included. "
    "Data obtained assuming a Kroupa IMF and h=0.6774. "
)
citation = "Rosdahl et al. (2022)"
bibcode = "2022MNRAS.515.2386R"
name = "UV Luminosity Function (1500A)"
plot_as = "line"
redshift = 5
h = h_sim

# Write everything
processed = ObservationalData()
processed.associate_x(
    m1500, scatter=None, comoving=True, description="Galaxy UV Luminosity (1500A)"
)
processed.associate_y(
    phi, scatter=None, comoving=True, description="Number per mag per cMpc^3"
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
