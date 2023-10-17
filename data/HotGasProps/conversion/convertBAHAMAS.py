from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)


def convert_linear(x):
    return x


def convert_log(x):
    return 10.0 ** x


quantities = {
    "LX": {
        "name": "BAHAMAS X-ray luminosities",
        "xlabel": "$M_{500, \mathrm{hse}}$",
        "xunit": unyt.Msun,
        "xconversion": convert_log,
        "ylabel": "$L_{0.5-2.0 \mathrm{keV, hse}}$",
        "yunit": unyt.ergs / unyt.s,
        "yconversion": convert_log,
    },
    "P": {
        "name": "BAHAMAS hot gas pressure profiles",
        "xlabel": "$r/r_{500, \mathrm{hse}}$",
        "xunit": unyt.dimensionless,
        "xconversion": convert_linear,
        "ylabel": "$P / P_{500, \mathrm{hse}} \,\, (r/r_{500, \mathrm{hse}})^2$",
        "yunit": unyt.dimensionless,
        "yconversion": convert_linear,
    },
    "rho": {
        "name": "BAHAMAS hot gas density profiles",
        "xlabel": "$r/r_{500, \mathrm{hse}}$",
        "xunit": unyt.dimensionless,
        "xconversion": convert_linear,
        "ylabel": "$\\rho/\\rho_\mathrm{crit} \,\, (r/r_{500, \mathrm{hse}})^2$",
        "yunit": unyt.dimensionless,
        "yconversion": convert_linear,
    },
    "S_S500": {
        "name": "BAHAMAS hot gas entropy profiles",
        "xlabel": "$r/r_{500, \mathrm{hse}}$",
        "xunit": unyt.dimensionless,
        "xconversion": convert_linear,
        "ylabel": "'$S / S_{500, \mathrm{hse}}$",
        "yunit": unyt.dimensionless,
        "yconversion": convert_linear,
    },
    "Ysz": {
        "name": "BAHAMAS SZ flux-halo mass relation",
        "xlabel": "$M_{500, \mathrm{hse}}$",
        "xunit": unyt.Msun,
        "xconversion": convert_log,
        "ylabel": "$\mathrm{E}(z)^{-2/3} Y_\mathrm{SZ, hse}(<5r_{500}) D_A^2$",
        "yunit": unyt.Mpc ** 2,
        "yconversion": convert_log,
    },
}
for quantity in quantities:
    input_filename = "../raw/new_BAHAMAS_{0}.csv".format(quantity)
    output_filename = "BAHAMAS_{0}.hdf5".format(quantity)

    data = np.loadtxt(input_filename, skiprows=1, delimiter=",")
    x = unyt.unyt_array(
        quantities[quantity]["xconversion"](data[:, 0]),
        quantities[quantity]["xunit"],
    )
    y = unyt.unyt_array(
        quantities[quantity]["yconversion"](data[:, 1]),
        quantities[quantity]["yunit"],
    )
    yerr = np.zeros((2, data.shape[0]))
    yerr[0, :] = quantities[quantity]["yconversion"](data[:, 1] - data[:, 2])
    yerr[1, :] = quantities[quantity]["yconversion"](data[:, 3] - data[:, 1])
    yerr = unyt.unyt_array(yerr, quantities[quantity]["yunit"])

    # Meta-data
    comment = "No comment"
    citation = "McCarthy et al. (2017)"
    bibcode = "2017MNRAS.465.2936M"
    name = quantities[quantity]["name"]
    plot_as = "line"
    redshift = 0.0

    # Write everything
    processed = ObservationalData()
    processed.associate_x(
        x,
        scatter=None,
        comoving=False,
        description=quantities[quantity]["xlabel"],
    )
    processed.associate_y(
        y,
        scatter=yerr,
        comoving=False,
        description=quantities[quantity]["ylabel"],
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
