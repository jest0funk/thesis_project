from datasets import Dataset
import pandas as pd


def get_train_dataset(train_dataset_path):
    train_df = pd.read_json(train_dataset_path, lines=True)
    train_df = train_df[['prompt', 'chosen']]
    train_df.columns = ['prompt', 'completion']
    train_df.completion = train_df.completion.str.replace("<<", "|").str.replace(">>", "|")
    train_df['formatted_prompt'] = train_df.prompt[0] + '\n' +  train_df.completion[0] + '<|end_of_text|>'
    train_dataset = Dataset.from_pandas(train_df)
    return train_dataset
