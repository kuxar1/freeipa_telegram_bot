from dataclasses import dataclass

from environs import Env
from typing import List


@dataclass
class FreeipaConfig:
    server: str
    user: str
    password: str


@dataclass
class MailConfig:
    server: str
    mail_acc: str
    password: str


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str
    admin_ids: List[int]
    use_redis: bool


@dataclass
class Miscellaneous:
    qr_code_path: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    freeipa: FreeipaConfig
    mail: MailConfig
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME')
        ),
        freeipa=FreeipaConfig(
            server=env.str('IPA_SERVER'),
            user=env.str('IPA_ADMIN'),
            password=env.str('IPA_PASS')
        ),
        mail=MailConfig(
            server=env.str('MAIL_SERVER'),
            mail_acc=env.str('MAIL_ACC'),
            password=env.str('MAIL_PASS')
        ),
        misc=Miscellaneous(
            qr_code_path=env.str('QR_CODE_PATH')
        ),
    )
