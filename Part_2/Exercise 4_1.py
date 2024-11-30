import pandas as pd

# Load the CSV file to inspect its content
file_path = 'filtered_omni_data_20221123_20221127.csv'
data = pd.read_csv(file_path)

# Display the first few rows to understand the structure
data.head(), data.columns
import numpy as np

# Add derived columns for B (total magnetic field) and clock angle (theta in radians)
data['B_total'] = np.sqrt(data['Bx_nT_GSE_GSM']**2 + data['By_nT_GSE']**2 + data['Bz_nT_GSE']**2)
data['Theta_rad'] = np.arctan2(data['By_nT_GSE'], data['Bz_nT_GSE'])

# Convert the 'Datetime' column to a proper datetime object
data['Datetime'] = pd.to_datetime(data['Datetime'])

# Extract relevant columns for further calculations
filtered_data = data[['Datetime', 'B_total', 'Flow_Speed_km_s', 'Theta_rad']]

# Display the first few rows of the processed data
filtered_data.head()

from datetime import datetime

# Define the substorm interval
start_time = datetime(2022, 11, 25, 18, 31, 51)
end_time = datetime(2022, 11, 25, 20, 2, 3)

# Filter the data within the substorm interval
substorm_data = filtered_data[(filtered_data['Datetime'] >= start_time) & (filtered_data['Datetime'] <= end_time)]

# Constants for the calculation
mu_0 = 4 * np.pi * 1e-7  # Vacuum permeability (H/m)
l_0 = 7 * 6.371e6  # Approximate l0 (7 Earth radii in meters)

# Convert units as necessary (B_total from nT to T, V from km/s to m/s)
substorm_data['B_total_T'] = substorm_data['B_total'] * 1e-9  # nT to T
substorm_data['Flow_Speed_m_s'] = substorm_data['Flow_Speed_km_s'] * 1e3  # km/s to m/s

# Calculate epsilon using the formula
substorm_data['Epsilon_W'] = (
    (4 * np.pi / mu_0)
    * substorm_data['Flow_Speed_m_s']
    * substorm_data['B_total_T']**2
    * np.sin(substorm_data['Theta_rad'] / 2)**4
    * l_0**2
)

# Integrate epsilon over time to get total energy input (approximation via summation)
# Assuming equal time intervals (1-minute data resolution)
time_interval = 60  # seconds (1 minute)
total_energy = substorm_data['Epsilon_W'].sum() * time_interval  # Total energy in Joules

total_energy, substorm_data[['Datetime', 'Epsilon_W']].head()

# Plot the energy input rate (Epsilon) over time
plt.figure(figsize=(12, 6))
plt.plot(substorm_data['Datetime'], substorm_data['Epsilon_W'] / 1e9, label='Energy Input Rate (GW)', color='blue')
plt.axvline(start_time, color='green', linestyle='--', label='Substorm Onset')
plt.axvline(end_time, color='red', linestyle='--', label='Substorm End')
plt.title('Energy Input Rate (\u03B5) During the Substorm', fontsize=14)
plt.xlabel('Time (UTC)', fontsize=12)
plt.ylabel('Energy Input Rate (GW)', fontsize=12)
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()
