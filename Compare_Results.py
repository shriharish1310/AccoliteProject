import json
from deepdiff import DeepDiff


def count_characters_in_json(file_path):
    try:
        # Open the file and read its contents
        with open(file_path, 'r') as file:
            json_content = file.read()

        # Count the number of characters
        num_characters = len(json_content)

        return num_characters

    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except IOError as e:
        print(f"Error reading file '{file_path}': {e}")
        return None
def load_file(file_path):
    """
    Description:
        Load a JSON file and return its contents as a dictionary.
    Args:
        file_path (str): The path to the JSON file to be loaded.
    Returns:
        dict: The contents of the JSON file as a dictionary if successfully loaded.
        None: If there is an error decoding the JSON.
    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file '{file_path}': {e}")
        return None

def compare_json_files(file1, file2):
    """
    Description:
        This function loads two JSON files, compares their contents using DeepDiff,
        and prints any differences found. If the JSON files cannot be decoded,
        an error message is printed.
    Args:
        file1 (str): The path to the first JSON file.
        file2 (str): The path to the second JSON file.
    """
    json1 = load_file(file1)
    json2 = load_file(file2)

    if json1 is not None and json2 is not None:
        diff = DeepDiff(json1, json2, ignore_order=True)
        if diff:
            print(f"There are differences between '{file1}' and '{file2}':")
            print(json.dumps(diff, indent=4))  # Pretty print the differences
        else:
            print("No differences between the two files")
    else:
        print("Comparison could not be performed due to JSON decoding errors.")

x = count_characters_in_json('nested1.json')
y = count_characters_in_json('nested2.json')

print(x,y)
# Specify the paths to your JSON files
file1 = 'nested1.json'
file2 = 'nested2.json'

# Compare the JSON files
compare_json_files(file1, file2)
