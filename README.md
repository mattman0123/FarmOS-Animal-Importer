
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

pip install farmOS


## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/[YourGitHubUsername]/FarmOS-Animal-Importer.git
   cd FarmOS-Animal-Importer
   ```

2. Update the script with your FarmOS instance credentials:
   ```python
   hostname = "your-farmos-hostname"
   username = "your-username"
   password = "your-password"
   ```

3. Prepare your input CSV file. The CSV file should include the following columns:

   | Column Name           | Description                                                                                     | Required |
   |-----------------------|-------------------------------------------------------------------------------------------------|----------|
   | `name`                | Name of the asset.                                                                              | Yes      |
   | `parents`             | Parents of the asset (comma-separated).                                                        | No       |
   | `notes`               | Notes about the asset.                                                                          | No       |
   | `is location`         | Whether this asset is a location. Accepts most boolean values.                                  | No       |
   | `is fixed`            | Whether this asset has a fixed location. Accepts most boolean values.                           | No       |
   | `intrinsic geometry`  | The intrinsic geometry of the asset in WKT format.                                              | No       |
   | `status`              | Status of the asset (`active`, `archived`). Defaults to `active`.                                | No       |
   | `id tag`              | ID tag of the asset.                                                                            | No       |
   | `id tag type`         | Type of the ID tag (`brand`, `ear_tag`, `eid`, `leg_band`, `other`, `tattoo`).                  | No       |
   | `id tag location`     | Location of the ID tag.                                                                         | No       |
   | `animal type`         | Species/breed of the animal.                                                                    | Yes      |
   | `birthdate`           | Birthdate of the animal in YYYY-MM-DD format.                                                   | No       |
   | `nickname`            | Nicknames of the animal (comma-separated).                                                     | No       |
   | `sex`                 | Sex of the animal (`M`, `F`).                                                                   | No       |

4. Place your CSV file in the same directory as the script.

5. Run the script:
   ```bash
   python farmos_animal_importer.py
   ```

## Logging and Output

- The script logs successful creation of assets and any warnings (e.g., missing parents).
- Created assets are output with a direct link to the FarmOS instance.

## Example CSV

```csv
name,parents,notes,is fixed,intrinsic geometry,status,id tag,id tag type,id tag location,animal type,birthdate,nickname,sex
Bessie,,Healthy cow,TRUE,,active,12345,ear_tag,right ear,Cow,2020-05-15,Bess,F
Calf,Bessie,Young calf,FALSE,,active,,,,Cow,2023-03-01,,M
```

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests to improve this project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
