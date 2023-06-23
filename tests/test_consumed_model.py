from app import app
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Food, Consumed

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///nutrition_log_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Don't req CSRF for testing
app.config['WTF_CSRF_ENABLED'] = False

db.create_all()


class ConsumedModelTestCase(TestCase):
    """"""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        food_dict = {
            "food_name": "bread",
            "brand_name": "",
            "serving_qty": 1,
            "serving_unit": "slice",
            "serving_weight_grams": 29,
            "calories": 77.14,
            "total_fat": 0.97,
            "saturated_fat": 0.2,
            "cholesterol": 0,
            "sodium": 142.1,
            "carbs": 14.33,
            "fiber": 0.78,
            "sugar": 1.64,
            "protein": 2.57,
            "img": "https://nix-tag-images.s3.amazonaws.com/8_thumb.jpg"
        }

        food = Food(**food_dict)

        f1 = Food.query.get(1)
        self.f1 = f1

        u1 = User.signup("test1", "email1@email.com", "password", None, 1000)
        uid1 = 1111
        u1.id = uid1

        u2 = User.signup("test2", "email2@email.com", "password", None, 2000)
        uid2 = 2222
        u2.id = uid2

        u1 = User.query.get(uid1)
        u2 = User.query.get(uid2)

        self.u1 = u1
        self.uid1 = uid1

        self.u2 = u2
        self.uid2 = uid2

        db.session.add(food)
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        csd_dict = {
            "user_id": 1111,
            "food_id": 1,
            "date": "2023-06-07",
            "meal": "Breakfast",
            "servings": 1,
            "favorite": False
        }

        csd = Consumed(**csd_dict)
        db.session.add(csd)
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self) -> None:
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_consumed_model(self):
        """Does basic model work?"""

        csd_dict = {
            "user_id": 1111,
            "food_id": 1,
            "date": "2023-06-07",
            "meal": "Breakfast",
            "servings": 1,
            "favorite": False
        }

        csd = Consumed(**csd_dict)
        db.session.add(csd)
        db.session.commit()

        c = Consumed.query.get(1)

        self.assertEqual(c.meal, "Breakfast")
        self.assertEqual(c.foods.food_name, "bread")
        self.assertEqual(c.foods.calories, 77.14)
        self.assertEqual(c.users.username, "test1")
        self.assertEqual(c.users.email, "email1@email.com")
        self.assertEqual(c.users.calorie_goal, 1000)
        self.assertEqual(c.users.protein_goal, 0)

    def test_consumed_user(self):
        """Does consumed food have only one user?"""

        c = Consumed.query.get(1)

        self.assertEqual(c.users.id, 1111)
        self.assertNotEqual(c.users.id, 2222)

        self.assertEqual(self.u2.id, 2222)
        self.assertFalse(self.u2.consumed, "No consumed")
