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
    # Read data into a DataFrame, skipping the first two rows
    df = pd.read_csv(file_name, delim_whitespace=True, skiprows=2, header=None)
    
    # Assign column names based on the original data
    df.columns = ['XGSM', 'YGSM', 'ZGSM', 'Radius', 'BXGSM', 'BYGSM', 'BZGSM', 'B']
    
    return df

def normalize_magnetic_field(df):
    """
    Normalizes the magnetic field components (BX, BY, BZ).
    Adds new columns for normalized magnetic field components.
    """
    # Calculate the magnitude of the magnetic field
    magnitude = np.sqrt(df['BXGSM']**2 + df['BYGSM']**2 + df['BZGSM']**2)
    
    # Normalize the magnetic field components
    df['BX_norm'] = df['BXGSM'] / magnitude
    df['BY_norm'] = df['BYGSM'] / magnitude
    df['BZ_norm'] = df['BZGSM'] / magnitude
    
    return df

def extract_city_code(file_name):
    """
    Extracts the city code (XXX) from the filename pattern "B_311_2015_2021TT_XXX_00.txt".
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
    # List all files in the directory
    files = os.listdir(directory)
    
    # Filter files that start with B311
    matching_files = fnmatch.filter(files, f"{file_prefix}*.txt")
    
    # Initialize an empty list to hold all data
    all_data = []

    # Loop through each matching file and process it
    for file_name in matching_files:
        print(f"Processing file: {file_name}")
        
        # Construct the full file path
        file_path = os.path.join(directory, file_name)
        
        # Load the data
        df = load_data_from_file(file_path)
        
        # Normalize the magnetic field components
        df_normalized = normalize_magnetic_field(df)
        
        # Extract the city code from the file name
        city_code = extract_city_code(file_name)
        df_normalized['City'] = city_code  # Add city code to the DataFrame
        
        # Add the normalized data to the list
        all_data.append(df_normalized)
    
    # Concatenate all data into a single DataFrame
    full_df = pd.concat(all_data, ignore_index=True)
    
    return full_df


import matplotlib.pyplot as plt
import numpy as np

def create_3d_quiver_plot(df, scale=0.1, zoom=True, save_as=None, arrows=True):
    """
    Creates a 3D quiver plot using the combined filtered and normalized data.
    Can be zoomed in (radius < 1.5) or full view based on the 'zoom' parameter.
    Optionally removes arrows if 'arrows=False'.
    """
    # Filter data for zoomed-in view (radius < 1.5) or full view
    if zoom:
        df = df[df['Radius'] < 1.5]
    
    # Create a 3D plot
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Use color to represent the magnitude of B with a better color map
    sc = ax.scatter(
        df['XGSM'], df['YGSM'], df['ZGSM'],
        c=df['B'], cmap='viridis', s=30, edgecolor='k', label='Positions (Filtered)'
    )

    # Add a color bar to show the magnitude of B with more detail
    cbar = plt.colorbar(sc, ax=ax, pad=0.1)
    cbar.set_label('B [nT]', rotation=270, labelpad=15)
    cbar.set_ticks(np.linspace(df['B'].min(), df['B'].max(), num=5))  # More ticks for detail

    # Label axes
    ax.set_xlabel('XGSM [Re]')
    ax.set_ylabel('YGSM [Re]')
    ax.set_zlabel('ZGSM [Re]')
    ax.set_title('3D Plot of Magnetic Field')

    # Set the axis limits based on zoom flag
    if zoom:
        ax.set_xlim([-1.5, 1.5])
        ax.set_ylim([-1.5, 1.5])
        ax.set_zlim([-1.5, 1.5])
    else:
        # Set limits for the full view based on the data range
        ax.set_xlim([df['XGSM'].min(), df['XGSM'].max()])
        ax.set_ylim([df['YGSM'].min(), df['YGSM'].max()])
        ax.set_zlim([df['ZGSM'].min(), df['ZGSM'].max()])

    # Create a set to track which cities have already been labeled
    labeled_cities = set()

    # Loop through unique cities and find the midpoint for each city's vector
    for city in df['City'].unique():
        # Skip if city has already been labeled
        if city in labeled_cities:
            continue

        # Get all the data for this city
        city_data = df[df['City'] == city]
        
        # Calculate the index of the middle data point
        middle_index = len(city_data) // 2  # Get the index of the middle point

        # Get the data at the middle index
        middle_row = city_data.iloc[middle_index]

        # Apply an offset to move the label slightly away from the line
        offset_x = 0.2  # Small offset in X direction
        offset_y = 0.2  # Small offset in Y direction
        offset_z = 0.2  # Small offset in Z direction

        # Label the midpoint of the city’s data with the offset
        ax.text(
            middle_row['XGSM'] + offset_x, 
            middle_row['YGSM'] + offset_y, 
            middle_row['ZGSM'] + offset_z,
            middle_row['City'], fontsize=8, color='blue'
        )

        # Add the city to the labeled set to avoid labeling again
        labeled_cities.add(city)

    # If arrows are requested, plot the magnetic field vectors
    if arrows:
        ax.quiver(
            df['XGSM'], df['YGSM'], df['ZGSM'],  # Starting points
            df['BX_norm'] * scale, df['BY_norm'] * scale, df['BZ_norm'] * scale,  # Normalized components of the vector
            color='r', length=0.5, normalize=False, linewidth=0.5, label='Normalized Field Vectors'
        )

    # Add a legend
    ax.legend()

    # Adjust layout to minimize margins
    plt.tight_layout()

    # Show the plot
    plt.show()

    # Save the plot as PDF if save_as is specified
    if save_as:
        fig.savefig(save_as, format='pdf')
        print(f"Plot saved as {save_as}")

# Example usage for creating both plots (with and without arrows):

# Assuming 'df' is the DataFrame with all the necessary data






# Main function to run the steps for all matching files in the directory
def main(directory):
    # Process files and get combined data
    combined_df = process_files_in_directory(directory)
    
    # Create and save the zoomed-in 3D quiver plot
    #create_3d_quiver_plot(combined_df, zoom=True, save_as="zoomed_plot.png")
    # Plot with arrows
    create_3d_quiver_plot(combined_df, scale=0.1, zoom=True, save_as="3d_plot_with_arrows.pdf", arrows=True)

    # Plot without arrows
    create_3d_quiver_plot(combined_df, scale=0.1, zoom=False, save_as="3d_plot_without_arrows.pdf", arrows=False)
    # Create and save the full 3D quiver plot
    #create_3d_quiver_plot(combined_df, zoom=False, save_as="full_plot.png")


# Run the main function with the directory where the files are located
directory = "./midnight"  # Replace with the path to your directory containing the files
main(directory)
