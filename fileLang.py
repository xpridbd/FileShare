import sys
import os 
from pathlib import Path
import subprocess

def get_highest_numbered_file(directory_path):    
    folder = Path(directory_path)
    files = folder.glob('*.txt')
    numbers = []
    
    for file in files:
        try:
            number = int(file.stem)
            numbers.append(number)
        
        except ValueError:
            continue
            
    if not numbers:
        return 0, None
        
    max_number = max(numbers)
    file_count = len(numbers)
    highest_file = f"{max_number}.txt"
    
    return file_count, highest_file

if len(sys.argv) < 2:
    print("Usage: python compiler.py <dirName to compile>")
    sys.exit(1)

args = sys.argv
directory_to_process = args[1]

count, largest_file = get_highest_numbered_file(directory_to_process)

fileIndex = 1
temp_script_lines = []

while fileIndex <= count:
    file_path = os.path.join(directory_to_process, f"{fileIndex}.txt")
    
    try:
        with open(file_path, 'r') as file:
            firstLine = file.readline().strip()
            secondLine = file.readline().strip()
            
            if firstLine:
                temp_script_lines.append(firstLine)
                
            if secondLine == "# END JOIN":
                break
            
    except IOError as e:
        print(f"Error reading file {file_path}: {e}")
        break 
        
    fileIndex += 1

temp_script_path = 'temp.py'

try:
    with open(temp_script_path, 'w') as file:
        for line in temp_script_lines:
            file.write(line + "\n")
    print(f"Created temporary script: {temp_script_path}")
            
except IOError as e:
    print(f"Error writing to temporary file: {e}")
    sys.exit(1)

print(f"Running {temp_script_path}...")

try:
    result = subprocess.run(['python', temp_script_path], capture_output=True, text=True, check=True)
    print("--- Output of temp.py ---")
    print(result.stdout)
    print("-------------------------")
except subprocess.CalledProcessError as e:
    print(f"Error running temp.py: {e.stderr}")
except FileNotFoundError:
    print(f"Python interpreter not found. Make sure 'python' is in your PATH.")

try:
    os.remove(temp_script_path)
    print(f"Cleaned up {temp_script_path}")
except OSError as e:
    print(f"Error removing temporary file: {e}")0