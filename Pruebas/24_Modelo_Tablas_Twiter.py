
import datetime
from peewee import *

DATABASE = 'tweepee.db'
# create a peewee database instance -- our models will use this database to
# persist information
database = SqliteDatabase(DATABASE)


class BaseModel(Model):
    class Meta:
        database = database

# the user model specifies its fields (or columns) declaratively, like django
class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    email = CharField()
    join_date = DateTimeField()


# this model contains two foreign keys to user -- it essentially allows us to
# model a "many-to-many" relationship between users.  by querying and joining
# on different columns we can expose who a user is "related to" and who is
# "related to" a given user
class Relationship(BaseModel):
    from_user = ForeignKeyField(User, backref='relationships')
    to_user = ForeignKeyField(User, backref='related_to')

    class Meta:
        indexes = (
            # Specify a unique multi-column index on from/to-user.
            (('from_user', 'to_user'), True),
        )

# a dead simple one-to-many relationship: one user has 0..n messages, exposed by
# the foreign key.  because we didn't specify, a users messages will be accessible
# as a special attribute, User.message_set
class Message(BaseModel):
    user = ForeignKeyField(User, backref='messages')
    content = TextField()
    pub_date = DateTimeField()


# simple utility function to create tables
def create_tables():
    with database:
        database.create_tables([User, Relationship, Message])

def insert_Info():
    try:
        User.insert_many([
            {'username': 'Borja','password': 'contraseña','email': 'borja.ticona@educa.madrid.org', 'join_date': datetime.datetime.now()},
            {'username': 'usuario2','password': 'password123','email': 'usuario.1@educa.madrid.org', 'join_date': datetime.datetime.now()}
        ]).execute()
    except Exception as e:
        print(f"Error: {e}")

def following(self):
 # query other users through the "relationship" table
 return (User
 .select()
 .join(Relationship, on=Relationship.to_user)
 .where(Relationship.from_user == self)
 .order_by(User.username))
def followers(self):
 return (User
 .select()
 .join(Relationship, on=Relationship.from_user)
 .where(Relationship.to_user == self)
 .order_by(User.username))





if __name__ == "__main__":
    create_tables()
    insert_Info()
    print(f"\nSeguidores ({User.username}):")
    for follower in User.folowers()
        print(following.username)
    except User.DoesNotExist:
    print(f"\")