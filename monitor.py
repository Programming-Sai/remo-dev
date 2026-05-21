import os
import sys
import json
import time
from pathlib import Path

class DirectoryMonitor:
    def __init__(self, directory, state_file='.monitor_state.json', log_file='log.txt'):
        self.directory = Path(directory)
        self.state_file = state_file
        self.log_file = log_file
    
    def _load_previous_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                return set(json.load(f))
        return set()
    
    def _save_current_state(self, files):
        with open(self.state_file, 'w') as f:
            json.dump(list(files), f)
    
    def _log_new_file(self, filepath):
        size_kb = filepath.stat().st_size / 1024
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        with open(self.log_file, 'a') as log:
            log.write(f"[{timestamp}] {filepath.name} | {size_kb:.2f} KB\n")
        print(f"NEW: file detected: {filepath.name}")
    
    def scan(self):
        if not self.directory.exists():
            print(f"ERROR: Directory '{self.directory}' does not exist")
            return
        
        previous = self._load_previous_state()
        current = set()
        
        for item in self.directory.iterdir():
            if item.is_file():
                current.add(item.name)
                if item.name not in previous:
                    self._log_new_file(item)
        
        self._save_current_state(current)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("USAGE: python monitor.py <directory>")
        sys.exit(1)
    
    monitor = DirectoryMonitor(sys.argv[1])
    monitor.scan()