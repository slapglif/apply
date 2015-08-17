from flask import Flask, redirect, session, json, g
import urllib2, re
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


app = Flask(__name__)
db = SQLAlchemy(app)
db.init_app(app)
engine = create_engine('sqlite:///app.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,

                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import app.models
    from app import views
    Base.metadata.create_all(bind=engine)

init_db()