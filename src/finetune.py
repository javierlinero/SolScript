import openai
import pythx
import json
import os
from pathlib import Path
from dotenv import dotenv_values

def main():
    # https://platform.openai.com/docs/guides/fine-tuning/use-a-fine-tuned-model

    # Load environment variables from .env file
    env_vars = dotenv_values("../gptkey.env")

    # Access specific environment variables
    openaikey = env_vars.get("OPENAIKEY")

    # we pre-process data into fine_tuning_prompt.jsonl
    client = openai.OpenAI(
        api_key = openaikey
    )

    # create openai files for validation and training set
    with open("ft_critique_train.jsonl", "rb") as file:
        train_response = client.files.create(file=file, purpose="fine-tune")
        train_id = train_response.id

    with open("ft_critique_val.jsonl", "rb") as file:
        val_response = client.files.create(file=file, purpose="fine-tune")
        val_id = val_response.id
    
    # setup open ai w/ relative API key in .env
    fine_tune_response = client.fine_tuning.jobs.create(
        training_file= train_id,
        validation_file= val_id,
        model="gpt-3.5-turbo-0125")
    fine_tune_id = fine_tune_response.id
    print(fine_tune_id)

if __name__ == '__main__':
    main()


