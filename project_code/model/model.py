from unsloth import FastLanguageModel, is_bfloat16_supported


def initialize(model_name, max_seq_length=512, load_in_4bit=False, dtype=None):
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name, max_seq_length, dtype, load_in_4bit)
    # model.generation_config.pad_token_ids = tokenizer.eos_token_id
    # tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "left"
    return model, tokenizer


def inference(model, tokenizer, inputs, language, alpaca_prompt, 
              padding=True, max_new_tokens=512, do_sample=False, use_cache=True, temperature=0.0):
    
    FastLanguageModel.for_inference(model)
    inputs = [inputs] if type(inputs) != list else inputs
    inputs = [alpaca_prompt.format(language=language, instruction=instruction, answer='') for instruction in inputs]
    inputs = tokenizer(inputs, return_tensors = 'pt', padding = padding).to('cuda')
    outputs = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=do_sample, use_cache=use_cache,
                             pad_token_id=tokenizer.eos_token_id, temperature=temperature)
    decoded = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    return decoded