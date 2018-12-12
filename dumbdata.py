from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, User, Category, Item

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Add default user
basic_user = User(name='Mohammed Mustafa', username='dotmido',
                  email='mjavax@gmail.com', imageurl='/images/default.jpg')

session.add(basic_user)
session.commit()

# Add 4 Categories
category1 = Category(name='Watches', user_id=1)
session.add(category1)
session.commit()

category2 = Category(name='Laptops', user_id=1)
session.add(category1)
session.commit()

category3 = Category(name='Phones', user_id=1)
session.add(category1)
session.commit()

category4 = Category(name='TVs', user_id=1)
session.add(category1)
session.commit()


# Add some items to categories

item1 = Item(name='Casio G-Shock',
             description='Casio G-Shock Analog digital for Men',
             category_id=1, user_id=1)
session.add(item1)
session.commit()

item2 = Item(name='Casio Youth',
             description='Combination Analog-Digital Gold Dial Watch for Men',
             category_id=1, user_id=1)
session.Add(item2)
session.commit()

description = """Laptop - Intel Celeron N3060,
             11.6 Inch, 16 GB Flash Memory, 4 GB RAM, Black""",
item3 = Item(name='HP Chromebook',
             category_id=2, user_id=1)
session.Add(item3)
session.commit()

item4 = Item('Apple MacBook Air',
             description="""13-inch Retina display,
             1.6GHz dual-core Intel Core i5,
             128GB - Silver (Latest Model)""",
             category_id=2, user_id=1)
session.Add(item4)
session.commit()

item5 = Item('iPhone 5S', description="""Apple iPhone 5S 16GB GSM Unlocked,
             Space Gray""",
             category_id=3, user_id=1)
session.Add(item5)
session.commit()

item6 = Item('iPhone 6S', description='Apple iPhone 6S (32GB) - Space Gray',
             category_id=3, user_id=1)
session.Add(item6)
session.commit()

item7 = Item('Sony XBR65X900F',
             description='65-Inch 4K Ultra HD Smart LED TV (2018 Model)',
             category_id=4, user_id=1)
session.Add(item7)
session.commit()

item8 = Item('Toshiba 43LF621U19',
             description="""43-inch 4K Ultra HD Smart LED TV HDR,
             Fire TV Edition""",
             category_id=4, user_id=1)
session.Add(item8)
session.commit()

print "Dump data added!"
