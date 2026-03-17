from flask import Flask, render_template, request, redirect, jsonify, session
from functools import wraps

# backend modules
from backend.business_module import add_business, get_all_businesses, search_businesses, get_top_businesses
from backend.user_activity_module import add_interaction
from backend.user_module import register_user, login_user

# AI engine
from ai_engine.recommendation import get_recommendations

app = Flask(__name__)
app.secret_key = "foodai_super_secret_key"


# Middleware to protect routes: Must be logged in!
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login_page")
        return f(*args, **kwargs)
    return decorated_function


# ---------------- HOME PAGE ----------------
@app.route("/")
def home():
    top_restaurants = get_top_businesses(limit=5)
    user_name = session.get("name") if "user_id" in session else None
    return render_template("index.html", user_name=user_name, top_restaurants=top_restaurants)


# ---------------- SHOW ALL BUSINESSES ----------------
@app.route("/businesses")
@login_required
def show_businesses():
    businesses = get_all_businesses()
    return render_template("restaurants.html", restaurants=businesses, user_id=session.get("user_id"))


# ---------------- 5 DIFFERENT RESTAURANT PAGES (NEW) ----------------
@app.route("/pizza_palace")
@login_required
def pizza_palace():
    return render_template("pizza_palace.html")

@app.route("/burger_hub")
@login_required
def burger_hub():
    return render_template("burger_hub.html")

@app.route("/cafe_aroma")
@login_required
def cafe_aroma():
    return render_template("cafe_aroma.html")

@app.route("/pizza_hut")
@login_required
def pizza_hut():
    return render_template("pizza_hut.html")

@app.route("/dominos")
@login_required
def dominos():
    return render_template("dominos.html")

@app.route("/restaurant/<name>")
@login_required
def generic_restaurant(name):
    return render_template("generic_restaurant.html", restaurant_name=name)


# ---------------- AI CHATBOT API (NEW) ----------------
@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json()
    user_message = data.get("message", "").lower()
    user_name = session.get("name", "User")
    
    # Default fallback message if it doesn't understand
    reply = f"I'm not sure I understand, {user_name}. You can ask me for 'Top 5 restaurants', 'Recommendations', or 'Pizza'!"

    # 1. Greetings
    if any(word in user_message for word in ["hello", "hi", "hey", "morning", "evening"]):
        reply = f"Hello there, {user_name}! I am FoodAI, your smart assistant. How can I help you today?"
        
    # 2. How it works
    elif any(word in user_message for word in ["how does this", "how it works", "how do you work", "about foodai"]):
        reply = "FoodAI uses your past ratings and likes to find the absolute best restaurants for you using Machine Learning! Try exploring the 'Recommendations' tab."
        
    # 3. Creator/Team
    elif any(word in user_message for word in ["who built you", "creator", "team", "who made you", "admin"]):
        reply = "I was built by an amazing team: Ritesh on Database, Sourabh on Frontend, and our Backend lead for this exciting Hackathon!"

    # 4. Specific Rating Checks
    elif any(x in user_message for x in ["5 star", "5 rating", "rating 5", "five star"]):
        reply = "Looking for 5-star perfection? 'Pizza Palace' and 'Cafe Aroma' are the closest we have right now with outstanding 4.6 and 4.5 ratings!"
        
    elif any(x in user_message for x in ["4 star", "4 rating", "rating 4", "four star"]):
        reply = "We have many great 4-star options! 'Burger Hub' (4.4 ⭐) and 'Pizza Hut' (4.2 ⭐) are fantastic choices in the 4-star range."
        
    elif any(x in user_message for x in ["3 star", "3 rating", "rating 3", "three star", "2 star", "2 rating", "rating 2", "1 star"]):
        reply = "We try to only recommend the best! Most of our featured restaurants are 4 stars or higher, but you can explore more under the 'Restaurants' tab."

    # 5. Top Rated / Top 5 (Catches "top 5" but won't trigger if they just said "4")
    elif any(word in user_message for word in ["top rated", "best restaurant", "top 5", "top five", "highest rated", "good food"]):
        reply = "Here are our Top Rated overall: 1. Pizza Palace (4.6 ⭐), 2. Cafe Aroma (4.5 ⭐), 3. Burger Hub (4.4 ⭐). They are highly recommended by users!"

    # 6. Recommendations
    elif any(word in user_message for word in ["recommend", "recommendation", "suggest", "what should i eat", "hungry"]):
        reply = f"Based on our AI model {user_name}, if you love fast food, you must try 'Burger Hub' or 'Pizza Hut'. Would you like the link to their menus?"

    # 6. Specific Food Cravings
    elif "pizza" in user_message:
        reply = "If you are craving pizza, I highly suggest 'Pizza Palace' or 'Dominos'. Pizza Palace has an amazing Margherita for ₹249."
    elif "burger" in user_message:
        reply = "'Burger Hub' is the place to go! Their Classic Cheeseburger is very popular at ₹199."
    elif any(word in user_message for word in ["coffee", "cafe", "tea", "drink"]):
        reply = "'Cafe Aroma' is perfect for that. Check out their Iced Caramel Macchiato!"
    elif any(word in user_message for word in ["dessert", "sweet", "cake"]):
        reply = "'Dominos' actually has a really good Choco Lava Cake for just ₹110!"

    return jsonify({"reply": reply})


# ---------------- RECOMMENDATION API ----------------
@app.route("/recommend")
@login_required
def recommend():
    user_id = session.get("user_id")
    result = get_recommendations(user_id)
    return render_template("recommendations.html", businesses=result)


# ---------------- USER REGISTER ----------------
@app.route("/register", methods=["POST"])
def register():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]

    result = register_user(name, email, password)
    return redirect("/login_page")


# ---------------- USER LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    user = login_user(email, password)

    if user["status"] == "success":
        session["user_id"] = user["user_id"]
        session["name"] = user["name"]
        return redirect("/")
    else:
        return "Invalid Credentials"


# ---------------- USER LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------------- LOGIN & REGISTER PAGES ----------------
@app.route("/login_page")
def login_page():
    return render_template("login.html")

@app.route("/register_page")
def register_page():
    return render_template("register.html")


# ---------------- RATE BUSINESS ----------------
@app.route("/rate_business", methods=["POST"])
@login_required
def rate_business():
    user_id = request.form["user_id"]
    business_id = request.form["business_id"]
    rating = request.form["rating"]

    result = add_interaction(user_id, business_id, rating)
    return jsonify({"status": result})


# ---------------- SEARCH BUSINESSES ----------------
@app.route("/search")
def search():
    query = request.args.get("query", "")
    results = search_businesses(query)
    return jsonify(results)


# ---------------- ADD TEST BUSINESS ----------------
@app.route("/add_test_business")
def add_test_business():
    add_business("Pizza Hut", "Food", "Indore", 4.2)
    add_business("Dominos", "Food", "Indore", 4.1)
    add_business("Samsung Store", "Electronics", "Indore", 4.5)
    return "Test Businesses Added"


# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(debug=True)
