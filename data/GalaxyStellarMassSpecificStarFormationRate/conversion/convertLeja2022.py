from velociraptor.observations.objects import (
    ObservationalData,
    MultiRedshiftObservationalData,
)

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

comment = (
    "Based on a Prospector SED fit to the COSMOS-2015 and 3D-HST UV-IR catalogues. "
    "The data corresponds to the median and 16/84 percentile for all galaxies in the sample, "
    "including both star-forming and quiescent galaxies."
)
citation = f"Leja et al. (2022)"
bibcode = "2021arXiv211004314L"
name = f"Galaxy Stellar Mass - Galaxy sSFR"
plot_as = "line"

multi_z = MultiRedshiftObservationalData()
multi_z.associate_citation(citation, bibcode)
multi_z.associate_name(name)
multi_z.associate_comment(comment)
multi_z.associate_cosmology(cosmology)
multi_z.associate_maximum_number_of_returns(1)

for z, zname in [
    (0.3, "0p3"),
    (0.6, "0p6"),
    (1.0, "1p0"),
    (1.5, "1p5"),
    (2.0, "2p0"),
    (2.7, "2p7"),
]:
    input_filename = f"../raw/Leja2022_z{zname}.txt"

    processed = ObservationalData()
    raw = np.loadtxt(input_filename, usecols=(0, 3, 4, 5), delimiter=",")

    Mstar = 10.0 ** raw[:, 0]
    SFR = 10.0 ** raw[:, 1]
    SFR_low = 10.0 ** raw[:, 3]
    SFR_high = 10.0 ** raw[:, 2]
    sSFR = SFR / Mstar
    sSFR_low = SFR_low / Mstar
    sSFR_high = SFR_high / Mstar
    Mstar = unyt.unyt_array(Mstar, units=unyt.Msun)
    sSFR_scatter = unyt.unyt_array(
        [sSFR - sSFR_low, sSFR_high - sSFR], units=1.0 / unyt.yr
    )
    sSFR = unyt.unyt_array(sSFR, units=1.0 / unyt.yr)

    # slice the data to avoid overcrowding in pipeline plots
    processed.associate_x(
        Mstar[::20], scatter=None, comoving=False, description="Galaxy Stellar Mass"
    )
    processed.associate_y(
        sSFR[::20],
        scatter=sSFR_scatter[:, ::20],
        comoving=False,
        description="Specific Star Formation Rate (sSFR)",
    )
    processed.associate_redshift(z, redshift_lower=z - 0.35, redshift_upper=z + 0.35)
    processed.associate_plot_as(plot_as)

    multi_z.associate_dataset(processed)

output_path = f"../Leja2022.hdf5"

if os.path.exists(output_path):
    os.remove(output_path)

multi_z.write(filename=output_path)
