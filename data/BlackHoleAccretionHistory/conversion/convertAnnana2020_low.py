from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys
from unyt import speed_of_light

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

# Cosmology
h_obs = 0.7
h_sim = cosmology.h

input_filename = "../raw/Annana_2020.txt"

output_filename = "Annana2020_low.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# Read the data
raw = np.loadtxt(input_filename)
z = unyt.unyt_array(raw[:, 0], "dimensionless")

# Convert to scale factor
a = 1 / (1 + z)

BLD = 10**unyt.unyt_array(raw[:, 1], "dimensionless") * unyt.erg / (unyt.s * unyt.Mpc**3)

# Correct for cosmology
BLD = BLD * (h_sim / h_obs) ** -2

# Convert to BHARD
radiative_efficiency = 0.34
speed_of_light = speed_of_light.to(unyt.cm / unyt.s)
BHARD = BLD / (radiative_efficiency * speed_of_light**2)

# Convert units to Msun * yr^-1 * Mpc^-3
BHARD = BHARD.to(unyt.Msun / unyt.yr / unyt.Mpc**3)

# Meta-data
comment = (
    "Mixed-wavelength observations"
    f"h-corrected using cosmology: {cosmology.name}. "
)
citation = r"Ananna et al. (2020) (X-ray, eps_rad = 0.34)"
bibcode = "2020ApJ...903...85A"
name = "Redshift - Black-hole Mass Accretion Rate Density relation"
plot_as = "line"
redshift = np.mean(z)
h = h_sim

# Write everything
processed = ObservationalData()
processed.associate_x(a, scatter=None, comoving=True, description="Scale-factor")
processed.associate_y(
    BHARD, scatter=None, comoving=True, description="Black-hole Accretion Rate Density"
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
