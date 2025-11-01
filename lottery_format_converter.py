"""
Lottery Draw Format Converter
Converts from: "DDth Month YYYY n1 n2 n3 n4 n5 n6 n7"
To: "YYMMDD : n1, n2, n3, n4, n5, n6 / n7"

Usage:
python lottery_format_converter.py
"""

import re
from datetime import datetime

def parse_ordinal_date(date_str):
    """
    Parse date string like "25th October 2025" to datetime object
    """
    # Remove ordinal suffixes (st, nd, rd, th)
    cleaned = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)
    
    # Parse the cleaned date
    try:
        dt = datetime.strptime(cleaned, '%d %B %Y')
        return dt
    except ValueError:
        # Try abbreviated month format
        try:
            dt = datetime.strptime(cleaned, '%d %b %Y')
            return dt
        except ValueError:
            return None

def convert_line(line):
    """
    Convert a single line from old format to new format
    """
    line = line.strip()
    
    if not line or line.startswith('#'):
        return None
    
    # Split by tab first
    if '\t' in line:
        parts = line.split('\t')
        # Remove empty parts
        parts = [p.strip() for p in parts if p.strip()]
        
        # First part should be the date, rest are numbers
        if len(parts) < 8:  # Need date + 7 numbers
            return None
        
        # Date is the first part, split it by spaces
        date_parts = parts[0].split()
        if len(date_parts) != 3:
            return None
        
        date_str = ' '.join(date_parts)
        numbers_parts = parts[1:]  # Rest are the 7 numbers
    else:
        # Split by spaces
        parts = line.split()
        parts = [p.strip() for p in parts if p.strip()]
        
        if len(parts) < 10:  # Need at least date (3 parts) + 7 numbers
            return None
        
        date_str = ' '.join(parts[:3])
        numbers_parts = parts[3:]
    
    dt = parse_ordinal_date(date_str)
    
    if not dt:
        print(f"Warning: Could not parse date: {date_str}")
        return None
    
    # Format date as YYMMDD
    formatted_date = dt.strftime('%y%m%d')
    
    # Extract numbers
    try:
        numbers = [int(n) for n in numbers_parts]
        
        if len(numbers) != 7:
            print(f"Warning: Expected 7 numbers, got {len(numbers)}: {line}")
            return None
        
        # Format: first 6 numbers, then bonus with /
        main_numbers = ', '.join(f'{n:2d}' for n in numbers[:6])
        bonus = f'{numbers[6]:2d}'
        
        # Create output line in the exact format required
        output = f"{formatted_date}:  {main_numbers} / {bonus}"
        return output
        
    except (ValueError, IndexError) as e:
        print(f"Warning: Error parsing numbers in line: {line}")
        return None

def convert_file(input_filename='649CA.txt', output_filename='a_649.txt'):
    """
    Convert entire file from old format to new format
    """
    converted_lines = []
    skipped_lines = 0
    
    print(f"Reading from: {input_filename}")
    
    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print(f"Total lines to process: {len(lines)}")
        print("\nProcessing...")
        
        for i, line in enumerate(lines, 1):
            converted = convert_line(line)
            
            if converted:
                converted_lines.append(converted)
            else:
                if line.strip() and not line.strip().startswith('#'):
                    skipped_lines += 1
            
            # Progress indicator
            if i % 100 == 0:
                print(f"Processed {i} lines...")
        
        # Write output file
        with open(output_filename, 'w', encoding='utf-8') as f:
            # Write header
            f.write("# Lottery Draw History - 6/49 Canada\n")
            f.write("# Format: YYMMDD:  N1, N2, N3, N4, N5, N6 / Bonus\n")
            f.write("#\n")
            
            # Write converted lines
            for line in converted_lines:
                f.write(line + '\n')
        
        print(f"\n{'='*60}")
        print(f"CONVERSION COMPLETE")
        print(f"{'='*60}")
        print(f"Total lines processed: {len(lines)}")
        print(f"Successfully converted: {len(converted_lines)}")
        print(f"Skipped lines: {skipped_lines}")
        print(f"\nOutput saved to: {output_filename}")
        print(f"{'='*60}")
        
        # Show sample of output
        if converted_lines:
            print(f"\nSample output (first 5 lines):")
            print("-" * 60)
            for line in converted_lines[:5]:
                print(line)
            print("-" * 60)
        
        return True
        
    except FileNotFoundError:
        print(f"ERROR: Input file '{input_filename}' not found!")
        print("\nPlease make sure the file exists in the same directory.")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_converter():
    """
    Test the converter with sample data
    """
    print("Testing converter with sample data...\n")
    
    test_lines = [
        "25th October 2025 6 9 13 21 24 38 5",
        "1st January 2024 1 5 12 18 29 42 7",
        "15th March 2023 3 8 14 25 33 47 11",
        "30th December 2022 2 11 19 28 36 44 9"
    ]
    
    print("Input format:")
    print("-" * 60)
    for line in test_lines:
        print(line)
    
    print("\nOutput format:")
    print("-" * 60)
    for line in test_lines:
        converted = convert_line(line)
        if converted:
            print(converted)
    print()

def main():
    print("="*60)
    print("Lottery Draw Format Converter")
    print("="*60)
    print("\nConverts from: DDth Month YYYY n1 n2 n3 n4 n5 n6 n7")
    print("To:            YYMMDD:  n1, n2, n3, n4, n5, n6 / n7")
    print("="*60)
    
    # Run test first
    test_converter()
    
    # Ask for filenames
    print("\n" + "="*60)
    input_file = input("Enter input filename [649CA.txt]: ").strip()
    if not input_file:
        input_file = '649CA.txt'
    
    output_file = input("Enter output filename [a_649.txt]: ").strip()
    if not output_file:
        output_file = 'a_649.txt'
    
    print()
    
    # Convert the file
    success = convert_file(input_file, output_file)
    
    if success:
        print("\n✅ Conversion successful!")
        print(f"You can now import '{output_file}' into your lottery analyzer.")
    else:
        print("\n❌ Conversion failed. Please check the error messages above.")

if __name__ == "__main__":
    main()