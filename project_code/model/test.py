from unsloth import FastLanguageModel, is_bfloat16_supported
from datasets import load_dataset

from tqdm.auto import tqdm

import argparse
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from utils.helpers import seed_setting, extract_last_num
from model import initialize, inference


parser = argparse.ArgumentParser()
parser.add_argument("-m", "--model", type=str)
parser.add_argument("-max", "--max_seq_length", type=int, default=512)
parser.add_argument("-4b", "--load_in_4bit", type=bool, default=False)
parser.add_argument("-mnt", "--max_new_tokens", type=int, default=512)
parser.add_argument("-b", "--per_device_test_batch_size", type=int, default=50)
parser.add_argument("-alp", "--alpaca_prompt", type=str)
parser.add_argument('-ls', '--language_selection', type=str)
parser.add_argument("-seed", "--seed_val", type=int, default=225)
args = parser.parse_args()


#----------------------------------------------------#
seed_val = args.seed_val
seed_setting(seed_val)
#----------------------------------------------------#


model_name = args.model
max_seq_length = args.max_seq_length
load_in_4bit = args.load_in_4bit
max_new_tokens = args.max_new_tokens
padding = True
do_sample = False # False for temperature 0.0
temperature = 0.00
use_cache = True
batch_size = args.per_device_test_batch_size

language_selection = args.language_selection.split()
alpaca_prompt = args.alpaca_prompt

#----------------------------------------------------#

eval_dataset_path = 'data/mgsm/'
read_file_prefix = 'mgsm_'

#----------------------------------------------------#

model_load_dir = '_base' if model_name[:2] == '00' else '_finetuned'
model_load_path = f'{model_load_dir}/{model_name}'
test_save_path = f'test_results/{model_name}.json'
print(f'\n>>> Testing {model_name}\n')
print(f'--- model load path: {model_load_path}')
print(f'--- test save path: {test_save_path}\n')

#----------------------------------------------------#

def testing(model, tokenizer, language_selection, batch_size):
    model_responses = {}

    for language in tqdm(language_selection):
        print('\n\n---', language)
        lang_eval_dataset = load_dataset('json', data_files=f'{eval_dataset_path}{read_file_prefix}{language}.json', split='train') # eval_dataset.filter(lambda row: row['language']==language)
        model_responses[language] = []
        for idx in tqdm(range(0, lang_eval_dataset.num_rows, batch_size)):
            inputs = lang_eval_dataset[idx:idx+batch_size]['query']
            responses = inference(model, tokenizer, inputs, language, alpaca_prompt, 
                                  padding, max_new_tokens, do_sample, use_cache, temperature)
            pred_responses = [extract_last_num(response) for response in responses]
            true_responses = [extract_last_num(response) for response in lang_eval_dataset[idx:idx+batch_size]['response']]
            model_responses[language].extend([(abs(pred_response - true_response) < 1e-3) for pred_response, true_response in zip(pred_responses, true_responses)])
        model_responses[language] = sum(model_responses[language])/len(model_responses[language])
    return model_responses


model, tokenizer = initialize(model_name=model_load_path, max_seq_length=max_seq_length, load_in_4bit=load_in_4bit)
model_responses = testing(model=model, tokenizer=tokenizer, language_selection=language_selection, batch_size=batch_size)

print(f'\n--- Dumping results for {model_name} ... ', end='')
with open(test_save_path, "w") as output_file:
    json.dump(model_responses, output_file)

print(f'Done\n')