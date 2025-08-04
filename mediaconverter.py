import os
import re
import subprocess
import sys  # for command line arguments

def numerical_sort(value):
    numbers = re.compile(r'(\d+)')
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

# Check if an output filename was provided
if len(sys.argv) < 2:
    print("Usage: python script.py output_filename.mp4")
    sys.exit(1)

output_filename = sys.argv[1]

root_dirs_files = [(root, dirs, files) for root, dirs, files in os.walk("./")]

# Sort directories by last part of the path (the actual directory name)
root_dirs_files.sort(key=lambda x: numerical_sort(x[0].split('/')[-1]))

# Create inputFileList.txt in write mode, which is deleted at the end
with open("inputFileList.txt", "w") as f:
    for root, dirs, files in root_dirs_files:
        for file in sorted(files, key=numerical_sort):
            if file.endswith(".media"):
                f.write(f"file '{os.path.join(root, file)}'\n")

# Call ffmpeg command
subprocess.run(["ffmpeg", "-f", "concat", "-safe", "0", "-i", "inputFileList.txt", output_filename])

# Remove inputFileList.txt if it exists
if os.path.exists("inputFileList.txt"):
    os.remove("inputFileList.txt")