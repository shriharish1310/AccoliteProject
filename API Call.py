import requests
import yaml
import time
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

def load_config(config_path: str) -> dict:
    """
    Description:
        Load configurations present in the YAML file.
    Arguments:
        config_path : Path to the configuration YAML file (Type: String).
    Returns:
        dict: Configurations data (Type: Dict).
    """
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def fetch_data(url: str) -> dict:
    """
    Description:
        Fetch data from a given URL (API Endpoint).
    Args:
        url : The URL to fetch data from (Type: String).
    Returns:
        Data fetched from the URL in JSON format (Type: Dict).
    Raises:
        HTTPError: An error occurred during the HTTP request (404 Error).
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def execute_sequential(urls: list) -> list:
    """
    Description:
        Execute API calls sequentially.
    Args:
        urls : List of URLs to fetch data from (Type: list).
    Returns:
        list: Results of the API calls.
    """
    results = []
    for url in urls:
        try:
            result = fetch_data(url)
            results.append(result)
        except Exception as e:
            print(f"An error occurred: {e}")
    return results
def execute_parallel(urls: list) -> list:
    """
    Description:
        Execute API calls in parallel and store in any order.
    Args:
        urls : List of URLs to fetch data from (Type: list).
    Returns:
        list: Results of the API calls.
    """
    results = []
    with ThreadPoolExecutor() as executor:
        future_to_url = {executor.submit(fetch_data, url): url for url in urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"An error occurred with URL {url}: {e}")
    return results
# def execute_parallel(urls: list) -> list:
#     """
#     Execute API calls in parallel in the order of APIs
#
#     Args:
#         urls : List of URLs to fetch data from (Type: list)
#
#     Returns:
#         list: Results of the API calls.
#     """
#     results = [None] * len(urls)
#     with ThreadPoolExecutor() as executor:
#         future_to_index = {executor.submit(fetch_data, url): idx for idx, url in enumerate(urls)}
#         for future in as_completed(future_to_index):
#             idx = future_to_index[future]
#             try:
#                 result = future.result()
#                 results[idx] = result
#             except Exception as e:
#                 print(f"An error occurred with URL at index {idx}: {e}")
#     return results

def main():
    """
    Main function to execute the sequential and parallel API calls and save the results.
    """
    config = load_config('config.yaml')
    urls = config['api']['urls']

    # Sequential execution
    start_time = time.perf_counter()
    sequential_results = execute_sequential(urls)
    end_time = time.perf_counter()

    print("Sequential execution success")
    with open('sequential_results.json', 'w') as json_file:
        json.dump(sequential_results, json_file, indent=4)
    run_time = end_time - start_time
    print(f"Sequential script run time: {run_time:.8f} seconds")

    # Parallel execution
    start_time = time.perf_counter()
    parallel_results = execute_parallel(urls)
    end_time = time.perf_counter()

    print("Parallel execution success")
    with open('parallel_results.json', 'w') as json_file:
        json.dump(parallel_results, json_file, indent=4)
    run_time = end_time - start_time
    print(f"Parallel script run time: {run_time:.8f} seconds")

if __name__ == "__main__":
    main()