import os
import sys
import random
import string
from pathlib import Path

def random_filename():
    """Generate a random filename."""
    letters = ''.join(random.choices(string.ascii_lowercase, k=8))
    extensions = ['.txt', '.log', '.json', '.py', '.csv']
    return letters + random.choice(extensions)

def random_content(size_kb):
    """Generate random text content of approx size."""
    size_bytes = int(size_kb * 1024)
    chars = string.ascii_letters + string.digits + ' \n'
    return ''.join(random.choices(chars, k=size_bytes))

def create_test_files(directory, file_count=15):
    """Create random test files in a directory."""
    target = Path(directory)
    target.mkdir(exist_ok=True)
    
    print(f"Creating {file_count} test files in {target}...")
    
    for i in range(file_count):
        # Random size between 1KB and 100KB
        size_kb = random.randint(1, 100)
        filename = random_filename()
        
        # Some files go in subfolders
        if random.choice([True, False]):
            subfolder = target / "subfolder"
            subfolder.mkdir(exist_ok=True)
            filepath = subfolder / filename
        else:
            filepath = target / filename
        
        content = random_content(size_kb)
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        print(f"  Created: {filepath.name} ({size_kb} KB)")
    
    print(f"Done! Check {target}")

if __name__ == '__main__':
    # Simple: just use command line or default
    if len(sys.argv) > 1:
        test_dir = sys.argv[1]
    else:
        test_dir = 'test_dir'
    
    create_test_files(test_dir)