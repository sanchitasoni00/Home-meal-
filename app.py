import streamlit as st
import json
import os


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="HomeMeal",
    page_icon="🍱",
    layout="wide"
)


# =========================================================
# JSON DATABASE
# =========================================================

DATABASE_FILE = "database.json"


def load_database():
    """Load database from JSON file."""

    default_database = {
        "users": [],
        "cooks": [],
        "meals": [],
        "orders": []
    }

    if not os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "w", encoding="utf-8") as file:
            json.dump(
                default_database,
                file,
                indent=4,
                ensure_ascii=False
            )

        return default_database

    try:
        with open(DATABASE_FILE, "r", encoding="utf-8") as file:
            database = json.load(file)

    except (json.JSONDecodeError, ValueError, OSError):

        database = default_database

        with open(DATABASE_FILE, "w", encoding="utf-8") as file:
            json.dump(
                database,
                file,
                indent=4,
                ensure_ascii=False
            )

        return database

    database.setdefault("users", [])
    database.setdefault("cooks", [])
    database.setdefault("meals", [])
    database.setdefault("orders", [])

    return database


def save_database(database):
    """Save database to JSON file."""

    with open(DATABASE_FILE, "w", encoding="utf-8") as file:
        json.dump(
            database,
            file,
            indent=4,
            ensure_ascii=False
        )


database = load_database()


# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "cook_name" not in st.session_state:
    st.session_state.cook_name = ""


# =========================================================
# MEALS
# =========================================================

if "meals" not in st.session_state:

    if database["meals"]:

        st.session_state.meals = database["meals"]

    else:

        st.session_state.meals = [
            {
                "id": 1,
                "name": "Rajma Chawal",
                "cook": "Navneet",
                "rating": 4.8,
                "price": 70,
                "quantity": 7
            },
            {
                "id": 2,
                "name": "Veg Thali",
                "cook": "Neha",
                "rating": 3.7,
                "price": 90,
                "quantity": 6
            },
            {
                "id": 3,
                "name": "Pasta",
                "cook": "Anjali",
                "rating": 3.9,
                "price": 100,
                "quantity": 4
            }
        ]

        database["meals"] = st.session_state.meals
        save_database(database)


# =========================================================
# ORDERS
# =========================================================

if "orders" not in st.session_state:
    st.session_state.orders = database["orders"]


# =========================================================
# NEXT MEAL ID
# =========================================================

if "next_meal_id" not in st.session_state:

    if st.session_state.meals:

        st.session_state.next_meal_id = (
            max(
                meal.get("id", 0)
                for meal in st.session_state.meals
            ) + 1
        )

    else:

        st.session_state.next_meal_id = 1


# =========================================================
# NEXT ORDER ID
# =========================================================

if "next_order_id" not in st.session_state:

    if st.session_state.orders:

        st.session_state.next_order_id = (
            max(
                order.get("id", 0)
                for order in st.session_state.orders
            ) + 1
        )

    else:

        st.session_state.next_order_id = 1


# =========================================================
# FIX OLD MEAL DATA
# =========================================================

for meal in st.session_state.meals:

    if "quantity" not in meal:
        meal["quantity"] = 10

    if "rating" not in meal:
        meal["rating"] = 5.0

    if "price" not in meal:
        meal["price"] = 50

    if "cook" not in meal:
        meal["cook"] = "Unknown Cook"

    if "name" not in meal:
        meal["name"] = "Unnamed Meal"


# =========================================================
# FIX OLD COOK DATA
# =========================================================

for cook in database["cooks"]:

    if "name" not in cook:
        cook["name"] = "Unknown Cook"

    if "location" not in cook:
        cook["location"] = ""

    if "ratings" not in cook:
        cook["ratings"] = []

    if "rating" not in cook:
        cook["rating"] = 5.0

    if "rating_count" not in cook:
        cook["rating_count"] = len(cook["ratings"])


# =========================================================
# FIX OLD ORDER DATA
# =========================================================

for order in st.session_state.orders:

    if "status" not in order:
        order["status"] = "Placed"

    if "rating" not in order:
        order["rating"] = None


database["meals"] = st.session_state.meals
database["orders"] = st.session_state.orders

save_database(database)


