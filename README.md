# Download-NEX-GDDP-CMIP6
This python code is created to download the [NASA Earth Exchange Global Daily Downscaled Projections (NEX-GDDP-CMIP6)](https://www.nccs.nasa.gov/services/data-collections/land-based-products/nex-gddp-cmip6), based on the [Tech Note](https://www.nccs.nasa.gov/sites/default/files/NEX-GDDP-CMIP6-Tech_Note_4.pdf). 

## 1️⃣ Prerequisites

- **Python 3.x**
- **`curl`** command-line tool (used for downloading files)
- Python libraries (pre-installed):
  - `os`
  - `hashlib`
  - `argparse`
  - `subprocess`
  - `urllib.parse`
  - `logging`

 ## 📂 Directory Structure
```
Base Direction/
└── Model name/
    └── Scenarios/
        └── variable_day_Model name_Scenarios_Year_v1.1.nc
```
For example: 
```
NEX-GDDP-CMIP6/
└── GFDL-CM4/
    ├── historical/
    │   ├── pr_day_GFDL-CM4_historical_1995_v1.1.nc
    │   └── pr_day_GFDL-CM4_historical_1996_v1.1.nc
    └── ssp245/
        ├── pr_day_GFDL-CM4_ssp245_2041_v1.1.nc
        └── pr_day_GFDL-CM4_ssp245_2042_v1.1.nc
```

## 🛠 Command-Line Arguments

| **Argument**   | **Type** | **Description**                                                                                 | **Example**                           |
|----------------|----------|-----------------------------------------------------------------------------------------------|---------------------------------------|
| `--base_dir`   | `str`    | **(Required)** Path to the base directory where data will be stored.                           | `/path/to/NEX-GDDP-CMIP6`            |
| `--model`      | `str`    | **(Required)** Name of the climate model.                                                      | `GFDL-CM4`                            |
| `--scenario`   | `str`    | **(Required)** Climate scenario. Must be one of: `historical`, `ssp126`, `ssp245`, `ssp370`, `ssp585`. | `ssp245`                         |
| `--variable`   | `str`    | **(Required)** Variable to download (e.g., `pr`, `tasmax`, `tasmin`).                          | `pr`                                  |
| `--start_year` | `int`    | **(Required)** Start year for downloading data.                                                | `2041`                                |
| `--end_year`   | `int`    | **(Required)** End year for downloading data.                                                  | `2100`                                |


## :rocket: Running the Script
In the terminal 
```
python3 download_CMIP6.py --base_dir "/path/to/Folder" --model <MODEL_NAME> --scenario <SCENARIO> --variable <VARIABLE> --start_year <START_YEAR> --end_year <END_YEAR>
```
For example: 
```
python3 download_CMIP6.py --base_dir "/Users/mengting.chen91/Desktop/Gridded Rainfall Data/NEX-GDDP-CMIP6" --model GFDL-CM4 --scenario ssp245 --variable pr --start_year 2041 --end_year 2100
```







