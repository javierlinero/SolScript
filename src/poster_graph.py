import matplotlib.pyplot as plt
import glob

# Function to read data from a file
def read_data_from_file(file_path):
    vulnerabilities = []
    interactions = []
    trials = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip():  # Ignore empty lines
                data = line.strip().split()
                if len(data) == 3:  # Ensure there are exactly three elements in the line
                    vulnerabilities.append(int(data[0]))
                    interactions.append(int(data[1]))
                    trials.append(int(data[2]))
                else:
                    print(f"Skipping invalid line: {line.strip()}")
    return interactions, vulnerabilities, trials


def main():
    prompt_types = ['stable_coin', 'sandwich_attack', 'borrow_lending', 'nft', 'dao']
    file_patterns = [f"poster_data/feedback_data_{pt}.txt" for pt in prompt_types]
    color_palette = [
        ['#1f77b4', '#aec7e8'],  # Colors for stable_coin
        ['#ff7f0e', '#ffbb78'],  # Colors for sandwich_attack
        ['#2ca02c', '#98df8a'],  # Colors for borrow_lending
        ['#d62728', '#ff9896'],  # Colors for nft
        ['#9467bd', '#c5b0d5']   # Colors for dao
    ]

    for i, (prompt_type, file_pattern) in enumerate(zip(prompt_types, file_patterns)):
        matching_files = glob.glob(file_pattern)
        
        if not matching_files:
            print(f"No file found for prompt type: {prompt_type}")
            continue
        
        file_path = matching_files[0]
        
        interactions, vulnerabilities, trials = read_data_from_file(file_path)
        unique_trials = sorted(set(trials))
        
        plt.figure(figsize=(7, 6))
        
        all_interactions = sorted(set(interactions))
        num_trials = len(unique_trials)
        total_width = 1.0  # Adjusted to make bars thicker
        bar_width = total_width / num_trials  # Calculate bar width based on total width and number of trials

        for j, trial in enumerate(unique_trials):
            trial_interactions = [all_interactions.index(interactions[k]) + j * bar_width for k in range(len(interactions)) if trials[k] == trial]
            trial_vulnerabilities = [vulnerabilities[k] for k in range(len(vulnerabilities)) if trials[k] == trial]
            
            plt.bar([x + bar_width / 2 for x in trial_interactions], trial_vulnerabilities, 
                    width=bar_width, 
                    color=color_palette[i][j % len(color_palette[i])], 
                    label=f'Trial {trial}')

        plt.title(f'Number of Vulnerabilities over interactions - {prompt_type}')
        plt.xlabel('Interactions')
        plt.ylabel('# of Vulnerabilities')

        plt.xticks(range(len(all_interactions)), all_interactions)
        plt.legend()
        plt.show()


if __name__ == '__main__':
    main()
