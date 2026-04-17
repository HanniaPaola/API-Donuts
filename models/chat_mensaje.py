from sqlalchemy import BigInteger, Column, Integer, String, Text

from database import Base


class ChatMensaje(Base):
    __tablename__ = "chat_mensaje"

    id = Column(Integer, primary_key=True, autoincrement=True)
    room = Column(String(255), nullable=False, index=True)
    sender_id = Column(String(200), nullable=False)
    texto = Column(Text, nullable=False)
    ts_ms = Column(BigInteger, nullable=False)
