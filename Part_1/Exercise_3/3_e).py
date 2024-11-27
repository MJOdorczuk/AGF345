import numpy as np

# Constants
e = 1.602e-19  # Elementary charge in Coulombs
m_e = 9.109e-31  # Electron mass in kg
m_i = 1.67e-27  # Ion mass (example for a proton, in kg)
pi = np.pi  # Pi constant
nu_ei = 1e9  # Electron-ion collision frequency (example value, in Hz)

# Define input values
n = 1e11  # Electron density in m^-3 (modify this as needed)
K_th = 1e-3  # Example constant K_th (modify this as needed)
n_e = 1e11  # Example electron density for Pedersen conductivity calculation

# Calculate K
K = (e**2 * n) / np.sqrt(2 * pi * m_e * K_th)
print(f"K = {K:.3e}")

# Calculate Pedersen conductivity (sigma_p)
sigma_p = (n_e * e**2) / (m_i * nu_ei)
print(f"Pedersen conductivity (sigma_p) = {sigma_p:.3e}")

# Calculate the resistive length scale (Lambda)
Lambda = np.sqrt(sigma_p / K)
print(f"Resistive length scale (Lambda) = {Lambda:.3e}")
