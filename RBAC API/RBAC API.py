import requests
import json
import yaml


def load_config(config_file):
    """
    Description:
        Loads configuration from a YAML file.
    Args:
        config_file (str): The path to the YAML configuration file.
    Returns:
        tuple: A tuple containing:
            - endpoints (list): A list of endpoint dictionaries, each containing 'url', 'method', 'description', and 'permission'.
            - roles (dict): A dictionary of role permissions and allowed fields.
            - users (dict): A dictionary of users and their associated roles.
    """
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    paths = config.get('paths', {})
    components = config.get('components', {})
    roles = components.get('roles', {})
    users = config.get('users', {})

    endpoints = []
    for path, methods in paths.items():
        for method, details in methods.items():
            endpoints.append({
                'url': f"https://api.github.com{path}",
                'method': method,
                'description': details.get('description', 'No description provided.'),
                'permission': details.get('operationId')
            })
    return endpoints, roles, users


def make_api_call(url):
    """
    Description:
        Makes a GET request to the specified URL.
    Args:
        url (str): The URL to make the GET request to.
    Returns:
        dict or None: The JSON response as a dictionary if the request is successful, otherwise None.
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def filter_response(data, allowed_fields):
    """
    Description:
        Filters the response data to include only the allowed fields.
    Args:
        data (dict or list): The response data to be filtered.
        allowed_fields (list): A list of allowed field names.
    Returns:
        dict or list: The filtered data.
    """
    if isinstance(data, list):
        return [{k: v for k, v in item.items() if k in allowed_fields} for item in data]
    elif isinstance(data, dict):
        return {k: v for k, v in data.items() if k in allowed_fields}
    else:
        return data


def check_permissions_and_call_apis(endpoints, user_role, roles):
    """
    Description:
        Checks the user's permissions and calls the APIs for the allowed endpoints.
    Args:
        endpoints (list): A list of endpoint dictionaries.
        user_role (str): The role of the user.
        roles (dict): A dictionary of role permissions and allowed fields.
    Returns:
        None
    """
    role_permissions = roles.get(user_role, {})
    allowed_endpoints = role_permissions.get('endpoints', [])
    allowed_fields = role_permissions.get('fields', {})

    for i, endpoint in enumerate(endpoints):
        url = endpoint['url']
        permission = endpoint.get('permission')
        if permission and permission in allowed_endpoints:
            data = make_api_call(url)
            if data is not None:
                filtered_data = filter_response(data, allowed_fields.get(permission, []))
                output_file = f'output_{user_role}.json'
                with open(output_file, 'w') as json_file:
                    json.dump(filtered_data, json_file, indent=4)
            else:
                print(f"Failed to fetch data from '{url}'")
        else:
            print(f"User with role '{user_role}' does not have permission to access '{url}'")
            print("No output file has been created since no access.")


def main():
    selected_config_file = 'users_and_roles.yaml'
    endpoints, roles, users = load_config(selected_config_file)

    if not roles:
        print("The selected configuration file does not define roles.")
        return

    print("Select the User:")
    for user in users:
        print(user)

    user = input("Enter the user name: ")
    user_roles = users.get(user, {}).get('roles')

    if user_roles:
        print(f"User '{user}' has the following roles: {', '.join(user_roles)}")
        print("Select the role for this session:")
        for idx, role in enumerate(user_roles, start=1):
            print(f"{idx}. {role}")

        role_index = input("Enter the role number: ").strip()
        if role_index.isdigit() and 0 < int(role_index) <= len(user_roles):
            selected_role = user_roles[int(role_index) - 1]
            check_permissions_and_call_apis(endpoints, selected_role, roles)
        else:
            print("Invalid role selection. Select a valid role.")
    else:
        print("Invalid user. Select a valid user.")

if __name__ == "__main__":
    main()