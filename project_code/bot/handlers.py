from aiogram import F, Router, types
from aiogram.filters import Command, or_f
from aiogram.types import Message
from aiogram import flags
from aiogram.fsm.context import FSMContext
from aiogram.types.callback_query import CallbackQuery

import utils
from states import Gen

import kb
import text


#----------------------------------------------------#
user_settings = dict()
#----------------------------------------------------#

router = Router()

@router.message(Command("start"))
async def start_handler(msg: Message, user_settings=user_settings):
    user_settings[str(msg.from_user.id)] = {}
    user_settings[str(msg.from_user.id)]['show_instructions'] = True
    user_settings[str(msg.from_user.id)]['show_exclamations'] = True
    user_settings[str(msg.from_user.id)]['language'] = "English"
    await msg.answer(text.greet, reply_markup=kb.menu)


@router.callback_query(F.data == "menu")
@router.message(F.text == "Menu")
@router.message(F.text == "Back to the menu")
@router.message(Command("menu"))
async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=kb.menu)


@router.callback_query(F.data == "English")
@router.callback_query(F.data == "Chinese")
@router.callback_query(F.data == "French")
@router.callback_query(F.data == "German")
@router.callback_query(F.data == "Japanese")
@router.callback_query(F.data == "Russian")
@router.callback_query(F.data == "Spanish")
@router.callback_query(F.data == "Swahili")
@router.callback_query(F.data == "sample_English")
@router.callback_query(F.data == "sample_Chinese")
@router.callback_query(F.data == "sample_French")
@router.callback_query(F.data == "sample_German")
@router.callback_query(F.data == "sample_Japanese")
@router.callback_query(F.data == "sample_Russian")
@router.callback_query(F.data == "sample_Spanish")
@router.callback_query(F.data == "sample_Swahili")
async def switch_language(clbck: CallbackQuery, state: FSMContext, user_settings=user_settings):
    sample_task = True if clbck.data[:7] == "sample_" else False
    language = str(clbck.data[7:]) if sample_task else str(clbck.data)
    user_settings[str(clbck.from_user.id)]['language'] = language
    state = await state.set_state(Gen.text_prompt)
    await clbck.message.answer(text.in_text.format(language=language), reply_markup=kb.exit_kb)
    # await clbck.message.answer(text.gen_exit, reply_markup=kb.exit_kb)
    if sample_task:
        prompt = text.sample_tasks[language]
        msg = await clbck.message.answer(text.msg_delimiter + prompt + text.msg_delimiter)
        await generate_text(msg, state, clbck.from_user.id)



@router.message(Gen.text_prompt)
@flags.chat_action("typing")
async def generate_text(msg: Message, state: FSMContext, user_id=0):
    d_len = len(text.msg_delimiter)-1
    prompt = msg.text if user_id == 0 else msg.text[d_len:-d_len].strip()
    user_id = msg.from_user.id if user_id == 0 else user_id
    language = user_settings[str(user_id)]['language']
    show_exclamations = user_settings[str(user_id)]['show_exclamations']
    mesg = await msg.answer(text.gen_wait() if show_exclamations else text.gen_standard)
    res = utils.generate_text(prompt, language, text.alpaca_prompt)
    if not res:
        return await mesg.edit_text(text.gen_error, reply_markup=kb.exit_kb)
    show_instructions = user_settings[str(user_id)]['show_instructions']
    await mesg.edit_text(res.split(text.split_delimiter)[1] if not show_instructions else res, 
                         disable_web_page_preview=True)



@router.callback_query(F.data == "show_instructions")
@router.callback_query(F.data == "show_exclamations")
async def toggle_visibility(clbck: CallbackQuery, user_settings=user_settings): 
    toggle_pointer = str(clbck.data)
    toggle_state = not user_settings[str(clbck.from_user.id)][toggle_pointer]
    user_settings[str(clbck.from_user.id)][toggle_pointer] = toggle_state
    await clbck.message.answer(text.toggle_text[toggle_pointer].format(toggle_state="ON" if toggle_state else "OFF"), reply_markup=kb.exit_kb)
