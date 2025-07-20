import dwani
import os
import json

# Set up dwani API credentials
dwani.api_key = os.getenv("DWANI_API_KEY")
dwani.api_base = os.getenv("DWANI_API_BASE_URL")

# Directory containing PDF files
input_directory = "./input_folder"  # Update with your directory path
output_directory = "./output"  # Update with your output directory path

# Create output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Prompt for processing PDFs
prompt = "list the key points and provide the response in json"

# Iterate through all files in the input directory
for filename in os.listdir(input_directory):
    if filename.lower().endswith('.pdf'):  # Process only PDF files
        file_path = os.path.join(input_directory, filename)
        try:
            # Query the PDF using dwani
            result = dwani.Documents.query_all(
                file_path, model="gemma3", tgt_lang="eng_Latn", prompt=prompt
            )

            # Extract translated query answer and original text
            pdf_answer = result["translated_query_answer"]
            extracted_text = result["original_text"]

            # Get top 5 important items
            result = dwani.Chat.direct(
                prompt="provide top 5 important items and return response as json: " + extracted_text
            )

            # Clean the JSON response
            clean_json_str = result['response'].replace('```json', '').replace('```', '').strip()

            # Parse the cleaned JSON string to ensure it's valid
            try:
                json_data = json.loads(clean_json_str)
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON for {filename}: {e}")
                continue

            # Define output JSON file path
            output_filename = os.path.splitext(filename)[0] + "_output.json"
            output_filepath = os.path.join(output_directory, output_filename)

            # Save the JSON data to a file
            with open(output_filepath, 'w', encoding='utf-8') as json_file:
                json.dump(json_data, json_file, indent=4)

            print(f"Processed {filename} and saved output to {output_filename}")

        except Exception as e:
            print(f"Error processing {filename}: {e}")

print("All PDF files processed.")