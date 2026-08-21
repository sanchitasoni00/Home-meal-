import streamlit as st
import json
import os
#========================================================
#  JSON DATABASE
# ========================================================
DATABASE_FILE= "database.json"
def  laod_database():
    if not
    
os.path.exists(DATABASE_FILE):
    database = {
        "users"  : [],
        "cooks":[],
        "meals":[],
        "orders":[]
    }
    with open(DATABASE_FILE,
"w") as file :
                   json.dump(database,
file , indent = 4)
          return database
    with open(DATABASE_FILE , "r")
as file:
    return json.load(file)
def save_dattabase(database):
    with open(DATABASE_FILE , "w")
as file:
    json.dump(database, file,
indent = 4)

database = load_database()

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="HomeMeal",
    page_icon="🍱",
    layout="wide"
)

# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "meals" not in st.session_state:
    st.session_state.meals = 
database["meals"]
else:
    st.session_state.meals = [
        {
            "id": 1,
            "name": "Rajma Chawal",
            "cook": "Navneet ",
            "rating": 4.8,
            "price": 70,
            "quantity": 7
        },
        {
            "id": 2,
            "name": "Veg Thali",
            "cook": "Neha",
            "rating": 4.7,
            "price": 90,
            "quantity": 6
        },
        {
            "id": 3,
            "name": "Pasta",
            "cook": "Anjali",
            "rating": 4.6,
            "price": 100,
            "quantity": 4
        }
    ]
    database["meals"] = 
st.session_state.meals
            save_database(database)

     

