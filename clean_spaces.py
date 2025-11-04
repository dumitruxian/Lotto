import sys
import os

def clean_spaces(input_file, output_file):
    if not os.path.isfile(input_file):
        print(f"Error: '{input_file}' does not exist.")
        return

    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            cleaned_line = ' '.join(line.split())
            outfile.write(cleaned_line + '\n')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python clean_spaces.py input.txt output.txt")
    else:
        input_path = sys.argv[1]
        output_path = sys.argv[2]
        clean_spaces(input_path, output_path)