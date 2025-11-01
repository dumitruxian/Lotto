"""
Lottery File Manager
Monitors Downloads folder and automatically updates files in your lottery folder

This script:
1. Watches your Downloads folder for lottery-data.json
2. Automatically moves it to your lottery folder
3. Updates a_649.txt when new draws are added
4. Keeps everything synchronized

Usage:
python lottery_file_manager.py <lottery_folder_path>

Example:
python lottery_file_manager.py C:\LotteryAnalyzer
"""

import os
import sys
import json
import time
import shutil
from pathlib import Path
from datetime import datetime

class LotteryFileManager:
    def __init__(self, lottery_folder):
        self.lottery_folder = Path(lottery_folder)
        self.downloads_folder = Path.home() / "Downloads"
        self.json_new = self.lottery_folder / "lottery-data-new.json"
        self.json_old = self.lottery_folder / "lottery-data-old.json"
        self.txt_file = self.lottery_folder / "a_649.txt"
        
        # Ensure folders exist
        self.lottery_folder.mkdir(parents=True, exist_ok=True)
        
        print(f"Lottery folder: {self.lottery_folder}")
        print(f"Downloads folder: {self.downloads_folder}")
        print(f"JSON new file: {self.json_new}")
        print(f"JSON old file: {self.json_old}")
        print(f"TXT file: {self.txt_file}")
    
    def watch_downloads(self, interval=2):
        """Watch Downloads folder for lottery-data.json"""
        print(f"\n{'='*60}")
        print("Watching Downloads folder for lottery-data.json")
        print("Press Ctrl+C to stop")
        print(f"{'='*60}\n")
        
        last_processed = None
        
        try:
            while True:
                download_json = self.downloads_folder / "lottery-data.json"
                
                if download_json.exists():
                    # Check if it's a new file (different modification time)
                    mod_time = download_json.stat().st_mtime
                    
                    if mod_time != last_processed:
                        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Found lottery-data.json in Downloads!")
                        time.sleep(0.5)  # Wait for file to finish writing
                        
                        if self.process_downloaded_file(download_json):
                            last_processed = mod_time
                            print("✅ File processed successfully\n")
                        else:
                            print("❌ Failed to process file\n")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\nStopped watching.")
    
    def process_downloaded_file(self, download_json):
        """Process downloaded lottery-data.json with rotation strategy"""
        try:
            # Read the downloaded file
            with open(download_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'draws' not in data:
                print("Error: Invalid JSON format (no 'draws' field)")
                return False
            
            # Rotation strategy:
            # 1. If lottery-data-new.json exists, rename it to lottery-data-old.json
            # 2. Move downloaded file to lottery-data-new.json
            
            if self.json_new.exists():
                print(f"Rotating: {self.json_new.name} → {self.json_old.name}")
                if self.json_old.exists():
                    self.json_old.unlink()  # Delete old backup
                self.json_new.rename(self.json_old)
            
            # Move downloaded file to lottery-data-new.json
            print(f"Moving to: {self.json_new}")
            shutil.move(str(download_json), str(self.json_new))
            
            # Update a_649.txt
            self.update_txt_file(data['draws'])
            
            print(f"\n📁 Files in folder:")
            if self.json_new.exists():
                print(f"   ✅ {self.json_new.name} (current)")
            if self.json_old.exists():
                print(f"   ✅ {self.json_old.name} (backup)")
            if self.txt_file.exists():
                print(f"   ✅ {self.txt_file.name} (text format)")
            
            return True
            
        except Exception as e:
            print(f"Error processing file: {e}")
            return False
    
    def update_txt_file(self, draws):
        """Update a_649.txt with current draws"""
        print(f"Updating: {self.txt_file}")
        
        try:
            # Sort draws by date
            draws_sorted = sorted(draws, key=lambda x: x['date'])
            
            # Write to file
            with open(self.txt_file, 'w', encoding='utf-8') as f:
                f.write("# Lottery Draw History - 6/49\n")
                f.write(f"# Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("# Format: YYMMDD:  N1, N2, N3, N4, N5, N6 / Bonus\n")
                f.write("#\n")
                
                for draw in draws_sorted:
                    # Convert date to YYMMDD format
                    date_obj = datetime.strptime(draw['date'], '%Y-%m-%d')
                    date_str = date_obj.strftime('%y%m%d')
                    
                    # Format numbers
                    nums_str = ', '.join(f"{n:2d}" for n in draw['numbers'])
                    bonus_str = f"{draw['bonus']:2d}"
                    
                    f.write(f"{date_str}:  {nums_str} / {bonus_str}\n")
            
            print(f"✅ Updated {self.txt_file} with {len(draws_sorted)} draws")
            return True
            
        except Exception as e:
            print(f"Error updating TXT file: {e}")
            return False
    
    def sync_now(self):
        """Manually sync lottery-data-new.json to a_649.txt"""
        if not self.json_new.exists():
            print(f"Error: {self.json_new} not found")
            print("\nAvailable files:")
            if self.json_old.exists():
                print(f"  - {self.json_old.name} (backup)")
            return False
        
        try:
            with open(self.json_new, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'draws' in data:
                self.update_txt_file(data['draws'])
                return True
            else:
                print("Error: Invalid JSON format")
                return False
                
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def list_files(self):
        """List all lottery files in folder"""
        print(f"\n{'='*60}")
        print(f"Files in {self.lottery_folder}:")
        print(f"{'='*60}")
        
        files_info = []
        
        if self.json_new.exists():
            size = self.json_new.stat().st_size
            mod_time = datetime.fromtimestamp(self.json_new.stat().st_mtime)
            files_info.append(f"✅ {self.json_new.name:25s} {size:>10,} bytes  {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            files_info.append(f"❌ {self.json_new.name:25s} (not found)")
        
        if self.json_old.exists():
            size = self.json_old.stat().st_size
            mod_time = datetime.fromtimestamp(self.json_old.stat().st_mtime)
            files_info.append(f"✅ {self.json_old.name:25s} {size:>10,} bytes  {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            files_info.append(f"❌ {self.json_old.name:25s} (not found)")
        
        if self.txt_file.exists():
            size = self.txt_file.stat().st_size
            mod_time = datetime.fromtimestamp(self.txt_file.stat().st_mtime)
            files_info.append(f"✅ {self.txt_file.name:25s} {size:>10,} bytes  {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            files_info.append(f"❌ {self.txt_file.name:25s} (not found)")
        
        for info in files_info:
            print(info)
        
        print(f"{'='*60}\n")

def main():
    print("="*60)
    print("Lottery File Manager")
    print("="*60)
    print()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python lottery_file_manager.py <lottery_folder>")
        print()
        print("Examples:")
        print("  python lottery_file_manager.py C:\\LotteryAnalyzer")
        print("  python lottery_file_manager.py .")
        print()
        print("What it does:")
        print("  1. Watches Downloads folder for lottery-data.json")
        print("  2. Moves it to your lottery folder")
        print("  3. Updates a_649.txt automatically")
        print("  4. Keeps everything synchronized")
        print()
        print("Run this script and keep it running while using the HTML app!")
        print("="*60)
        sys.exit(0)
    
    lottery_folder = sys.argv[1]
    
    if not os.path.exists(lottery_folder):
        print(f"Creating folder: {lottery_folder}")
        os.makedirs(lottery_folder, exist_ok=True)
    
    manager = LotteryFileManager(lottery_folder)
    
    # Check if we should sync now
    print("\nOptions:")
    print("1. Watch Downloads folder (auto-sync)")
    print("2. Sync now (lottery-data-new.json → a_649.txt)")
    print("3. List files")
    print()
    choice = input("Choose option (1, 2, or 3): ").strip()
    
    if choice == "2":
        print("\nSyncing files...")
        if manager.sync_now():
            print("✅ Sync complete!")
        else:
            print("❌ Sync failed")
    elif choice == "3":
        manager.list_files()
    else:
        manager.watch_downloads()

if __name__ == "__main__":
    main()