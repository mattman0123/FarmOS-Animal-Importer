"""
FarmOS Animal Asset Importer Script
===================================

This script imports animal assets into FarmOS using a CSV file as input. It connects to a FarmOS instance, processes 
the provided data, and creates animal assets with optional relationships, metadata, and attributes.

Features:
- Handles required fields (e.g., `name`, `animal type`) and validates their presence.
- Supports optional fields such as `birthdate`, `parents`, `notes`, `is fixed`, and more.
- Automatically creates animal types if they do not exist in the FarmOS taxonomy.
- Links animal assets to their parents (if specified) using existing FarmOS records.

Dependencies:
- farmOS Python package
- pandas (optional, for extended data processing)
- datetime
- csv

Usage:
1. Update the `hostname`, `username`, and `password` variables with your FarmOS instance credentials.
2. Ensure the input CSV file matches the required structure and contains necessary columns.
3. Run the script in your Python environment.

Author: Matthew Vinck
GitHub: https://github.com/mattman0123/FarmOS-Animal-Importer
License: MIT License
"""


from farmOS import farmOS
from datetime import datetime
import csv

# Define FarmOS credentials
hostname = *****************
username = *************
password = *************

# Maintain an external state of the token.
current_token = None

# Callback function to save new tokens
def token_updater(new_token):
    print(f"Got a new token! {new_token}")
    # Update state with the new token
    global current_token
    current_token = new_token

# Create the FarmOS client
farm_client = farmOS(
    hostname=hostname,
    token_updater=token_updater,  # Provide the token updater callback
)

# Authorize the client (initial or refresh token)
if not current_token:
    current_token = farm_client.authorize(username, password, scope="farm_manager")
else:
    # Use existing token if available (optional refresh logic can be added here)
    pass

# Function to find or create an animal type
def create_find_animal_type(data):
    """
    Searches for an existing animal type in FarmOS.
    If not found, creates a new one.
    """
    animal_type_search = farm_client.term.iterate(
        'animal_type',
        params=farm_client.filter('name', data),
    )
    animal_type = next(iter(animal_type_search), None)

    if animal_type is None:  # Create the animal type if it doesn't exist
        term_create_response = farm_client.term.send(
            'animal_type',
            {"attributes": {"name": data}}
        )
        animal_type = term_create_response["data"]
    return animal_type

# Function to process parent relationships
def process_parents(parents_data):
    """
    Processes the 'parents' field from the CSV.
    Finds and returns the FarmOS relationships for the listed parents.
    """
    if not parents_data:
        return []  # Return an empty list if no parents are provided

    parent_list = []
    # Split the parent data into individual entries and clean up whitespace
    parent_ids = [p.strip() for p in parents_data.split(",")]
    for parent in parent_ids:
        # Search for each parent by name in FarmOS
        parent_search = farm_client.asset.iterate(
            "animal",
            params=farm_client.filter("name", parent),
        )
        parent_asset = next(iter(parent_search), None)
        if parent_asset:  # If the parent is found, add it to the list
            parent_list.append({
                "type": parent_asset["type"],
                "id": parent_asset["id"],
            })
        else:
            print(f"Warning: Parent '{parent}' not found in FarmOS.")
    return parent_list

# Open the CSV file and process each row
with open(r"csv_asset--animal.csv", newline="") as csvfile:
    csv_reader = csv.DictReader(csvfile)  # Read the CSV as a dictionary
    for animal in csv_reader:
        try:
            # Ensure required fields are present
            if not animal.get("name"):
                raise ValueError("Missing required field: 'name'")
            if not animal.get("animal type"):
                raise ValueError("Missing required field: 'animal type'")

            # Handle the optional birthdate field
            animal_dob = None
            if animal.get("birthdate"):  # Check if a birthdate is provided
                try:
                    # Parse the date using the expected format
                    animal_dob = datetime.strptime(animal["birthdate"], "%Y-%m-%d")
                except ValueError:
                    print(f"Invalid date format for birthdate: {animal['birthdate']}")
                    animal_dob = None

            # Find or create the animal type in FarmOS
            animal_type = create_find_animal_type(animal["animal type"])

            # Process parent relationships
            parent_relationships = process_parents(animal.get("parents"))

            # Build the payload for the API request
            payload = {
                "attributes": {
                    "name": animal["name"],  # Name of the animal
                    "birthdate": animal_dob.strftime("%Y-%m-%dT%H:%M:%S+00:00") if animal_dob else None,
                    "notes": animal.get("notes"),  # Notes about the animal
                    "is_fixed": animal.get("is fixed"),  # Boolean: Is the animal fixed?
                    "is_location": animal.get("is location"),  # Boolean: Is this a location asset?
                    "intrinsic_geometry": animal.get("intrinsic geometry"),  # Location geometry in WKT format
                    "status": animal.get("status", "active"),  # Defaults to "active"
                    "id_tag": animal.get("id tag"),  # ID tag
                    "id_tag_type": animal.get("id tag type"),  # Type of ID tag
                    "id_tag_location": animal.get("id tag location"),  # Location of the ID tag
                    "nickname": animal.get("nickname"),  # Nicknames of the animal
                    "sex": animal.get("sex"),  # Sex of the animal
                },
                "relationships": {
                    "animal_type": {
                        "data": {
                            "type": animal_type["type"],  # Type of the animal (e.g., species)
                            "id": animal_type["id"],  # ID of the animal type
                        },
                    },
                },
            }

            # Add parent relationships if they exist
            if parent_relationships:
                payload["relationships"]["parents"] = {"data": parent_relationships}

            # Send the payload to create the animal asset in FarmOS
            animal_create_response = farm_client.asset.send("animal", payload)

            # Print confirmation of the created asset
            print(
                f"Created animal '{animal['name']}': "
                f"{farm_client.session.hostname}/asset/"
                f"{animal_create_response['data']['attributes']['drupal_internal__id']}"
            )

        except Exception as e:
            # Log errors encountered while processing a specific row
            print(f"Error processing animal '{animal.get('name', 'Unnamed')}': {e}")
