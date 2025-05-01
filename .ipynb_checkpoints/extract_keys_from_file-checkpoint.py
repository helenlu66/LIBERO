# Python script to read a dictionary from a file and return a list of keys

def extract_keys(file_path):
    """
    Reads a dictionary from the specified file, extracts its keys, 
    and returns them as a list.

    :param file_path: Path to the file containing the dictionary
    :return: List of keys from the dictionary
    """
    try:
        with open(file_path, 'r') as file:
            # Read the file content and evaluate it as a dictionary
            data = eval(file.read())

            # Ensure the content is a dictionary
            if not isinstance(data, dict):
                raise ValueError("The file does not contain a valid dictionary.")

            # Extract the keys as a list
            ALL_SYMBOLS = list(data.keys())

            return ALL_SYMBOLS
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Example usage
if __name__ == "__main__":
    file_path = "LIBERO/Spatial-action_detector.txt"  # Replace with your file path

    # Extract keys from the file
    keys = extract_keys(file_path)

    # Print the result
    print("ALL_SYMBOLS =", keys)
