import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from model.model import initialize, inference
from config import model_name

max_seq_length = 512
load_in_4bit = False
max_new_tokens = 512
padding = True
do_sample = False # False for temperature 0.0
temperature = 0.00
use_cache = True


model_load_dir = '_base' if model_name[:2] == '00' else '_finetuned'
model_load_path = f'{model_load_dir}/{model_name}'
model, tokenizer = initialize(model_load_path, max_seq_length, load_in_4bit)


def generate_text(prompt, language, alpaca_prompt):
    response = inference(model, tokenizer, prompt, language, alpaca_prompt, 
                         padding, max_new_tokens, do_sample, use_cache, temperature)
    return response[0].replace("<<", "|").replace(">>", "|")