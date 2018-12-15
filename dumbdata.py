#!/usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, User, Category, Item

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Add 4 Categories
category1 = Category(name='Watches', user_id=1)
session.add(category1)
session.commit()

category2 = Category(name='Laptops', user_id=1)
session.add(category2)
session.commit()

category3 = Category(name='Phones', user_id=1)
session.add(category3)
session.commit()

category4 = Category(name='TVs', user_id=1)
session.add(category4)
session.commit()


# Add some items to categories

item1 = Item(name='Casio G-Shock',
             description='Casio G-Shock Analog digital for Men',
             price=60,
             category_id=1, user_id=1)
session.add(item1)
session.commit()

item2 = Item(name='Casio Youth',
             description='Combination Analog-Digital Gold Dial Watch for Men',
             price=110,
             category_id=1, user_id=1)
session.add(item2)
session.commit()


item3 = Item(name='HP Chromebook',
             description='Laptop - Intel Celeron N3060',
             price=3500,
             category_id=1, user_id=1)
session.add(item3)
session.commit()

item4 = Item(name='Apple MacBook',
             description="""13-inch Retina display
             1.6GHz dual-core Intel Core i5""",
             price=6750,
             category_id=2, user_id=1)
session.add(item4)
session.commit()

item5 = Item(name='iPhone 5S',
             description="""Apple iPhone 5S 16GB GSM Unlocked,
             Space Gray""",
             price=450,
             category_id=3, user_id=1)
session.add(item5)
session.commit()

item6 = Item(name='iPhone 6S',
             description='Apple iPhone 6S (32GB) - Space Gray',
             price=550,
             category_id=3, user_id=1)
session.add(item6)
session.commit()

item7 = Item(name='Sony XBR65X900F',
             description='65-Inch 4K Ultra HD Smart LED TV (2018 Model)',
             price=400,
             category_id=4, user_id=1)
session.add(item7)
session.commit()

item8 = Item(name='Toshiba 43LF621U19',
             description="""43-inch 4K Ultra HD Smart LED TV HDR,
             Fire TV Edition""",
             price=600,
             category_id=4, user_id=1)
session.add(item8)
session.commit()

print "Dump data added!"
