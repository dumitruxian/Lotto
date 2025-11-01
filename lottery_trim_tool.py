"""
Lottery Combinations Trimmer
Removes combinations containing specific numbers

Usage:
python lottery_trim_tool.py <show> <max_play>

Arguments:
  show      - 1 to show remaining combinations, 0 to hide
  max_play  - 6 or 7 (number of numbers per combination)

Examples:
python lottery_trim_tool.py 0 6
python lottery_trim_tool.py 1 7
"""

import sys
import os

SP = 32

def tochar(ch):
    """Convert number to character"""
    return (ch + SP) & 0xFF

def unchar(ch):
    """Convert character back to number"""
    return (ch - SP) & 0xFF

def var_to_bin(variant):
    """Convert variant to binary"""
    return bytes([tochar(n) for n in variant])

def bin_to_var(data, max_play):
    """Convert binary to variant"""
    return [unchar(data[i]) for i in range(max_play)]

def read_variant_text(line):
    """Parse text line to variant"""
    variant = []
    line = line.strip()
    
    # Remove spaces and split by comma
    parts = line.replace(' ', '').split(',')
    
    for part in parts:
        if part.isdigit():
            variant.append(int(part))
    
    return variant

def trim_variant(variant, number):
    """Check if variant contains the number"""
    return number in variant

def is_binary_file(filename):
    """Check if file is binary"""
    return (filename.lower().endswith('b') or 
            filename.lower().endswith('.b') or
            'b' in filename.lower()[-2:])

def trim_set_played(show, max_play):
    """Main trimming function"""
    
    # Get input filename
    print("\nInput file name: ", end='')
    f_name = input().strip()
    
    if not f_name:
        print("No filename provided")
        return
    
    if not os.path.exists(f_name):
        print(f"Cannot open file: {f_name}")
        return
    
    is_binary = is_binary_file(f_name)
    
    # Create temporary filenames
    temp_a = f_name + "$"
    temp_b = f_name + "&"
    i_name = f_name
    o_name = temp_a
    
    print(f"File type: {'Binary' if is_binary else 'Text'}")
    print(f"Max play: {max_play}")
    print()
    
    while True:
        print("Trim number (0 to finish): ", end='')
        s = input().strip()
        
        try:
            num = int(s)
        except ValueError:
            print("Invalid number")
            continue
        
        if num == 0:
            break
        
        max_val = 47 if max_play == 7 else 49
        if num < 1 or num > max_val:
            print(f"Number must be between 1 and {max_val}")
            continue
        
        # Process file
        try:
            if is_binary:
                process_binary(i_name, o_name, num, max_play, show)
            else:
                process_text(i_name, o_name, num, max_play, show)
            
            # Swap temp files
            i_name = o_name
            o_name = temp_b if o_name == temp_a else temp_a
            
        except Exception as e:
            print(f"Error processing: {e}")
            break
    
    # Save final result
    if i_name != f_name:
        output_name = f_name.replace('.', '_trimmed.')
        if '.' not in output_name:
            output_name = f_name + '_trimmed'
        
        try:
            if os.path.exists(i_name):
                os.replace(i_name, output_name)
                print(f"\n✅ Final output saved as: {output_name}")
        except Exception as e:
            print(f"Error saving final file: {e}")
    
    # Clean up temp files
    for temp_file in [temp_a, temp_b]:
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass

def process_binary(i_name, o_name, num, max_play, show):
    """Process binary file"""
    cnt_line = 0
    cnt_trim = 0
    
    with open(i_name, 'rb') as ifp, open(o_name, 'wb') as ofp:
        if show:
            print()
        
        while True:
            data = ifp.read(max_play)
            if len(data) != max_play:
                break
            
            variant = bin_to_var(data, max_play)
            cnt_line += 1
            
            if trim_variant(variant, num):
                cnt_trim += 1
            else:
                ofp.write(data)
                if show:
                    line = ', '.join(f'{n:2d}' for n in variant[:-1])
                    line += f', {variant[-1]:2d}'
                    print(f" {line}")
    
    print(f"Initial: {cnt_line}, Trimmed: {cnt_trim}, Remaining: {cnt_line - cnt_trim}")
    if show:
        print()

def process_text(i_name, o_name, num, max_play, show):
    """Process text file"""
    cnt_line = 0
    cnt_trim = 0
    
    with open(i_name, 'r') as ifp, open(o_name, 'w') as ofp:
        if show:
            print()
        
        for line in ifp:
            if not line.strip() or not line[0].isdigit():
                continue
            
            variant = read_variant_text(line)
            if len(variant) != max_play:
                continue
            
            cnt_line += 1
            
            if trim_variant(variant, num):
                cnt_trim += 1
            else:
                ofp.write(line)
                if show:
                    print(f" {line.strip()}")
    
    print(f"Initial: {cnt_line}, Trimmed: {cnt_trim}, Remaining: {cnt_line - cnt_trim}")
    if show:
        print()

def main():
    if len(sys.argv) < 3:
        print("=" * 60)
        print("Lottery Combinations Trimmer")
        print("=" * 60)
        print("\nRemoves combinations containing specific numbers")
        print("\nUsage:")
        print("  python lottery_trim_tool.py <show> <max_play>")
        print("\nArguments:")
        print("  show     - 1 to display remaining combinations, 0 to hide")
        print("  max_play - 6 or 7 (numbers per combination)")
        print("\nExamples:")
        print("  python lottery_trim_tool.py 0 6")
        print("  python lottery_trim_tool.py 1 7")
        print("\nHow it works:")
        print("  1. Enter input filename (text or binary)")
        print("  2. Enter numbers to trim (one at a time)")
        print("  3. Enter 0 when done")
        print("  4. Trimmed file will be saved")
        print("=" * 60)
        sys.exit(0)
    
    try:
        show = int(sys.argv[1])
        show = bool(show)
    except ValueError:
        print("Error: show must be 0 or 1")
        sys.exit(1)
    
    try:
        max_play = int(sys.argv[2])
    except ValueError:
        print("Error: max_play must be a number")
        sys.exit(1)
    
    if max_play < 6 or max_play > 7:
        print("Error: max_play must be 6 or 7")
        sys.exit(1)
    
    print("=" * 60)
    print("Lottery Combinations Trimmer")
    print("=" * 60)
    print(f"Display mode: {'ON' if show else 'OFF'}")
    print(f"Max play: {max_play}")
    print("=" * 60)
    
    trim_set_played(show, max_play)
    
    print("\n✅ Trimming complete!")

if __name__ == "__main__":
    main()