# Import required libraries
import os
import hashlib
import logging
import argparse
from subprocess import run as srun
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(level=logging.INFO)

def download_file(uri, output_filename, md5_expected):
    """Download a file and verify its checksum."""
    try:
        # Download using curl
        srun(['curl', '-s', '-o', output_filename, uri], capture_output=True, check=True)
        logging.info(f"Downloaded file: {output_filename}")

        # Verify MD5 checksum
        with open(output_filename, 'rb') as f:
            md5_downloaded = hashlib.md5(f.read()).hexdigest()

        if md5_downloaded != md5_expected:
            logging.warning(f"Checksum mismatch for {output_filename}.\nExpected: {md5_expected}\nGot: {md5_downloaded}")
        else:
            logging.info(f"Checksum verified for {output_filename}")

    except Exception as e:
        logging.error(f"Failed to download {uri}. Error: {e}")

# Function to download files for a specific model, scenario, and variable
def download_model_data(base_dir, model_name, scenario, variable, start_year, end_year):
    # Ensure base directory exists
    if not os.path.exists(base_dir):
        logging.error(f"Base directory '{base_dir}' does not exist. Please create it first.")
        return

    # Create model and scenario-specific directories within base_dir
    output_dir = os.path.join(base_dir, model_name, scenario)
    os.makedirs(output_dir, exist_ok=True)
    logging.info(f"Created directory: {output_dir}")

    # Download the index file if not already present
    index_file = "index_v1.1_md5.txt"
    index_url = "https://nex-gddp-cmip6.s3.us-west-2.amazonaws.com/index_v1.1_md5.txt"

    if not os.path.exists(index_file):
        srun(['curl', '-O', index_url], check=True)
        logging.info(f"Index file downloaded: {index_file}")
    else:
        logging.info("Index file already exists.")

    # Parse index file and download matching files
    with open(index_file, 'r') as file:
        for line in file:
            if not line.strip():
                continue  # Skip empty lines

            parts = line.strip().split()
            if len(parts) != 2:
                logging.warning(f"Invalid line format: {line.strip()}")
                continue

            md5_checksum, file_path = parts
            file_url = f"https://nex-gddp-cmip6.s3.us-west-2.amazonaws.com/{file_path}"
            filename = os.path.basename(file_path)

            # Filter based on variable, model, scenario, version, and time period
            if variable in filename and "v1.1.nc" in filename and model_name in file_path and scenario in file_path:
                # Extract year from filename
                year_in_filename = [int(s) for s in filename.split('_') if s.isdigit()]
                if year_in_filename and (start_year <= year_in_filename[0] <= end_year):
                    output_path = os.path.join(output_dir, filename)
                    logging.info(f"Starting download for: {filename}")
                    download_file(file_url, output_path, md5_checksum)

    logging.info(f"All '{variable}' v1.1 files ({start_year}-{end_year}) for model '{model_name}' and scenario '{scenario}' have been downloaded and verified.")

# Main function to handle user input
if __name__ == "__main__":
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Download NEX-GDDP-CMIP6 data organized by model and scenario.")
    parser.add_argument('--base_dir', type=str, required=True, help='Base directory where data will be stored (e.g., /path/to/NEX-GDDP-CMIP6)')
    parser.add_argument('--model', type=str, required=True, help='Model name (e.g., GFDL-CM4)')
    parser.add_argument('--scenario', type=str, required=True, choices=['historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585'], help='Scenario (e.g., historical, ssp245)')
    parser.add_argument('--variable', type=str, required=True, help='Variable name (e.g., pr, tasmax, tasmin)')
    parser.add_argument('--start_year', type=int, required=True, help='Start year (e.g., 1995)')
    parser.add_argument('--end_year', type=int, required=True, help='End year (e.g., 2014)')

    args = parser.parse_args()

    # Call the download function with user inputs
    download_model_data(args.base_dir, args.model, args.scenario, args.variable, args.start_year, args.end_year)
