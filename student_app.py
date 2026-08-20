import json
from pathlib import Path
import streamlit as st


# -------------------------------------------------
# HOME MEAL - MEMBER 2
# Student-side application
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "cooks.json"


# -------------------------------------------------
# LOAD COOK DATA
# -------------------------------------------------

def load_cooks():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return []


cooks = load_cooks()


# -------------------------------------------------
# PAGE SETTINGS
# -------------------------------------------------

st.set_page_config(
    page_title="HomeMeal - Student",
    page_icon="🍱",
    layout="wide"
)


# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------

if "selected_cook" not in st.session_state:
    st.session_state.selected_cook = None

if "plan" not in st.session_state:
    st.session_state.plan = None

if "order_confirmed" not in st.session_state:
    st.session_state.order_confirmed = False


# -------------------------------------------------
# HEADER
# -------------------------------------------------

st.title("🍱 HomeMeal")

st.subheader("Find Fresh, Affordable Home-Cooked Meals")

st.write(
    "Discover home cooks near you and choose meals "
    "according to your budget and preferences."
)

st.divider()


# -------------------------------------------------
# 1. LOCATION
# -------------------------------------------------

st.header("📍 1. Choose Your Location")

locations = [
    "Sector 15",
    "Sector 17",
    "Sector 22",
    "Sector 34"
]

location = st.selectbox(
    "Where are you staying?",
    locations
)

st.success("Location selected: " + location)


# -------------------------------------------------
# 2. FILTERS
# -------------------------------------------------

st.header("🔎 2. Find Your Meal")

col1, col2 = st.columns(2)

with col1:
    max_price = st.number_input(
        "Maximum price (₹)",
        min_value=0,
        max_value=1000,
        value=150,
        step=10
    )

    food_preference = st.selectbox(
        "Food preference",
        [
            "All",
            "North Indian",
            "South Indian",
            "Punjabi",
            "Chinese",
            "Vegetarian"
        ]
    )

with col2:
    meal_type = st.selectbox(
        "Meal type",
        [
            "All",
            "Lunch",
            "Dinner"
        ]
    )

    spice_level = st.selectbox(
        "Spice level",
        [
            "All",
            "Mild",
            "Medium",
            "Spicy"
        ]
    )


# -------------------------------------------------
# FILTER COOKS
# -------------------------------------------------

filtered_cooks = []

for cook in cooks:

    price = cook.get("price", 0)
    food = cook.get("food_preference", "")
    meals = cook.get("meals", [])
    spice = cook.get("spice_level", "")

    if price > max_price:
        continue

    if food_preference != "All":
        if food.lower() != food_preference.lower():
            continue

    if meal_type != "All":
        if meal_type not in meals:
            continue

    if spice_level != "All":
        if spice.lower() != spice_level.lower():
            continue

    filtered_cooks.append(cook)


st.divider()


# -------------------------------------------------
# 3. NEARBY COOKS
# -------------------------------------------------

st.header("🏠 3. Nearby Home Cooks")

if not filtered_cooks:

    st.warning(
        "No cooks match your current filters. "
        "Try increasing your maximum price or changing your preferences."
    )

else:

    for cook in filtered_cooks:

        col1, col2, col3 = st.columns([3, 2, 1])

        with col1:
            st.subheader("👩‍🍳 " + cook.get("name", "Home Cook"))

            st.write(
                cook.get(
                    "description",
                    "Fresh home-cooked meals."
                )
            )

        with col2:
            st.write("💰 Price: ₹" + str(cook.get("price", 0)))
            st.write("⭐ Rating: " + str(cook.get("rating", 0)))
            st.write(
                "📍 Distance: "
                + str(cook.get("distance_km", 0))
                + " km"
            )

        with col3:

            if st.button(
                "View Menu",
                key="cook_" + str(cook.get("id"))
            ):

                st.session_state.selected_cook = cook

                st.session_state.order_confirmed = False

        st.divider()


# -------------------------------------------------
# 4. MENU
# -------------------------------------------------

if st.session_state.selected_cook:

    cook = st.session_state.selected_cook

    st.header("🍛 4. Today's Menu")

    st.subheader(
        "Menu from " + cook.get("name", "Home Cook")
    )

    st.write(
        "Food preference: "
        + cook.get("food_preference", "Not specified")
    )

    st.write(
        "Spice level: "
        + cook.get("spice_level", "Not specified")
    )

    st.write(
        "Available meals: "
        + ", ".join(cook.get("meals", []))
    )

    st.write(
        "Price per meal: ₹"
        + str(cook.get("price", 0))
    )

    st.info(
        cook.get(
            "description",
            "Fresh home-cooked food."
        )
    )

    st.divider()


    # -------------------------------------------------
    # 5. MEAL PLAN
    # -------------------------------------------------

    st.header("📅 5. Choose Your Meal Plan")

    plan = st.selectbox(
        "Select a plan",
        [
            "One Meal",
            "7-Day Plan",
            "30-Day Plan"
        ]
    )

    if plan == "One Meal":
        meals_count = 1

    elif plan == "7-Day Plan":
        meals_count = 7

    else:
        meals_count = 30


    price_per_meal = cook.get("price", 0)

    total_price = price_per_meal * meals_count

    st.write("Number of meals:", meals_count)

    st.metric(
        "Total Price",
        "₹" + str(total_price)
    )


    # -------------------------------------------------
    # 6. SUBSCRIPTION CONFIRMATION
    # -------------------------------------------------

    st.header("✅ 6. Confirm Subscription")

    st.write("**Cook:**", cook.get("name", "Home Cook"))

    st.write("**Plan:**", plan)

    st.write("**Meals:**", meals_count)

    st.write("**Total:** ₹" + str(total_price))


    if st.button(
        "Confirm Subscription",
        type="primary"
    ):

        st.session_state.plan = {
            "cook": cook.get("name", "Home Cook"),
            "cook_id": cook.get("id"),
            "plan": plan,
            "meals": meals_count,
            "total": total_price
        }

        st.session_state.order_confirmed = True

        st.success(
            "🎉 Subscription confirmed successfully!"
        )


# -------------------------------------------------
# 7. ORDER STATUS
# -------------------------------------------------

if st.session_state.order_confirmed:

    st.divider()

    st.header("📦 7. Order Status")

    order = st.session_state.plan

    st.success("Order Confirmed")

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            "**Cook:** "
            + str(order["cook"])
        )

        st.write(
            "**Plan:** "
            + str(order["plan"])
        )

        st.write(
            "**Total:** ₹"
            + str(order["total"])
        )

    with col2:

        st.write(
            "**Meals remaining:** "
            + str(order["meals"])
        )

        st.write(
            "**Status:** Order Confirmed"
        )

        st.write(
            "**Location:** "
            + location
        )

    st.info(
        "Your home-cooked meal order has been confirmed."
    )


# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.divider()

st.caption(
    "HomeMeal • Connecting students with affordable "
    "home-cooked meals"
)
