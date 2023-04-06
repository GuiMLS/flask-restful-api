from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///messages.db')
# engine = create_engine('sqlite:///atividades.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

class Apps(Base):
    __tablename__='apps'
    id = Column(Integer, primary_key=True)
    name = Column(String(40), index=True, unique=True)
    context = Column(String(40))

    def __repr__(self):
        return '<App {}>'.format(self.name)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

class Messages(Base):
    __tablename__='messages'
    id = Column(Integer, primary_key=True)
    content = Column(String(80))
    from_user = Column(String(20))
    to_user = Column(String(20))
    app_id = Column(Integer, ForeignKey('apps.id'))
    app = relationship("Apps")

    def __repr__(self):
        return '<Messages {}>'.format(self.content)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String(20), unique=True)
    password = Column(String(20))
    role = Column(String(20))

    def __repr__(self):
        return '<User {}>'.format(self.login)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db()

