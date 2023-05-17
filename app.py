import os
import requests

from flask import Flask, render_template, request, flash, redirect, session, g, abort
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import UserAddForm, LoginForm, FoodLogForm, FoodAddForm, UserEditGoalsForm, UserEditProfileForm
from models import db, connect_db, User, Food, Consumed

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///nutrition_log'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
# toolbar = DebugToolbarExtension(app)

connect_db(app)
# db.create_all()


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If there already is a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
                calorie_goal=form.calorie_goal.data
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""
    do_logout()
    flash("Logged Out", "info")
    return redirect('/login')

##############################################################################
# User Pages


@app.route('/users/<int:user_id>/goals', methods=["GET", "POST"])
def goals(user_id):
    """Show user goals"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)
    form = UserEditGoalsForm(obj=user)

    if form.validate_on_submit():
        user.calorie_goal = form.calorie_goal.data
        user.carbs_goal = form.carbs_goal.data
        user.protein_goal = form.protein_goal.data
        user.fat_goal = form.fat_goal.data

        db.session.commit()
        return redirect("/")

    return render_template("goals.html", user=user, form=form)


@app.route('/users/<int:user_id>/profile', methods=["GET", "POST"])
def profile(user_id):
    """Update profile for current user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)
    form = UserEditProfileForm(obj=user)

    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.email = form.email.data
            user.image_url = form.image_url.data or "/static/images/default-pic.png"

            db.session.commit()
            return redirect("/")

        flash("Wrong password, please try again.", 'danger')

    return render_template("profile.html", user=user, form=form)

##############################################################################
# Homepage and error pages


@app.route('/')
def homepage():
    """Show homepage"""

    if g.user:

        return render_template('home.html')

    else:
        return render_template('home-anon.html')


##############################################################################
# Search pages

search_result = {
    'food_name': "",
    'brand_name': "",
    'serving_qty': "",
    'serving_unit': "",
    'serving_weight_grams': "",
    'calories': "",
    'total_fat': "",
    'saturated_fat': "",
    'cholesterol': "",
    'sodium': "",
    'carbs': "",
    'fiber': "",
    'sugar': "",
    'protein': "",
    'img': "",
}


def food_search(food):
    res = requests.post("https://trackapi.nutritionix.com/v2/natural/nutrients",
                        headers={'x-app-id': 'e026dae3',
                                 'x-app-key': '3a70fac62af0aa32ff3de29f939848d2'},
                        data={'query': food})

    data = res.json()
    result = {
        'food_name': data["foods"][0]["food_name"],
        'brand_name': data["foods"][0]["brand_name"],
        'serving_qty': data["foods"][0]["serving_qty"],
        'serving_unit': data["foods"][0]["serving_unit"],
        'serving_weight_grams': data["foods"][0]["serving_weight_grams"],
        'calories': data["foods"][0]["nf_calories"],
        'total_fat': data["foods"][0]["nf_total_fat"],
        'saturated_fat': data["foods"][0]["nf_saturated_fat"],
        'cholesterol': data["foods"][0]["nf_cholesterol"],
        'sodium': data["foods"][0]["nf_sodium"],
        'carbs': data["foods"][0]["nf_total_carbohydrate"],
        'fiber': data["foods"][0]["nf_dietary_fiber"],
        'sugar': data["foods"][0]["nf_sugars"],
        'protein': data["foods"][0]["nf_protein"],
        'img': data["foods"][0]["photo"]["thumb"],
    }
    return result


@app.route('/add', methods=["GET", "POST"])
def search_page():
    """Search for food in Nutrionix API and add food to database"""

    if not g.user:
        flash("Must sign in to search.", "danger")
        return redirect("/")

    form = FoodAddForm()

    if form.validate_on_submit():
        new_food = Food(**search_result)
        db.session.add(new_food)
        db.session.commit()

        # csd = Consumed(
        #     user_id = g.user.id
        #     food_id = 1
        #     date =
        #     meal =
        # )

        flash("Food added")
        return redirect('/')

    return render_template('search.html', result=search_result, form=form)


@app.route('/search', methods=["POST"])
def search():
    """Search for food in Nutrionix API"""

    if not g.user:
        flash("Must sign in to search.", "danger")
        return redirect("/")

    search_term = request.form["search"]
    result = food_search(search_term)
    for r in result:
        search_result[r] = result[r]

    return redirect("/add")
