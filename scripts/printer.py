import os
import fnmatch
import sys

def find_files(patterns, root, max_depth):
    for path, dirs, files in os.walk(root):
        # Calculate the current depth
        current_depth = path[len(root):].count(os.sep)
        if current_depth >= max_depth:
            # If the current depth exceeds max_depth, don't go deeper
            dirs[:] = []
        
        for filename in files:
            if any(fnmatch.fnmatch(filename, pattern) for pattern in patterns):
                file_path = os.path.join(path, filename)
                print(file_path)
                try:
                    with open(file_path, 'r') as f:
                        print(f.read())
                except (OSError, IOError) as e:
                    print(f"Error reading {file_path}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python printer.py <root_directory> <max_depth> <pattern1> <pattern2> ... <patternN>")
        sys.exit(1)
    
    root_directory = sys.argv[1]
    max_depth = int(sys.argv[2])
    patterns = sys.argv[3:]
    
    find_files(patterns, root_directory, max_depth)