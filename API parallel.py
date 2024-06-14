import requests
import yaml
import time
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

# Function to read the YAML configuration
def load_config(config_path: str) -> dict:
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

# Function to make an API call
def fetch_data(url: str) -> dict:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

# Load configuration
config = load_config('config.yaml')

# Extract the URLs from the configuration
urls = config['api']['urls']

# Start timing the script
start_time = time.perf_counter()
# Execute API calls in parallel
results = [None] * len(urls)
with ThreadPoolExecutor() as executor:
    future_to_index = {executor.submit(fetch_data, url): idx for idx, url in enumerate(urls)}
    for future in as_completed(future_to_index):
        idx = future_to_index[future]
        try:
            result = future.result()
            results[idx] = result
        except Exception as e:
            print(f"An error occurred with URL at index {idx}: {e}")

# End timing the script
end_time = time.perf_counter()

# Indicate success
print("Parallel execution success")

# Save the results to a JSON file
with open('parallel_results.json', 'w') as json_file:
    json.dump(results, json_file, indent=4)

# Calculate and print the run time with high accuracy
run_time = end_time - start_time
print(f"Parallel script run time: {run_time:.8f} seconds")