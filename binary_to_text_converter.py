"""
Binary Lottery File Converter
Converts binary lottery files to readable text format

Usage:
python binary_to_text_converter.py <input_file.b> <max_play> [output_file.txt]

Examples:
python binary_to_text_converter.py b_649.b 6
python binary_to_text_converter.py b_649.b 6 output.txt
python binary_to_text_converter.py b_747.b 7
"""

import sys
import struct

SP = 32

def unchar(ch):
    """Convert character back to number"""
    return (ch - SP) & 0xFF

def bin_to_variant(data, max_play):
    """Convert binary data to variant numbers"""
    variant = []
    for i in range(max_play):
        variant.append(unchar(data[i]))
    return variant

def list_binary(filename, max_play, output_file=None):
    """Read binary file and output as text"""
    
    # Check if filename ends with 'b' or 'B'
    if not (filename.lower().endswith('b') or 
            filename.lower().endswith('.b') or
            'b' in filename.lower()[-2:]):
        print(f"Error: File '{filename}' doesn't appear to be a binary file")
        return False
    
    try:
        with open(filename, 'rb') as fp:
            count = 0
            
            # Open output file if specified
            out_fp = None
            if output_file:
                out_fp = open(output_file, 'w')
                out_fp.write(f"# Binary Lottery File: {filename}\n")
                out_fp.write(f"# Max Play: {max_play}\n")
                out_fp.write(f"# Format: N1, N2, N3, N4, N5, N6[, N7]\n")
                out_fp.write("#\n")
            
            while True:
                # Read max_play bytes
                data = fp.read(max_play)
                
                if len(data) != max_play:
                    break
                
                # Convert to variant
                variant = bin_to_variant(data, max_play)
                
                # Format output
                output_line = ', '.join(f'{n:2d}' for n in variant[:-1])
                output_line += f', {variant[-1]:2d}'
                
                # Print to console
                print(output_line)
                
                # Write to file if specified
                if out_fp:
                    out_fp.write(output_line + '\n')
                
                count += 1
            
            if out_fp:
                out_fp.close()
                print(f"\n✅ Converted {count} combinations")
                print(f"Output saved to: {output_file}")
            else:
                print(f"\n✅ Listed {count} combinations")
            
            return True
            
    except FileNotFoundError:
        print(f"Error: Cannot open file '{filename}'")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    if len(sys.argv) < 3:
        print("Binary Lottery File Converter")
        print("=" * 60)
        print("\nUsage:")
        print("  python binary_to_text_converter.py <input_file> <max_play> [output_file]")
        print("\nArguments:")
        print("  input_file  - Binary file to convert (e.g., b_649.b)")
        print("  max_play    - Number of numbers per combination (6 or 7)")
        print("  output_file - Optional output text file (default: console only)")
        print("\nExamples:")
        print("  python binary_to_text_converter.py b_649.b 6")
        print("  python binary_to_text_converter.py b_649.b 6 output.txt")
        print("  python binary_to_text_converter.py b_747.b 7 output_747.txt")
        print("=" * 60)
        sys.exit(0)
    
    filename = sys.argv[1]
    
    try:
        max_play = int(sys.argv[2])
    except ValueError:
        print("Error: max_play must be a number (6 or 7)")
        sys.exit(1)
    
    if max_play < 6 or max_play > 7:
        print("Error: max_play must be 6 or 7")
        sys.exit(1)
    
    output_file = sys.argv[3] if len(sys.argv) > 3 else None
    
    print("=" * 60)
    print("Binary Lottery File Converter")
    print("=" * 60)
    print(f"Input file:  {filename}")
    print(f"Max play:    {max_play}")
    if output_file:
        print(f"Output file: {output_file}")
    else:
        print(f"Output:      Console only")
    print("=" * 60)
    print()
    
    success = list_binary(filename, max_play, output_file)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()