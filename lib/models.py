# Import necessary SQLAlchemy modules
from sqlalchemy import create_engine, func
from sqlalchemy import ForeignKey, Table, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

# Define the database engine (SQLite in this example)
engine = create_engine('sqlite:///many_to_many.db')

# Create a base class for declarative models
Base = declarative_base()

# Define the association table 'game_users'
game_user = Table(
    'game_users',
    Base.metadata,
    Column('game_id', ForeignKey('games.id'), primary_key=True),
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    extend_existing=True,
)

# Define the 'Game' model
class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer(), primary_key=True)
    title = Column(String())
    genre = Column(String())
    platform = Column(String())
    price = Column(Integer())

    # Define the many-to-many relationship with 'User' model using 'game_users'
    users = relationship('User', secondary=game_user, back_populates='games')

    # Define a one-to-many relationship with 'Review' model
    reviews = relationship('Review', backref=backref('game'), cascade='all, delete-orphan')

    def __repr__(self):
        return f'Game(id={self.id}, ' + \
            f'title={self.title}, ' + \
            f'platform={self.platform})'

# Define the 'User' model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

    # Define the many-to-many relationship with 'Game' model using 'game_users'
    games = relationship('Game', secondary=game_user, back_populates='users')

    # Define a one-to-many relationship with 'Review' model
    reviews = relationship('Review', backref=backref('user'), cascade='all, delete-orphan')

    def __repr__(self):
        return f'User(id={self.id}, ' + \
            f'name={self.name})'

# Define the 'Review' model
class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer(), primary_key=True)
    score = Column(Integer())
    comment = Column(String())

    # Define foreign keys to associate 'Review' with 'Game' and 'User'
    game_id = Column(Integer(), ForeignKey('games.id'))
    user_id = Column(Integer(), ForeignKey('users.id'))

    def __repr__(self):
        return f'Review(id={self.id}, ' + \
            f'score={self.score}, ' + \
            f'game_id={self.game_id})'

# Create the tables in the database
Base.metadata.create_all(engine)
