# SolScript AI

## contracts
- contracts is a folder containing all 47,000 contracts from the [SmartBugs](https://github.com/smartbugs/smartbugs-wild) dataset.

## sb-curated
- sb-curated is a folder containing the [SmartBugs](https://github.com/smartbugs/smartbugs-curated) vulnerable contracts. We used this data to train a gpt3.5 instance to critique contracts, however we did not end up using this model in our final analysis.

## src
- src contains all of our source code we used to parse contract data, prepare finetuning prompts, and run the feedback loop. The main files to inspect for our final product are generate_prompt_gpt3-5.py, where we prepare prompts to use in finetune.py, where we connect to the OpenAI API. In feedback_loop.py, we enact the main reinforcement loop between the finetuned model and a gpt4 instance. We store the conversation history in history_feedback and the raw results in poster_data. davinci, old-critique, and old-train contain past/unfinished iterations towards our final product.

Made by Ernesto Moreno, Javier Linero, Kaan Odabas, and Mack Merriman in ECE473 (Spring 2024)