import numpy as np
import sys

import mcdc

N_particle = int(sys.argv[2])

# =============================================================================
# Set model
# =============================================================================
# The infinite homogenous medium is modeled with reflecting slab

# Load material data
with np.load('CASMO-70.npz') as data:
    SigmaC = data['SigmaC']*1.5 # /cm
    SigmaS = data['SigmaS']
    SigmaF = data['SigmaF']
    nu_p   = data['nu_p']
    nu_d   = data['nu_d']
    chi_p  = data['chi_p']
    chi_d  = data['chi_d']
    G      = data['G']
    speed    = data['v']
    lamd     = data['lamd']

# Set material
m = mcdc.material(capture=SigmaC, scatter=SigmaS, fission=SigmaF, nu_p=nu_p,
                  chi_p=chi_p, nu_d=nu_d, chi_d=chi_d)

# Set surfaces
s1 = mcdc.surface('plane-x', x=-1E10, bc="reflective")
s2 = mcdc.surface('plane-x', x=1E10,  bc="reflective")

# Set cells
c = mcdc.cell([+s1, -s2], m)

# =============================================================================
# Set initial source
# =============================================================================

energy = np.zeros(G); energy[-1] = 1.0
source = mcdc.source(energy=energy)

# =============================================================================
# Set problem and tally, and then run mcdc
# =============================================================================

# Tally
mcdc.tally(scores=['flux'])

# Setting
mcdc.setting(N_particle=N_particle, output='output_'+str(N_particle), 
             active_bank_buff=1000, progress_bar=False)

# Run
mcdc.run()
