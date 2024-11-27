import os
from datetime import datetime, timedelta

# Define the input and output files
input_file = "../Data/Omni/omni_min202211.asc"
output_file = "../Data/Omni/filtered_omni_data_20221123_20221127.csv"

# Define the header (with Datetime as the first column)
header = (
    "Datetime,Bx_nT_GSE_GSM,By_nT_GSE,Bz_nT_GSE,Flow_Speed_km_s,Proton_Density_n_cc,"
    "Temperature_K,Flow_Pressure_nPa,Plasma_Beta,Alfven_Mach_Number,AE_index_nT,"
    "SYM_H_index_nT"
)

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
    "Temperature_K": 26,  # Temperature_K
    "Flow_Pressure_nPa": 27,  # Flow_Pressure_nPa
    "Plasma_Beta": 29,  # Plasma_Beta
    "Alfven_Mach_Number": 30,  # Alfven_Mach_Number
    "AE_index_nT": 37,  # AE_index_nT
    "SYM_H_index_nT": 41 # SYM_H_index_nT
}

# Define the date range for filtering
start_date = datetime(2022, 11, 23)
end_date = datetime(2022, 11, 27)

# Open the input file and process the data
with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    # Write the header to the output file
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
                # Filter the time of day to be between 09:00 and 16:00
                if 9 <= dt.hour <= 16:
                    dt_str = dt.strftime("%Y-%m-%d %H:%M")

                    # Prepare the selected columns for output
                    selected_columns = [
                        dt_str,  # Datetime
                        columns[column_indexes["Bx_nT_GSE_GSM"]],
                        columns[column_indexes["By_nT_GSE"]],
                        columns[column_indexes["Bz_nT_GSE"]],
                        columns[column_indexes["Flow_Speed_km_s"]],
                        columns[column_indexes["Proton_Density_n_cc"]],
                        columns[column_indexes["Temperature_K"]],
                        columns[column_indexes["Flow_Pressure_nPa"]],
                        columns[column_indexes["Plasma_Beta"]],
                        columns[column_indexes["Alfven_Mach_Number"]],
                        columns[column_indexes["AE_index_nT"]],
                        columns[column_indexes["SYM_H_index_nT"]]
                    ]

                    # Check if any value equals "99999.9", "999999", "9999.99", or "999.99" and skip the line if true
                    invalid_values = {"99999.9", "999999", "9999.99", "999.99", "99999"}
                    if any(value in invalid_values for value in selected_columns):
                        continue  # Skip this line

                    # Write the selected columns to the output file
                    outfile.write(",".join(selected_columns) + '\n')

print(f"Filtered data has been written to {output_file}.")
