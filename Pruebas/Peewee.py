from peewee import *
from datetime import date

# Connect to the SQLite database "people.db"
db = SqliteDatabase('people.db')

# Define the Person model (table)
class Person(Model):
    name = CharField()
    birthday = DateField()

    class Meta:
        database = db  # This model uses the "people.db" database.

# Define the Pet model (table)
class Pet(Model):
    owner = ForeignKeyField(Person, backref='pets')  # Foreign key to Person table
    name = CharField()
    animal_type = CharField()

    class Meta:
        database = db  # This model uses the "people.db" database

# Connect to the database
db.connect()

# Create tables for Person and Pet if they do not exist already
db.create_tables([Person, Pet])

# Create instances of Person
uncle_bob = Person(name='Bob', birthday=date(1960, 1, 15))
uncle_bob.save()  # Save to database, returns the ID of the created object (1)

# Insert more Person records
grandma = Person.create(name='Grandma', birthday=date(1935, 3, 1))
herb = Person.create(name='Herb', birthday=date(1950, 5, 5))

# Update an existing record for Grandma
grandma.name = 'Grandma L.'
grandma.save()  # Save updated name in the database

# Create instances of Pet associated with specific owners
bob_kitty = Pet.create(owner=uncle_bob, name='Kitty', animal_type='cat')
herb_fido = Pet.create(owner=herb, name='Fido', animal_type='dog')
herb_mittens = Pet.create(owner=herb, name='Mittens', animal_type='cat')
herb_mittens_jr = Pet.create(owner=herb, name='Mittens Jr', animal_type='cat')

# Delete a pet (Mittens)
herb_mittens.delete_instance()

# Reassign owner for herb_fido
herb_fido.owner = uncle_bob
herb_fido.save()

# Retrieve a person by name and print their name
grandma = Person.select().where(Person.name == 'Grandma L.').get()

# Another way to retrieve a person by name
grandma = Person.get(Person.name == 'Grandma L.')

# Print the names of all persons
for person in Person.select():
    print(person.name)
# Output:
# Bob
# Grandma L.
# Herb

# Query to get pets with animal_type 'cat'
query = Pet.select().where(Pet.animal_type == 'cat')
for pet in query:
    print(pet.name, pet.owner.name)
# Output:
# Kitty Bob
# Mittens Jr Herb

# Join Pet and Person tables to get pets with animal_type 'cat'
query = (Pet
         .select(Pet, Person)
         .join(Person)  # Join with the Person table
         .where(Pet.animal_type == 'cat'))

for pet in query:
    print(pet.name, pet.owner.name)
# Output:
# Kitty Bob
# Mittens Jr Herb

# Print all pets owned by Bob using a join
for pet in Pet.select().join(Person).where(Person.name == 'Bob'):
    print(pet.name)
# Output:
# Kitty
# Fido

# Print pets owned by uncle_bob using the ForeignKey reference
for pet in Pet.select().where(Pet.owner == uncle_bob):
    print(pet.name)
# Output:
# Kitty
# Fido
for pet in Pet.select().where(Pet.owner == uncle_bob).order_by(Pet.name):
  print(pet.name)
# # prints:
# # Fido
# # Kitty
for person in Person.select().order_by(Person.birthday.desc()):
   print(person.name, person.birthday)
# # prints:
# # Bob 1960-01-15
# # Herb 1950-05-05
# # Grandma L. 1935-03-01
print("-------------------------------------")
d1940 = date(1940, 1, 1)
d1960 = date(1960, 1, 1)
query = (Person
         .select()
        .where((Person.birthday < d1940) | (Person.birthday > d1960)))
for person in query:
     print(person.name, person.birthday)

#  prints:
#  Bob 1960-01-15
#  Grandma L. 1935-03-01
print("-------------------------------------")
query = (Person
         .select()
          .where(Person.birthday.between(d1940, d1960)))

for person in query:
     print(person.name, person.birthday)

#  prints:
#  Herb 1950-05-05
print("-------------------------------------")
for person in Person.select():
  print(person.name, person.pets.count(), 'pets')
#  prints:
# Bob 2 pets
# Grandma L. 0 pets
#  Herb 1 pets
print("-------------------------------------")
query = (Person
        .select(Person, fn.COUNT(Pet.id).alias('pet_count'))
          .join(Pet, JOIN.LEFT_OUTER)  # include people without pets.
          .group_by(Person)
         .order_by(Person.name))

for person in query:
# "pet_count" becomes an attribute on the returned model instances.
    print(person.name, person.pet_count, 'pets')

# # prints:
# # Bob 2 pets
# # Grandma L. 0 pets
# # Herb 1 pets
print("-------------------------------------")
database = db  # this model uses the "people.db" database

query = (Person
         .select(Person, Pet)
         .join(Pet, JOIN.LEFT_OUTER)
         .order_by(Person.name, Pet.name))
for person in query:
    # We need to check if they have a pet instance attached, since not all
    # people have pets.
    if hasattr(person, 'pet'):
        print(person.name, person.pet.name)
    else:
        print(person.name, 'no pets')

# prints:
# Bob Fido
# Bob Kitty
# Grandma L. no pets
# Herb Mittens Jr

print("-------------------------------------")
query = Person.select().order_by(Person.name).prefetch(Pet)
for person in query:
    print(person.name)
    for pet in person.pets:
        print('  *', pet.name)

# prints:
# Bob
#   * Kitty
#   * Fido
# Grandma L.
# Herb
#   * Mittens Jr

print("-------------------------------------")
expression = fn.Lower(fn.Substr(Person.name, 1, 1)) == 'g'
for person in Person.select().where(expression):
    print(person.name)

# prints:
# Grandma L.

db.close()

