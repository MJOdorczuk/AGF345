import os
import fnmatch
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re

def load_data_from_file(file_name):
    """
    Loads data from the provided file into a Pandas DataFrame.
    Skips the first two rows (header rows).
    """
    df = pd.read_csv(file_name, delim_whitespace=True, skiprows=2, header=None)
    df.columns = ['XGSM', 'YGSM', 'ZGSM', 'Radius', 'BXGSM', 'BYGSM', 'BZGSM', 'B']
    return df

def normalize_magnetic_field(df):
    """
    Normalizes the magnetic field components (BX, BY, BZ).
    Adds new columns for normalized magnetic field components.
    """
    magnitude = np.sqrt(df['BXGSM']**2 + df['BYGSM']**2 + df['BZGSM']**2)
    df['BX_norm'] = df['BXGSM'] / magnitude
    df['BY_norm'] = df['BYGSM'] / magnitude
    df['BZ_norm'] = df['BZGSM'] / magnitude
    return df

def extract_city_code(file_name):
    """
    Extracts the city code (XXX) from the filename pattern "B_311_2015_2001TT_XXX_00.txt".
    """
    match = re.search(r'B_311_\d{4}_\d{4}TT_(\w{3})_\d{2}\.txt', file_name)
    if match:
        return match.group(1)  # Extracted city code (XXX)
    else:
        return "Unknown"

def process_files_in_directory(directory, file_prefix="B_311"):
    """
    Processes all files in the directory that start with file_prefix and accumulates their data.
    """
    files = os.listdir(directory)
    matching_files = fnmatch.filter(files, f"{file_prefix}*.txt")
    all_data = []

    for file_name in matching_files:
        print(f"Processing file: {file_name}")
        file_path = os.path.join(directory, file_name)
        df = load_data_from_file(file_path)
        df_normalized = normalize_magnetic_field(df)
        city_code = extract_city_code(file_name)
        df_normalized['City'] = city_code  # Add city code to the DataFrame
        all_data.append(df_normalized)

    full_df = pd.concat(all_data, ignore_index=True)
    return full_df

def create_3d_quiver_plot(df, scale=0.1, zoom=True, save_as=None, arrows=True, hour_label=""):
    """
    Creates a 3D quiver plot using the combined filtered and normalized data.
    Optionally saves the plot with or without arrows, and with zoom option.
    """
    if zoom:
        df = df[df['Radius'] < 1.5]

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    sc = ax.scatter(
        df['XGSM'], df['YGSM'], df['ZGSM'],
        c=df['B'], cmap='viridis', s=30, edgecolor='k', label='Positions (Filtered)'
    )

    cbar = plt.colorbar(sc, ax=ax, pad=0.1)
    cbar.set_label('B [nT]', rotation=270, labelpad=15)
    cbar.set_ticks(np.linspace(df['B'].min(), df['B'].max(), num=5))

    ax.set_xlabel('XGSM [Re]')
    ax.set_ylabel('YGSM [Re]')
    ax.set_zlabel('ZGSM [Re]')
    ax.set_title(f'3D Plot of Magnetic Field - {hour_label}')

    if zoom:
        ax.set_xlim([-1.5, 1.5])
        ax.set_ylim([-1.5, 1.5])
        ax.set_zlim([-1.5, 1.5])
    else:
        ax.set_xlim([df['XGSM'].min(), df['XGSM'].max()])
        ax.set_ylim([df['YGSM'].min(), df['YGSM'].max()])
        ax.set_zlim([df['ZGSM'].min(), df['ZGSM'].max()])

    labeled_cities = set()

    for city in df['City'].unique():
        if city in labeled_cities:
            continue

        city_data = df[df['City'] == city]
        middle_index = len(city_data) // 2
        middle_row = city_data.iloc[middle_index]

        offset_x = 0.2
        offset_y = 0.2
        offset_z = 0.2

        ax.text(
            middle_row['XGSM'] + offset_x,
            middle_row['YGSM'] + offset_y,
            middle_row['ZGSM'] + offset_z,
            middle_row['City'], fontsize=8, color='blue'
        )

        labeled_cities.add(city)

    if arrows:
        ax.quiver(
            df['XGSM'], df['YGSM'], df['ZGSM'],
            df['BX_norm'] * scale, df['BY_norm'] * scale, df['BZ_norm'] * scale,
            color='r', length=0.5, normalize=False, linewidth=0.5, label='Normalized Field Vectors'
        )

    ax.legend()
    plt.tight_layout()
    plt.show()

    if save_as:
        fig.savefig(save_as, format='pdf')
        print(f"Plot saved as {save_as}")

def process_all_hours(directory):
    """
    Processes each subdirectory (hour folder) in the given directory and generates plots.
    """
    subdirectories = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]

    for subdirectory in subdirectories:
        hour_label = subdirectory[-2:]  # Get the last two characters (YY) from folder name, e.g., '00' or '17'
        print(f"Processing data for Hour {hour_label}...")

        # Get the path for the subdirectory
        subdirectory_path = os.path.join(directory, subdirectory)

        # Process files in the subdirectory
        combined_df = process_files_in_directory(subdirectory_path)

        # Create and save the plots
        create_3d_quiver_plot(combined_df, scale=0.1, zoom=True, save_as=f"3d_plot_with_arrows_hour_{hour_label}.pdf", arrows=True, hour_label=hour_label)
        create_3d_quiver_plot(combined_df, scale=0.1, zoom=False, save_as=f"3d_plot_without_arrows_hour_{hour_label}.pdf", arrows=False, hour_label=hour_label)

# Run the process for all subdirectories inside '../../data'
directory = "../../data"  # Parent directory containing 'Hour_00' and 'Hour_17'
process_all_hours(directory)
