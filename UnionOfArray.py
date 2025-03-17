# Function to find the union of two arrays of strings
def union_of_arrays(arr1, arr2):
    # Convert both arrays to sets and find their union
    #return list(set(arr1) | set(arr2))
    return sorted(list(set(arr1) | set(arr2)))

# Function to read an array of strings from a file and return them as a list
def read_array_from_file(file_name):
    with open(file_name, 'r') as file:
        # Read the content, split by commas, and return it as a list of strings
        return file.read().strip().split(',')

# Read arrays from files
arr1 = read_array_from_file('/path/array3.txt')  # Replace with the correct file path
arr2 = read_array_from_file('/path/array4.txt')  # Replace with the correct file path

# Get the union of the two arrays
result = union_of_arrays(arr1, arr2)

# Print the resulting array
print("Union of the two arrays without duplicates:", result)
