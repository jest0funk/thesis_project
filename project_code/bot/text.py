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

gen_standard = "..."

sample_tasks = {
    "English": "Two hens lay 2 eggs in two days. How many eggs will 4 hens lay in three days?",
    "Chinese": "两只母鸡在两天内产下2个蛋。 4只母鸡在三天内会下多少个蛋？",
    "French": "Deux poules pondent 2 œufs en deux jours. Combien d'œufs 4 poules pondent en trois jours?",
    "German": "Zwei Hühner legen 2 Eier in zwei Tagen. Wie viele Eier werden 4 Hühner in drei Tagen legen?",
    "Japanese": "2つの鶏は2日で2つの卵を産みます。 4羽の鶏は3日でいくつの卵を産みますか？",
    "Russian": "Две курицы сносят 2 яйца за два дня. Сколько яиц снесут 4 курицы за три дня?",
    "Spanish": "Dos gallinas ponen 2 huevos en dos días. ¿Cuántos huevos pondrán 4 gallinas en tres días?",
    "Swahili": "Kuku wawili hutaga mayai 2 kwa siku mbili. Kuku 4 watataga mayai mangapi kwa siku tatu?"
}

toggle_text = {'show_instructions': "--- Visibility of repeated prompt instruction is turned {toggle_state}",
               'show_exclamations': "--- Pre-generation funny bot messages are turned {toggle_state}"}
split_delimiter = "### Response:\n"

msg_delimiter = f"\n{'-'*20}\n"
