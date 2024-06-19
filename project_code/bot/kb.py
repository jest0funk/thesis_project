from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

menu = [
    [InlineKeyboardButton(text="🇬🇧 English", callback_data="English"),
    InlineKeyboardButton(text="🧩 Sample task in English", callback_data="sample_English")],
    [InlineKeyboardButton(text="🇨🇳 Chinese", callback_data="Chinese"),
    InlineKeyboardButton(text="🧩 Sample task in Chinese", callback_data="sample_Chinese")],
    [InlineKeyboardButton(text="🇫🇷 French", callback_data="French"),
    InlineKeyboardButton(text="🧩 Sample task in French", callback_data="sample_French")],
    [InlineKeyboardButton(text="🇩🇪 German", callback_data="German"),
    InlineKeyboardButton(text="🧩 Sample task in German", callback_data="sample_German")],
    [InlineKeyboardButton(text="🇯🇵 Japanese", callback_data="Japanese"),
    InlineKeyboardButton(text="🧩 Sample task in Japanese", callback_data="sample_Japanese")],
    [InlineKeyboardButton(text="🇷🇺 Russian", callback_data="Russian"),
    InlineKeyboardButton(text="🧩 Sample task in Russian", callback_data="sample_Russian")],
    [InlineKeyboardButton(text="🇪🇦 Spanish", callback_data="Spanish"),
    InlineKeyboardButton(text="🧩 Sample task in Spanish", callback_data="sample_Spanish")],
    [InlineKeyboardButton(text="🇸🇿 Swahili", callback_data="Swahili"),
    InlineKeyboardButton(text="🧩 Sample task in Swahili", callback_data="sample_Swahili")],
    [InlineKeyboardButton(text="⚙ Toggle instruction visibility", callback_data="show_instructions"),
    InlineKeyboardButton(text="⚙ Toggle funny messages", callback_data="show_exclamations")],
    [InlineKeyboardButton(text="🔍Help", callback_data="help")]
]

menu = InlineKeyboardMarkup(inline_keyboard=menu)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Back to the menu")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Back to the menu", callback_data="menu")]])


