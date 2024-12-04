import numpy as np
import matplotlib.pyplot as plt

# Constants
m_e = 9.11e-31  # Electron mass (kg)
e = 1.6e-19     # Elementary charge (C)
j_I = 1e-6      # Current density (A/m^2)
R_0 = 6.37e6    # Earth's radius (m)

# Load plasma density data from a .txt file, skipping the first two rows (headers)
data = np.loadtxt('n.txt', skiprows=2)  # Skip the first two rows
heights_km = data[:, 0]  # First column: height (km)
h_extended = np.arange(2000, 1e5, 10)
n_cm3 = data[:, 1]       # Second column: plasma density (Ne/cm^3)
n_cm3 = n_cm3[heights_km >= 200]
heights_km = heights_km[heights_km >= 200]
fit_height = 1000
cs = np.polyfit(heights_km[heights_km >= fit_height], 1 / n_cm3[heights_km >= fit_height], 7)
n_extended = 1 / np.polyval(cs, h_extended)
heights_km = np.concatenate((heights_km, h_extended))
n_cm3 = np.concatenate((n_cm3, n_extended)) + 0.1

# Convert plasma density from Ne/cm^3 to Ne/m^3
n_m3 = n_cm3 * 1e6  # Conversion factor: 1 cm^3 = 1e6 m^3

# Load the magnetic field data from a file, skipping the first two header rows
B_data = np.loadtxt('B_311_2015_2001TT_LYR_17.txt', skiprows=2)

# Extract the relevant columns: 4th column for distance (Re) and 8th column for total magnetic field (nT)
distance_Re = B_data[:, 3]  # Distance in Earth radii
B_total_nT = B_data[:, 7]   # Total magnetic field in nT
ZGSM = B_data[:, 2]         # ZGSM (3rd column, to filter out negative values)

# Convert the distance from Earth radii (Re) to kilometers (1 Re = 6371 km) and subtract Earth's radius to get the altitude
distance_km = distance_Re * 6371  # Convert distance from Re to km
altitude_km = distance_km - 6371  # Subtract Earth's radius to get altitude

# Filter the data to include only positive ZGSM values (removes duplicate data from the opposite hemisphere)
mask_B = ZGSM >= 0  # Only keep rows where ZGSM is non-negative
filtered_altitude_km = altitude_km[mask_B]
filtered_B_total_nT = B_total_nT[mask_B]

# Filter the magnetic field data to include only altitudes up to 2000 km
mask_altitude = filtered_altitude_km <= heights_km.max()
filtered_altitude_km = filtered_altitude_km[mask_altitude]
filtered_B_total_nT = filtered_B_total_nT[mask_altitude]

# Acceleration potential (Phi_h) as a function of altitude
# Interpolate magnetic field data to match the heights_km data points
B_interpolated = np.interp(heights_km, filtered_altitude_km, filtered_B_total_nT)
B_0 = B_interpolated.max()

# Calculate the acceleration potential (Phi_h) based on the interpolated B field
B_naive = B_interpolated.max() * (6571 / (6371 + heights_km)) ** 2
Phi_h = (m_e * j_I**2) / (2 * e**3 * B_0**2) * (B_naive / n_m3)**2  # Acceleration potential (V)
Phi_h_uV = Phi_h * 1e6  # Convert from volts to microvolts
print(heights_km[Phi_h.argmax()])  # Print the height (in km) where Phi_h is maximum
print(f'The maximum accelerating potential is {Phi_h.max()}V')

# Plot the ionospheric plasma density and the acceleration potential
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot plasma density
ax1.plot(heights_km, n_m3, 'b--', label=r'$n(h)$ (plasma density)', linewidth=2)
ax1.set_xlabel('Altitude (km)')
ax1.set_ylabel('Plasma Density (particles/m$^3$)', color='b')
ax1.tick_params(axis='y', labelcolor='b')
ax1.grid(True, linestyle='--', linewidth=0.5)

# Create another y-axis for the acceleration potential
ax2 = ax1.twinx()
ax2.plot(heights_km, Phi_h_uV, 'r-', label=r'$\Phi(h)$ (Acceleration Potential)', linewidth=2)
ax2.set_ylabel('Acceleration Potential (μV)', color='r')
ax2.tick_params(axis='y', labelcolor='r')

# Create another y-axis for the magnetic field
ax3 = ax1.twinx()
ax3.plot(heights_km, B_naive, 'g-.', label=r'$B(h)$ (Magnetic Field)', linewidth=2)
ax3.set_ylabel('Magnetic Field (nT)', color='g')
ax3.tick_params(axis='y', labelcolor='g')
ax3.spines['right'].set_position(('outward', 60))  # Offset for clarity

# Tertiary y-axis offset text
ax3.yaxis.get_offset_text().set_x(1.15)

# Title and legend
plt.title('Ionospheric Plasma Density and Acceleration Potential as a Function of Altitude')
fig.tight_layout()
plt.xscale('log')
ax1.set_yscale('log')
ax2.set_yscale('log')
ax3.set_yscale('log')
plt.show()
