import os

# Define the relative path from the current working directory
target_folder = "QCImages"
target_file = "QCRef.jpg"
image_path = os.path.join(target_folder, target_file)

# Check if the file exists
if os.path.isfile(image_path):
    print(f"Image found at: {os.path.abspath(image_path)}")
else:
    print("Image not found.")
