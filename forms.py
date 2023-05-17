from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DecimalField, FloatField, RadioField, BooleanField, DateField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, Length


class UserAddForm(FlaskForm):
    """Form for adding users."""
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')
    calorie_goal = FloatField('Daily Calorie Goal',
                              validators=[DataRequired()])


class UserEditGoalsForm(FlaskForm):
    """Form for editing user health info and goals"""
    calorie_goal = FloatField('Calories',
                              validators=[DataRequired()])
    carbs_goal = FloatField('Carbohydrates')
    protein_goal = FloatField('Proteins')
    fat_goal = FloatField('Fats')


class UserEditProfileForm(FlaskForm):
    """Form for editing User info"""
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('Image URL')


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class FoodAddForm(FlaskForm):
    """Form for adding food to db"""

    food_name = StringField('Food')
    brand_name = StringField('Brand Name')
    serving_qty = FloatField('Qty')
    serving_unit = StringField('Unit')
    serving_weight_grams = FloatField('Weight in Grams')
    calories = FloatField('Calories')
    total_fat = FloatField('Fat')
    saturated_fat = FloatField('Saturated Fat')
    cholesterol = FloatField('Cholesterol')
    sodium = FloatField('Sodium')
    carbs = FloatField('Carbs')
    fiber = FloatField('Fiber')
    sugar = FloatField('Sugar')
    protein = FloatField('Protein')
    img = StringField('Img')


class FoodLogForm(FlaskForm):
    """Form for logging consumed food"""

    user_id = IntegerField('User ID')
    food_id = IntegerField('Food ID')
    date = DateField('Date')
    meal = RadioField('Meal', choices=[
                      'Breakfast', 'Lunch', 'Dinner', 'Snacks'], validators=[DataRequired()])
    servings = FloatField('Servings')
    favorite = BooleanField('Add to favorites?')
