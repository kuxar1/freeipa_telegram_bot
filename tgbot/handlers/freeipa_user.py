from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hbold

from tgbot.config import load_config
from tgbot.keyboards.inline import keyboard_user
from tgbot.keyboards.callback_datas import click_find
from tgbot.handlers.states import FreeipaState
from tgbot.services.freeipa_methods import find_user

from tgbot.services.db_session_create import create_db_session
from tgbot.models.freeipa_db import Freeipa
import sqlalchemy.exc
from contextlib import suppress


# start
async def start_bot_admin(message: types.Message):
    await message.answer(f'Welcome!', reply_markup=keyboard_user)


async def help_msg(call: types.CallbackQuery):
    await call.answer(cache_time=5)
    await call.message.answer('This is help message')


async def register_user_btn(call: types.CallbackQuery):
    await call.answer(cache_time=5)
    await call.message.answer('Enter your freeIPA login:')
    await FreeipaState.add_login_st.set()


async def register_user_func(message: types.Message, state: FSMContext):
    answer = message.text.lower()
    telegram_name = message.from_user.username
    telegram_id = message.from_user.id
    config = load_config()
    session_maker = await create_db_session(config)
    ipa_user = await find_user(user_name=answer)

    if ipa_user['count'] == 0:
        await message.answer(f'User {hbold(answer)} not found on freeIPA server')
        await state.finish()
    else:
        with suppress(sqlalchemy.exc.IntegrityError):
            try:
                tg = await Freeipa.get_id_ipa(
                    session_maker=session_maker,
                    telegram_id=telegram_id,
                    freeipa_login=answer
                )
                await message.answer(f'You already registered in database, you account name: {hbold(tg.freeipa_login)}')
                await state.finish()
            except AttributeError:
                try:
                    ipa = await Freeipa.get_freeipa_login(
                        session_maker=session_maker,
                        freeipa_login=answer
                    )
                    await message.answer(
                        f'Login {hbold(ipa.freeipa_login)} already registered in database.')
                    await state.finish()
                except AttributeError:
                    try:
                        tg_id = await Freeipa.get_tg_id(
                            session_maker=session_maker,
                            telegram_id=telegram_id
                        )
                        if tg_id.telegram_id == telegram_id:
                            await message.answer(
                                f'You already registered in database, you account name: {hbold(tg_id.freeipa_login)}')
                        await state.finish()
                    except AttributeError:
                        await Freeipa.add_user(
                            session_maker=session_maker,
                            telegram_id=telegram_id,
                            telegram_name=telegram_name,
                            freeipa_login=answer
                        )
                        await message.answer(
                            text=f"You're successfully registered in database, your account information:\n"
                                 f"{hbold('Telegram name:')} {telegram_name}\n"
                                 f"{hbold('FreeIPA login:')} {answer}")
                    await state.finish()


def register_freeipa_user(dp: Dispatcher):
    # start command
    dp.register_message_handler(start_bot_admin, commands='start')
    # help message
    dp.register_callback_query_handler(help_msg, click_find.filter(msg='help'))
    # show info about freeipa account
    dp.register_callback_query_handler(register_user_btn, click_find.filter(msg='register'))
    dp.register_message_handler(register_user_func, state=FreeipaState.add_login_st)
