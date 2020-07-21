from sqlalchemy import *
from sqlalchemy.orm import *

class user(object):
	def __init__(self, name, age, passwd):
		self.name = name
		self.age = age
		self.passwd = passwd

db = create_engine('sqlite:///test.db')

metadata = MetaData(db)

metadata.create_all(checkfirst=True)

users = Table('users', metadata,
	Column('user_id', Integer, primary_key=True),
	Column('name', String(40)),
	Column('age', Integer),
	Column('passwd', String)
)

users.create(checkfirst=True)

mapper(user, users)

Session = sessionmaker(bind=db)
session = Session()

item = user('Faker', 25, 'passwd')

session.add(item)

session.commit()

u = session.query(user).filter_by(age=25).first()

print u.age
