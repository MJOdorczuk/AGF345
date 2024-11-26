import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define constants
MU0 = 4 * np.pi * 1e-7  # Permeability of free space

# Define the plotting function for magnetic field lines
def plot_field_lines(ax, filename, color):
    """
    Plots the magnetic field lines from the given file onto the provided Axes3D object.

    Parameters:
        ax (Axes3D): The 3D axes to plot on.
        filename (str): The path to the data file.
        color (str): The color of the quiver plot.
    """
    # Load data from the file
    data = np.genfromtxt(filename, skip_header=1, delimiter=None)

    # Extract relevant columns
    XGSM = data[:, 0]
    YGSM = data[:, 1]
    ZGSM = data[:, 2]
    BXGSM = data[:, 4]
    BYGSM = data[:, 5]
    BZGSM = data[:, 6]

    # Plot the magnetic field lines
    ax.quiver(XGSM, YGSM, ZGSM, BXGSM, BYGSM, BZGSM, length=1, normalize=True, color=color, label=os.path.basename(filename))

    return XGSM, YGSM, ZGSM, BXGSM, BYGSM, BZGSM  # Return data for further calculations

# Defining plasma density
def plasma_density(XGSM,YGSM,ZGSM) :
    N_r = []
    R_E = 6371
    for i in range(len(XGSM)):
        r = np.sqrt(XGSM[i]**2 + YGSM[i]**2 + ZGSM[i]**2)
        n_r = 5e3 * (R_E / r)**3
        N_r.append(n_r)
        
    return N_r
# Define the function to compute and plot the Alfvén speed heatmap
def plot_alfven_speed(ax, filename):
    """
    Plots a 3D scatter plot of the Alfvén speed along the magnetic field lines.

    Parameters:
        ax (Axes3D): The 3D axes to plot on.
        filename (str): The path to the data file.
    """
    # Load data from the file
    data = np.genfromtxt(filename, skip_header=1, delimiter=None)

    # Extract relevant columns
    XGSM = data[:, 0]
    YGSM = data[:, 1]
    ZGSM = data[:, 2]
    BXGSM = data[:, 4] 
    BYGSM = data[:, 5]
    BZGSM = data[:, 6]
    rho = plasma_density(XGSM,YGSM,ZGSM)  # Assuming  plasma density model(rho)

    # Calculate magnetic field magnitude and Alfvén speed
    alfven_speed = []
    for i in range(len(XGSM)):
        B = np.sqrt(BXGSM[i]**2 + BYGSM[i]**2 + BZGSM[i]**2)
        alfven_spd = B / np.sqrt(MU0 * rho[i])
        alfven_speed.append(alfven_spd)

    # Plot the Alfvén speed using scatter, coloring by Alfvén speed
    sc = ax.scatter(XGSM, YGSM, ZGSM, c=alfven_speed, cmap='plasma', s=50, label = filename)
    ax.set_title(f'Alfvén Speed along Magnetic Field Line')
    ax.set_xlabel('XGSM [Re]')
    ax.set_ylabel('YGSM [Re]')
    ax.set_zlabel('ZGSM [Re]')
    ax.legend()
    
    # Add color bar to show the Alfvén speed scale
    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label('Alfvén Speed [m/s]')


# Main code
def plot_all_files_in_folder(folder_path):
    """
    Plots data from all .txt files in the specified folder, including magnetic field lines and Alfvén speed in 3D.

    Parameters:
        folder_path (str): Path to the folder containing .txt files.
    """
    # Get a list of all .txt files in the folder
    txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

    # Define a list of colors for each dataset
    colors = ['b', 'r', 'g', 'c', 'm', 'y', 'k']
    color_cycle = iter(colors)  # Create an iterator for cycling colors

    # Create the figure for magnetic field lines
    fig1 = plt.figure(figsize=(10, 7))
    ax1 = fig1.add_subplot(111, projection='3d')

    # Create the figure for Alfvén speed plot
    fig2 = plt.figure(figsize=(10, 7))
    ax2 = fig2.add_subplot(111, projection='3d')

    # Plot each file
    for txt_file in txt_files:
        color = next(color_cycle, 'k')  # Use the next color or default to 'k' (black)
        filepath = os.path.join(folder_path, txt_file)

        # Plot magnetic field lines
        plot_field_lines(ax1, filepath, color)

        # Plot Alfvén speed
        plot_alfven_speed(ax2, filepath)

    # Finalize 3D plot
    ax1.set_title('Earth Magnetic Field Lines over LYR (GSM)')
    ax1.set_xlabel('XGSM [Re]')
    ax1.set_ylabel('YGSM [Re]')
    ax1.set_zlabel('ZGSM [Re]')
    ax1.legend()

    # Show plots
    plt.show()

# Specify the folder path containing the .txt files
folder_path = './'  # Use the current folder or specify a different path
plot_all_files_in_folder(folder_path)