# =========================================================
# NAVIGATION
# =========================================================

def go_to(page):
    st.session_state.page = page


# =========================================================
# CUSTOM CSS
# =========================================================

st.html(
    """
    <style>

    .hero {
        text-align: center;
        padding: 35px 20px 25px 20px;
    }

    .hero-icon {
        font-size: 65px;
    }

    .hero-title {
        font-size: 48px;
        font-weight: 800;
        margin: 10px 0;

        background: linear-gradient(
            90deg,
            #166534,
            #22c55e,
            #15803d
        );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-tagline {
        font-size: 21px;
        font-weight: 600;
        color: #6b7280;
    }

    .hero-description {
        font-size: 16px;
        color: #6b7280;
        max-width: 750px;
        margin: auto;
        line-height: 1.6;
    }

    .feature-card {
        background: #eafff0;
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        border: 2px solid #86efac;
        min-height: 180px;
        color: #14532d;
    }

    .feature-card h3 {
        color: #14532d !important;
        font-size: 24px;
        margin-top: 10px;
    }

    .feature-card p {
        color: #166534 !important;
        font-size: 16px;
    }

    .feature-icon {
        font-size: 45px;
    }

    .meal-card {
        background: #f0fdf4;
        border: 2px solid #bbf7d0;
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 12px;
        min-height: 220px;
    }

    .meal-card h3 {
        color: #166534;
        margin-bottom: 12px;
    }

    .meal-card p {
        color: #374151;
        margin: 7px 0;
    }

    .why-title {
        text-align: center;
        color: #166534;
        font-size: 36px;
        font-weight: 800;
        margin-top: 20px;
    }

    .why-subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 17px;
        margin-bottom: 30px;
    }

    .dashboard-header {
        background: linear-gradient(
            135deg,
            #166534,
            #22c55e
        );
        padding: 30px;
        border-radius: 22px;
        color: white;
        margin-bottom: 25px;
    }

    .dashboard-header h1 {
        color: white !important;
        margin-bottom: 8px;
    }

    .dashboard-header p {
        color: #ecfdf5 !important;
        font-size: 17px;
    }

    </style>
    """
)


# =========================================================
# HOME PAGE
# =========================================================

def home_page():

    # =====================================================
    # HERO
    # =====================================================

    st.html(
        """
        <div class="hero">

            <div class="hero-icon">
                🍱
            </div>

            <div class="hero-title">
                Ghar Ka Khana, Ghar Se Khamai
            </div>

            <div class="hero-tagline">
                Fresh • Affordable • Home-Cooked
            </div>

            <div class="hero-description">
                Discover delicious homemade meals from trusted
                local cooks, made with care and designed to fit
                your budget.
            </div>

        </div>
        """
    )

    st.divider()

    # =====================================================
    # FEATURES
    # =====================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.html(
            """
            <div class="feature-card">

                <div class="feature-icon">💰</div>

                <h3>Affordable</h3>

                <p>
                    Find delicious meals that fit your budget.
                </p>

            </div>
            """
        )

    with col2:

        st.html(
            """
            <div class="feature-card">

                <div class="feature-icon">🏠</div>

                <h3>Home-Cooked</h3>

                <p>
                    Fresh meals prepared by local home cooks.
                </p>

            </div>
            """
        )

    with col3:

        st.html(
            """
            <div class="feature-card">

                <div class="feature-icon">❤️</div>

                <h3>Trusted</h3>

                <p>
                    Connect with reliable local cooks.
                </p>

            </div>
            """
        )

    st.divider()

    # =====================================================
    # GET STARTED
    # =====================================================

    st.markdown(
        "<h2 style='text-align:center;'>🚀 Get Started</h2>",
        unsafe_allow_html=True
    )

    user_type = st.radio(
        "I am:",
        ["User", "Home Cook"],
        horizontal=True
    )

    if user_type == "User":

        st.info(
            "👤 Users can discover meals, compare cooks "
            "and place orders."
        )

        if st.button(
            "👤 Open User Dashboard",
            use_container_width=True
        ):

            go_to("User")
            st.rerun()

    else:

        st.info(
            "👨‍🍳 Home cooks can add meals, view orders "
            "and manage their food business."
        )

        if st.button(
            "👨‍🍳 Open Cook Dashboard",
            use_container_width=True
        ):

            go_to("cook")
            st.rerun()

    # =====================================================
    # WHY HOME MEAL
    # =====================================================

    st.divider()

    st.html(
        """
        <div class="why-title">
            💚 Why HomeMeal?
        </div>

        <div class="why-subtitle">
            Making everyday meals better, easier and more affordable.
        </div>
        """
    )

    why1, why2, why3, why4 = st.columns(4)

    with why1:

        st.html(
            """
            <div class="feature-card">

                <div class="feature-icon">🏠</div>

                <h3>Home-Cooked</h3>

                <p>
                    Enjoy fresh meals prepared with the
                    comfort and care of home cooking.
                </p>

            </div>
            """
        )

    with why2:

        st.html(
            """
            <div class="feature-card">

                <div class="feature-icon">💰</div>

                <h3>Student-Friendly</h3>

                <p>
                    Affordable meal options designed
                    for students and budget-conscious users.
                </p>

            </div>
            """
        )

    with why3:

        st.html(
            """
            <div class="feature-card">

                <div class="feature-icon">👩‍🍳</div>

                <h3>Support Local Cooks</h3>

                <p>
                    Help talented home cooks earn by
                    sharing their delicious meals.
                </p>

            </div>
            """
        )

    with why4:

        st.html(
            """
            <div class="feature-card">

                <div class="feature-icon">❤️</div>

                <h3>Simple & Trusted</h3>

                <p>
                    Discover, order and enjoy meals
                    through a simple and convenient platform.
                </p>

            </div>
            """
        )


