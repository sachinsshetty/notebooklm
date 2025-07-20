import os
import json
from pathlib import Path

import dwani
import os
import json

# Set up dwani API credentials
dwani.api_key = os.getenv("DWANI_API_KEY")
dwani.api_base = os.getenv("DWANI_API_BASE_URL")


def combine_json_files(directory_path, output_file):
    # Dictionary to store all JSON contents
    combined_data = {}
    
    # Convert directory_path to Path object
    directory = Path(directory_path)
    
    # Ensure directory exists
    if not directory.exists():
        raise FileNotFoundError(f"Directory {directory_path} does not exist")
    
    try:
        # Iterate through all files in directory
        for file_path in directory.glob("*.json"):
            # Get filename without extension
            file_name = file_path.stem
            
            try:
                # Read and parse JSON file
                with open(file_path, 'r', encoding='utf-8') as file:
                    json_data = json.load(file)
                    # Store content with filename as key
                    combined_data[file_name] = json_data
                    
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in {file_path}: {e}")
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                
        # Write combined data to output file
        with open(output_file, 'w', encoding='utf-8') as output:
            json.dump(combined_data, output, indent=4)
            
        print(f"Combined JSON written to {output_file}")
        return combined_data
        
    except Exception as e:
        print(f"Error processing directory {directory_path}: {e}")
        return None


def qa_book_creator(key_points_json, qa_json_file):
    with open(key_points_json, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        # Store content with filename as key
    
    system_prompt = "return answer in json format"
    result = dwani.Chat.direct(
    prompt="You are a teacher, creating questions for an oral exam based on context " + str(json_data) , system_prompt= system_prompt)

    print(result)
        # Write combined data to output file
    with open(qa_json_file, 'w', encoding='utf-8') as output:
        json.dump(result, output, indent=4)
        
    print(f"QA written to {qa_json_file}")

    
# Example usage
if __name__ == "__main__":
    # Specify your directory path and output file
    input_directory = "output"  # Replace with your directory path
    output_json = "combined_output.json"
    
    qa_json_file = "qa_bank.json"
    combine_json_files(input_directory, output_json)

    qa_book_creator(output_json, qa_json_file)