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


class FoodModelTestCase(TestCase):
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
        db.session.commit()

        f1 = Food.query.get(1)
        self.f1 = f1

        self.client = app.test_client()

    def tearDown(self) -> None:
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_food_model(self):
        """Does basic model work?"""

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
        db.session.add(food)
        db.session.commit()

        f = Food.query.get(1)

        self.assertEqual(f.food_name, "bread")
        self.assertEqual(f.carbs, 14.33)
        self.assertEqual(f.protein, 2.57)
        self.assertEqual(f.total_fat, 0.97)