# =========================================================
# USER DASHBOARD
# =========================================================

def User_dashboard():

    st.html(
        """
        <div class="dashboard-header">

            <h1>👤 User Dashboard</h1>

            <p>
                Discover fresh, affordable and delicious
                home-cooked meals.
            </p>

        </div>
        """
    )

    if st.button("⬅️ Back to Home"):

        go_to("home")
        st.rerun()

    st.divider()

    # =====================================================
    # USER PROFILE
    # =====================================================

    st.subheader("👤 Your Profile")

    col1, col2 = st.columns(2)

    with col1:

        user_name = st.text_input(
            "Your Name",
            placeholder="Enter your name",
            key="user_name"
        )

    with col2:

        budget = st.selectbox(
            "Preferred Meal Budget",
            [
                "Under ₹50",
                "₹50 - ₹100",
                "₹100 - ₹150",
                "Above ₹150"
            ]
        )

    # Save user profile

    if user_name.strip():

        existing_user = None

        for user in database["users"]:

            if (
                user.get("name", "").lower()
                == user_name.strip().lower()
            ):

                existing_user = user
                break

        if existing_user:

            existing_user["budget"] = budget

        else:

            database["users"].append(
                {
                    "name": user_name.strip(),
                    "budget": budget
                }
            )

        save_database(database)

    st.divider()

    # =====================================================
    # AVAILABLE MEALS
    # =====================================================

    st.subheader("🍱 Available Home-Cooked Meals")

    search = st.text_input(
        "🔎 Search meals or cooks",
        placeholder="Example: Rajma, Thali, Anjali..."
    )

    available_meals = []

    for meal in st.session_state.meals:

        quantity = meal.get("quantity", 0)

        if quantity > 0:

            meal_name = meal.get("name", "")
            cook_name = meal.get("cook", "")

            if (
                not search
                or search.lower() in meal_name.lower()
                or search.lower() in cook_name.lower()
            ):

                available_meals.append(meal)

    if not available_meals:

        st.warning(
            "No meals found. Try another search."
        )

    else:

        columns = st.columns(3)

        for index, meal in enumerate(available_meals):

            with columns[index % 3]:

                # =================================================
                # FIND COOK RATING
                # =================================================

                cook_rating = 5.0
                cook_rating_count = 0

                for cook in database["cooks"]:

                    if (
                        cook.get("name", "").lower()
                        == meal.get("cook", "").lower()
                    ):

                        cook_rating = cook.get(
                            "rating",
                            5.0
                        )

                        cook_rating_count = cook.get(
                            "rating_count",
                            0
                        )

                        break

                # =================================================
                # MEAL CARD
                # =================================================

                st.html(
                    f"""
                    <div class="meal-card">

                        <h3>
                            🍱 {meal.get("name", "Meal")}
                        </h3>

                        <p>
                            👨‍🍳 <b>Cook:</b>
                            {meal.get("cook", "Unknown")}
                        </p>

                        <p>
                            ⭐ <b>Rating:</b>
                            {cook_rating}/5
                            ({cook_rating_count} ratings)
                        </p>

                        <p>
                            💰 <b>Price:</b>
                            ₹{meal.get("price", 0)}
                        </p>

                        <p>
                            📦 <b>Available:</b>
                            {meal.get("quantity", 0)}
                        </p>

                    </div>
                    """
                )

                if st.button(
                    f"🛒 Order {meal['name']}",
                    key=f"order_{meal['id']}",
                    use_container_width=True
                ):

                    customer = (
                        user_name.strip()
                        if user_name.strip()
                        else "User"
                    )

                    new_order = {
                        "id": st.session_state.next_order_id,
                        "meal": meal["name"],
                        "cook": meal["cook"],
                        "customer": customer,
                        "price": meal["price"],
                        "status": "Placed",
                        "rating": None
                    }

                    st.session_state.orders.append(
                        new_order
                    )

                    # Reduce quantity

                    for saved_meal in st.session_state.meals:

                        if saved_meal["id"] == meal["id"]:

                            if saved_meal["quantity"] > 0:
                                saved_meal["quantity"] -= 1

                            break

                    database["orders"] = st.session_state.orders
                    database["meals"] = st.session_state.meals

                    save_database(database)

                    st.session_state.next_order_id += 1

                    st.success(
                        f"✅ Order placed for {meal['name']}!"
                    )

                    st.rerun()

    st.divider()

    # =====================================================
    # MY ORDERS
    # =====================================================

    st.subheader("📦 My Orders")

    current_user = (
        user_name.strip()
        if user_name.strip()
        else "User"
    )

    my_orders = []

    for order in st.session_state.orders:

        if order.get("customer", "") == current_user:

            my_orders.append(order)

    if not my_orders:

        st.info(
            "No orders yet. Start exploring meals!"
        )

    else:

        for order in reversed(my_orders):

            with st.container(border=True):

                st.markdown(
                    f"### 🧾 Order #{order.get('id', 0):03d}"
                )

                st.write(
                    f"🍱 **Meal:** "
                    f"{order.get('meal', 'Unknown')}"
                )

                st.write(
                    f"👨‍🍳 **Cook:** "
                    f"{order.get('cook', 'Unknown')}"
                )

                st.write(
                    f"💰 **Price:** "
                    f"₹{order.get('price', 0)}"
                )

                st.write(
                    f"📍 **Status:** "
                    f"{order.get('status', 'Placed')}"
                )

                # =================================================
                # RATING
                # =================================================

                if order.get("status") == "Completed":

                    if order.get("rating") is None:

                        st.markdown(
                            "### ⭐ Rate Your Cook"
                        )

                        rating = st.radio(
                            "How was your experience?",
                            [1, 2, 3, 4, 5],
                            format_func=lambda x: "⭐" * x,
                            horizontal=True,
                            key=f"rating_{order['id']}"
                        )

                        if st.button(
                            "⭐ Submit Rating",
                            key=f"submit_rating_{order['id']}",
                            use_container_width=True
                        ):

                            # Save rating to order

                            for saved_order in st.session_state.orders:

                                if (
                                    saved_order["id"]
                                    == order["id"]
                                ):

                                    saved_order["rating"] = rating
                                    break

                            # Find cook

                            cook_found = False

                            for cook in database["cooks"]:

                                if (
                                    cook.get("name", "").lower()
                                    == order.get("cook", "").lower()
                                ):

                                    if "ratings" not in cook:
                                        cook["ratings"] = []

                                    cook["ratings"].append(
                                        rating
                                    )

                                    cook["rating_count"] = len(
                                        cook["ratings"]
                                    )

                                    cook["rating"] = round(
                                        sum(cook["ratings"])
                                        / len(cook["ratings"]),
                                        1
                                    )

                                    cook_found = True
                                    break

                            # Create cook if missing

                            if not cook_found:

                                database["cooks"].append(
                                    {
                                        "name": order.get(
                                            "cook",
                                            "Unknown Cook"
                                        ),
                                        "location": "",
                                        "ratings": [rating],
                                        "rating": float(rating),
                                        "rating_count": 1
                                    }
                                )

                            database["orders"] = (
                                st.session_state.orders
                            )

                            save_database(database)

                            st.success(
                                "⭐ Thank you! "
                                "Your rating has been submitted."
                            )

                            st.rerun()

                    else:

                        st.success(
                            f"⭐ You rated this cook "
                            f"{order['rating']}/5"
                        )


