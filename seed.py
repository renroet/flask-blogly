from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()



u1 = User(first_name='John', last_name='Dorian', email='jdisthebest@gmail.com', image_url='https://i.pinimg.com/originals/25/8e/b9/258eb97071206129113d36c7686b64b8.jpg')

u2 = User(first_name='Elliot', last_name='Reid', email='bajingolingo@aol.com', image_url='https://tv-fanatic-res.cloudinary.com/iu/s--WYhKKyyz--/t_full/cs_srgb,f_auto,fl_strip_profile.lossy,q_auto:420/v1371071450/sarah-chalke-as-elliot-reed.png')

u3 = User(first_name='Perry', last_name='Cox', email='coxyloxy@hotmail.com', image_url='https://assets.mycast.io/actor_images/actor-perry-cox-522109_large.jpg?1661228871')

u4 = User(first_name='Christopher', last_name='Turk', email='turkletonthesurgeon@gmail.com', image_url='https://images5.fanpop.com/image/photos/27500000/Turk-scrubs-27527647-1024-768.png')


db.session.add(u1)
db.session.add(u2)
db.session.add(u3)
db.session.add(u4)

db.session.commit()
