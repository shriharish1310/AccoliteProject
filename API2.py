import requests
import json
import yaml
import time
from dataclasses import dataclass
from typing import List


# Define dataclasses for the new structure
@dataclass
class Organization:
    login: str
    id: int
    node_id: str
    url: str
    repos_url: str
    events_url: str
    hooks_url: str
    issues_url: str
    members_url: str
    public_members_url: str
    avatar_url: str
    description: str


# Function to read the YAML configuration
def load_config(config_path: str) -> dict:
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


# Load configuration
config = load_config('config.yaml')

# Extract the URL from the configuration
url = config['api']['url']

# Start timing the script
start_time = time.perf_counter()

# Make the API call
response = requests.get(url)

if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Print the raw JSON data to understand its structure
    print(json.dumps(data, indent=4))

    # Map the JSON data to dataclasses
    try:
        organizations = [Organization(**org) for org in data]

        # Print the response dataclass
        for org in organizations:
            print(org)

        # Save the JSON response to a file
        with open('github_orgs_output.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)

        print("Data has been saved to github_orgs_output.json")
    except TypeError as e:
        print(f"Error: {e}")
        print("Data structure might not match the expected Organization dataclass.")
else:
    print(f"Failed to retrieve data: {response.status_code}")

# End timing the script
end_time = time.perf_counter()

# Calculate and print the run time with high accuracy
run_time = end_time - start_time
print(f"Script run time: {run_time:.15f} seconds")
