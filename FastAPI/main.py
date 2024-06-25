from fastapi import FastAPI, HTTPException, Query
import requests
import yaml

app = FastAPI()

# Function to load configuration from YAML file
def load_config(config_file):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    users = config.get('users', {})
    roles = config.get('components', {}).get('roles', {})
    paths = config.get('paths', {})
    return users, roles, paths

# Function to make API call
def make_api_call(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to filter response data based on allowed fields
def filter_response(data, allowed_fields):
    if isinstance(data, list):
        return [{k: v for k, v in item.items() if k in allowed_fields} for item in data]
    elif isinstance(data, dict):
        return {k: v for k, v in data.items() if k in allowed_fields}
    else:
        return data

# Load configuration initially
users, roles, paths = load_config('roles_per.yaml')

# FastAPI endpoint to fetch data based on endpoint, user, and role
@app.get("/")
async def fetch_data(
    endpoint: str = Query("/users/hadley/orgs", description="API endpoint to call"),
    user: str = Query(..., description="The user from the YAML configuration"),
    role: str = Query(..., description="The role of the user")
):
    user_roles = users.get(user, {}).get('roles', [])

    if role not in user_roles:
        raise HTTPException(status_code=403, detail=f"User '{user}' does not have the role '{role}'")

    role_permissions = roles.get(role, {})
    allowed_endpoints = role_permissions.get('endpoints', [])
    allowed_fields = role_permissions.get('fields', {})

    # Find the operationId for the given endpoint
    operation_id = None
    for path, methods in paths.items():
        if path == endpoint:
            operation_id = methods.get('get', {}).get('operationId')
            break

    if not operation_id:
        raise HTTPException(status_code=404, detail=f"Endpoint '{endpoint}' not found in configuration")

    if operation_id not in allowed_endpoints:
        raise HTTPException(status_code=403, detail=f"Role '{role}' does not have permission to access '{endpoint}'")

    endpoint_url = f"https://api.github.com{endpoint}"
    data = make_api_call(endpoint_url)
    if data is not None:
        filtered_data = filter_response(data, allowed_fields.get(operation_id, []))
        return filtered_data
    else:
        raise HTTPException(status_code=500, detail=f"Failed to fetch data from '{endpoint_url}'")
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)