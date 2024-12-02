# Import necessary libraries
import numpy as np

# Formula 1: UJ [GW] = a * AE + b
def calculate_UJ(a, AE, b):
    return a * AE + b

# Formula 2: UA [GW] = a * AE**gamma + b
def calculate_UA(a, AE, gamma, b):
    return a * (AE ** gamma) + b

# Formula 3: URC [GW] = -4e4 * (∂Dst*/∂t + Dst*/τ)
def calculate_URC(dDst_dt, Dst_star, tau):
    return -4e4 * (dDst_dt + Dst_star / tau)

# Example usage:
# Replace these with your actual values
a = 0.1          # value for a
AE = 1500e-9 #T         # value for AE
b = 0           # value for b
gamma = 0.39        #  value for gamma
dDst_dt = (-13 - 8)/(120*60)  # 120 minutes to seconds  value for ∂Dst*/∂t
Dst_star = -13    # value for Dst*
kp = 4
tau = 3/kp #days         # value for τ
duration = 6060  # Substorm duration in seconds

# Calculate the results
UJ = calculate_UJ(a, AE, b)
UA = calculate_UA(a, AE, gamma, b)
URC = calculate_URC(dDst_dt, Dst_star, tau)

# Calculate energy outcome in GJ (GW * seconds)
energy_UJ = UJ * duration
energy_UA = UA * duration
energy_URC = URC * duration

# Print results
print(f"UJ [GW]: {UJ}")
print(f"UA [GW]: {UA}")
print(f"URC [GW]: {URC}")
print(f"Energy from UJ [GJ]: {energy_UJ}")
print(f"Energy from UA [GJ]: {energy_UA}")
print(f"Energy from URC [GJ]: {energy_URC}")
