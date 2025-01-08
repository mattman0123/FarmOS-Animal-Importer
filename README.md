# FarmOS Animal Asset Importer

A Python script to bulk import animal assets into a [FarmOS](https://farmos.org/) instance using a CSV file. The script allows you to define attributes, relationships, and metadata for each animal asset.

## Features

- Import animal assets from a CSV file.
- Automatically create animal types (e.g., species or breeds) if they don't exist in FarmOS.
- Handle parent-child relationships between animals.
- Process optional fields like birthdate, notes, ID tags, nicknames, and more.
- Validate required fields and log errors for missing or invalid data.

## Requirements

- Python 3.7+
- [farmOS Python package](https://github.com/farmOS/farmOS.py)
- `datetime`
- `csv`

Install the farmOS library using pip:
```bash
pip install farmOS
