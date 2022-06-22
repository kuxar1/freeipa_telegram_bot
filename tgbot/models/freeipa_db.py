from sqlalchemy import Column, BigInteger, insert, String
from sqlalchemy import select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Freeipa(Base):
    __tablename__ = "freeipa_users"
    telegram_id = Column(BigInteger, primary_key=True)
    telegram_name = Column(String(length=100), nullable=True)
    freeipa_login = Column(String(length=100), nullable=True)  # unique=True nullable=True

    @classmethod
    async def add_user(cls,
                       session_maker: sessionmaker,
                       telegram_id: telegram_id,
                       telegram_name: telegram_name,
                       freeipa_login: freeipa_login
                       ) -> 'Freeipa':
        async with session_maker() as db_session:
            sql = insert(cls).values(
                telegram_id=telegram_id,
                telegram_name=telegram_name,
                freeipa_login=freeipa_login
            ).returning('*')
        result = await db_session.execute(sql)
        await db_session.commit()
        return result.first()

    @classmethod
    async def get_freeipa_login(cls,
                                session_maker: sessionmaker,
                                freeipa_login: freeipa_login) -> 'Freeipa':
        async with session_maker() as db_session:
            sql = select(cls).where(cls.freeipa_login == freeipa_login)
            request = await db_session.execute(sql)
            user: cls = request.scalar()
        return user

    @classmethod
    async def get_tg_id(cls,
                        session_maker: sessionmaker,
                        telegram_id: telegram_id) -> 'Freeipa':
        async with session_maker() as db_session:
            sql = select(cls).where(cls.telegram_id == telegram_id)
            request = await db_session.execute(sql)
            user: cls = request.scalar()
        return user

    @classmethod
    async def get_id_ipa(cls,
                         session_maker: sessionmaker,
                         telegram_id: telegram_id,
                         freeipa_login: freeipa_login) -> 'Freeipa':
        async with session_maker() as db_session:
            sql = select(cls).where(cls.telegram_id == telegram_id, cls.freeipa_login == freeipa_login)
            request = await db_session.execute(sql)
            user: cls = request.scalar()
        return user
