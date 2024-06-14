import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))
from credentials.tokens import telegram_bot

def get_token():
    return telegram_bot

model_names = [
    '00_model_MathOctopus_Parallel_7B',
    '00_model_llama_3_8B_Instruct_meta',
    '05_r480_rsF_lr6_e3s0',
    '11_r480_rsT_lr5_e0s2000'
]

model_idx = 1

model_name = model_names[model_idx]