# Calculating the acceleration potential as a function of altitude (h)

import numpy as np
import matplotlib.pyplot as plt

# Constants
m_e = 9.11e-31  # Electron mass (kg)
e = 1.6e-19     # Elementary charge (C)
j_I = CHOOSE IT  # Current density (A/m^2)
B_0 = CHOOSE IT      # Magnetic field strength at Earth's surface (T)
n_0 = CHOOSE IT       # Plasma density at Earth's surface (m^3)
R_0 = 6.37e6    # Earth's radius (m)

# Altitude range from 100 km to 1000 km
altitudes = np.linspace(100e3, 1000e3, 100)  # in meters

# Magnetic field and plasma density as functions of altitude
B_h = B_0 * (R_0 / altitudes)**2  # Magnetic field strength as a function of altitude
n_h = n_0 * (R_0 / altitudes)**3  # Plasma density as a function of altitude

# Calculate acceleration potential for each altitude
Phi_h = (m_e * j_I**2) / (2 * e**3 * B_h**2) * (B_h / n_h)**2

# Plot the distribution of the potential as a function of altitude
plt.figure(figsize=(8, 6))
plt.plot(altitudes / 1e3, Phi_h * 1e6, label=r'$\Phi(h)$ (μV)', color='b')  # μV for convenience
plt.xlabel('Altitude (km)')
plt.ylabel('Acceleration Potential (μV)')
plt.title('Auroral Acceleration Potential as a Function of Altitude')
plt.grid(True)
plt.legend()
plt.show()

