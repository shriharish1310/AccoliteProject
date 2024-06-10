import requests
import json


def get_api_json(api_url, json_file):
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            with open(json_file, 'w') as file:
                json.dump(data, file, indent=4)
            print(f"Data successfully saved to {json_file}")
        else:
            print(f"Failed to retrieve data. HTTP Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

api_url = 'https://api.coindesk.com/v1/bpi/currentprice.json'
json_file = 'json_output.json'
get_api_json(api_url, json_file)