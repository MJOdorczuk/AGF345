import numpy as np
import matplotlib.pyplot as plt

# Constants
m_e = 9.11e-31  # Electron mass (kg)
e = 1.6e-19     # Elementary charge (C)
j_I = 3e-6      # Current density (A/m^2)
n_0 = 1e12      # Peak plasma density at lower altitudes (particles/m^3)
h_peak = 400e3  # Peak density altitude (m)
sigma = 500e3   # Width of Gaussian for plasma density (m)
R_0 = 6.37e6    # Earth's radius (m)

# Altitude range: 1,000 km to 15,000 km
altitudes = np.linspace(1e3, 15e3, 500) * 1e3  # Altitude in meters

# Plasma density profile: Gaussian-like at lower altitudes, exponential decay above 4,000 km
n_h = n_0 * np.exp(-0.5 * ((altitudes - h_peak) / sigma) ** 2) + 1e6# * np.exp(-altitudes / (2e6))  # Combined profile

# Magnetic field profile: Dipole model with a slower falloff at high altitudes
B_0 = 5e-5      # Magnetic field strength at Earth's surface (T)
B_h = B_0 * (R_0 / altitudes)**3  # Magnetic field strength as a function of altitude (T)
B_h_nT = B_h * 1e9  # Convert from Tesla to nanoTesla

# Acceleration potential (Phi_h) as a function of altitude
Phi_h = (m_e * j_I**2) / (2 * e**3 * B_0**2) * (B_h / n_h)**2  # Acceleration potential (V)
Phi_h_uV = Phi_h * 1e6  # Convert from volts to microvolts

# Plot the ionospheric plasma density and the acceleration potential
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot plasma density
ax1.plot(altitudes / 1e3, n_h, 'b--', label=r'$n(h)$ (plasma density)', linewidth=2)
ax1.set_xlabel('Altitude (km)')
ax1.set_ylabel('Plasma Density (particles/m$^3$)', color='b')
ax1.tick_params(axis='y', labelcolor='b')
ax1.grid(True, linestyle='--', linewidth=0.5)

# Create another y-axis for the acceleration potential
ax2 = ax1.twinx()
ax2.plot(altitudes / 1e3, Phi_h_uV, 'r-', label=r'$\Phi(h)$ (Acceleration Potential)', linewidth=2)
ax2.set_ylabel('Acceleration Potential (μV)', color='r')
ax2.tick_params(axis='y', labelcolor='r')

# Create another y-axis for the magnetic field
ax3 = ax1.twinx()
ax3.plot(altitudes / 1e3, B_h_nT, 'g-.', label=r'$B(h)$ (Magnetic Field)', linewidth=2)
ax3.set_ylabel('Magnetic Field (nT)', color='g')
ax3.tick_params(axis='y', labelcolor='g')
ax3.spines['right'].set_position(('outward', 60))  # Offset for clarity

# Tertiary y-axis offset text
ax3.yaxis.get_offset_text().set_x(1.15)

# Title and legend
plt.title('Ionospheric Plasma Density and Acceleration Potential as a Function of Altitude')
fig.tight_layout()
plt.show()


