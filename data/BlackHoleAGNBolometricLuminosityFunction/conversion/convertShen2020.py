from velociraptor.observations.objects import ObservationalData
from velociraptor.observations.objects import MultiRedshiftObservationalData

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

input_filename = "../raw/Shen2020.txt"

output_filename_base = "Shen2020_"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# Read the data (only those columns we need here)
raw = np.genfromtxt(input_filename, dtype=None, usecols=(0, 1, 2, 3, 4, 5))

wavelength_band = np.array([raw[j][0].decode("utf-8") for j in range(len(raw))])
redshifts = np.array([raw[j][1] for j in range(len(raw))])

L = np.array([10 ** raw[j][2] for j in range(len(raw))]) * unyt.erg / unyt.s
L_low = (
    np.array([10 ** (raw[j][2] - raw[j][3]) for j in range(len(raw))])
    * unyt.erg
    / unyt.s
)
L_high = (
    np.array([10 ** (raw[j][2] + raw[j][3]) for j in range(len(raw))])
    * unyt.erg
    / unyt.s
)

Phi = np.array([10 ** raw[j][4] for j in range(len(raw))]) / unyt.Mpc ** 3
Phi_low = (
    np.array([10 ** (raw[j][4] - raw[j][5]) for j in range(len(raw))]) / unyt.Mpc ** 3
)
Phi_high = (
    np.array([10 ** (raw[j][4] + raw[j][5]) for j in range(len(raw))]) / unyt.Mpc ** 3
)

# Define the scatter as offset from the mean value
x_scatter = unyt.unyt_array((L - L_low, L_high - L))
y_scatter = unyt.unyt_array((Phi - Phi_low, Phi_high - Phi_low))

wavelength_band_types = ["hard_X_ray", "soft_X_ray", "B_band", "UV", "mid_IR"]
citations = [f"Shen+ (2020), {band}" for band in wavelength_band_types]
redshift_list = [round((i + 1) * 0.2, 2) for i in range(30) if i != 27]
redshift_list.append(6.6)
redshift_list.append(7.0)
bibcode = "2020ApJ.892.17D"
name = "AGN Bolometric Luminosity Function"
plot_as = "points"

# Let's write 5 different files for each wavelength type.
for i in range(np.size(wavelength_band_types)):
    comment = (
        " AGN bolometric luminosity data, taken from Shen et al. (2020):"
        " 2020ApJ.892.17D. This file contains data in the "
        + wavelength_band_types[i]
        + " band."
    )
    citation = citations[i]

    multi_z = MultiRedshiftObservationalData()
    multi_z.associate_citation(citation, bibcode)
    multi_z.associate_name(name)
    multi_z.associate_comment(comment)
    multi_z.associate_cosmology(cosmology)
    multi_z.associate_maximum_number_of_returns(1)

    # Loop over all data in terms of redshift
    for z in redshift_list:
        mask = (wavelength_band == wavelength_band_types[i]) & (redshifts == z)

        processed = ObservationalData()

        processed.associate_x(
            L[mask],
            scatter=np.array(
                [
                    x_scatter[0][mask],
                    x_scatter[1][mask],
                ]
            )
            * unyt.erg
            / unyt.s,
            comoving=False,
            description="AGN bolometric luminosity derived from the given band (see name of file) ",
        )
        processed.associate_y(
            Phi[mask],
            scatter=np.array(
                [
                    y_scatter[0][mask],
                    y_scatter[1][mask],
                ]
            )
            / unyt.Mpc ** 3,
            comoving=False,
            description="AGN bolometric luminosity function in the given band (see name of file) ",
        )

        processed.associate_redshift(z, z - 0.1, z + 0.1)
        processed.associate_plot_as(plot_as)

        multi_z.associate_dataset(processed)

    output_path = (
        f"{output_directory}/{output_filename_base}{wavelength_band_types[i]}_Data.hdf5"
    )

    if os.path.exists(output_path):
        os.remove(output_path)

    multi_z.write(filename=output_path)