if "orders" not in st.session_state:
    st.session_state.orders = database["orders']

if "next_meal_id" not in st.session_state:
    st.session_state.next_meal_id = 4

if "next_order_id" not in st.session_state:
    st.session_state.next_order_id = 1

if "cook_name" not in st.session_state:
    st.session_state.cook_name = ""
# =========================================================
# FIX OLD MEAL DATA
# =========================================================

for meal in st.session_state.meals:

    if "quantity" not in meal:
        meal["quantity"] = 10

    if "id" not in meal:
        meal["id"] = st.session_state.next_meal_id
        st.session_state.next_meal_id += 1


# =========================================================
# NAVIGATION
# =========================================================

def go_to(page):
    st.session_state.page = page


# =========================================================
# CUSTOM CSS
# =========================================================

st.html("""
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

</style>
""")


# =========================================================
# HOME PAGE
# =========================================================

def home_page():

    st.html("""
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
    """)

    st.divider()

    # =====================================================
    # FEATURES
    # =====================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.html("""
        <div class="feature-card">

            <div class="feature-icon">💰</div>

            <h3>Affordable</h3>

            <p>
                Find delicious meals that fit your budget.
            </p>

        </div>
        """)

    with col2:

        st.html("""
        <div class="feature-card">

            <div class="feature-icon">🏠</div>

            <h3>Home-Cooked</h3>

            <p>
                Fresh meals prepared by local home cooks.
            </p>

        </div>
        """)

    with col3:

        st.html("""
        <div class="feature-card">

            <div class="feature-icon">❤️</div>

            <h3>Trusted</h3>

            <p>
                Connect with reliable local cooks.
            </p>

        </div>
        """)

    st.divider()

    # =====================================================
    # CHOOSE ROLE
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


# =========================================================
# USER DASHBOARD
# =========================================================

def User_dashboard():

    st.title("👤 User Dashboard")

    st.write(
        "Welcome to HomeMeal! Discover fresh, affordable "
        "and delicious home-cooked meals near you."
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
if user_name.strip():
    existing_user = None
for user in database ["users"]:
    if users["name"].lower() == user_name.strip.lower():
        existing_user = user
        break
    if existing_user:
        existing_user["budget"] = budget
    else:
        database["users"].append(
            {
                "name": user_name.strip(),
                "budget":budget
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
        placeholder="Example: Rajma, Thali, Priya..."
    )

    available_meals = []

    for meal in st.session_state.meals:

        if meal["quantity"] > 0:

            if (
                not search
                or search.lower() in meal["name"].lower()
                or search.lower() in meal["cook"].lower()
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

                st.markdown(
                    f"""
                    <div class="meal-card">

                    <h3>🍱 {meal["name"]}</h3>

                    <p>👨‍🍳 Cook: {meal["cook"]}</p>

                    <p>⭐ {meal["rating"]}/5</p>

                    <p>💰 ₹{meal["price"]}</p>

                    <p>📦 Available: {meal["quantity"]}</p>

                    </div>
                    """,
                    unsafe_allow_html=True
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
                        "status": "Placed"
                    }

                    st.session_state.orders.append(
                        new_order
                    )
                    database["orders"] = st.session_state.orders
                    save_database(database)
                    

                    # Reduce meal quantity
                    for saved_meal in st.session_state.meals:

                        if saved_meal["id"] == meal["id"]:

                            saved_meal["quantity"] -= 1
                            break

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

        if order["customer"] == current_user:

            my_orders.append(order)

    if not my_orders:

        st.info(
            "No orders yet. Start exploring meals!"
        )

    else:

        for order in reversed(my_orders):

            with st.container(border=True):

                st.markdown(
                    f"### 🧾 Order #{order['id']:03d}"
                )

                st.write(
                    f"🍱 **Meal:** {order['meal']}"
                )

                st.write(
                    f"👨‍🍳 **Cook:** {order['cook']}"
                )

                st.write(
                    f"💰 **Price:** ₹{order['price']}"
                )

                st.write(
                    f"📍 **Status:** {order['status']}"
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
if cook_name.strip():
    existing_cook = None
    for cook in database["cooks"]:
        if cook["name"].lower() == cook_name.strip().lower():
            existing_cook = cook
            break
if existing_cook:
    existing_cook["location"] = location
else:
      database["cooks"].append(
          {
              "name" : cook_name.strip()
              "location" : location
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
            or order["cook"].lower()
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
            or meal["cook"].lower()
            == cook_name.strip().lower()
        ):

            my_meals.append(meal)

    # =====================================================
    # STATISTICS
    # =====================================================

    total_orders = len(cook_orders)

    earnings = sum(
        order["price"]
        for order in cook_orders
        if order["status"] in [
            "Accepted",
            "Completed"
        ]
    )

    total_meals = len(my_meals)

    customers = len(
        set(
            order["customer"]
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
            database["meals'] = st.session_state.meals
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
                        f"### 🍱 {meal['name']}"
                    )

                    st.write(
                        f"⭐ {meal['rating']}/5"
                    )

                with col2:

                    st.write(
                        f"💰 ₹{meal['price']}"
                    )

                with col3:

                    st.write(
                        f"📦 {meal['quantity']}"
                    )

    st.divider()

    # =====================================================
    # RECENT ORDERS
    # =====================================================

    st.subheader("📦 Recent Orders")

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
                        f"### 🧾 Order #{order['id']:03d}"
                    )

                    st.write(
                        f"🍱 **Meal:** {order['meal']}"
                    )

                    st.write(
                        f"👤 **User:** {order['customer']}"
                    )

                    st.write(
                        f"💰 **Price:** ₹{order['price']}"
                    )

                    st.write(
                        f"📍 **Status:** {order['status']}"
                    )

                with col2:

                    if order["status"] == "Placed":

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

                                    saved_order[
                                        "status"
                                    ] = "Accepted"

                                    break
                          database["orders"] = st.session_state.orders
                          save_database(database)

                            st.success(
                                "Order accepted!"
                            )

                            st.rerun()

                    elif order["status"] == "Accepted":

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

                                    saved_order[
                                        "status"
                                    ] = "Completed"

                                    break
                             database["orders"] = st.session_state.orders
                             save_database(database)

                            st.success(
                                "Order completed!"
                            )

                            st.rerun()

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
    import streamlit as st
from supabase import create_client

