import shutil

def save_copy(input_file_path):
    output_file_path = "credentials_2.json"
    try:
        # Copy the file to the specified output path
        shutil.copy(input_file_path, output_file_path)
        print(f"File saved successfully at: {output_file_path}")
    except Exception as e:
        print(f"Error saving file: {e}")
    

