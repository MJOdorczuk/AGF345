import numpy as np

e = 1.602e-19  # Elementary charge in Coulombs
m_e = 9.109e-31  # Electron mass in kg
m_i = 1.67e-27  # Ion mass (for proton, in kg)
pi = np.pi  # Pi constant
nu_ei = 1e9  # Electron-ion collision frequency in Hz (typical for ionospheric conditions)

# Define ionospheric plasma parameters
n = 1e11  # Electron density in m^-3 (typical for ionospheric plasma)

# Convert K_th from 10 keV to Joules (SI)
K_th = 1.602e-15  # 10 keV in joules (1 eV = 1.602e-19 J)

n_e = 10e11  # Example electron density for Pedersen conductivity calculation

# Calculate K
K = (e**2 * n) / np.sqrt(2 * pi * m_e * K_th)
print(f"K = {K:.3e}")

# Calculate Pedersen conductivity (sigma_p)
sigma_p = (n_e * e**2) / (m_i * nu_ei)
print(f"Pedersen conductivity (sigma_p) = {sigma_p:.3e}")

# Calculate the resistive length scale (Lambda)
Lambda = np.sqrt(sigma_p / K)
print(f"Resistive length scale (Lambda) = {Lambda:.3e}")
