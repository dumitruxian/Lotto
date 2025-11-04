import os

def clean_spaces_in_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as infile, \
         open(output_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            cleaned = ' '.join(line.split())
            outfile.write(cleaned + '\n')

def process_all_txt_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.txt'):
            input_file = os.path.join(folder_path, filename)
            name, ext = os.path.splitext(filename)
            output_file = os.path.join(folder_path, f"{name}_cleaned{ext}")
            print(f"Processing: {filename} → {os.path.basename(output_file)}")
            clean_spaces_in_file(input_file, output_file)

if __name__ == "__main__":
    folder = os.getcwd()  # Use current working directory
    process_all_txt_files(folder)
    print("✅ All .txt files processed.")