from aiogram.client.bot import DefaultBotProperties
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from unsloth import FastLanguageModel #, is_bfloat16_supported

import asyncio
import logging
import argparse
import json
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from utils.helpers import seed_setting
from model.model import initialize, inference


parser = argparse.ArgumentParser()
parser.add_argument("-m", "--model", type=str)
parser.add_argument("-max", "--max_seq_length", type=int, default=512)
parser.add_argument("-4b", "--load_in_4bit", type=bool, default=False)
parser.add_argument("-mnt", "--max_new_tokens", type=int, default=512)
parser.add_argument('-ls', '--language_selection', type=str, default="English Russian")
parser.add_argument("-seed", "--seed_val", type=int, default=225)
parser.add_argument("-alp", "--alpaca_prompt", type=str, default="""
Below is an instruction that describes a task. Write a response that appropriately completes the request in {language}.  Please answer in {language}.

### Instruction:
{instruction}

### Response:
{answer}""")
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


intro_greeting = f"""Hi there, I am a Large Language Model based on Llama family by Meta AI.
{'-'*20}
I can solve school math tasks in English and some other languages. Let's give it a try and see what comes out! 🤓
"""

error_message = """Oops... I've pressed something and everything just broke down. 😬
Mind trying again?"""



alpaca_prompt = args.alpaca_prompt
languages = args.language_selection.split()
language = languages[0]

split_delimiter = "### Response:\n"
hide_instruction = False


#----------------------------------------------------#

token_path = 'credentials/tokens.json'
with open(token_path, "r") as json_file: TOKEN = json.load(json_file)['telegram']

#----------------------------------------------------#

model_load_dir = '_base' if model_name[:2] == '00' else '_finetuned'
model_load_path = f'{model_load_dir}/{model_name}'
print(f'\n>>> Running {model_name}')
print(f'--- model load path: {model_load_path}\n')

#----------------------------------------------------#


model, tokenizer = initialize(model_load_path, max_seq_length, load_in_4bit)

dispatcher = Dispatcher()


@dispatcher.message(CommandStart())
async def command_handler(message: Message) -> None:
    await message.answer(intro_greeting)


@dispatcher.message()
async def echo_handler(message: types.Message) -> None:
    global hide_instruction
    if message.text == '/hide':
        hide_instruction = not hide_instruction
        await message.answer(f"Hide prompt instruction set to {hide_instruction}")
    elif message.text[0] == '/' and message.text[0] != '/hide':
        await command_handler(message)
    else:
        try:
            output = inference(model, tokenizer, message.text, language, alpaca_prompt, 
            padding, max_new_tokens, do_sample, use_cache, temperature)[0].replace("<<", "|").replace(">>", "|")
            await message.answer(output.split(split_delimiter)[1] if hide_instruction else output)
        except TypeError:
            await message.answer(error_message)


async def main():
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
