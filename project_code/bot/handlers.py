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

router = Router()

@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet, reply_markup=kb.menu)
    

@router.message(F.text == "Menu")
@router.message(F.text == "Call the menu")
@router.message(F.text == "Back to the menu")
@router.message(Command("menu"))
async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=kb.menu)

#----------------------------------------------------#
languages = ['English', 'Russian']
language = languages[0]
show_instructions = True
#----------------------------------------------------#

@router.callback_query(F.data == "0")
@router.callback_query(F.data == "1")
async def switch_language(clbck: CallbackQuery, state: FSMContext):
    global language
    language = languages[int(clbck.data)]
    await state.set_state(Gen.text_prompt)
    await clbck.message.edit_text(text.in_text.format(language=language))
    await clbck.message.answer(text.gen_exit, reply_markup=kb.exit_kb)


@router.message(Gen.text_prompt)
@flags.chat_action("typing")
async def generate_text(msg: Message, state: FSMContext):
    prompt = msg.text
    mesg = await msg.answer(text.gen_wait())
    res = utils.generate_text(prompt, language, text.alpaca_prompt)
    if not res:
        return await mesg.edit_text(text.gen_error, reply_markup=kb.iexit_kb)
    await mesg.edit_text(res.split(text.split_delimiter)[1] if not show_instructions else res, 
                         disable_web_page_preview=True)


@router.callback_query(F.data == "sample_0")
@router.callback_query(F.data == "sample_1")
@flags.chat_action("typing")
async def sample_task(clbck: CallbackQuery, state: FSMContext):
    language_idx = int(clbck.data[7:])
    language = languages[language_idx]
    prompt = text.sample_tasks[language_idx]
    await state.set_state(Gen.text_prompt)
    await clbck.message.edit_text(text.msg_delimiter + prompt + text.msg_delimiter)
    # await clbck.message.answer(text.gen_exit, reply_markup=kb.exit_kb)
    mesg = await clbck.message.answer(text.gen_wait())
    res = utils.generate_text(prompt, language, text.alpaca_prompt)
    if not res:
        await mesg.edit_text(text.gen_error) #, reply_markup=kb.iexit_kb)
    else: 
        await mesg.edit_text(res.split(text.split_delimiter)[1] if not show_instructions else res, 
                         disable_web_page_preview=True)
    await mesg.answer(text.menu, reply_markup=kb.menu)


@router.callback_query(F.data == "toggle_visibility")
async def toggle_visibility(clbck: CallbackQuery): #, state: FSMContext):
    global show_instructions
    show_instructions = not show_instructions
    # await state.set_state(Gen.text_prompt)
    await clbck.message.edit_text(text.toggle_text.format(toggle_state="ON" if show_instructions else "OFF"))
    await clbck.message.answer(text.menu, reply_markup=kb.menu)
