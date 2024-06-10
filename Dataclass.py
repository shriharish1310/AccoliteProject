import requests
import json
import yaml
from dataclasses import dataclass
from typing import Dict


# Define dataclasses
@dataclass
class Time:
    updated: str
    updatedISO: str
    updateduk: str


@dataclass
class Currency:
    code: str
    symbol: str
    rate: str
    description: str
    rate_float: float


@dataclass
class Bpi:
    USD: Currency
    GBP: Currency
    EUR: Currency


@dataclass
class CoindeskResponse:
    time: Time
    disclaimer: str
    chartName: str
    bpi: Bpi


# Function to read the YAML configuration
def load_config(config_path: str) -> Dict:
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


# Load configuration
config = load_config('config.yaml')

# Extract the URL from the configuration
url = config['api']['url']

# Make the API call
response = requests.get(url)

if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Map the JSON data to dataclasses
    time_data = Time(**data['time'])
    bpi_data = Bpi(**{k: Currency(**v) for k, v in data['bpi'].items()})
    coindesk_response = CoindeskResponse(
        time=time_data,
        disclaimer=data['disclaimer'],
        chartName=data['chartName'],
        bpi=bpi_data
    )

    # Print the response dataclass
    print(coindesk_response)

    # Save the JSON response to a file
    with open('coindesk_output.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print("Data has been saved to coindesk_output.json")
else:
    print(f"Failed to retrieve data: {response.status_code}")
