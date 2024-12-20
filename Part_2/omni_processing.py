import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Function to filter data from input file
def filter_data(input_file, output_file, start_date, end_date):
    # Define the header with the reduced set of columns
    header = "Datetime,Bx_nT_GSE_GSM,By_nT_GSE,Bz_nT_GSE,Flow_Speed_km_s,Proton_Density_n_cc,Temperature_K"

    # Indexes for the fields based on the original data layout (column positions are zero-based)
    column_indexes = {
        "Year": 0,  # Year
        "Day": 1,   # Day of the year
        "Hour": 2,  # Hour
        "Minute": 3,  # Minute
        "Bx_nT_GSE_GSM": 14,  # Bx_nT_GSE_GSM
        "By_nT_GSE": 15,  # By_nT_GSE
        "Bz_nT_GSE": 16,  # Bz_nT_GSE
        "Flow_Speed_km_s": 21,  # Flow_Speed_km_s
        "Proton_Density_n_cc": 25,  # Proton_Density_n_cc
        "Temperature_K": 26  # Temperature_K
    }

    # Open the input file and process the data
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        # Write the reduced header to the output file
        outfile.write(header + '\n')

        for line in infile:
            # Skip headers in the input file by checking if the first character is a digit
            if line.strip() and line[0].isdigit():
                # Split the line into columns based on whitespace
                columns = line.split()

                # Extract Year, Day, Hour, and Minute for Datetime calculation
                year = int(columns[column_indexes["Year"]])
                day_of_year = int(columns[column_indexes["Day"]])
                hour = int(columns[column_indexes["Hour"]])
                minute = int(columns[column_indexes["Minute"]])

                # Calculate the datetime
                dt = datetime(year, 1, 1) + timedelta(days=day_of_year - 1, hours=hour, minutes=minute)

                # Check if the date is within the specified range
                if start_date <= dt <= end_date:
                    dt_str = dt.strftime("%Y-%m-%d %H:%M")

                    # Prepare the reduced set of selected columns for output
                    selected_columns = [
                        dt_str,  # Datetime
                        columns[column_indexes["Bx_nT_GSE_GSM"]],
                        columns[column_indexes["By_nT_GSE"]],
                        columns[column_indexes["Bz_nT_GSE"]],
                        columns[column_indexes["Flow_Speed_km_s"]],
                        columns[column_indexes["Proton_Density_n_cc"]],
                        columns[column_indexes["Temperature_K"]]
                    ]

                    # Check if any value equals "99999.9", "999999", "9999.99", or "999.99" and skip the line if true
                    invalid_values = {"99999.9", "999999", "9999.99", "999.99", "99999"}
                    if any(value in invalid_values for value in selected_columns):
                        continue  # Skip this line

                    # Write the selected columns to the output file
                    outfile.write(",".join(selected_columns) + '\n')

    print(f"Filtered data with reduced columns has been written to {output_file}.")

# Function to create and save a plot
def create_plot(df, plot_title, output_file):
        # Calculate the necessary columns first
    df["Flow_Speed_m_s"] = df["Flow_Speed_km_s"] * 1000  # Convert km/s to m/s
    df["B_module"] = (df["Bx_nT_GSE_GSM"]**2 + df["By_nT_GSE"]**2 + df["Bz_nT_GSE"]**2)**0.5  # B module

    # Apply rolling mean with window size of 5 to relevant columns
    cols_to_smooth = ["Bz_nT_GSE", "Bx_nT_GSE_GSM", "By_nT_GSE", 
                      "B_module", "Flow_Speed_m_s", 
                      "Proton_Density_n_cc", "Temperature_K"]
    df[cols_to_smooth] = df[cols_to_smooth].rolling(window=5).mean()


    # Create a figure with subplots
    fig, axes = plt.subplots(5, 1, figsize=(12, 15), sharex=True)
    fig.suptitle(plot_title, fontsize=16)

    # Subplot 1: Bz_nT_GSE over Datetime
    axes[0].plot(df["Datetime"], df["Bz_nT_GSE"], label="Bz_nT_GSE", color="blue")
    axes[0].set_ylabel("Bz (nT)")
    axes[0].legend()
    axes[0].grid()

    # Subplot 2: Bx_nT_GSE_GSM, By_nT_GSE, and B_module over Datetime
    axes[1].plot(df["Datetime"], df["Bx_nT_GSE_GSM"], label="Bx_nT_GSE_GSM", color="red")
    axes[1].plot(df["Datetime"], df["By_nT_GSE"], label="By_nT_GSE", color="green")
    axes[1].plot(df["Datetime"], df["B_module"], label="B Module", color="purple")
    axes[1].set_ylabel("B Components (nT)")
    axes[1].legend()
    axes[1].grid()

    # Subplot 3: Flow_Speed_m_s over Datetime
    axes[2].plot(df["Datetime"], df["Flow_Speed_m_s"], label="Flow Speed (m/s)", color="orange")
    axes[2].set_ylabel("Flow Speed (m/s)")
    axes[2].legend()
    axes[2].grid()

    # Subplot 4: Proton_Density_n_cc over Datetime
    axes[3].plot(df["Datetime"], df["Proton_Density_n_cc"], label="Proton Density (n/cc)", color="cyan")
    axes[3].set_ylabel("Proton Density (n/cc)")
    axes[3].legend()
    axes[3].grid()

    # Subplot 5: Temperature_K over Datetime
    axes[4].plot(df["Datetime"], df["Temperature_K"], label="Temperature (K)", color="magenta")
    axes[4].set_ylabel("Temperature (K)")
    axes[4].legend()
    axes[4].grid()

    # Set x-axis label
    axes[4].set_xlabel("Datetime")

    # Adjust layout
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)

    # Save the plot
    plt.savefig(output_file)
    print(f"Plot saved as '{output_file}'.")

    # Show the plot
    plt.show()

# Main execution
if __name__ == "__main__":
    input_file = "../data/Omni/omni_min202211.asc"
    output_file = "../data/Omni/filtered_omni_data_20221123_20221127.csv"
    start_date = datetime(2022, 11, 23)
    end_date = datetime(2022, 11, 27)

    # Filter data
    filter_data(input_file, output_file, start_date, end_date)

    # Load filtered data
    df = pd.read_csv(output_file, parse_dates=["Datetime"])

    # Create the full-range plot
    create_plot(df, "OMNI Data: Full Range", "omni_data_full_range.pdf")

    # Create the focused plot (24th Nov 12am to 26th Nov 12am)
    focused_start = datetime(2022, 11, 24)
    focused_end = datetime(2022, 11, 26)
    focused_df = df[(df["Datetime"] >= focused_start) & (df["Datetime"] < focused_end)]
    create_plot(focused_df, "OMNI Data: Focused Range (24th Nov  - 26th Nov )", "omni_data_focused_range.png")


    # Create the focused plot (24th Nov 12am to 26th Nov 12am)
    focused_start = datetime(2022, 11, 25, 14, 0, 0)
    focused_end = datetime(2022, 11, 25, 21, 0, 0)
    focused_df = df[(df["Datetime"] >= focused_start) & (df["Datetime"] < focused_end)]
    create_plot(focused_df, "OMNI Data: Short Range (25th Nov 14:00  - 21:00 )", "omni_data_short_range.png")