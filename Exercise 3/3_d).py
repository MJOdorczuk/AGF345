# Constants and given values
import math

# Physical constants
m_e = 9.11e-31  # Electron mass (kg)
e = 1.6e-19     # Elementary charge (C)

# Given values
j_I = 5e-6      # Current density (A/m^2)
B_I = CHOOSE IT    # Magnetic field in the ionosphere (T)
B = CHOOSE IT       # Magnetic field in the magnetosphere (T)
n = CHOOSE IT         # Plasma density (particles/m^3)

# Formula for acceleration potential
Phi = (m_e * j_I**2) / (2 * e**3 * B_I**2) * (B / n)**2

Phi
