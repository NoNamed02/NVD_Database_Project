# NVD Project - README

This project is designed to download, parse, and store National Vulnerability Database (NVD) data locally using Python.

---

## ✅ Features

- Download NVD JSON data for specific years or a range of years.
- Parse the downloaded data and store it in a SQLite database.
- Display stored data based on severity level (e.g., CRITICAL, HIGH, MEDIUM, LOW).
- Sort and limit data based on publication date.
- Search by specific CVE ID.

---

## ✅ Requirements

**Python 3.x** and **SQLite**

```bash
pip install requests pandas

nvd_project/
├── env/                   # Virtual environment folder
├── nvd_data.db            # SQLite database file
├── download_and_populate.py # Main script to download and populate the database
├── view_data.py           # Script to view and query data
├── database.py            # Script to create the SQLite database
├── README.md              # Project documentation (Markdown)

# Clone the repository
git clone <repository-url>
cd nvd_project

# Create and activate a virtual environment (Windows)
python -m venv env
.\env\Scripts\activate

# Or for macOS/Linux
source env/bin/activate

# Install the required libraries
pip install requests pandas

# Create the SQLite database
python database.py

# Run the main script to download and populate the NVD data
python download_and_populate.py

# Example Input:
# Enter start year (e.g., 2002): 2020
# Enter end year (e.g., 2023): 2023

# To query and view the data, run:
python view_data.py

# Options:
# 1. View all data in ascending order by date.
# 2. View all data in descending order by date.
# 3. Filter by severity level (CRITICAL, HIGH, MEDIUM, LOW, UNKNOWN).
# 4. Limit the number of records displayed.

# To remove the virtual environment (Windows)
deactivate
rmdir /S /Q env

# To remove the virtual environment (macOS/Linux)
deactivate
rm -rf env
