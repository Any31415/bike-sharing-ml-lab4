import os
from sqlalchemy import create_engine, Column, Integer, Float, TIMESTAMP, func
from sqlalchemy.orm import declarative_base, sessionmaker

# читаем настройки подключения из переменных окружения (не хардкодим!)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# строка подключения для SQLAlchemy: диалект+драйвер://пользователь:пароль@хост:порт/база
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    season = Column(Integer, nullable=False)
    holiday = Column(Integer, nullable=False)
    workingday = Column(Integer, nullable=False)
    weather = Column(Integer, nullable=False)
    temp = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    windspeed = Column(Float, nullable=False)
    hour = Column(Integer, nullable=False)
    dayofweek = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    predicted_count = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())


def save_prediction(features: dict, predicted_count: float):
    """Сохраняет один запрос+результат предсказания в базу"""
    session = SessionLocal()
    try:
        record = Prediction(**features, predicted_count=predicted_count)
        session.add(record)
        session.commit()
    finally:
        session.close()

Base.metadata.create_all(bind=engine)
