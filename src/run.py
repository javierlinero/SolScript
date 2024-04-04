import openai
import pythx
import json

def main():
    # https://platform.openai.com/docs/guides/fine-tuning/use-a-fine-tuned-model
    # load sb-curated

    # pre-process data to i/o for openai llm

    # {"prompt": "<prompt text>", "completion": "<ideal generated text>"}
    # {"prompt": "<prompt text>", "completion": "<ideal generated text>"}
    # {"prompt": "<prompt text>", "completion": "<ideal generated text>"}

    # jsonify data into "train.json"

    client = openai.OpenAI()

    # create openai file
    client.files.create(
        file=open("train.json", "rb"),
        purpose="fine-tune"
    )

    # setup open ai w/ relative API key in .env

    client.fine_tuning.jobs.create(
        training_file="train.json", 
        model="gpt-3.5-turbo"
    )

    # train model w/ curated data 

    # create output w/ prompt 

    completion = client.chat.completions.create(
        model="ft:gpt-3.5-turbo:my-org:custom_suffix:id",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"}
        ]
    )
    print(completion.choices[0].message)

    # feed prompt thru loop to 3 different llm models with specified prompt to score based on number of vulnerabities

    # collect scores and feed each one individually to retrain w/ relative score

    # then we test out some prompts against a vanilla model with mythx interface and see which one performs better

    # https://github.com/Consensys/pythx <- python interface for mythx


    return None

if __name__ == '__main__':
    main()