# =========================================================
# COOK DASHBOARD
# =========================================================

def cook_dashboard():

    st.html(
        """
        <div class="dashboard-header">

            <h1>👨‍🍳 Home Cook Dashboard</h1>

            <p>
                Manage your meals, orders and earnings
                from one place.
            </p>

        </div>
        """
    )

    if st.button("⬅️ Back to Home"):

        go_to("home")
        st.rerun()

    st.divider()

    # =====================================================
    # COOK PROFILE
    # =====================================================

    st.subheader("👤 Cook Profile")

    cook_name = st.text_input(
        "Cook Name",
        value=st.session_state.cook_name,
        placeholder="Enter your name",
        key="cook_name_input"
    )

    st.session_state.cook_name = cook_name

    location = st.text_input(
        "Location",
        placeholder="Enter your area"
    )

    # Save cook profile

    if cook_name.strip():

        existing_cook = None

        for cook in database["cooks"]:

            if (
                cook.get("name", "").lower()
                == cook_name.strip().lower()
            ):

                existing_cook = cook
                break

        if existing_cook:

            existing_cook["location"] = location

        else:

            database["cooks"].append(
                {
                    "name": cook_name.strip(),
                    "location": location,
                    "ratings": [],
                    "rating": 5.0,
                    "rating_count": 0
                }
            )

        save_database(database)

    st.divider()

    # =====================================================
    # COOK ORDERS
    # =====================================================

    cook_orders = []

    for order in st.session_state.orders:

        if (
            not cook_name.strip()
            or order.get("cook", "").lower()
            == cook_name.strip().lower()
        ):

            cook_orders.append(order)

    # =====================================================
    # MY MEALS
    # =====================================================

    my_meals = []

    for meal in st.session_state.meals:

        if (
            not cook_name.strip()
            or meal.get("cook", "").lower()
            == cook_name.strip().lower()
        ):

            my_meals.append(meal)

    # =====================================================
    # STATISTICS
    # =====================================================

    total_orders = len(cook_orders)

    earnings = sum(
        order.get("price", 0)
        for order in cook_orders
        if order.get("status") in [
            "Accepted",
            "Completed"
        ]
    )

    total_meals = len(my_meals)

    customers = len(
        set(
            order.get("customer", "User")
            for order in cook_orders
        )
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "🍱 Orders",
            total_orders
        )

    with col2:

        st.metric(
            "💰 Earnings",
            f"₹{earnings}"
        )

    with col3:

        st.metric(
            "🍽️ Meals",
            total_meals
        )

    with col4:

        st.metric(
            "👥 Customers",
            customers
        )

    st.divider()

    # =====================================================
    # ADD MEAL
    # =====================================================

    st.subheader("🍱 Add a Meal")

    meal_name = st.text_input(
        "Meal Name",
        placeholder="Example: Rajma Chawal"
    )

    col1, col2 = st.columns(2)

    with col1:

        price = st.number_input(
            "Price (₹)",
            min_value=1,
            max_value=1000,
            value=50
        )

    with col2:

        quantity = st.number_input(
            "Available Quantity",
            min_value=1,
            max_value=100,
            value=10
        )

    if st.button(
        "➕ Add Meal",
        use_container_width=True
    ):

        if not cook_name.strip():

            st.warning(
                "Please enter your Cook Name first."
            )

        elif not meal_name.strip():

            st.warning(
                "Please enter a meal name."
            )

        else:

            new_meal = {
                "id": st.session_state.next_meal_id,
                "name": meal_name.strip(),
                "cook": cook_name.strip(),
                "rating": 5.0,
                "price": price,
                "quantity": quantity
            }

            st.session_state.meals.append(
                new_meal
            )

            database["meals"] = st.session_state.meals

            save_database(database)

            st.session_state.next_meal_id += 1

            st.success(
                f"✅ {meal_name} has been added to HomeMeal!"
            )

            st.rerun()

    st.divider()

    # =====================================================
    # MY ADDED MEALS
    # =====================================================

    st.subheader("🍽️ My Added Meals")

    my_meals = []

    for meal in st.session_state.meals:

        if (
            not cook_name.strip()
            or meal.get("cook", "").lower()
            == cook_name.strip().lower()
        ):

            my_meals.append(meal)

    if not my_meals:

        st.info(
            "You haven't added any meals yet."
        )

    else:

        for meal in my_meals:

            with st.container(border=True):

                col1, col2, col3 = st.columns(
                    [3, 1, 1]
                )

                with col1:

                    st.markdown(
                        f"### 🍱 "
                        f"{meal.get('name', 'Meal')}"
                    )

                    st.write(
                        f"⭐ "
                        f"{meal.get('rating', 5.0)}/5"
                    )

                with col2:

                    st.write(
                        f"💰 ₹"
                        f"{meal.get('price', 0)}"
                    )

                with col3:

                    st.write(
                        f"📦 "
                        f"{meal.get('quantity', 0)}"
                    )

    st.divider()

    # =====================================================
    # RECENT ORDERS
    # =====================================================

    st.subheader("📦 Recent Orders")

    cook_orders = []

    for order in st.session_state.orders:

        if (
            not cook_name.strip()
            or order.get("cook", "").lower()
            == cook_name.strip().lower()
        ):

            cook_orders.append(order)

    if not cook_orders:

        st.info(
            "No orders have been placed yet."
        )

    else:

        for order in reversed(cook_orders):

            with st.container(border=True):

                col1, col2 = st.columns(
                    [4, 1]
                )

                with col1:

                    st.markdown(
                        f"### 🧾 "
                        f"Order #{order.get('id', 0):03d}"
                    )

                    st.write(
                        f"🍱 **Meal:** "
                        f"{order.get('meal', 'Unknown')}"
                    )

                    st.write(
                        f"👤 **User:** "
                        f"{order.get('customer', 'User')}"
                    )

                    st.write(
                        f"💰 **Price:** "
                        f"₹{order.get('price', 0)}"
                    )

                    st.write(
                        f"📍 **Status:** "
                        f"{order.get('status', 'Placed')}"
                    )

                with col2:

                    # =============================================
                    # ACCEPT ORDER
                    # =============================================

                    if order.get("status") == "Placed":

                        if st.button(
                            "✅ Accept",
                            key=f"accept_{order['id']}",
                            use_container_width=True
                        ):

                            for saved_order in st.session_state.orders:

                                if (
                                    saved_order["id"]
                                    == order["id"]
                                ):

                                    saved_order["status"] = "Accepted"
                                    break

                            database["orders"] = (
                                st.session_state.orders
                            )

                            save_database(database)

                            st.success(
                                "Order accepted!"
                            )

                            st.rerun()

                    # =============================================
                    # COMPLETE ORDER
                    # =============================================

                    elif order.get("status") == "Accepted":

                        if st.button(
                            "🎉 Complete",
                            key=f"complete_{order['id']}",
                            use_container_width=True
                        ):

                            for saved_order in st.session_state.orders:

                                if (
                                    saved_order["id"]
                                    == order["id"]
                                ):

                                    saved_order["status"] = "Completed"
                                    break

                            database["orders"] = (
                                st.session_state.orders
                            )

                            save_database(database)

                            st.success(
                                "Order completed!"
                            )

                            st.rerun()

                    # =============================================
                    # COMPLETED
                    # =============================================

                    else:

                        st.success(
                            "Completed"
                        )


# =========================================================
# PAGE ROUTER
# =========================================================

if st.session_state.page == "home":

    home_page()

elif st.session_state.page == "User":

    User_dashboard()

elif st.session_state.page == "cook":

    cook_dashboard()
