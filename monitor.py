#!/usr/bin/env python3
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
        self.new_count = 0
    
    def _load_previous_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                return set(json.load(f))
        return set()
    
    def _save_current_state(self, files):
        with open(self.state_file, 'w') as f:
            json.dump(list(files), f)
    
    def _log_new_file(self, filepath, rel_path, max_width=60):
        size_kb = filepath.stat().st_size / 1024
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        if max_width > 0:
            padded_path = rel_path.ljust(max_width)
        else:
            padded_path = rel_path
        with open(self.log_file, 'a') as log:
            log.write(f"[{timestamp}] {padded_path} | {size_kb:.2f} KB\n")
        print(f"  NEW: {rel_path} ({size_kb:.2f} KB)")
        self.new_count += 1
    
    def _scan(self, directory, previous, current):
        for item in directory.iterdir():
            if item.is_file():
                rel_path = str(item.relative_to(self.directory))
                current.add(rel_path)
                if rel_path not in previous:
                    self._log_new_file(item, rel_path)
            elif item.is_dir():
                self._scan(item, previous, current)
    
    def scan(self):
        if not self.directory.exists():
            print(f"ERROR: Directory '{self.directory}' does not exist")
            return
        
        print(f"\nScanning: {self.directory}")
        print("-" * 40)
        
        previous = self._load_previous_state()
        current = set()
        
        self._scan(self.directory, previous, current)
        self._save_current_state(current)
        
        print("-" * 40)
        if self.new_count == 0:
            print("No new files found.")
        else:
            print(f"Total: {self.new_count} new file(s)")
        print("")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("USAGE: python monitor.py <directory>")
        sys.exit(1)
    
    monitor = DirectoryMonitor(sys.argv[1])
    monitor.scan()