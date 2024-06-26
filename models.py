import os
from flask_login import UserMixin
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey

print(os.path.abspath(os.getcwd()))
database = create_engine(f'sqlite:///{os.path.abspath(os.getcwd())}/app.db', connect_args={'check_same_thread': False})
Session = sessionmaker(bind=database)
session = Session()
Base = declarative_base()


class User(UserMixin, Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String(100), unique=True)
    status = Column(String(10)) # teacher or student 
    password = Column(String(100))


class Exam(Base):
    __tablename__ = 'exams'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    questions = relationship('Question', back_populates='exam')

class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    exam_id = Column(Integer, ForeignKey('exams.id'))
    question = Column(String(256))
    answer1 = Column(String(256))
    answer2 = Column(String(256))
    correct = Column(String(256))
    exam = relationship('Exam', back_populates='questions')

if __name__ == "__main__":
    Base.metadata.create_all(database)