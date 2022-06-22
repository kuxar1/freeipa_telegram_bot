from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_reply_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Find user info from FreeIPA server"),
            KeyboardButton(text="Create OTP Token")
        ],
        [
            KeyboardButton(text='Find user info from database'),
            KeyboardButton(text="Send OTP to mail")
        ]
    ],
    resize_keyboard=True
)
