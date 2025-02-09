from pathlib import Path
from typing import List, Optional
from sqlalchemy import (
    Table,
    Column,
    Integer,
    create_engine,
    ForeignKey,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    Session,
)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    pass


association_table = Table(
    "association_table",
    Base.metadata,
    Column("chat_id", Integer, ForeignKey("chat.chat_id"), primary_key=True),
    Column("username", Integer, ForeignKey("operator.username"), primary_key=True),
)


class Chat(Base):
    __tablename__ = "chat"

    chat_id: Mapped[int] = Column(Integer, unique=True)
    is_on: Mapped[bool]
    balance: Mapped["Balance"] = relationship()
    payment: Mapped["Payment"] = relationship()
    rate: Mapped["Rate"] = relationship()
    course: Mapped["Course"] = relationship()
    deposit: Mapped["Deposit"] = relationship()
    operators: Mapped[List["Operator"]] = relationship(
        "Operator", secondary=association_table, back_populates="chats"
    )
    history: Mapped[List["History"]] = relationship()


class History(Base):
    __tablename__ = "history"

    chat_id: Mapped[int] = Column(Integer, (ForeignKey("chat.chat_id")))
    date: Mapped[str]
    num: Mapped[str]


class Operator(Base):
    __tablename__ = "operator"

    chats: Mapped[List["Chat"]] = relationship(
        "Chat", secondary=association_table, back_populates="operators"
    )
    username: Mapped[str]


class Balance(Base):
    __tablename__ = "balance"

    chat_id: Mapped[int] = Column(Integer, (ForeignKey("chat.chat_id")), unique=True)
    usdt: Mapped[float] = Column(Integer, default=0)
    rub: Mapped[float] = Column(Integer, default=0)


class Payment(Base):
    __tablename__ = "payment"

    chat_id: Mapped[int] = Column(Integer, (ForeignKey("chat.chat_id")), unique=True)
    usdt: Mapped[float] = Column(Integer, default=0)
    rub: Mapped[float] = Column(Integer, default=0)


class Rate(Base):
    __tablename__ = "rate"

    chat_id: Mapped[int] = Column(Integer, (ForeignKey("chat.chat_id")), unique=True)
    rate: Mapped[float] = Column(Integer, default=0)


class Course(Base):
    __tablename__ = "course"
    chat_id: Mapped[int] = Column(Integer, (ForeignKey("chat.chat_id")), unique=True)
    course: Mapped[float] = Column(Integer, default=90)


class Deposit(Base):
    __tablename__ = "deposit"
    chat_id: Mapped[int] = Column(Integer, (ForeignKey("chat.chat_id")), unique=True)
    deposit: Mapped[float] = Column(Integer, default=0)


engine = create_engine(f"sqlite+pysqlite:///{Path(__file__).parent}\\bot.db")

Base.metadata.create_all(engine)

session = Session(engine)


async def add_chat(chat_id):
    try:
        session.add(Chat(chat_id=chat_id, is_on=True))
        session.commit()
    except:
        session.rollback()


async def get_chat(chat_id):
    return session.query(Chat).filter(Chat.chat_id == chat_id).first()


async def update_chat(chat_id, is_on):
    session.query(Chat).filter(Chat.chat_id == chat_id).update({"is_on": is_on})
    session.commit()


async def get_balance(chat_id):
    return session.query(Balance).filter(Balance.chat_id == chat_id).first()


async def set_balance(chat_id):
    try:
        session.add(Balance(chat_id=chat_id))
        session.commit()
    except:
        session.rollback()


async def update_balance(chat_id, rub, usdt):
    session.query(Balance).filter(Balance.chat_id == chat_id).update(
        {"rub": rub, "usdt": usdt}
    )
    session.commit()


async def set_payment(chat_id):
    try:
        session.add(Payment(chat_id=chat_id))
        session.commit()
    except:
        session.rollback()


async def get_payment(chat_id):
    return session.query(Payment).filter(Payment.chat_id == chat_id).first()


async def update_payment(chat_id, rub, usdt):
    session.query(Payment).filter(Payment.chat_id == chat_id).update(
        {"rub": rub, "usdt": usdt}
    )
    session.commit()


async def set_rate(chat_id):
    try:
        session.add(Rate(chat_id=chat_id))
        session.commit()
    except:
        session.rollback()


async def get_rate(chat_id):
    return session.query(Rate).filter(Rate.chat_id == chat_id).first()


async def update_rate(chat_id, rate):
    session.query(Rate).filter(Rate.chat_id == chat_id).update({"rate": rate})
    session.commit()


async def set_course(chat_id):
    try:
        session.add(Course(chat_id=chat_id))
        session.commit()
    except:
        session.rollback()


async def get_course(chat_id):
    return session.query(Course).filter(Course.chat_id == chat_id).first()


async def update_course(chat_id, course):
    session.query(Course).filter(Course.chat_id == chat_id).update({"course": course})
    session.commit()


async def set_deposit(chat_id):
    try:
        session.add(Deposit(chat_id=chat_id))
        session.commit()
    except:
        session.rollback()


async def get_deposit(chat_id):
    return session.query(Deposit).filter(Deposit.chat_id == chat_id).first()


async def update_deposit(chat_id, deposit):
    session.query(Deposit).filter(Deposit.chat_id == chat_id).update(
        {"deposit": deposit}
    )
    session.commit()


async def get_operator(username):
    return session.query(Operator).filter(Operator.username == username).first()


async def get_operator_by_chat_id(chat_id, username):
    return (
        session.query(Operator)
        .filter(Operator.username == username and Chat.chat_id == chat_id)
        .first()
    )


async def add_operator(chat_id, username):
    operator = await get_operator(username)
    chat = await get_chat(chat_id)

    if operator:
        operator.chats.append(chat)
        session.commit()
        return

    operator = Operator(username=username)
    chat.operators.append(operator)
    session.add(operator)
    session.commit()

async def delete_operator(username):
    session.query(Operator).filter(Operator.username == username).delete()
    session.commit()

async def update_history(chat_id, date, num):
    history = (
        session.query(History)
        .filter(History.chat_id == chat_id)
        .order_by(History.id.asc())
        .limit(5)
        .all()
    )

    if len(history) > 4:
        id = history[-5].id
        session.query(History).filter(History.id == id).delete()

    session.add(History(chat_id=chat_id, date=date, num=num))
    session.commit()


async def clear_history(chat_id):
    session.query(History).filter(History.chat_id == chat_id).delete()
    session.commit()
