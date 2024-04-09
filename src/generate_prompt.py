import os
import json
import re

def generate_jsonl_entries(dataset_dir):
    output_file = 'fine_tuning_prompt.jsonl'
    pattern = re.compile(r'\* @vulnerable_at_lines: ([\d,]+)')

    with open(output_file, 'w') as jsonl_file:
        for root, dirs, files in os.walk(dataset_dir):
            for file in files:
                if file.endswith('.sol'):
                    vulnerability = os.path.basename(root)
                    vulnerability = vulnerability.replace('_', ' ') # fix _
                    prompt = f"Write a solidity smart contract with {vulnerability} vulnerabilities according to the DASP standard. After, reproduce the lines where the vulnerabilities occur."
                    file_path = os.path.join(root, file)

                    with open(file_path, 'r') as file_content:
                        lines = file_content.read().splitlines()
                        completion = '\n'.join(lines)

                        # Search for the pattern and extract line numbers
                        vulnerability_lines = []
                        for line in lines:
                            match = pattern.search(line)
                            if match:
                                line_numbers = match.group(1)
                                vulnerability_lines.extend([int(num) for num in line_numbers.split(',')])

                        # Retrieve actual vulnerable lines from the file
                        vulnerable_lines_text = [lines[i - 1] for i in vulnerability_lines]  # Adjusting index for 0-based
                        vulnerability_info = f"\nVulnerable lines:\n" + '\n'.join(vulnerable_lines_text)

                        # Append the actual vulnerable lines to the completion
                        completion += vulnerability_info

                        entry = {"prompt": prompt, "completion": completion}
                        jsonl_file.write(json.dumps(entry) + '\n')

if __name__ == '__main__':
    dataset_dir = '../sb-curated/dataset'  # Path to the dataset directory
    generate_jsonl_entries(dataset_dir)
