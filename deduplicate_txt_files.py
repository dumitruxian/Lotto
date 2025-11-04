import os

def deduplicate_file(input_path, output_path):
    seen = set()
    duplicates = []

    with open(input_path, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    with open(output_path, 'w', encoding='utf-8') as outfile:
        for line in lines:
            stripped = line.rstrip('\n')
            if stripped in seen:
                duplicates.append(stripped)
            else:
                seen.add(stripped)
                outfile.write(stripped + '\n')

    if duplicates:
        print(f"\nDuplicates found in {os.path.basename(input_path)}:")
        for dup in duplicates:
            print(f"  {dup}")
    else:
        print(f"\nNo duplicates in {os.path.basename(input_path)}.")

def process_all_txt_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.txt'):
            input_file = os.path.join(folder_path, filename)
            name, ext = os.path.splitext(filename)
            output_file = os.path.join(folder_path, f"{name}_deduped{ext}")
            deduplicate_file(input_file, output_file)

if __name__ == "__main__":
    folder = os.getcwd()
    process_all_txt_files(folder)
    print("\n✅ All .txt files processed.")