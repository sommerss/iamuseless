""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db


from sqlalchemy.exc import IntegrityError



''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

# Define the Post class to manage actions in 'posts' table,  with a relationship to 'users' table
class Post(db.Model):
    __tablename__ = 'posts'
    # Define the Notes schema
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String, unique=False)
    snakescore = db.Column(db.String, unique=False)
    # Define a relationship in Notes Schema to userID who originates the note, many-to-one (many notes to one user)
    userID = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Constructor of a Notes object, initializes of instance variables within object
    def __init__(self, id, image, snakescore):
        self.userID = id
        self.snakescore = snakescore
        
        self.image = image

    # Returns a string representation of the Notes object, similar to java toString()
    # returns string
    

    # CRUD create, adds a new record to the Notes table
    # returns the object added or None in case of an error
    def create(self):
        try:
            # creates a Notes object from Notes(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Notes table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read, returns dictionary representation of Notes object
    # returns dictionary
    def read(self):
        # encode image
        path = app.config['UPLOAD_FOLDER']
        file = os.path.join(path, self.image)
        file_text = open(file, 'rb')
        file_read = file_text.read()
     
        
        return {
            "id": self.id,
            "userID": self.userID,
            "image": self.image,
            "snakescore": self.snakescore
            
        }


# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL
class User(db.Model):
    __tablename__ = 'users'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _uid = db.Column(db.String(255), unique=True, nullable=False)
    _snakescore = db.Column(db.String(255), unique=False, nullable=False)
    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
    posts = db.relationship("Post", cascade='all, delete', backref='users', lazy=True)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, name, uid, snakescore):
        self._name = name    # variables with self prefix become part of the object, 
        self._uid = uid
        self._snakescore = snakescore
        
        

    # a name getter method, extracts name from object
    @property
    def name(self):
        return self._name
    
    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name
    
    # a getter method, extracts email from object
    @property
    def uid(self):
        return self._uid
    
    # a setter function, allows name to be updated after initial object creation
    @uid.setter
    def uid(self, uid):
        self._uid = uid
        
    # check if uid parameter matches user id in object, return boolean
    def is_uid(self, uid):
        return self._uid == uid
    

    
    
    # dob property is returned as string, to avoid unfriendly outcomes
    @property
    def snakescore(self):
        return self._snakescore
    
    # a setter function, allows name to be updated after initial object creation
    @snakescore.setter
    def snakescore(self, snakescore):
        self._snakescore = snakescore



    
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "uid": self.uid,
            
            "snakescore": self.snakescore
            
           
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self, name="", uid="", snakescore=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(uid) > 0:
            self.uid = uid
        if len(snakescore) > 0:
            self.snakescore = snakescore
        
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None


"""Database Creation and Testing """


# Builds working data for testing
def initUsers():
     with app.app_context():
         """Create database and tables"""
         db.init_app(app)
         db.create_all()
         """Tester data for table"""
         u1 = User(name='sabine', uid='sab', snakescore = 10)
       

         users = [u1]

         """Builds sample user/note(s) data"""
         for user in users:
             try:
                 user.posts.append(Post(id=user.id, image='ncs_logo.png', snakescore= user.snakescore))
                 '''add user/post data to table'''
                 user.create()
             except IntegrityError:
                 '''fails with bad or duplicate data'''
                 db.session.remove()
                 print(f"Duplicate email, or error: {user.uid}")