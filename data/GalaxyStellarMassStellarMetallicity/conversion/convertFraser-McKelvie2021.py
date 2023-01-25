from velociraptor.observations.objects import ObservationalData

import unyt
import os
import sys
import csv

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

# Cosmology
h_sim = cosmology.h

input_filename = "../raw/Fraser-McKelvie_2021.csv"
output_filename = "Fraser-McKelvie_2021.hdf5"
output_directory = "../"

Mstar_arr, Zstar_arr = [], []
Zstar_min = -10

# Used in colibre
Zsun_Asplund09 = 0.0134
Xsun_Asplund09 = 0.7381
Z_over_X_Asplund09 = Zsun_Asplund09 / Xsun_Asplund09

# Used in Fraser-McKelvie's work
Zsun_Vazdekis15 = 0.0198
Xsun_Vazdekis15 = 0.7068
Z_over_X_Vazdekis15 = Zsun_Vazdekis15 / Xsun_Vazdekis15

with open(input_filename, "r") as file:
    data = csv.reader(file, delimiter=",")
    for c, row in enumerate(data):
        if c > 0:

            # The raw stellar mass is given in log10
            Mstar = (10.0 ** float(row[4]),)

            # The raw Zstar is mass-weighted log10( (Z/H) / (Z/H)_Sun )
            Zstar = 10.0 ** float(row[-2]) * Z_over_X_Vazdekis15 / Z_over_X_Asplund09

            # Some galaxies in the sample do not have Zstar (set to A very negative value)
            # We thus do not include them
            if Zstar > Zstar_min:
                Mstar_arr.append(Mstar)
                Zstar_arr.append(Zstar)

Mstar_arr = unyt.unyt_array(Mstar_arr, units="Msun")
Zstar_arr = unyt.unyt_array(Zstar_arr, units="dimensionless")

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# Meta-data
comment = (
    "Stellar metallicity versus stellar mass for 472 star-forming galaxies "
    "extracted from the SAMI Galaxy Survey. "
    "Data obtained assuming a Chabrier IMF and h=0.704. "
    "Full spectral fitting was employed to determine mass- (and light-) weighted "
    "average ages and metallicities of the SAMI galaxies from "
    "the 1Re aperture spectra. "
)
citation = "Fraser-McKelvie et al. (2022, SAMI)"
bibcode = "2022MNRAS.510..320F"
name = "Stellar mass - stellar metallicity relation "
plot_as = "points"
redshift = 0.1
h = h_sim

# Write everything
processed = ObservationalData()
processed.associate_x(
    Mstar_arr, scatter=None, comoving=True, description="Galaxy Stellar Mass"
)
processed.associate_y(
    Zstar_arr, scatter=None, comoving=True, description="Stellar metallicity"
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
