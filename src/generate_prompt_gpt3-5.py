import os
import json
import random

MAX_TOKENS = 16384  # Maximum tokens allowed for fine-tuning in GPT-3.5 Turbo
NUM_CONTRACTS = 1250  # Number of contracts to generate

def generate_jsonl_entries(dataset_dir):
    # output files
    output_file_train = 'fine_tuning_prompt_train.jsonl'
    output_file_val = 'fine_tuning_prompt_val.jsonl'

    entries = []

    for root, dirs, files in os.walk(dataset_dir):
        for file_name in files:
            if file_name.endswith('.sol'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r') as file_content:
                    completion = file_content.read()

                    # Check if the completion exceeds the token limit
                    if len(completion.split()) > MAX_TOKENS:
                        continue

                    # Initialize messages
                    messages = [
                        {"role": "system", "content": "SolScript is a smart contract code generator trying to reduce the number of vulnerabilities."},
                        {"role": "user", "content": f"Write a solidity smart contract with respect to the guidelines of DASP (Decentralized Application Security Project)"}
                    ]

                    # Append the coder completion
                    messages.append({"role": "assistant", "content": completion})
                    entry = {"messages": messages}
                    entries.append(entry)

    # randomize the entries
    random.shuffle(entries)

    # select 1250 random entries
    selected_entries = random.sample(entries, NUM_CONTRACTS)

    # split indices by 75% for training
    split_index = int(0.75 * NUM_CONTRACTS)

    # split into training & validation
    train_entries = selected_entries[:split_index]
    val_entries = selected_entries[split_index:]

    with open(output_file_train, 'w') as jsonl_file_train:
        for entry in train_entries:
            jsonl_file_train.write(json.dumps(entry) + '\n')

    with open(output_file_val, 'w') as jsonl_file_val:
        for entry in val_entries:
            jsonl_file_val.write(json.dumps(entry) + '\n')

if __name__ == '__main__':
    dataset_dir = '../contracts'  # Path to the dataset directory
    generate_jsonl_entries(dataset_dir)
