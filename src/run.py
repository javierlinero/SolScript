import openai
import pythx
import json
import os
from dotenv import dotenv_values

def main():
    # https://platform.openai.com/docs/guides/fine-tuning/use-a-fine-tuned-model

    # Load environment variables from .env file
    env_vars = dotenv_values("gptkey.env")

    # Access specific environment variables
    openaikey = env_vars.get("OPENAIKEY")

    # we pre-process data into fine_tuning_prompt.jsonl
    openai.api_key = openaikey

    # create openai file
    file_response = openai.File.create(
        file=open("fine_tuning_prompt.jsonl", "rb"),
        purpose="fine-tune"
    )
    file_id = file_response['id']

    # setup open ai w/ relative API key in .env

    fine_tune_response = openai.FineTune.create(
        training_file=file_id, 
        model="davinci-002"
    )
    fine_tune_id = fine_tune_response['id']
    print(fine_tune_id)
    # create output w/ prompt 

    # completion = openai.chat.completions.create(
    #     model="ft:gpt-3.5-turbo:my-org:custom_suffix:id",
    #     messages=[
    #         {"role": "system", "content": "You are a helpful assistant."},
    #         {"role": "user", "content": "Hello!"}
    #     ]
    # )
    # print(completion.choices[0].message)

    # feed prompt thru loop to 3 different llm models with specified prompt to score based on number of vulnerabities

    # collect scores and feed each one individually to retrain w/ relative score

    # then we test out some prompts against a vanilla model with mythx interface and see which one performs better

    # https://github.com/Consensys/pythx <- python interface for mythx


    return None

if __name__ == '__main__':
    main()