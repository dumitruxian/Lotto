"""
Text to JSON Converter for Lottery Draws
Converts a_649.txt format to JSON for the HTML lottery analyzer

Usage:
python txt_to_json_converter.py input.txt output.json

Format expected:
YYMMDD:  n1, n2, n3, n4, n5, n6 / bonus
"""

import json
import sys
import re
from datetime import datetime

def parse_draw_line(line):
    """Parse a single draw line"""
    line = line.strip()
    
    # Skip comments and empty lines
    if not line or line.startswith('#'):
        return None
    
    # Parse format: YYMMDD:  n1, n2, n3, n4, n5, n6 / bonus
    if ':' not in line:
        return None
    
    try:
        parts = line.split(':')
        date_str = parts[0].strip()
        
        # Convert YYMMDD to YYYY-MM-DD
        if len(date_str) == 6:
            year = '20' + date_str[:2]
            month = date_str[2:4]
            day = date_str[4:6]
            full_date = f"{year}-{month}-{day}"
        else:
            return None
        
        # Split numbers and bonus
        nums_part = parts[1].split('/')
        if len(nums_part) != 2:
            return None
        
        # Extract numbers
        numbers = []
        for num_str in nums_part[0].split(','):
            num_str = num_str.strip()
            if num_str.isdigit():
                num = int(num_str)
                if 1 <= num <= 49:
                    numbers.append(num)
        
        # Extract bonus
        bonus_str = nums_part[1].strip()
        if not bonus_str.isdigit():
            return None
        bonus = int(bonus_str)
        
        if len(numbers) != 6 or bonus < 1 or bonus > 49:
            return None
        
        # Calculate holes
        sorted_nums = sorted(numbers)
        holes = 0
        for i in range(1, len(sorted_nums)):
            if sorted_nums[i] - sorted_nums[i-1] > 2:
                holes += 1
        
        # Calculate odd count
        odd = sum(1 for n in numbers if n % 2 == 1)
        
        return {
            'date': full_date,
            'numbers': numbers,
            'bonus': bonus,
            'holes': holes,
            'odd': odd
        }
        
    except Exception as e:
        print(f"Warning: Could not parse line: {line} ({e})")
        return None

def convert_txt_to_json(input_file, output_file):
    """Convert text file to JSON"""
    draws = []
    skipped = 0
    
    print(f"Reading from: {input_file}")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                draw = parse_draw_line(line)
                if draw:
                    draws.append(draw)
                elif line.strip() and not line.strip().startswith('#'):
                    skipped += 1
                
                if line_num % 500 == 0:
                    print(f"Processed {line_num} lines...")
        
        # Sort by date
        draws.sort(key=lambda x: x['date'])
        
        # Create output structure
        output_data = {
            'draws': draws,
            'generated': []
        }
        
        # Write JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"\n{'='*60}")
        print("CONVERSION COMPLETE")
        print(f"{'='*60}")
        print(f"Total draws converted: {len(draws)}")
        print(f"Skipped lines: {skipped}")
        print(f"Output saved to: {output_file}")
        print(f"{'='*60}")
        
        # Show sample
        if draws:
            print(f"\nSample (first 5 draws):")
            print("-" * 60)
            for draw in draws[:5]:
                nums_str = ', '.join(f'{n:2d}' for n in draw['numbers'])
                print(f"{draw['date']}: {nums_str} / {draw['bonus']:2d}")
            print("-" * 60)
        
        return True
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found!")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    print("="*60)
    print("Text to JSON Converter for Lottery Draws")
    print("="*60)
    print()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python txt_to_json_converter.py <input.txt> [output.json]")
        print()
        print("Examples:")
        print("  python txt_to_json_converter.py a_649.txt")
        print("  python txt_to_json_converter.py a_649.txt lottery_data.json")
        print()
        print("Input format expected:")
        print("  YYMMDD:  n1, n2, n3, n4, n5, n6 / bonus")
        print("  Example: 251025:  6,  8, 19, 39, 43, 49 / 46")
        print("="*60)
        sys.exit(0)
    
    input_file = sys.argv[1]
    
    # Default output filename
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        # Create output name from input name
        if input_file.endswith('.txt'):
            output_file = input_file.replace('.txt', '.json')
        else:
            output_file = input_file + '.json'
    
    print(f"Input file:  {input_file}")
    print(f"Output file: {output_file}")
    print("="*60)
    print()
    
    success = convert_txt_to_json(input_file, output_file)
    
    if success:
        print(f"\n✅ Success! You can now import '{output_file}' into the HTML lottery analyzer.")
    else:
        print("\n❌ Conversion failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()