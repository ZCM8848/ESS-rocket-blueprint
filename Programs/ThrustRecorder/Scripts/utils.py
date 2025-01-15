import os
import glob
import csv

def find_png_images(directory):
    png_files = glob.glob(os.path.join(directory, '**', '*.png'), recursive=True)
    return png_files

def to_csv(dictionary, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(['time', 'thrust'])

        for key, value in dictionary.items():
            writer.writerow([key, value])
    
    return None

def sort_dict_by_keys(input_dict):
    sorted_keys = sorted(input_dict.keys())
    
    sorted_dict = {key: input_dict[key] for key in sorted_keys}
    
    return sorted_dict