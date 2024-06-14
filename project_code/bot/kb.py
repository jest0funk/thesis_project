from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

menu = [
    [InlineKeyboardButton(text="🌐 Switch to English", callback_data="0"),
    InlineKeyboardButton(text="🌐 Switch to Russian", callback_data="1")],
    [InlineKeyboardButton(text="🧩 Sample task in English", callback_data="sample_0"),
    InlineKeyboardButton(text="🧩 Sample task in Russian", callback_data="sample_1")],
    [InlineKeyboardButton(text="🏳 Toggle instruction visibility", callback_data="toggle_visibility")],
    [InlineKeyboardButton(text="🔍Help", callback_data="help")]
]

menu = InlineKeyboardMarkup(inline_keyboard=menu)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Call the menu")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Back to the menu", callback_data="menu")]])
