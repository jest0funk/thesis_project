from unsloth import FastLanguageModel, is_bfloat16_supported
from trl import SFTTrainer
from transformers import TrainingArguments
import argparse
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from utils.helpers import seed_setting
from model import initialize
from data.dataset import get_train_dataset


parser = argparse.ArgumentParser()
parser.add_argument("-m", "--model", type=str)
parser.add_argument("-max", "--max_seq_length", type=int, default=512)
parser.add_argument("-4b", "--load_in_4bit", type=bool, default=False)
parser.add_argument("-r", "--lora_rank", type=int)
parser.add_argument("-a", "--lora_alpha", type=int, default=1)
parser.add_argument("-rs", "--use_rslora", type=bool)
parser.add_argument("-b", "--per_device_train_batch_size", type=int, default=4)
parser.add_argument("-s", "--max_steps", type=int, default=0)
parser.add_argument("-e", "--num_train_epochs", type=int, default=0)
parser.add_argument("-log", "--logging_steps", type=int, default=100)
parser.add_argument("-lr", "--learning_rate", type=float)
parser.add_argument("-seed", "--seed_val", type=int, default=225)
parser.add_argument("-idx", "--finetuning_index", type=int)
args = parser.parse_args()


#----------------------------------------------------#
seed_val = args.seed_val
seed_setting(seed_val)
#----------------------------------------------------#


model_name = args.model
max_seq_length = args.max_seq_length
dtype = None # 'Float16' | 'Bfloat16'  # None for autodetection
load_in_4bit = args.load_in_4bit

# LoRA parameters
lora_rank = args.lora_rank
lora_alpha = args.lora_alpha
use_rslora = args.use_rslora # use rank stabilized LoRA
target_modules = ['q_proj', 'k_proj', 'v_proj', 'o_proj', 'gate_proj', 'up_proj', 'down_proj'] # names of the modules to apply the adapter to
lora_dropout = 0 # dropout probability for LoRA layers
bias  = 'none'
use_gradient_checkpointing = True # True or 'unsloth' for very long context
loftq_config = None # use LoFTQ technique


# SFTTrainer training arguments
per_device_train_batch_size = args.per_device_train_batch_size
max_steps = args.max_steps
num_train_epochs = args.num_train_epochs
save_strategy = 'no'
logging_steps = args.logging_steps
output_dir = 'output'


learning_rate = args.learning_rate
lr_scheduler_type = 'cosine'
warmup_steps = 0
optimizer_name = 'adamw_torch'
weight_decay = 0.0
adam_beta1 = 0.9
adam_beta2 = 0.95
gradient_accumulation_steps = 4


#----------------------------------------------------#

train_dataset_path = 'data/MGSM8KInstruct/MGSM8KInstruct_Parallel.json'
train_dataset = get_train_dataset(train_dataset_path)
dataset_text_field = 'formatted_prompt'
dataset_num_proc = 2 # not used when packing=True
packing = False

#----------------------------------------------------#

model_load_path = f'_base/{model_name}'
model_save_path = f'_finetuned/{(str(0)+str(args.finetuning_index+1))[-2:]}_r{lora_rank}_rs{str(use_rslora)[0]}_lr{str(learning_rate)[-1]}_e{num_train_epochs}s{max_steps}'
print(f'\n>>> Finetuning {model_name}')
print(f'--- base model load path: {model_load_path}')
print(f'--- finetuned model save path: {model_save_path}\n')

#----------------------------------------------------#


model, tokenizer = initialize(
    model_name=model_load_path, max_seq_length=max_seq_length, 
    load_in_4bit=load_in_4bit, dtype=dtype)

print(f'\n--- Model {model_name} initialized from {model_load_path}\n')

model = FastLanguageModel.get_peft_model(
    model,
    r = lora_rank,
    target_modules = target_modules,
    lora_alpha = lora_alpha,
    lora_dropout = lora_dropout,
    bias = bias,
    use_gradient_checkpointing = use_gradient_checkpointing,
    random_state = seed_val,
    use_rslora = use_rslora,
    loftq_config = loftq_config
)


trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = train_dataset,
    dataset_text_field = dataset_text_field,
    max_seq_length = max_seq_length,
    dataset_num_proc = dataset_num_proc,
    packing = packing,
    args = TrainingArguments(
        per_device_train_batch_size = per_device_train_batch_size,
        gradient_accumulation_steps = gradient_accumulation_steps,
        warmup_steps = warmup_steps,
        max_steps = max_steps,
        num_train_epochs = num_train_epochs,
        learning_rate = learning_rate,
        fp16 = not is_bfloat16_supported(),
        bf16 = is_bfloat16_supported(),
        logging_steps = logging_steps,
        optim = optimizer_name,
        weight_decay = weight_decay,
        lr_scheduler_type = lr_scheduler_type,
        seed = seed_val,
        save_strategy = save_strategy,
        output_dir = output_dir
    )
)

print('\n')
trainer.train()
print(f'\n--- Saving to {model_save_path}\n')
model.save_pretrained_merged(model_save_path, tokenizer, save_method = 'merged_16bit',)
print()