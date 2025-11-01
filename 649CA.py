"""
Convert a_649.txt to JSON format for the lottery analyzer app

Input format:  YYMMDD: , n1, n2, n3, n4, n5, n6,  bonus
Example:       251025: ,  6,  9, 13, 21, 24, 38,   5

Output: JSON file compatible with the lottery analyzer HTML app

Usage:
python txt_to_json_converter.py
"""

import json
import re
from datetime import datetime

def parse_txt_line(line):
    """
    Parse a line in format: YYMMDD: , n1, n2, n3, n4, n5, n6,  bonus
    """
    line = line.strip()
    
    # Skip empty lines and comments
    if not line or line.startswith('#'):
        return None
    
    try:
        # Split by colon to get date and numbers
        parts = line.split(':')
        if len(parts) != 2:
            return None
        
        date_str = parts[0].strip()
        numbers_str = parts[1].strip()
        
        # Parse date from YYMMDD to YYYY-MM-DD
        if len(date_str) == 6:
            yy = date_str[0:2]
            mm = date_str[2:4]
            dd = date_str[4:6]
            
            # Convert YY to YYYY (assume 2000s for 00-99)
            year = '20' + yy if int(yy) < 50 else '19' + yy
            formatted_date = f"{year}-{mm}-{dd}"
        else:
            return None
        
        # Extract all numbers (remove commas and extra spaces)
        numbers_str = numbers_str.replace(',', ' ')
        numbers = [int(x) for x in numbers_str.split() if x.strip().isdigit()]
        
        if len(numbers) != 7:
            print(f"Warning: Expected 7 numbers, got {len(numbers)} in line: {line}")
            return None
        
        # Split into main numbers and bonus
        main_numbers = numbers[:6]
        bonus = numbers[6]
        
        # Calculate holes (gaps in sequence)
        sorted_nums = sorted(main_numbers)
        holes = 0
        for i in range(1, len(sorted_nums)):
            if sorted_nums[i] - sorted_nums[i-1] > 2:
                holes += 1
        
        # Calculate odd count
        odd_count = sum(1 for n in main_numbers if n % 2 == 1)
        
        return {
            'date': formatted_date,
            'numbers': main_numbers,
            'bonus': bonus,
            'holes': holes,
            'odd': odd_count
        }
        
    except Exception as e:
        print(f"Error parsing line: {line} - {e}")
        return None

def convert_txt_to_json(input_file='a_649.txt', output_file='lottery_data.json'):
    """
    Convert text file to JSON format
    """
    draws = []
    total_lines = 0
    skipped_lines = 0
    
    print(f"Reading from: {input_file}")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        total_lines = len(lines)
        print(f"Total lines: {total_lines}")
        print("\nProcessing...")
        
        for i, line in enumerate(lines, 1):
            draw = parse_txt_line(line)
            
            if draw:
                draws.append(draw)
            else:
                if line.strip() and not line.strip().startswith('#'):
                    skipped_lines += 1
            
            # Progress indicator
            if i % 500 == 0:
                print(f"Processed {i} lines...")
        
        # Sort by date
        draws.sort(key=lambda x: x['date'])
        
        # Create JSON structure
        output_data = {
            'draws': draws,
            'generated': []  # Empty generated combinations
        }
        
        # Write JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"\n{'='*60}")
        print(f"CONVERSION COMPLETE")
        print(f"{'='*60}")
        print(f"Total lines processed: {total_lines}")
        print(f"Successfully converted: {len(draws)}")
        print(f"Skipped lines: {skipped_lines}")
        print(f"\nOutput saved to: {output_file}")
        print(f"{'='*60}")
        
        # Show sample
        if draws:
            print(f"\nSample data (first 3 draws):")
            print("-" * 60)
            for draw in draws[:3]:
                nums = ', '.join(str(n) for n in draw['numbers'])
                print(f"{draw['date']}: {nums} / {draw['bonus']} [H:{draw['holes']} O:{draw['odd']}]")
            print("-" * 60)
            
            print(f"\nLast 3 draws:")
            print("-" * 60)
            for draw in draws[-3:]:
                nums = ', '.join(str(n) for n in draw['numbers'])
                print(f"{draw['date']}: {nums} / {draw['bonus']} [H:{draw['holes']} O:{draw['odd']}]")
            print("-" * 60)
        
        print(f"\n✅ You can now import '{output_file}' into the HTML lottery analyzer!")
        return True
        
    except FileNotFoundError:
        print(f"ERROR: Input file '{input_file}' not found!")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def main():
    print("="*60)
    print("Text to JSON Converter for Lottery Analyzer")
    print("="*60)
    print("\nConverts a_649.txt to JSON format for the HTML app")
    print("="*60)
    print()
    
    # Get filenames
    input_file = input("Enter input filename [a_649.txt]: ").strip()
    if not input_file:
        input_file = 'a_649.txt'
    
    output_file = input("Enter output filename [lottery_data.json]: ").strip()
    if not output_file:
        output_file = 'lottery_data.json'
    
    print()
    
    # Convert
    success = convert_txt_to_json(input_file, output_file)
    
    if success:
        print("\n" + "="*60)
        print("HOW TO IMPORT INTO HTML APP:")
        print("="*60)
        print("1. Open the lottery HTML file in your browser")
        print("2. Click the 'Import Data' button")
        print(f"3. Select '{output_file}'")
        print("4. Your 5000 draws will be loaded!")
        print("="*60)

if __name__ == "__main__":
    main()