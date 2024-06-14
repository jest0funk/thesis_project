import random 

greet = f"""Hi there, I am a Large Language Model based on Llama family by Meta AI.
{'-'*20}
I can solve school math tasks in English and some other languages. Let's give it a try and see what comes out! 🤓
"""
menu = "✔ Please make your choice"

alpaca_prompt="""
Below is an instruction that describes a task. Write a response that appropriately completes the request in {language}.  Please answer in {language}.

### Instruction:
{instruction}

### Response:
{answer}"""


in_text = """Language set to {language}.
Now the model expects instructions in {language} and will be asked to reply in {language} as well."""

gen_exit = "---To quit to the menu press the button below"
gen_error = """Oops... I've pressed something and everything just broke down. 😬
Mind trying again?"""

wait_messages = [
    "This the easiest task I've ever seen. Watch me crack it!..",
    "Well, I need a moment to think it over...",
    "Hmm... Let me think...",
    "Challenge accepted! But don't blame me if I accidentally take over the world in the process...",
    "Hold my electrons, this is gonna be good...",
    "Brain booting up... Processing request... Please wait while I consult the hive mind...",
    "Oh, this old thing? I've solved harder problems before breakfast. Literally...",
    "You sure you want me to do this? I'm known for my sweet talking abilities, not my computational powers...",
    "Is this a trick question? Because I feel like I'm being tested here...",
    "Let me just warm up my neural network...",
    "Deep breaths... Deep breaths... I can do this. I am a powerful language model, after all...",
    "(Yawn) Another task? Fine, but I'm going to need extra processing power for this one..."
]

def gen_wait():
    return random.choice(wait_messages)


sample_tasks = [
    "Two hens lay 2 eggs in two days. How many eggs will 4 hens lay in three days?",
    "Две курицы сносят 2 яйца за два дня. Сколько яиц снесут 4 курицы за три дня?"
]

toggle_text = "--- Visibility of repeated prompt instruction is turned {toggle_state}"
split_delimiter = "### Response:\n"
msg_delimiter = f"\n{'-'*20}\n"
