import json
from pathlib import Path
import streamlit as st


# -------------------------------------------------
# HOME MEAL - MEMBER 3
# Cook Dashboard
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

COOKS_FILE = BASE_DIR / "data" / "cooks.json"
ORDERS_FILE = BASE_DIR / "data" / "orders.json"


# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

def load_json(file_path, default):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return default


cooks = load_json(COOKS_FILE, [])
orders = load_json(ORDERS_FILE, [])


# -------------------------------------------------
# PAGE SETTINGS
# -------------------------------------------------

st.set_page_config(
    page_title="HomeMeal - Cook Dashboard",
    page_icon="👩‍🍳",
    layout="wide"
)


# -------------------------------------------------
# SELECT COOK
# -------------------------------------------------

if cooks:

    cook_names = [
        cook.get("name", "Home Cook")
        for cook in cooks
    ]

    selected_name = st.sidebar.selectbox(
        "Select Cook",
        cook_names
    )

    cook = next(
        (
            item for item in cooks
            if item.get("name") == selected_name
        ),
        cooks[0]
    )

else:

    cook = {
        "id": 1,
        "name": "Sample Home Cook",
        "price": 80,
        "food_preference": "North Indian",
        "rating": 4.5,
        "distance_km": 1.5,
        "spice_level": "Medium",
        "description": "Fresh home-cooked meals.",
        "meals": ["Lunch", "Dinner"]
    }


cook_id = cook.get("id")


# -------------------------------------------------
# HEADER
# -------------------------------------------------

st.title("👩‍🍳 HomeMeal Cook Dashboard")

st.subheader(
    "Welcome, " + cook.get("name", "Home Cook")
)

st.write(
    "Manage your profile, meals, orders and earnings."
)

st.divider()


# -------------------------------------------------
# FIND COOK ORDERS
# -------------------------------------------------

cook_orders = []

for order in orders:

    if str(order.get("cook_id")) == str(cook_id):
        cook_orders.append(order)


# -------------------------------------------------
# SUMMARY CARDS
# -------------------------------------------------

today_orders = len(cook_orders)

active_orders = len(
    [
        order
        for order in cook_orders
        if order.get("status", "").lower()
        not in ["completed", "cancelled"]
    ]
)

price_per_meal = cook.get("price", 0)

estimated_earnings = (
    today_orders * price_per_meal
)


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Today's Orders",
        today_orders
    )

with col2:
    st.metric(
        "Active Orders",
        active_orders
    )

with col3:
    st.metric(
        "Daily Capacity",
        cook.get("daily_capacity", 25)
    )

with col4:
    st.metric(
        "Estimated Earnings",
        "₹" + str(estimated_earnings)
    )


st.divider()


# -------------------------------------------------
# PROFILE
# -------------------------------------------------

st.header("👤 Cook Profile")

col1, col2 = st.columns(2)

with col1:

    st.write(
        "**Name:** "
        + cook.get("name", "Home Cook")
    )

    st.write(
        "**Food Type:** "
        + cook.get(
            "food_preference",
            "Not specified"
        )
    )

    st.write(
        "**Rating:** ⭐ "
        + str(cook.get("rating", 0))
    )

with col2:

    st.write(
        "**Price:** ₹"
        + str(cook.get("price", 0))
        + " / meal"
    )

    st.write(
        "**Distance:** "
        + str(cook.get("distance_km", 0))
        + " km"
    )

    st.write(
        "**Spice Level:** "
        + cook.get(
            "spice_level",
            "Not specified"
        )
    )


# -------------------------------------------------
# VERIFICATION
# -------------------------------------------------

if cook.get("verified", True):

    st.success("✓ Verified Home Cook")

else:

    st.warning("Verification Pending")


st.divider()


# -------------------------------------------------
# TODAY'S MENU
# -------------------------------------------------

st.header("🍛 Today's Menu")

menu_items = cook.get("menu", [])

if menu_items:

    for item in menu_items:

        st.write("• " + str(item))

else:

    st.info(
        "Today's sample menu is based on the cook's "
        "available meal type."
    )

    meals = cook.get("meals", [])

    if meals:

        for meal in meals:
            st.write(
                "• " + str(meal)
                + " - Home-cooked meal"
            )


st.write(
    "**Price:** ₹"
    + str(cook.get("price", 0))
    + " per meal"
)


# -------------------------------------------------
# PRICE & CAPACITY
# -------------------------------------------------

st.header("💰 Price & Daily Capacity")

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Price per Meal",
        "₹" + str(cook.get("price", 0))
    )

with col2:

    st.metric(
        "Maximum Daily Meals",
        cook.get("daily_capacity", 25)
    )


st.divider()


# -------------------------------------------------
# ORDERS
# -------------------------------------------------

st.header("📦 Subscriber / Order List")

if cook_orders:

    for order in cook_orders:

        with st.container():

            st.write(
                "**Order ID:** "
                + str(
                    order.get(
                        "order_id",
                        order.get("id", "N/A")
                    )
                )
            )

            st.write(
                "**Student:** "
                + str(
                    order.get(
                        "student_id",
                        "Student"
                    )
                )
            )

            st.write(
                "**Plan:** "
                + str(
                    order.get(
                        "plan",
                        "One Meal"
                    )
                )
            )

            st.write(
                "**Meal Type:** "
                + str(
                    order.get(
                        "meal_type",
                        "Meal"
                    )
                )
            )

            status = order.get(
                "status",
                "Pending"
            )

            if status.lower() == "confirmed":

                st.success(
                    "Status: " + status
                )

            elif status.lower() == "completed":

                st.info(
                    "Status: " + status
                )

            else:

                st.warning(
                    "Status: " + status
                )

            st.divider()

else:

    st.info(
        "No orders have been received yet."
    )


# -------------------------------------------------
# EARNINGS
# -------------------------------------------------

st.header("💵 Earnings")

st.write(
    "Today's Orders: "
    + str(today_orders)
)

st.write(
    "Price per Meal: ₹"
    + str(price_per_meal)
)

st.metric(
    "Estimated Today's Earnings",
    "₹" + str(estimated_earnings)
)

st.caption(
    "This is a simple MVP estimate. "
    "Advanced accounting is not included."
)


# -------------------------------------------------
# ORDER STATUS
# -------------------------------------------------

st.header("🔄 Order Status")

if cook_orders:

    for order in cook_orders:

        current_status = order.get(
            "status",
            "Pending"
        )

        new_status = st.selectbox(
            "Status for Order "
            + str(
                order.get(
                    "order_id",
                    order.get("id", "N/A")
                )
            ),
            [
                "Pending",
                "Confirmed",
                "Completed"
            ],
            index=(
                [
                    "Pending",
                    "Confirmed",
                    "Completed"
                ].index(current_status)
                if current_status in
                ["Pending", "Confirmed", "Completed"]
                else 0
            ),
            key="status_" + str(
                order.get(
                    "order_id",
                    order.get("id", "N/A")
                )
            )
        )

        if st.button(
            "Update Status",
            key="update_" + str(
                order.get(
                    "order_id",
                    order.get("id", "N/A")
                )
            )
        ):

            order["status"] = new_status

            st.success(
                "Order status changed to "
                + new_status
            )

else:

    st.info(
        "Order status will appear here when "
        "students place orders."
    )


# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.divider()

st.caption(
    "HomeMeal • Home Cook Dashboard • SIH MVP"
)
