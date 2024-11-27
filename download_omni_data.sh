#!/bin/bash

# Define the base URL for downloading
base_url="https://cdaweb.gsfc.nasa.gov/pub/data/omni/high_res_omni/monthly_5min/"
output_dir="../Data/omni_data_monthly_5min"

# Create output directory if it doesn't exist
mkdir -p "$output_dir"

# Download the index page of the data directory
wget --no-check-certificate -O "$output_dir/index.html" "$base_url"

# Extract the file links from the index.html and download each .asc file
grep -oP 'href="\K[^"]+' "$output_dir/index.html" | while read -r file_name; do
    # Only download .asc files (skip other files or directories)
    if [[ "$file_name" =~ \.asc$ ]]; then
        echo "Downloading file: $file_name"
        wget --no-check-certificate -P "$output_dir" "$base_url$file_name"
    fi
done
