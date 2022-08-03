import logging
import pandas
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import config, db_functions, checking_functions

logging.basicConfig(level=logging.INFO)

bot = Bot(token = config.TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class Form(StatesGroup):
    add = State()
    delete = State()
    pos = State()
    setid = State()

@dp.message_handler(commands=['start', 'help', 'start@hse_abit_2022_bot', 'help@hse_abit_2022_bot'])
async def send_welcome(message):
    await bot.send_message(message.chat.id, config.help_text, parse_mode="Markdown", disable_web_page_preview=True)

@dp.message_handler(commands=['set', 'set@hse_abit_2022_bot'])
async def set_cmd(message):
    await Form.setid.set()
    await message.answer(config.snils_text, disable_web_page_preview=True, parse_mode="Markdown")

@dp.message_handler(commands=['pos', 'pos@hse_abit_2022_bot'])
async def pos_cmd(message):
    try:
        if await db_functions.get_snils(message.from_user.id) == []:
            await message.answer('_Похоже ты не указал свой балл ЕГЭ или номер СНИЛС_\nМожешь это сделать с помощью команды /set', parse_mode="Markdown")
        else:
            await Form.pos.set()
            await message.answer(config.add_del_msg, parse_mode="Markdown", disable_web_page_preview=True)
    except:
        await message.answer('База данных не отвечает')

@dp.message_handler(commands=['add', 'add@hse_abit_2022_bot'])
async def add_cmd(message):
    await Form.add.set()
    await message.answer(config.add_del_msg, parse_mode="Markdown", disable_web_page_preview=True)

@dp.message_handler(commands=['del', 'del@hse_abit_2022_bot'])
async def del_cmd(message):
    await Form.delete.set()
    await message.answer(config.add_del_msg, parse_mode="Markdown", disable_web_page_preview=True)

@dp.message_handler(state=[Form.pos])
async def send_pos(message, state: FSMContext):
    await state.finish()
    try:
        msg = ''
        try:
            info = await db_functions.get_program_info_by_url(message.text[:message.text.find("?")])
        except:
            info = await db_functions.get_program_info_by_url(message.text)
        prog = info[0]
        position = await db_functions.get_pos(message.from_user.id, prog)
        if position is None:
            await message.answer('_Похоже ты неправильно указал свой балл ЕГЭ или номер СНИЛС_\nМожешь изменить его с помощью команды /set',parse_mode="Markdown")
        else:
            sheet = pandas.read_csv(f'csvfiles/{prog}.csv')
            msg += sheet.iat[0, 2]
            msg += f' {info[8]}\n'
            msg += '_Место в списке:_ *' + str(position) + '*\n'
            await message.answer(msg, parse_mode="Markdown")
    except:
        await message.reply('Проверь еще раз ссылку или указанный СНИЛС/балл ЕГЭ')


@dp.message_handler(state=[Form.setid])
async def set_id(message, state: FSMContext):
    await state.finish()
    try:
        if message.text.isdigit() or await checking_functions.issnils(message.text):
            await db_functions.add_snils(message.text, message.from_user.id)
            await message.reply('Добавил :)')
        else:
            await message.answer('_Похоже ты неправильно указал свой балл ЕГЭ или номер СНИЛС_\nМожешь изменить его с помощью команды /set',parse_mode="Markdown")
    except:
        await message.answer('База данных не отвечает')


@dp.message_handler(state=[Form.delete, Form.add])
async def get_prog(message: types.Message, state: FSMContext):
    try:
        try:
            info = await db_functions.get_program_info_by_url(message.text[:message.text.find("?")])
        except:
            info = await db_functions.get_program_info_by_url(message.text)
        program = info[0]
        current_state = await state.get_state()
        if current_state == 'Form:add':
            await bot.send_message(message.chat.id, await db_functions.add_user(program, message.from_user.id), parse_mode=types.ParseMode.MARKDOWN)
        elif current_state == 'Form:delete':
            await db_functions.del_user(program, message.from_user.id)
            await message.reply('Удалил эту программу у тебя')
        else:
            await message.reply('Ты уже добавил уведомление на эту программу')
    except:
        await message.reply('Ты уже добавил уведомление на эту программу')
    await state.finish()


async def sending(list_snd):
    for program in list_snd:
        info = await db_functions.get_program_info(program)
        msg = info[2]
        for id in await db_functions.get_users_by_program(program):
            try:
                pos = await db_functions.get_pos(id[0], program)
                if pos is None:
                    await bot.send_message(str(id[0]), msg, parse_mode=types.ParseMode.MARKDOWN)
                else:
                    await bot.send_message(str(id[0]), f'{msg}\n_Место в списке:_ *{pos}*\n', parse_mode=types.ParseMode.MARKDOWN)
            except:
                print('Error bot was blocked')

if __name__ == '__main__':
    sched = AsyncIOScheduler()
    sched.add_job(checking_functions.checking, 'cron', minute = f'5-59/{config.check_every}')
    sched.start()
    executor.start_polling(dp, skip_updates=True)