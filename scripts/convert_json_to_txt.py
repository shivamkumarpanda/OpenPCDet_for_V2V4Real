import os
import json
import shutil
import argparse
import sys
import pudb

def get_next_filename(directory, extension):
    existing_files = [f for f in os.listdir(directory) if f.endswith(extension)]
    if not existing_files:
        return "000001"
    existing_files.sort()
    last_file = existing_files[-1]
    last_number = int(os.path.splitext(last_file)[0])
    next_number = last_number + 1
    return f"{next_number:06d}"

def map_classes(category_name):
    class_mapping = {
        'Car': 'Car',
        'Truck': 'Car',
        'Van': 'Car',
        'Pedestrian': 'Pedestrian',
        'Cyclist': 'Cyclist',
    }
    return class_mapping.get(category_name, 'Misc')

def convert_json_to_txt(json_source_directory, pcd_source_directory, txt_target_directory, pcd_target_directory):
    # List all json files in the directory
    json_files = [f for f in os.listdir(json_source_directory) if f.endswith('.json')]
    json_files.sort()

    for json_file in json_files:
        next_filename = get_next_filename(txt_target_directory, '.txt')
        json_path = os.path.join(json_source_directory, json_file)
        txt_path = os.path.join(txt_target_directory, next_filename + '.txt')
        
        pcd_file = os.path.splitext(json_file)[0] + '.bin'
        pcd_source_path = os.path.join(pcd_source_directory, pcd_file)
        pcd_target_path = os.path.join(pcd_target_directory, next_filename + '.bin')

        if not os.path.exists(pcd_source_path):
            print(f"Error: {pcd_file} does not exist in {pcd_source_directory}.")
            continue

        # Read the JSON file
        with open(json_path, 'r') as f:
            data = json.load(f)

        # Write to the TXT file
        with open(txt_path, 'w') as f:
            for obj in data:
                x = obj['psr']['position']['x']
                y = obj['psr']['position']['y']
                z = obj['psr']['position']['z']
                dx = obj['psr']['scale']['x']
                dy = obj['psr']['scale']['y']
                dz = obj['psr']['scale']['z']
                yaw = obj['psr']['rotation']['z']
                category_name = map_classes(obj['obj_type'])

                line = f"{x} {y} {z} {dx} {dy} {dz} {yaw} {category_name}\n"
                f.write(line)
        
        # Copy the PCD file to the target directory with the new filename
        shutil.copy2(pcd_source_path, pcd_target_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert JSON to TXT and copy corresponding PCD files.')
    parser.add_argument('-s', '--source_directory', type=str, required=True, help='Source directory containing the car directories')
    parser.add_argument('-c', '--car', type=str, choices=['tesla', 'astuff'], default= 'tesla', help='Car type (tesla or astuff)')
    parser.add_argument('-t', '--txt_target_directory', type=str, help='Directory to save converted TXT files', default='../data/v2v4real/labels/')
    parser.add_argument('-p', '--pcd_target_directory', type=str, help='Directory to save copied PCD files', default='../data/v2v4real/points/')

    args = parser.parse_args()

    if args.car not in ['tesla', 'astuff']:
        print(f"Error: {args.car} is not a valid car type.")
        sys.exit(1)

    json_source_directory = os.path.join(args.source_directory, args.car, 'label_kitti')
    pcd_source_directory = os.path.join(args.source_directory, args.car, 'lidar')
    txt_target_directory = args.txt_target_directory
    pcd_target_directory = args.pcd_target_directory

    for directory in [json_source_directory, pcd_source_directory, txt_target_directory, pcd_target_directory]:
        if not os.path.isdir(directory):
            print(f"Error: {directory} is not a valid directory.")
            sys.exit(1)

    convert_json_to_txt(json_source_directory, pcd_source_directory, txt_target_directory, pcd_target_directory)
