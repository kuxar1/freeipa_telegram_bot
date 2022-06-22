import qrcode
from python_freeipa import ClientMeta, exceptions
from tgbot.config import load_config


# create connection to freeipa server
async def freeipa_server_get(server: str, login: str, password: str):
    try:
        client = ClientMeta(server)
        client.login(login, password)
        return client
    except exceptions.InvalidSessionPassword as err:
        print(err)


async def find_user(user_name: str):
    config = load_config('.env')
    connection = await freeipa_server_get(
        server=config.freeipa.server,
        login=config.freeipa.user,
        password=config.freeipa.password)
    user = connection.user_find(o_uid=user_name)
    return user


async def create_qr(data: str, username: str):
    qr_img = qrcode.make(data=data)
    qr_img.save(f'tgbot/qr_img/{username}.png')


async def create_otp(user_name: str):
    config = load_config('.env')
    connection = await freeipa_server_get(
        server=config.freeipa.server,
        login=config.freeipa.user,
        password=config.freeipa.password)
    otp = connection.otptoken_add(o_ipatokenowner=user_name, o_no_qrcode=True)
    otp_url = otp['result']['uri']
    await create_qr(data=otp_url, username=user_name)
    return otp_url


async def find_otp(user_name: str):
    config = load_config('.env')
    connection = await freeipa_server_get(
        server=config.freeipa.server,
        login=config.freeipa.user,
        password=config.freeipa.password
    )
    otp = connection.otptoken_find(o_ipatokenowner=user_name)
    return otp


async def remove_otp(uid: str):
    config = load_config('.env')
    connection = await freeipa_server_get(
        server=config.freeipa.server,
        login=config.freeipa.user,
        password=config.freeipa.password
    )
    connection.otptoken_del(a_ipatokenuniqueid=uid)


async def change_auth(uid: str):
    config = load_config('.env')
    connection = await freeipa_server_get(
        server=config.freeipa.server,
        login=config.freeipa.user,
        password=config.freeipa.password
    )
    connection.user_mod(a_uid=uid, o_ipauserauthtype='otp')
