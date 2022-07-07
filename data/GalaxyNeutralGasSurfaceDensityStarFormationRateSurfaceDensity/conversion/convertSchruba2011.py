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
name = "Neutral Gas Surface Density vs Star Formation Rate Surface Density"
plot_as = "points"

raw = np.loadtxt(input_filename, usecols=(3, 4, 5, 6, 7, 8))

sigmaSFR = raw[:, 0]
sigmaSFR_err = raw[:, 1]
sigmaSFR_low = 10.0 ** (np.log10(sigmaSFR) - sigmaSFR_err)
sigmaSFR_high = 10.0 ** (np.log10(sigmaSFR) + sigmaSFR_err)
sigmaHI = raw[:, 2]
sigmaHI_err = raw[:, 3]
sigmaHI_low = 10.0 ** (np.log10(sigmaHI) - sigmaHI_err)
sigmaHI_high = 10.0 ** (np.log10(sigmaHI) + sigmaHI_err)
sigmaH2 = raw[:, 4]
sigmaH2_err = raw[:, 5]
sigmaH2_low = 10.0 ** (np.log10(sigmaH2) - sigmaH2_err)
sigmaH2_high = 10.0 ** (np.log10(sigmaH2) + sigmaH2_err)

sigmaSFR_err = unyt.unyt_array(
    [sigmaSFR - sigmaSFR_low, sigmaSFR_high - sigmaSFR], units="Msun/yr/kpc**2"
)
sigmaSFR = unyt.unyt_array(sigmaSFR, units="Msun/yr/kpc**2")
sigmaHI_err = unyt.unyt_array(
    [sigmaHI - sigmaHI_low, sigmaHI_high - sigmaHI], units="Msun/pc**2"
)
sigmaHI = unyt.unyt_array(sigmaHI, units="Msun/pc**2")
sigmaH2_err = unyt.unyt_array(
    [sigmaH2 - sigmaH2_low, sigmaH2_high - sigmaH2], units="Msun/pc**2"
)
sigmaH2 = unyt.unyt_array(sigmaH2, units="Msun/pc**2")

sigmaHIpH2 = sigmaHI + sigmaH2
sigmaHIpH2_err = np.sqrt(sigmaHI_err ** 2 + sigmaH2_err ** 2)

processed.associate_x(
    sigmaHIpH2,
    scatter=sigmaHIpH2_err,
    comoving=False,
    description="Neutral Gas (HI+H2) Surface Density",
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
