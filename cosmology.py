from astropy.cosmology import FlatLambdaCDM

# Cosmology from table II (3x2pt + all external constraints) from T. Abbott et al. (2022)
cosmology = FlatLambdaCDM(
    H0=0.681e2, Om0=0.306, Ob0=0.0486, m_nu=[0.0, 0.0, 0.06], Tcmb0=2.7255
)

# Asplund et al. (2009)
solar_metallicity = 0.0134

# IMF conversion factors from Furlong+ 2015
kroupa_to_chabrier_mass = 0.912
salpeter_to_chabrier_mass = 0.606
