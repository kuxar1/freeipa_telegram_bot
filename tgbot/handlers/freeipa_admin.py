from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InputFile
from aiogram.utils.markdown import hcode, hbold

from tgbot.config import load_config
from tgbot.keyboards.inline import send_qr_keyboard
from tgbot.keyboards.callback_datas import click_find
from tgbot.handlers.states import FreeipaState, Mailing
from tgbot.keyboards.reply import admin_reply_keyboard
from tgbot.services.freeipa_methods import find_user, create_otp, find_otp, remove_otp, change_auth
from tgbot.services.send_mail import send_mail
from python_freeipa import exceptions

from tgbot.services.db_session_create import create_db_session
from tgbot.models.freeipa_db import Freeipa
import sqlalchemy.exc
from contextlib import suppress


# start
async def start_bot_admin(message: types.Message):
    await message.answer(f'Welcome!', reply_markup=admin_reply_keyboard)


# show info about freeipa user account
async def show_user_btn(message: types.Message):
    await message.answer(hbold('Enter FreeIPA login that you want to find:'))
    await FreeipaState.show_user_freeipa_st.set()


async def show_user_func(message: types.Message, state: FSMContext):
    answer = message.text.lower()
    user = await find_user(user_name=answer)
    if user['count'] == 0 or answer == 'admin':
        await message.answer(f'{answer}: User not found')
    else:
        await message.answer(text=f"""
{hbold('User login')}: {hcode(user['result'][0]['uid'][0])}
{hbold('Display name')}: {hcode(user['result'][0]['displayname'][0])}
{hbold('Mail')}: {hcode(user['result'][0]['mail'][0])}
     """)
    await state.finish()


# show info from database
async def show_db_user_btn(message: types.Message):
    await message.answer(hbold('Enter FreeIPA login that you want to find:'))
    await FreeipaState.show_user_db_st.set()


async def show_db_user_func(message: types.Message, state: FSMContext):
    answer = message.text.lower()
    config = load_config()
    session_maker = await create_db_session(config)
    with suppress(sqlalchemy.exc.IntegrityError):
        select_from_db = await Freeipa.get_freeipa_login(
            session_maker=session_maker,
            freeipa_login=answer
        )
        try:
            await message.answer(f"{hbold('Telegram_id:')} {hcode(select_from_db.telegram_id)}\n"
                                 f"{hbold('Telegram_name:')} {hcode(select_from_db.telegram_name)}\n"
                                 f"{hbold('FreeIPA login:')} {hcode(select_from_db.freeipa_login)}")
            await state.finish()
        except AttributeError:
            await message.answer(text=f'{answer}: user not registered in database')
        await state.finish()


# generate otp token
async def create_otp_btn(message: types.Message):
    await message.answer(hbold('Enter FreeIPA login:'))
    await FreeipaState.create_otp_st.set()


async def create_otp_func(message: types.Message, state: FSMContext):
    answer = message.text.lower()
    confing = load_config()
    qr_code_path = confing.misc.qr_code_path
    try:
        otp = await find_otp(user_name=answer)
        otp_quantity = otp['count']
        if otp_quantity != 0:
            otp_uid = otp['result'][0]['ipatokenuniqueid'][0]
            await remove_otp(uid=otp_uid)
            otp_url = await create_otp(user_name=answer)
            await change_auth(uid=answer)
            qr_img_send = InputFile(path_or_bytesio=f'{qr_code_path}/{answer}.png')
            await message.answer_photo(photo=qr_img_send, caption=f'qr code for {hcode(answer)} \n \n'
                                                                  f'{hcode(otp_url)}',
                                       reply_markup=send_qr_keyboard)
            await state.finish()
        else:
            otp_url = await create_otp(user_name=answer)
            await change_auth(uid=answer)
            qr_img_send = InputFile(path_or_bytesio=f'{qr_code_path}/{answer}.png')
            await message.answer_photo(photo=qr_img_send, caption=f'qr code for {hcode(answer)} \n \n'
                                                                  f'{hcode(otp_url)}',
                                       reply_markup=send_qr_keyboard)
            await state.finish()
    except exceptions.NotFound as err:
        await message.answer(text=f'{err}')
        await state.finish()


# send qr code
async def send_otp_btn(call: types.CallbackQuery):
    await call.message.answer('Enter user name:')
    await Mailing.send_otp.set()


async def send_otp_func(message: types.Message, state: FSMContext):
    answer = message.text.lower()
    confing = load_config()
    qr_code_path = confing.misc.qr_code_path
    session_maker = await create_db_session(confing)
    with suppress(sqlalchemy.exc.IntegrityError):
        select_from_db = await Freeipa.get_freeipa_login(
            session_maker=session_maker,
            freeipa_login=answer
        )
        try:
            telegram_id = select_from_db.telegram_id
            qr_img_send = InputFile(
                path_or_bytesio=f'{qr_code_path}/{answer}.png'
            )
            await message.bot.send_photo(chat_id=telegram_id, photo=qr_img_send, caption=f'qr code for {answer}')
            await message.answer('QR code successfully sent')
            await state.finish()
        except AttributeError:
            await message.answer(text=f'{answer}: user not registered in database')
            await state.finish()


# test db
async def send_mail_btn(message: types.Message):
    await message.answer(hbold('Enter user mail address:'))
    await Mailing.send_mail1.set()


async def send_mail_func1(message: types.Message, state: FSMContext):
    answer = message.text.lower()
    await state.update_data(mail_address=answer)
    await message.answer(hbold('Enter freeIPA username:'))
    await Mailing.send_mail2.set()


async def send_mail_func2(message: types.Message, state: FSMContext):
    data = await state.get_data()
    mail_address = data.get('mail_address')
    username = message.text

    await send_mail(receiver=mail_address, username=username)
    await message.answer('Mail was successfully sent')
    await state.finish()


def register_freeipa_admin(dp: Dispatcher):
    # start command
    dp.register_message_handler(start_bot_admin, commands='start', is_admin=True)
    # show info about freeipa account
    dp.register_message_handler(show_user_btn, text='Find user info from FreeIPA server')
    dp.register_message_handler(show_user_func, state=FreeipaState.show_user_freeipa_st)
    # show info about user from database
    dp.register_message_handler(show_db_user_btn, text='Find user info from database')
    dp.register_message_handler(show_db_user_func, state=FreeipaState.show_user_db_st)
    # generate otp token
    dp.register_message_handler(create_otp_btn, text='Create OTP Token')
    dp.register_message_handler(create_otp_func, state=FreeipaState.create_otp_st)
    # send qr code
    dp.register_callback_query_handler(send_otp_btn, click_find.filter(msg='send_otp'))
    dp.register_message_handler(send_otp_func, state=Mailing.send_otp)

    # test database methods
    dp.register_message_handler(send_mail_btn, text='Send OTP to mail')
    dp.register_message_handler(send_mail_func1, state=Mailing.send_mail1)
    dp.register_message_handler(send_mail_func2, state=Mailing.send_mail2)
