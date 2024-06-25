import yaml
import json
import requests
import time
import concurrent.futures


def write_to_file(filename: str, data):
    '''Writes data to a file in json format'''
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        print(f'Data successfully written to {filename}')
    except Exception as e:
        print(f'Error writing data to {filename}: {e}')


def load_yaml_file(filepath):
    '''Reads and loads the YAML configuration file'''
    try:
        with open(filepath, 'r') as file:
            print(f'Loading YAML file: {filepath}')
            return yaml.safe_load(file)
    except Exception as e:
        print(f'Error loading YAML file {filepath}: {e}')
        return None


def fetch_data(api: str) -> dict:
    '''Fetches data from an API and returns it as a dictionary'''
    try:
        response = requests.get(api)
        response.raise_for_status()
        print(f'Data fetched from API: {api}')
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Error fetching data from API {api}: {e}')
        return {}


def get_and_write(base_url: str, username: str):
    '''Fetches data from the API for a given user and writes it to a file'''
    api_url = f"{base_url}/users/{username}/orgs"
    organizations = fetch_data(api_url)
    write_to_file('data.json', organizations)
    return organizations


def print_organization_details(organizations):
    '''Prints organization details'''
    if organizations:
        for i, org in enumerate(organizations, 1):
            print(f"{i}. Organization: {org['login']}")
            print(f"   ID: {org['id']}")
            print(f"   Node ID: {org['node_id']}")
            print(f"   URL: {org['url']}")
            print(f"   Description: {org['description'] or 'Not provided'}")
            print("=" * 50)
    else:
        print("No organizations found.")


if __name__ == '__main__':
    config_filename = 'OpenAPI_Config.yaml'
    config = load_yaml_file(config_filename)

    if not config:
        print(f'No config file found for filename: {config_filename}')
    else:
        base_url = "https://api.github.com"

        paths = config.get('paths')
        if paths:
            username_path = '/users/{username}/orgs'
            path_config = paths.get(username_path)

            if path_config:
                print("Enter the GitHub username to fetch organizations for:")
                username = input().strip()

                organizations = get_and_write(base_url, username)
                print_organization_details(organizations)

                if organizations:
                    selection = input("Enter the numbers of organizations you want to fetch (comma-separated): ")
                    selected_indexes = [int(idx.strip()) - 1 for idx in selection.split(',')]

                    selected_organizations = [organizations[idx] for idx in selected_indexes if
                                              0 <= idx < len(organizations)]

                    if selected_organizations:
                        print("Selected Organizations:")
                        print_organization_details(selected_organizations)
                    else:
                        print("Invalid selection. No organizations fetched.")
            else:
                print(f'Path configuration for "{username_path}" not found in the OpenAPI spec.')
        else:
            print('Paths section not found in the OpenAPI spec.')