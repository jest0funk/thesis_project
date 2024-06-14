from transformers import set_seed
import numpy as np
import random
import torch
import os
import re


def seed_setting(seed_val): 
    set_seed(seed_val)
    random.seed(seed_val)
    np.random.seed(seed_val)
    torch.manual_seed(seed_val)
    torch.random.manual_seed(seed_val)
    torch.cuda.manual_seed(seed_val)
    torch.cuda.manual_seed_all(seed_val)  # if using multi-GPU.
    os.environ['PYTHONHASHSEED'] = str(seed_val)
    torch.backends.cudnn.benchmark = True
    torch.backends.cudnn.deterministic = True


def extract_last_num(text: str) -> float:
    text = re.sub(r"(\d),(\d)", "\g<1>\g<2>", text) # 123,456
    res = re.findall(r"(\d+(\.\d+)?)", text)  # 123456.789
    if len(res) > 0:
        num_str = res[-1][0]
        return float(num_str)
    else:
        return 0.0