from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()
db= SQLAlchemy()


def connect_db(app):
    """Connect to database"""

    db.app = app
    db.init_app(app)




class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, 
                   primary_key=True,
                   autoincrement=True) 
    
    username = db.Column(db.String(20),
                         nullable= False,
                         unique= True,
                         primary_key= True
                         )
    password = db.Column(db.Text,
                         nullable= False)
    email = db.Column(db.String(50),
                      nullable = False,
                      unique = True)
    first_name = db.Column(db.String(30),
                           nullable = False)
    last_name = db.Column(db.String(30),
                          nullable = False)
    feedback = db.relationship("Feedback", backref="user", cascade="all,delete")

    # start of convenience class methods

    @classmethod
    def register(cls, username, password, first_name, last_name, email):
        """Register a user and hash their password."""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        user = cls(
            username=username,
            password=hashed_utf8,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Validates if user and password are coorect.

        Return user if valid; else return False.
        """

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False


class Feedback(db.Model):
    """Feedback."""

    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(
        db.String(20),
        db.ForeignKey('users.username'),
        nullable=False,
    )





    