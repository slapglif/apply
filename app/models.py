from app import db_session,Base
from sqlalchemy import Column, Integer, String, Boolean, BLOB

class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    steam_id = Column(String(40))
    nickname = Column(String(80))
    email = Column(String(80))
    community = Column(String(80))
    ign = Column(String(80))
    div = Column(String(80))
    time = Column(String(80))
    admin = Column(Boolean())
    skills = Column(String())
    stuff = Column(String())
    bio = Column(String())
    disciplines = Column(String())
    date = Column(String())
    age = Column(String())
    status = Column(String())
    flag = Column(String())
    voteye = Column(Integer())
    voteno = Column(Integer())
    voted = Column(String())
    vflag = Column(Integer())
    rank = Column(String())



    @staticmethod
    def get_or_create(steam_id):
        rv = User.query.filter_by(steam_id=steam_id).first()
        if rv is None:
            rv = User()
            rv.steam_id = steam_id
            db_session.add(rv)
            db_session.close()
        return rv

    def __repr__(self):
        """docstring for __repr__"""
        return self.nickname