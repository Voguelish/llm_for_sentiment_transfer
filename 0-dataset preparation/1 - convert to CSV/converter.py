import os
import csv

def convert_to_csv(input_file, output_file):
    with open(input_file, 'r') as in_file:
        lines = in_file.readlines()
        data = [line.strip().split('\t') for line in lines]  # Splitting by tab character

    with open(output_file, 'w', newline='', encoding='utf-8') as out_file:
        writer = csv.writer(out_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(data)

def main():
    input_folder = "./dataset/"
    output_folder = "./result/"

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        if file_name.endswith('.0') or file_name.endswith('.1'):
            input_file_path = os.path.join(input_folder, file_name)
            if file_name.endswith('.0'):
                output_file_path = os.path.join(output_folder, file_name.replace('.0', '-0.csv'))
            elif file_name.endswith('.1'):
                output_file_path = os.path.join(output_folder, file_name.replace('.1', '-1.csv'))
            convert_to_csv(input_file_path, output_file_path)
            print(f"Converted {input_file_path} to {output_file_path}")

if __name__ == "__main__":
    main()
