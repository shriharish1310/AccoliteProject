import requests
import json
import yaml
import time
from dataclasses import dataclass
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

# Define dataclasses for the GitHub API response
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

# Define dataclasses for the Coindesk API response
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
def load_config(config_path: str) -> dict:
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

# Function to make an API call
def fetch_data(url: str) -> Dict[str, Any]:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

# Load configuration
config = load_config('config.yaml')

# Extract the URLs from the configuration
urls = config['api']['urls']

# Start timing the script
start_time = time.perf_counter()

# Execute API calls in parallel using ThreadPoolExecutor
results = []
with ThreadPoolExecutor() as executor:
    futures = [executor.submit(fetch_data, url) for url in urls]
    for future in as_completed(futures):
        try:
            results.append(future.result())
        except Exception as e:
            print(f"An error occurred: {e}")

# End timing the script
end_time = time.perf_counter()

# Process and display the results
for result, url in zip(results, urls):
    print(f"Results from {url}:")
    if 'bpi' in result:  # This is the Coindesk API response
        time_data = Time(**result['time'])
        bpi_data = Bpi(**{k: Currency(**v) for k, v in result['bpi'].items()})
        coindesk_response = CoindeskResponse(
            time=time_data,
            disclaimer=result['disclaimer'],
            chartName=result['chartName'],
            bpi=bpi_data
        )
        print(coindesk_response)
    elif isinstance(result, list):  # This is the GitHub API response
        organizations = [Organization(**org) for org in result]
        for org in organizations:
            print(org)
    else:
        print("Unknown data format")

# Calculate and print the run time with high accuracy
run_time = end_time - start_time
print(f"Script run time: {run_time:.15f} seconds")
