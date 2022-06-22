from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.keyboards.callback_datas import click_find

keyboard_admin = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Help', callback_data=click_find.new(msg='help'))
        ],
        [
            InlineKeyboardButton(text='Show user info', callback_data=click_find.new(msg='show_user'))
        ],
        [
            InlineKeyboardButton(text='Create OTP', callback_data=click_find.new(msg='create_otp'))
        ],
        [
            InlineKeyboardButton(text='DB Test', callback_data=click_find.new(msg='db'))
        ],
        [
            InlineKeyboardButton(text='Telegram user info', callback_data=click_find.new(msg='tg_info'))
        ]
    ]
)

keyboard_user = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Help', callback_data=click_find.new(msg='help'))
        ],
        [
            InlineKeyboardButton(text='Registration', callback_data=click_find.new(msg='register'))
        ]
    ]
)

send_qr_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Send QR code', callback_data=click_find.new(msg='send_otp'))
        ]
    ]
)