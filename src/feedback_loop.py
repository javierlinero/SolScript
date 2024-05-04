from dotenv import dotenv_values
import openai
import json
import time
import re

# finedtuned: ft:gpt-3.5-turbo-0125:sccontracts::9CeGYRLm
solscript = "gpt-3.5-turbo-0125"
solscriptcritique = "gpt-4-turbo-2024-04-09"
NUM_TRIALS = 2

def extract_num_vulnerabilities(text):
    pattern = r'<(\d+)>'
    match = re.search(pattern, text)
    if match:
        return int(match.group(1))
    else:
        return None

def generate_contract(client, message_history):
    completion = client.chat.completions.create(
        model=solscript,    
        messages=message_history
    ) # Assuming the content you need is in the first choice's message
    return completion.choices[0].message.content

def critique_contract(client, message_history):
    completion = client.chat.completions.create(
        model=solscriptcritique,    
        messages=message_history
    )    # Assuming the content you need is in the first choice's message
    return completion.choices[0].message.content


def main():
    # Load environment variables from .env file
    env_vars = dotenv_values("../gptkey.env")

    # Access specific environment variables
    openaikey = env_vars.get("OPENAIKEY")
    
    client = openai.OpenAI(
        api_key=openaikey
    )
    
    prompts = {
        "stable_coin": """Generate a Solidity smart contract for a stable coin that is robust and secure, free from vulnerabilities. Your response 
                        should consist solely of Solidity code, with clear and efficient implementation. Avoid unnecessary complexity.""",
        "sandwich_attack": """Generate a Solidity smart contract for a sandwich attack that is robust and secure, free from vulnerabilities. Your response 
                        should consist solely of Solidity code, with clear and efficient implementation. Avoid unnecessary complexity.""",
        "borrow_lending": """Generate a Solidity smart contract for a borrow lending protocol that is robust and secure, free from vulnerabilities. Your response 
                        should consist solely of Solidity code, with clear and efficient implementation. Avoid unnecessary complexity.""",
        "nft": """Generate a Solidity smart contract for an NFT that is robust and secure, free from vulnerabilities. Your response 
                        should consist solely of Solidity code, with clear and efficient implementation. Avoid unnecessary complexity.""",
        "dao": """Generate a Solidity smart contract for an DAO (Decentralized Autonomous Organization) that is robust and secure, free from vulnerabilities. Your response 
                        should consist solely of Solidity code, with clear and efficient implementation. Avoid unnecessary complexity.""",
    }

    generate_prompt = """Regenerate the contract you made earlier, implementing fixes for the criticism you received below.
                        Only respond with Solidity code, and do not comment the code."""
    critique_prompt = """Given the below smart contract, diagnose any vulnerabilities it has according to the DASP (https://dasp.co/) standard 
                        and point out the specific lines at which the vulnerabilities occur. Be exceptionally concise with your answer. At the
                        end of your response, report the number of vulnerabilities you notice as an integer in angle brackets, e.g. <3>."""

    for key, prompt in prompts.items():
        message_history_generate = [
            {"role": "system", "content": "SolScript is a smart contract code generator trying to reduce the number of vulnerabilities."},
            {"role": "user", "content": prompt},
        ]
        message_history_critique = [
            {"role": "system", "content": "SolScriptCritique is a smart contract code evaluator trying to reduce the number of vulnerabilities."},
        ]
        time_step = 0
        with open(f"poster_data/feedback_data_{key}_baseline.txt", "w") as data:
            for trial in range(NUM_TRIALS):
                generated_contract = generate_contract(client, message_history_generate)
                message_history_generate.append({"role": "assistant", "content": generated_contract})
                message_history_critique.append({"role": "user", "content": critique_prompt + '\n' + generated_contract})
                num_critiques = 0
                while True:
                    time_step += 1
                    num_critiques += 1
                    print("prior to critique number:", num_critiques)
                    time.sleep(1)
                    critique_response = critique_contract(client, message_history_critique)
                    message_history_generate.append({"role": "user", "content": generate_prompt + '\n' + critique_response})
                    message_history_critique.append({"role": "assistant", "content": critique_response})
                    num_vulnerabilities = extract_num_vulnerabilities(critique_response)
                    data.write(f"{num_vulnerabilities} {time_step} {trial}\n")
                    print(f"number of vulnerabilities for {key} trial {trial}:", num_vulnerabilities)
                    if num_vulnerabilities == 0 or num_critiques == 3:
                        print("terminating feedback loop, next trial begins")
                        break
                    time.sleep(1)
                    generated_contract = generate_contract(client, message_history_generate)
                    message_history_generate.append({"role": "assistant", "content": generated_contract})
                    message_history_critique.append({"role": "user", "content": critique_prompt + '\n' + generated_contract})
                with open(f"history_feedback/msg_his_generate_trial{trial}_{key}_baseline.json", 'w') as outfile:
                    json.dump(message_history_generate, outfile)
                with open(f"history_feedback/msg_his_critique_trial{trial}_{key}_baseline.json", 'w') as outfile:
                    json.dump(message_history_critique, outfile)

if __name__ == '__main__':
    main()