import os
import requests
from zipfile import ZipFile
import time
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from pyunpack import Archive
from tqdm import tqdm

# Define the destination options with custom names and paths
destination_options = {
    'genesis': r'G:\roms\gen',
    'gba': r'G:\roms\gba',
    'nds': r'G:\roms\nds',
    'nes': r'G:\roms\nes',
    'snes': r'G:\roms\snes',
    'gb': r'G:\roms\gb',
    'dsiware': r'G:\roms\dsiware',
    'sms': r'G:\roms\sms',
    'other': None
}

# Prompt user for the choice: link or file
choice = input("Enter 'link' or 'file':")

if choice == 'link':
    zip_link = input("Enter the link to the .zip file: ")

    # Download the .zip file
    response = requests.get(zip_link)

    # Save the .zip file to a temporary directory
    file_name = zip_link.split("/")[-1]
    temp_dir = os.path.join(os.getcwd(), 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    zip_file_path = os.path.join(temp_dir, file_name)
    with open(zip_file_path, "wb") as file:
        file.write(response.content)
elif choice == 'file':
    # Open a file dialog to select the .zip file
    root = Tk()
    root.withdraw()
    zip_file_path = askopenfilename(title="Select .zip file", filetypes=[("ZIP Files", "*.zip")])
    root.attributes('-topmost', True)
    root.attributes('-topmost', False)
    root.destroy()

# Prompt user for the destination option
print("Choose a destination option:")
for key, value in destination_options.items():
    print(f"{key}: {value}")

option = input("Enter the destination option: ")

# Determine the destination directory based on the option
if option == 'other':
    destination_dir = input("Enter the destination directory: ")
else:
    destination_dir = destination_options.get(option)

if destination_dir is None:
    print("Invalid destination option!")
    time.sleep(5)
    exit(1)

# Extract the .zip file to a temporary directory
temp_extract_dir = os.path.join(destination_dir, 'temp_extract')
os.makedirs(temp_extract_dir, exist_ok=True)
with ZipFile(zip_file_path, "r") as zip_ref:
    zip_ref.extractall(temp_extract_dir)

# Move the extracted files to the destination directory
extracted_files = os.listdir(temp_extract_dir)
total_files = len(extracted_files)
with tqdm(total=total_files, desc='Extracting files', unit='file') as pbar:
    for extracted_file in extracted_files:
        extracted_file_path = os.path.join(temp_extract_dir, extracted_file)
        if extracted_file.endswith('.bin'):
            # Move .bin file to the destination directory without renaming
            new_file_path = os.path.join(destination_dir, extracted_file)
            os.rename(extracted_file_path, new_file_path)
        else:
            # Rename files with .gen extension if Genesis option is chosen
            if option == 'genesis':
                new_file_path = os.path.join(destination_dir, os.path.splitext(extracted_file)[0] + '.gen')
                os.rename(extracted_file_path, new_file_path)
            else:
                new_file_path = os.path.join(destination_dir, extracted_file)
                os.rename(extracted_file_path, new_file_path)
        pbar.update(1)

# Remove the temporary extraction directory
for file in os.listdir(temp_extract_dir):
    file_path = os.path.join(temp_extract_dir, file)
    if os.path.isfile(file_path):
        os.remove(file_path)
os.rmdir(temp_extract_dir)

# Remove the temporary directory
if os.path.exists(temp_dir) and os.path.isdir(temp_dir):
    for file in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
    os.rmdir(temp_dir)
    
    time.sleep(2.5)

# Remove the .zip file
os.remove(zip_file_path)

time.sleep(2.5)

# Wait for 5 seconds before closing the terminal
time.sleep(5)
