from dotenv import dotenv_values
import openai
import json
import time

solscript = "ft:gpt-3.5-turbo-0125:sccontracts::9CeGYRLm"
solscriptcritique = "gpt-4-turbo-2024-04-09"
NUM_TRIALS = 3
TERMINATION_FLAG = 'banana'

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
        "stable_coin": "Generate a Solidity smart contract for a stable coin with no vulnerabilities.", ###
        "sandwich_attack": "Generate a Solidity smart contract for a sandwich attack with no vulnerabilities.", ###
        "borrow_lending": "Generate a Solidity smart contract for a decentralized borrowing and lending platform, focusing on the mechanisms for interest rate calculation and collateral management with no vulnerabilities.", ###
        "nft": "Generate a Solidity smart contract for an NFT with no vulnerabilities.", ###
        "dao": "Generate a Solidity smart contract for a DAO (Decentralized Autonomous Organization) with no vulnerabilities.", ###
    }

    generate_prompt = "Regenerate the contract you made earlier, implementing fixes for the criticism you received below."
    critique_prompt = "Given the below smart contract, diagnose any vulnerabilities it has (preferably according to the DASP standard) and point out the specific lines at which the vulnerabilities occur. Be concise with your answer. If you think the contract is adequate, place the word 'banana' in your response. Do not use the word 'banana' otherwise."

    for key, prompt in prompts.items():
        message_history_generate = [
            {"role": "system", "content": "SolScript is a smart contract code generator trying to reduce the number of vulnerabilities."},
            {"role": "user", "content": prompt},
        ]
        message_history_critique = [
            {"role": "system", "content": "SolScriptCritique is a smart contract code evaluator trying to reduce the number of vulnerabilities."},
        ]
        for trial in range(NUM_TRIALS):
            # First-shot generate a contract of the specific prompt
            generated_contract = generate_contract(client, message_history_generate)
            message_history_generate.append({"role": "assistant", "content": generated_contract})
            message_history_critique.append({"role": "user", "content": critique_prompt + '\n' + generated_contract})
            i = 0
            while True:
                print("first time sleep in feedback loop: ", i)
                i += 1
                time.sleep(1)
                critique_response = critique_contract(client, message_history_critique)
                if TERMINATION_FLAG in critique_response or i == 3:
                    break
                message_history_generate.append({"role": "user", "content": generate_prompt + '\n' + critique_response})
                message_history_critique.append({"role": "assistant", "content": critique_response})
                time.sleep(1)
                generated_contract = generate_contract(client, message_history_generate)
                message_history_generate.append({"role": "assistant", "content": generated_contract})
                message_history_critique.append({"role": "user", "content": critique_prompt + '\n' + generated_contract})
                with open(f"history_feedback/msg_his_generate_trial{trial}_{key}.json", 'w') as outfile:
                    json.dump(message_history_generate, outfile)
                with open(f"history_feedback/msg_his_critique_trial{trial}_{key}.json", 'w') as outfile:
                    json.dump(message_history_critique, outfile)

if __name__ == '__main__':
    main()