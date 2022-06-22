from aiogram.dispatcher.filters.state import StatesGroup, State


class FreeipaState(StatesGroup):
    show_user_freeipa_st = State()
    show_user_db_st = State()
    create_otp_st = State()
    add_login_st = State()
    test_state = State()


class Mailing(StatesGroup):
    send_otp = State()
    send_mail1 = State()
    send_mail2 = State()