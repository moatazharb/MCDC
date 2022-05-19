import numpy as np

# Disable Numba-JIT for pure Python mode
from numba import config
config.DISABLE_JIT = True

# Get path to mcdc (not necessary if mcdc is installed)
import sys
sys.path.append('../../../../')

import mcdc

# =============================================================================
# Set model
# =============================================================================
# The infinite homogenous medium is modeled with reflecting slabs

# Load material data
with np.load('SHEM-361.npz') as data:
    SigmaC = data['SigmaC']   # /cm
    SigmaS = data['SigmaS']
    SigmaF = data['SigmaF']
    nu_p   = data['nu_p']
    nu_d   = data['nu_d']
    chi_p  = data['chi_p']
    chi_d  = data['chi_d']
    G      = data['G']

SigmaC *= 2.0 # augment capture to achieve subcriticality

# Set material
m = mcdc.material(capture=SigmaC, scatter=SigmaS, fission=SigmaF, nu_p=nu_p,
                  chi_p=chi_p, nu_d=nu_d, chi_d=chi_d)

# Set surfaces
s1 = mcdc.surface('plane-x', x=-1E10, bc="reflective")
s2 = mcdc.surface('plane-x', x=1E10,  bc="reflective")

# Set cells
c = mcdc.cell([+s1, -s2], m)

# =============================================================================
# Set source
# =============================================================================
# Uniform in energy

source = mcdc.source(energy=np.ones(G))

# =============================================================================
# Set problem and tally, and then run mcdc
# =============================================================================

# Tally
mcdc.tally(scores=['flux'])

# Setting
mcdc.setting(N_hist=1E3)

# Run
mcdc.run()