import os
import json
import re
import random

def generate_jsonl_entries(dataset_dir):
    # output files
    output_file_train = 'fine_tuning_prompt_train.jsonl'
    output_file_val = 'fine_tuning_prompt_val.jsonl'
    pattern = re.compile(r'\* @vulnerable_at_lines: ([\d,]+)')

    entries = []

    for root, dirs, files in os.walk(dataset_dir):
        for file_name in files:
            if file_name.endswith('.sol'):
                vulnerability = os.path.basename(root)
                vulnerability = vulnerability.replace('_', ' ')  # Fix underscores

                # init message
                messages = [
                    {"role": "system", "content": "SolScript is a smart contract code generator trying to reduce the number of vulnerabilities."},
                    {"role": "user", "content": f"Write a solidity smart contract with {vulnerability} vulnerabilities according to the DASP standard. After, reproduce the lines where the vulnerabilities occur."}
                ]

                file_path = os.path.join(root, file_name)
                with open(file_path, 'r') as file_content:
                    lines = file_content.read().splitlines()
                    completion = '\n'.join(lines)

                    vulnerability_lines = []
                    for line in lines:
                        match = pattern.search(line)
                        if match:
                            line_numbers = match.group(1)
                            vulnerability_lines.extend([int(num) for num in line_numbers.split(',')])

                    # retrieve actual vulnerable lines from the file and append
                    vulnerable_lines_text = [lines[i - 1] for i in vulnerability_lines]  # Adjusting index for 0-based
                    vulnerability_info = "\nVulnerable lines:\n" + '\n'.join(vulnerable_lines_text)
                    completion += vulnerability_info

                    # Append the coder completion
                    messages.append({"role": "assistant", "content": completion})
                    entry = {"messages": messages}
                    entries.append(entry)

    # randomize the entries
    random.shuffle(entries)

    # split indices by 75% for training
    num_entries = len(entries)
    split_index = int(0.75 * num_entries)

    # split into training & validation
    train_entries = entries[:split_index]
    val_entries = entries[split_index:]

    with open(output_file_train, 'w') as jsonl_file_train:
        for entry in train_entries:
            jsonl_file_train.write(json.dumps(entry) + '\n')

    with open(output_file_val, 'w') as jsonl_file_val:
        for entry in val_entries:
            jsonl_file_val.write(json.dumps(entry) + '\n')

if __name__ == '__main__':
    dataset_dir = '../sb-curated/dataset'  # Path to the dataset directory
    generate_jsonl_entries(dataset_dir)
