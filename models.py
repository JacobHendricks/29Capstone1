"""SQLAlchemy models for Nutrition Log."""

from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    username = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, default="/static/images/default-pic.png")
    password = db.Column(db.Text, nullable=False)
    calorie_goal = db.Column(db.Float, nullable=False)
    protein_goal = db.Column(db.Float)
    carbs_goal = db.Column(db.Float)
    fat_goal = db.Column(db.Float)
    gender = db.Column(db.Text)
    age = db.Column(db.Integer)
    height_ft = db.Column(db.Integer)
    height_in = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    activity_level = db.Column(db.Text)

    consumed = db.relationship('Consumed', backref='users')

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    @classmethod
    def signup(cls, username, email, password, image_url, calorie_goal):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            image_url=image_url,
            calorie_goal=calorie_goal,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Food(db.Model):
    """User in the system."""

    __tablename__ = 'foods'

    id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.Text, nullable=False,)
    brand_name = db.Column(db.Text)
    serving_qty = db.Column(db.Float)
    serving_unit = db.Column(db.Text)
    serving_weight_grams = db.Column(db.Float)
    calories = db.Column(db.Float)
    total_fat = db.Column(db.Float)
    saturated_fat = db.Column(db.Float)
    cholesterol = db.Column(db.Float)
    sodium = db.Column(db.Float)
    carbs = db.Column(db.Float)
    fiber = db.Column(db.Float)
    sugar = db.Column(db.Float)
    protein = db.Column(db.Float)
    img = db.Column(db.Text)


class Consumed(db.Model):
    """User in the system."""

    __tablename__ = 'consumed'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey(
        'foods.id', ondelete='CASCADE'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    meal = db.Column(db.Text, nullable=False)
    servings = db.Column(db.Float, nullable=False, default=1)
    favorite = db.Column(db.Boolean)

    foods = db.relationship('Food', backref='consumed')


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
