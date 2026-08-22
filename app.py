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


# Load database
database = load_database()


# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "home"


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
# COOK NAME
# =========================================================

if "cook_name" not in st.session_state:
    st.session_state.cook_name = ""


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


# Save corrected data
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

    /* =========================================
       MAIN PAGE
       ========================================= */

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* =========================================
       HERO SECTION
       ========================================= */

    .hero {
        text-align: center;

        padding: 55px 30px 45px 30px;

        border-radius: 30px;

        background:
            linear-gradient(
                135deg,
                #fffbeb 0%,
                #f0fdf4 55%,
                #ecfccb 100%
            );

        border: 2px solid #bbf7d0;

        box-shadow:
            0 12px 35px rgba(22, 101, 52, 0.10);

        margin-bottom: 35px;
    }


    .hero-icon {
        font-size: 75px;
        margin-bottom: 5px;
    }


    .hero-title {
        font-size: 52px;
        font-weight: 900;

        margin: 5px 0 10px 0;

        background:
            linear-gradient(
                90deg,
                #166534,
                #22c55e,
                #15803d
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }


    .hero-tagline {
        font-size: 23px;
        font-weight: 700;

        color: #166534;

        margin-bottom: 12px;
    }


    .hero-description {
        max-width: 760px;

        margin: auto;

        color: #57534e;

        font-size: 17px;

        line-height: 1.7;
    }


    /* =========================================
       HERO BADGES
       ========================================= */

    .hero-badges {
        display: flex;

        justify-content: center;

        align-items: center;

        gap: 12px;

        flex-wrap: wrap;

        margin-top: 25px;
    }


    .badge {
        background: white;

        color: #166534;

        border: 1px solid #bbf7d0;

        border-radius: 30px;

        padding: 9px 17px;

        font-size: 14px;

        font-weight: 700;

        box-shadow:
            0 4px 12px rgba(0, 0, 0, 0.04);
    }


    /* =========================================
       SECTION HEADINGS
       ========================================= */

    .section-title {
        text-align: center;

        color: #166534;

        font-size: 36px;

        font-weight: 850;

        margin-top: 30px;

        margin-bottom: 8px;
    }


    .section-subtitle {
        text-align: center;

        color: #78716c;

        font-size: 17px;

        margin-bottom: 30px;
    }


    /* =========================================
       FEATURE CARDS
       ========================================= */

    .feature-card {
        background: white;

        border-radius: 22px;

        padding: 28px 22px;

        text-align: center;

        min-height: 190px;

        border: 2px solid #dcfce7;

        box-shadow:
            0 8px 25px rgba(22, 101, 52, 0.07);

        transition:
            transform 0.25s ease,
            box-shadow 0.25s ease,
            border-color 0.25s ease;
    }


    .feature-card:hover {
        transform: translateY(-7px);

        border-color: #86efac;

        box-shadow:
            0 15px 35px rgba(22, 101, 52, 0.14);
    }


    .feature-icon {
        font-size: 46px;

        margin-bottom: 5px;
    }


    .feature-card h3 {
        color: #166534 !important;

        font-size: 22px;

        margin: 8px 0 10px 0;
    }


    .feature-card p {
        color: #57534e !important;

        font-size: 15px;

        line-height: 1.6;
    }


    /* =========================================
       HOW IT WORKS
       ========================================= */

    .step-card {
        background: #fffdf7;

        border: 2px solid #fde68a;

        border-radius: 22px;

        padding: 25px 18px;

        text-align: center;

        min-height: 175px;

        box-shadow:
            0 7px 20px rgba(245, 158, 11, 0.08);

        transition:
            transform 0.25s ease;
    }


    .step-card:hover {
        transform: translateY(-6px);
    }


    .step-number {
        width: 46px;
        height: 46px;

        margin: auto;

        display: flex;

        align-items: center;
        justify-content: center;

        border-radius: 50%;

        background: #f59e0b;

        color: white;

        font-size: 18px;

        font-weight: 800;
    }


    .step-card h3 {
        color: #166534;

        font-size: 20px;

        margin: 12px 0 8px 0;
    }


    .step-card p {
        color: #57534e;

        font-size: 14px;

        line-height: 1.5;
    }


    /* =========================================
       TRUST BANNER
       ========================================= */

    .trust-banner {
        text-align: center;

        padding: 30px;

        border-radius: 25px;

        background:
            linear-gradient(
                135deg,
                #166534,
                #15803d
            );

        color: white;

        margin-top: 35px;

        box-shadow:
            0 12px 30px rgba(22, 101, 52, 0.18);
    }


    .trust-banner h2 {
        color: white;

        font-size: 26px;

        margin-bottom: 8px;
    }


    .trust-banner p {
        color: #dcfce7;

        font-size: 16px;

        margin: 0;
    }


    /* =========================================
       MEAL CARDS
       ========================================= */

    .meal-card {
        background:
            linear-gradient(
                145deg,
                #ffffff,
                #f0fdf4
            );

        border: 2px solid #bbf7d0;

        border-radius: 20px;

        padding: 22px;

        min-height: 220px;

        box-shadow:
            0 7px 22px rgba(22, 101, 52, 0.07);

        transition:
            transform 0.25s ease,
            box-shadow 0.25s ease;
    }


    .meal-card:hover {
        transform: translateY(-5px);

        box-shadow:
            0 14px 30px rgba(22, 101, 52, 0.13);
    }


    .meal-card h3 {
        color: #166534;

        margin-bottom: 12px;
    }


    .meal-card p {
        color: #44403c;

        margin: 7px 0;
    }


    </style>
    """
)
    /* =========================================
       USER DASHBOARD
       ========================================= */

    .dashboard-header {
        background: linear-gradient(
            135deg,
            #166534,
            #15803d
        );

        border-radius: 25px;

        padding: 30px;

        color: white;

        margin-bottom: 25px;

        box-shadow:
            0 10px 30px rgba(22, 101, 52, 0.18);
    }

    .dashboard-header h1 {
        color: white;

        font-size: 36px;

        margin: 0 0 8px 0;
    }

    .dashboard-header p {
        color: #dcfce7;

        font-size: 16px;

        margin: 0;
    }


    /* =========================================
       STAT CARDS
       ========================================= */

    .stat-card {
        background: #fffdf7;

        border: 2px solid #fde68a;

        border-radius: 20px;

        padding: 20px;

        text-align: center;

        min-height: 120px;

        box-shadow:
            0 6px 18px rgba(245, 158, 11, 0.07);
    }

    .stat-icon {
        font-size: 30px;
    }

    .stat-value {
        color: #166534;

        font-size: 25px;

        font-weight: 800;

        margin-top: 5px;
    }

    .stat-label {
        color: #78716c;

        font-size: 14px;
    }


    /* =========================================
       PROFILE CARD
       ========================================= */

    .profile-card {
        background: white;

        border: 2px solid #dcfce7;

        border-radius: 20px;

        padding: 22px;

        box-shadow:
            0 6px 20px rgba(22, 101, 52, 0.06);
    }


    /* =========================================
       MEAL CARD
       ========================================= */

    .user-meal-card {
        background: white;

        border: 2px solid #dcfce7;

        border-radius: 22px;

        padding: 22px;

        min-height: 245px;

        box-shadow:
            0 8px 25px rgba(22, 101, 52, 0.07);

        transition:
            transform 0.25s ease,
            box-shadow 0.25s ease;
    }

    .user-meal-card:hover {
        transform: translateY(-6px);

        box-shadow:
            0 15px 35px rgba(22, 101, 52, 0.13);
    }

    .meal-emoji {
        font-size: 45px;
    }

    .user-meal-card h3 {
        color: #166534;

        font-size: 21px;

        margin: 7px 0 12px 0;
    }

    .meal-info {
        color: #57534e;

        font-size: 14px;

        margin: 7px 0;
    }

    .meal-price {
        color: #166534;

        font-size: 23px;

        font-weight: 800;
    }

    .rating-badge {
        display: inline-block;

        background: #fef3c7;

        color: #92400e;

        padding: 5px 10px;

        border-radius: 20px;

        font-weight: 700;

        font-size: 13px;
    }

    .availability-badge {
        display: inline-block;

        background: #dcfce7;

        color: #166534;

        padding: 5px 10px;

        border-radius: 20px;

        font-weight: 600;

        font-size: 13px;
    }


    /* =========================================
       ORDER CARD
       ========================================= */

    .order-card {
        background: white;

        border: 2px solid #e7e5e4;

        border-radius: 20px;

        padding: 20px;

        margin-bottom: 15px;

        box-shadow:
            0 5px 18px rgba(0, 0, 0, 0.04);
    }

    .order-title {
        color: #166534;

        font-size: 20px;

        font-weight: 800;
    }

    .order-info {
        color: #57534e;

        margin: 5px 0;
    }

    .status-placed {
        color: #92400e;

        background: #fef3c7;

        padding: 6px 12px;

        border-radius: 20px;

        font-weight: 700;

        display: inline-block;
    }

    .status-accepted {
        color: #1d4ed8;

        background: #dbeafe;

        padding: 6px 12px;

        border-radius: 20px;

        font-weight: 700;

        display: inline-block;
    }

    .status-completed {
        color: #166534;

        background: #dcfce7;

        padding: 6px 12px;

        border-radius: 20px;

        font-weight: 700;

        display: inline-block;
    }

    /* =========================================
       EMPTY STATE
       ========================================= */

    .empty-state {
        text-align: center;

        background: #fffbeb;

        border: 2px dashed #fde68a;

        border-radius: 22px;

        padding: 35px;

        color: #78716c;
    }

    .empty-icon {
        font-size: 50px;
    }

# =========================================================
# HOME PAGE
# =========================================================

def home_page():

    # =========================================
    # HERO
    # =========================================

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
                Discover delicious homemade meals from
                trusted local cooks — made with care,
                delivered with convenience and designed
                to fit your budget.
            </div>

            <div class="hero-badges">

                <div class="badge">
                    🏠 Homemade
                </div>

                <div class="badge">
                    💰 Affordable
                </div>

                <div class="badge">
                    🌱 Fresh
                </div>

                <div class="badge">
                    ⭐ Trusted
                </div>

            </div>

        </div>
        """
    )


    # =========================================
    # WHAT MAKES HOME MEAL SPECIAL
    # =========================================

    st.markdown(
        """
        <div class="section-title">
            🍱 What Makes HomeMeal Special?
        </div>

        <div class="section-subtitle">
            Good food, fair prices and the comfort of home.
        </div>
        """,
        unsafe_allow_html=True
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.html(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    💰
                </div>

                <h3>
                    Affordable
                </h3>

                <p>
                    Delicious homemade meals
                    that fit your everyday budget.
                </p>

            </div>
            """
        )


    with col2:

        st.html(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    🏠
                </div>

                <h3>
                    Home-Cooked
                </h3>

                <p>
                    Fresh meals prepared by
                    local home cooks with care.
                </p>

            </div>
            """
        )


    with col3:

        st.html(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    ❤️
                </div>

                <h3>
                    Trusted
                </h3>

                <p>
                    Ratings and reviews help
                    you choose with confidence.
                </p>

            </div>
            """
        )


    st.divider()


    # =========================================
    # GET STARTED
    # =========================================

    st.markdown(
        """
        <div class="section-title">
            🚀 Get Started
        </div>

        <div class="section-subtitle">
            Choose how you want to use HomeMeal.
        </div>
        """,
        unsafe_allow_html=True
    )


    user_type = st.radio(
        "I am:",
        ["User", "Home Cook"],
        horizontal=True
    )


    if user_type == "User":

        st.info(
            "👤 Discover meals, compare cooks and "
            "place orders."
        )


        if st.button(
            "🍱 Open User Dashboard",
            use_container_width=True
        ):

            go_to("User")

            st.rerun()


    else:

        st.info(
            "👨‍🍳 Add your meals, manage orders and "
            "grow your food business."
        )


        if st.button(
            "👨‍🍳 Open Cook Dashboard",
            use_container_width=True
        ):

            go_to("cook")

            st.rerun()


    st.divider()


    # =========================================
    # WHY HOME MEAL
    # =========================================

    st.markdown(
        """
        <div class="section-title">
            💚 Why HomeMeal?
        </div>

        <div class="section-subtitle">
            More than just a meal — it's the taste of home.
        </div>
        """,
        unsafe_allow_html=True
    )


    why1, why2, why3, why4 = st.columns(4)


    with why1:

        st.html(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    🏠
                </div>

                <h3>
                    Taste of Home
                </h3>

                <p>
                    Enjoy comforting meals
                    prepared like home.
                </p>

            </div>
            """
        )


    with why2:

        st.html(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    💰
                </div>

                <h3>
                    Budget Friendly
                </h3>

                <p>
                    Affordable options for
                    students and everyday users.
                </p>

            </div>
            """
        )


    with why3:

        st.html(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    👩‍🍳
                </div>

                <h3>
                    Support Cooks
                </h3>

                <p>
                    Help talented home cooks
                    turn food into income.
                </p>

            </div>
            """
        )


    with why4:

        st.html(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    ⭐
                </div>

                <h3>
                    Trusted Choices
                </h3>

                <p>
                    Ratings help you discover
                    reliable cooks.
                </p>

            </div>
            """
        )


    st.divider()


    # =========================================
    # HOW HOME MEAL WORKS
    # =========================================

    st.markdown(
        """
        <div class="section-title">
            ⚡ How HomeMeal Works
        </div>

        <div class="section-subtitle">
            From craving to comfort in four simple steps.
        </div>
        """,
        unsafe_allow_html=True
    )


    step1, step2, step3, step4 = st.columns(4)


    with step1:

        st.html(
            """
            <div class="step-card">

                <div class="step-number">
                    1
                </div>

                <h3>
                    🔎 Find
                </h3>

                <p>
                    Explore homemade meals
                    from local cooks.
                </p>

            </div>
            """
        )


    with step2:

        st.html(
            """
            <div class="step-card">

                <div class="step-number">
                    2
                </div>

                <h3>
                    🛒 Order
                </h3>

                <p>
                    Choose your meal and
                    place your order.
                </p>

            </div>
            """
        )


    with step3:

        st.html(
            """
            <div class="step-card">

                <div class="step-number">
                    3
                </div>

                <h3>
                    👩‍🍳 Prepare
                </h3>

                <p>
                    Your home cook prepares
                    your fresh meal.
                </p>

            </div>
            """
        )


    with step4:

        st.html(
            """
            <div class="step-card">

                <div class="step-number">
                    4
                </div>

                <h3>
                    😋 Enjoy
                </h3>

                <p>
                    Enjoy your meal and
                    share your rating.
                </p>

            </div>
            """
        )


    # =========================================
    # FINAL BANNER
    # =========================================

    st.html(
        """
        <div class="trust-banner">

            <h2>
                🍱 Bringing the Taste of Home Closer to You
            </h2>

            <p>
                Connecting hungry users with talented
                local home cooks.
            </p>

        </div>
        """
    )


# =========================================================
# USER DASHBOARD
# =========================================================

def User_dashboard():

    # =========================================
    # HEADER
    # =========================================

    st.html(
        """
        <div class="dashboard-header">

            <h1>
                🍱 Welcome to HomeMeal
            </h1>

            <p>
                Discover fresh, affordable and
                delicious home-cooked meals.
            </p>

        </div>
        """
    )


    # =========================================
    # BACK BUTTON
    # =========================================

    if st.button("⬅️ Back to Home"):

        go_to("home")

        st.rerun()


    st.divider()


    # =========================================
    # USER PROFILE
    # =========================================

    st.markdown(
        """
        <div class="section-title">
            👤 Your Profile
        </div>

        <div class="section-subtitle">
            Tell us what you're looking for.
        </div>
        """,
        unsafe_allow_html=True
    )


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
            ],
            key="user_budget"
        )


    # =========================================
    # SAVE USER
    # =========================================

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


    # =========================================
    # DASHBOARD STATS
    # =========================================

    current_user = (
        user_name.strip()
        if user_name.strip()
        else "User"
    )


    my_orders = [

        order

        for order in st.session_state.orders

        if order.get("customer", "") == current_user

    ]


    completed_orders = sum(
        1
        for order in my_orders
        if order.get("status") == "Completed"
    )


    active_orders = sum(
        1
        for order in my_orders
        if order.get("status") in [
            "Placed",
            "Accepted"
        ]
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.html(
            f"""
            <div class="stat-card">

                <div class="stat-icon">
                    📦
                </div>

                <div class="stat-value">
                    {len(my_orders)}
                </div>

                <div class="stat-label">
                    Total Orders
                </div>

            </div>
            """
        )


    with col2:

        st.html(
            f"""
            <div class="stat-card">

                <div class="stat-icon">
                    🔄
                </div>

                <div class="stat-value">
                    {active_orders}
                </div>

                <div class="stat-label">
                    Active Orders
                </div>

            </div>
            """
        )


    with col3:

        st.html(
            f"""
            <div class="stat-card">

                <div class="stat-icon">
                    ✅
                </div>

                <div class="stat-value">
                    {completed_orders}
                </div>

                <div class="stat-label">
                    Completed
                </div>

            </div>
            """
        )


    st.divider()


    # =========================================
    # FIND MEALS
    # =========================================

    st.markdown(
        """
        <div class="section-title">
            🍱 Find Your Meal
        </div>

        <div class="section-subtitle">
            Homemade food from cooks around you.
        </div>
        """,
        unsafe_allow_html=True
    )


    search = st.text_input(
        "🔎 Search",
        placeholder="Search for Rajma, Thali, Pasta, Cook name..."
    )


    # =========================================
    # BUDGET FILTER
    # =========================================

    budget_filter = st.selectbox(
        "💰 Filter by Budget",
        [
            "All Meals",
            "Under ₹50",
            "₹50 - ₹100",
            "₹100 - ₹150",
            "Above ₹150"
        ]
    )


    available_meals = []


    for meal in st.session_state.meals:

        quantity = meal.get(
            "quantity",
            0
        )


        if quantity <= 0:

            continue


        meal_name = meal.get(
            "name",
            ""
        )


        cook_name = meal.get(
            "cook",
            ""
        )


        price = meal.get(
            "price",
            0
        )


        # Search filter

        if search:

            search_lower = search.lower()


            if (
                search_lower not in meal_name.lower()
                and
                search_lower not in cook_name.lower()
            ):

                continue


        # Budget filter

        if budget_filter == "Under ₹50":

            if price >= 50:
                continue


        elif budget_filter == "₹50 - ₹100":

            if price < 50 or price > 100:
                continue


        elif budget_filter == "₹100 - ₹150":

            if price < 100 or price > 150:
                continue


        elif budget_filter == "Above ₹150":

            if price <= 150:
                continue


        available_meals.append(meal)


    # =========================================
    # DISPLAY MEALS
    # =========================================

    if not available_meals:

        st.html(
            """
            <div class="empty-state">

                <div class="empty-icon">
                    🔎
                </div>

                <h3>
                    No meals found
                </h3>

                <p>
                    Try another search or budget range.
                </p>

            </div>
            """
        )


    else:

        columns = st.columns(3)


        for index, meal in enumerate(
            available_meals
        ):

            with columns[index % 3]:

                # =================================
                # FIND COOK RATING
                # =================================

                cook_rating = 5.0

                cook_rating_count = 0


                for cook in database["cooks"]:

                    if (
                        cook.get("name", "").lower()
                        ==
                        meal.get("cook", "").lower()
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


                # =================================
                # MEAL CARD
                # =================================

                st.html(
                    f"""
                    <div class="user-meal-card">

                        <div class="meal-emoji">
                            🍱
                        </div>

                        <h3>
                            {meal.get("name", "Meal")}
                        </h3>

                        <div class="meal-info">
                            👩‍🍳
                            <b>Cook:</b>
                            {meal.get("cook", "Unknown")}
                        </div>

                        <div class="meal-info">

                            <span class="rating-badge">
                                ⭐ {cook_rating}/5
                            </span>

                            &nbsp;

                            <small>
                                {cook_rating_count} ratings
                            </small>

                        </div>

                        <div class="meal-info">

                            <span class="availability-badge">
                                📦
                                {meal.get("quantity", 0)}
                                available
                            </span>

                        </div>

                        <div class="meal-price">
                            ₹{meal.get("price", 0)}
                        </div>

                    </div>
                    """
                )


                # =================================
                # ORDER BUTTON
                # =================================

                if st.button(
                    f"🛒 Order {meal.get('name', 'Meal')}",
                    key=f"order_{meal.get('id')}",
                    use_container_width=True
                ):

                    customer = (
                        user_name.strip()
                        if user_name.strip()
                        else "User"
                    )


                    new_order = {

                        "id":
                            st.session_state.next_order_id,

                        "meal":
                            meal.get(
                                "name",
                                "Meal"
                            ),

                        "cook":
                            meal.get(
                                "cook",
                                "Unknown"
                            ),

                        "customer":
                            customer,

                        "price":
                            meal.get(
                                "price",
                                0
                            ),

                        "status":
                            "Placed",

                        "rating":
                            None
                    }


                    # Add order

                    st.session_state.orders.append(
                        new_order
                    )


                    # Reduce quantity

                    for saved_meal in (
                        st.session_state.meals
                    ):

                        if (
                            saved_meal.get("id")
                            ==
                            meal.get("id")
                        ):

                            saved_meal["quantity"] -= 1

                            break


                    # Save

                    database["orders"] = (
                        st.session_state.orders
                    )

                    database["meals"] = (
                        st.session_state.meals
                    )


                    save_database(
                        database
                    )


                    st.session_state.next_order_id += 1


                    st.success(
                        f"✅ Order placed for "
                        f"{meal.get('name', 'Meal')}!"
                    )


                    st.rerun()


    st.divider()


    # =========================================
    # MY ORDERS
    # =========================================

    st.markdown(
        """
        <div class="section-title">
            📦 My Orders
        </div>

        <div class="section-subtitle">
            Track your meals and manage your orders.
        </div>
        """,
        unsafe_allow_html=True
    )


    if not my_orders:

        st.html(
            """
            <div class="empty-state">

                <div class="empty-icon">
                    🍱
                </div>

                <h3>
                    No orders yet
                </h3>

                <p>
                    Find your first homemade meal above!
                </p>

            </div>
            """
        )


    else:

        for order in reversed(my_orders):

            order_id = order.get(
                "id",
                0
            )

            status = order.get(
                "status",
                "Placed"
            )


            # =================================
            # STATUS CLASS
            # =================================

            if status == "Accepted":

                status_html = (
                    '<span class="status-accepted">'
                    '🔵 Accepted'
                    '</span>'
                )


            elif status == "Completed":

                status_html = (
                    '<span class="status-completed">'
                    '🟢 Completed'
                    '</span>'
                )


            else:

                status_html = (
                    '<span class="status-placed">'
                    '🟡 Placed'
                    '</span>'
                )


            # =================================
            # ORDER CARD
            # =================================

            st.html(
                f"""
                <div class="order-card">

                    <div class="order-title">
                        🧾 Order #{order_id:03d}
                    </div>

                    <div class="order-info">
                        🍱
                        <b>Meal:</b>
                        {order.get("meal", "Unknown")}
                    </div>

                    <div class="order-info">
                        👩‍🍳
                        <b>Cook:</b>
                        {order.get("cook", "Unknown")}
                    </div>

                    <div class="order-info">
                        💰
                        <b>Price:</b>
                        ₹{order.get("price", 0)}
                    </div>

                    <div class="order-info">
                        📍
                        <b>Status:</b>
                        {status_html}
                    </div>

                </div>
                """
            )


            # =================================
            # RATING
            # =================================

            if status == "Completed":

                if order.get("rating") is None:

                    st.markdown(
                        "### ⭐ Rate Your Cook"
                    )


                    rating = st.radio(
                        "How was your experience?",
                        [1, 2, 3, 4, 5],

                        format_func=lambda x:
                            "⭐" * x,

                        horizontal=True,

                        key=f"rating_{order_id}"
                    )


                    if st.button(
                        "⭐ Submit Rating",
                        key=f"submit_rating_{order_id}",
                        use_container_width=True
                    ):

                        # Save rating to order

                        for saved_order in (
                            st.session_state.orders
                        ):

                            if (
                                saved_order.get("id")
                                ==
                                order_id
                            ):

                                saved_order["rating"] = rating

                                break


                        # Find cook

                        cook_found = False


                        for cook in database["cooks"]:

                            if (
                                cook.get("name", "").lower()
                                ==
                                order.get(
                                    "cook",
                                    ""
                                ).lower()
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
                                    sum(
                                        cook["ratings"]
                                    )
                                    /
                                    len(
                                        cook["ratings"]
                                    ),
                                    1
                                )


                                cook_found = True

                                break


                        # Create cook if missing

                        if not cook_found:

                            database["cooks"].append(
                                {
                                    "name":
                                        order.get(
                                            "cook",
                                            "Unknown Cook"
                                        ),

                                    "location":
                                        "",

                                    "ratings":
                                        [rating],

                                    "rating":
                                        float(rating),

                                    "rating_count":
                                        1
                                }
                            )


                        database["orders"] = (
                            st.session_state.orders
                        )


                        save_database(
                            database
                        )


                        st.success(
                            "⭐ Thank you! "
                            "Your rating has been submitted."
                        )


                        st.rerun()


                else:

                    st.success(
                        f"⭐ You rated this cook "
                        f"{order.get('rating')}/5"
                    )
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
                    f"🍱 **Meal:** {order.get('meal', 'Unknown')}"
                )

                st.write(
                    f"👨‍🍳 **Cook:** {order.get('cook', 'Unknown')}"
                )

                st.write(
                    f"💰 **Price:** ₹{order.get('price', 0)}"
                )

                st.write(
                    f"📍 **Status:** {order.get('status', 'Placed')}"
                )

                # =============================================
                # RATING
                # =============================================

                if order.get("status") == "Completed":

                    if order.get("rating") is None:

                        st.markdown("### ⭐ Rate Your Cook")

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

                            # Find cook and update rating
                            cook_found = False

                            for cook in database["cooks"]:

                                if (
                                    cook.get("name", "").lower()
                                    == order.get("cook", "").lower()
                                ):

                                    if "ratings" not in cook:
                                        cook["ratings"] = []

                                    cook["ratings"].append(rating)

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

                            # Create cook if not found
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
                                "⭐ Thank you! Your rating has been submitted."
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

    st.title("👨‍🍳 Home Cook Dashboard")

    st.write(
        "Manage your meals, orders and earnings from one place."
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
                        f"### 🍱 {meal.get('name', 'Meal')}"
                    )

                    st.write(
                        f"⭐ {meal.get('rating', 5.0)}/5"
                    )

                with col2:

                    st.write(
                        f"💰 ₹{meal.get('price', 0)}"
                    )

                with col3:

                    st.write(
                        f"📦 {meal.get('quantity', 0)}"
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
                        f"### 🧾 Order #{order.get('id', 0):03d}"
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

                    # =================================================
                    # ACCEPT ORDER
                    # =================================================

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

                    # =================================================
                    # COMPLETE ORDER
                    # =================================================

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

                    # =================================================
                    # COMPLETED
                    # =================================================

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
