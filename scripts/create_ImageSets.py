import os
import random

# Define the data_root directory
data_root = "../data/v2v4real/"

# Paths to the relevant directories
imagesets_dir = os.path.join(data_root, "ImageSets")
training_dir = os.path.join(data_root, "points")

# Ensure ImageSets directory exists
os.makedirs(imagesets_dir, exist_ok=True)

# Get the list of file names (without extensions) in the training and testing directories
training_files = [os.path.splitext(f)[0] for f in os.listdir(training_dir) if os.path.isfile(os.path.join(training_dir, f))]

# Shuffle the training files for random splitting
random.shuffle(training_files)

# 80-20 split for training and validation
split_index = int(0.8 * len(training_files))
train_files = training_files[:split_index]
val_files = training_files[split_index:]

# Create the ImageSets files and write the file names
def write_files(file_list, file_path):
    with open(file_path, 'w') as f:
        for file_name in file_list:
            f.write(file_name + '\n')

# Paths to the text files under ImageSets
train_txt = os.path.join(imagesets_dir, "train.txt")
val_txt = os.path.join(imagesets_dir, "val.txt")

# Write the files
write_files(train_files, train_txt)
write_files(val_files, val_txt)

print("Files have been successfully created in the ImageSets directory.")
