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

    # create openai file
    with open("fine_tuning_prompt.jsonl", "rb") as file:
        file_response = client.files.create(file=file, purpose="fine-tune")
        file_id = file_response.id
    # setup open ai w/ relative API key in .env

    fine_tune_response = client.fine_tuning.jobs.create(
        training_file=file_id,
        model="davinci-002")
    fine_tune_id = fine_tune_response.id
    print(fine_tune_id)

if __name__ == '__main__':
    main()


