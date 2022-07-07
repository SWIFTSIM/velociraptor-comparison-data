from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

input_filename = "../raw/Schruba2011.txt"

processed = ObservationalData()

comment = "Based on the IRAM HERCULES survey."
citation = "Schruba et al. (2011)"
bibcode = "2011AJ....142...37S"
name = "H2 Gas Surface Density vs Star Formation Rate Surface Density"
plot_as = "points"

raw = np.loadtxt(input_filename, usecols=(3, 4, 7, 8))

sigmaSFR = raw[:, 0]
sigmaSFR_err = raw[:, 1]
sigmaSFR_low = 10.0 ** (np.log10(sigmaSFR) - sigmaSFR_err)
sigmaSFR_high = 10.0 ** (np.log10(sigmaSFR) + sigmaSFR_err)
sigmaH2 = raw[:, 2]
sigmaH2_err = raw[:, 3]
sigmaH2_low = 10.0 ** (np.log10(sigmaH2) - sigmaH2_err)
sigmaH2_high = 10.0 ** (np.log10(sigmaH2) + sigmaH2_err)

sigmaSFR_err = unyt.unyt_array(
    [sigmaSFR - sigmaSFR_low, sigmaSFR_high - sigmaSFR], units="Msun/yr/kpc**2"
)
sigmaSFR = unyt.unyt_array(sigmaSFR, units="Msun/yr/kpc**2")
sigmaH2_err = unyt.unyt_array(
    [sigmaH2 - sigmaH2_low, sigmaH2_high - sigmaH2], units="Msun/pc**2"
)
sigmaH2 = unyt.unyt_array(sigmaH2, units="Msun/pc**2")

processed.associate_x(
    sigmaH2, scatter=sigmaH2_err, comoving=False, description="H2 Surface Density"
)
processed.associate_y(
    sigmaSFR,
    scatter=sigmaSFR_err,
    comoving=False,
    description="Star Formation Rate Surface Density",
)
processed.associate_citation(citation, bibcode)
processed.associate_name(name)
processed.associate_comment(comment)
processed.associate_redshift(0.0, 0.0, 0.0)
processed.associate_plot_as(plot_as)
processed.associate_cosmology(cosmology)

output_path = f"../Schruba2011.hdf5"

if os.path.exists(output_path):
    os.remove(output_path)

processed.write(filename=output_path)
