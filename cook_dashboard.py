import json
from pathlib import Path
import streamlit as st

from logic.order_logic import (
    get_orders_for_cook,
    update_order_status,
    calculate_earnings
)


# -------------------------------------------------
# HOME MEAL - MEMBER 3
# COOK DASHBOARD
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
COOKS_FILE = BASE_DIR / "data" / "cooks.json"


# -------------------------------------------------
# LOAD COOKS
# -------------------------------------------------

def load_cooks():
    try:
        with open(COOKS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return []


cooks = load_cooks()


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

st.sidebar.title("👩‍🍳 Cook Panel")

if not cooks:

    st.error("No cooks found in cooks.json")
    st.stop()

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

cook_id = cook.get("id")


# -------------------------------------------------
# HEADER
# -------------------------------------------------

st.title("👩‍🍳 HomeMeal Cook Dashboard")

st.subheader(
    "Welcome, " + cook.get("name", "Home Cook")
)

st.write(
    "Manage your meals, orders and earnings."
)

st.divider()


# -------------------------------------------------
# GET REAL ORDERS
# -------------------------------------------------

cook_orders = get_orders_for_cook(cook_id)


# -------------------------------------------------
# SUMMARY
# -------------------------------------------------

total_orders = len(cook_orders)

active_orders = len([
    order
    for order in cook_orders
    if order.get("status") in
    ["Pending", "Confirmed"]
])

earnings = calculate_earnings(cook_id)


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Orders",
        total_orders
    )

with col2:
    st.metric(
        "Active Orders",
        active_orders
    )

with col3:
    st.metric(
        "Rating",
        "⭐ " + str(cook.get("rating", 0))
    )

with col4:
    st.metric(
        "Earnings",
        "₹" + str(earnings)
    )


st.divider()


# -------------------------------------------------
# COOK PROFILE
# -------------------------------------------------

st.header("👤 My Profile")

col1, col2 = st.columns(2)

with col1:

    st.write(
        "**Name:** "
        + cook.get("name", "Home Cook")
    )

    st.write(
        "**Food:** "
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


st.success("✓ Verified Home Cook")

st.divider()


# -------------------------------------------------
# MENU
# -------------------------------------------------

st.header("🍛 Today's Menu")

meals = cook.get("meals", [])

if meals:

    for meal in meals:
        st.write("• " + str(meal))

else:

    st.info("No meals added yet.")


st.write(
    "**Price per meal:** ₹"
    + str(cook.get("price", 0))
)


st.divider()


# -------------------------------------------------
# REAL ORDERS
# -------------------------------------------------

st.header("📦 Student Orders")

if not cook_orders:

    st.info(
        "No orders yet. Orders placed by students "
        "will appear here."
    )

else:

    for order in cook_orders:

        order_id = order.get(
            "order_id",
            "Unknown"
        )

        st.subheader(
            "Order " + str(order_id)
        )

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                "**Student:** "
                + str(
                    order.get(
                        "student_name",
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
                "**Meal:** "
                + str(
                    order.get(
                        "meal_type",
                        "Meal"
                    )
                )
            )

        with col2:

            st.write(
                "**Amount:** ₹"
                + str(
                    order.get(
                        "total",
                        0
                    )
                )
            )

            st.write(
                "**Current Status:** "
                + str(
                    order.get(
                        "status",
                        "Pending"
                    )
                )
            )


        # -----------------------------------------
        # UPDATE STATUS
        # -----------------------------------------

        statuses = [
            "Pending",
            "Confirmed",
            "Completed"
        ]

        current_status = order.get(
            "status",
            "Pending"
        )

        if current_status not in statuses:
            current_status = "Pending"

        new_status = st.selectbox(
            "Change order status",
            statuses,
            index=statuses.index(
                current_status
            ),
            key="status_" + str(order_id)
        )


        if st.button(
            "Update Order",
            key="update_" + str(order_id)
        ):

            updated_order = update_order_status(
                order_id,
                new_status
            )

            if updated_order:

                st.success(
                    "Order updated to "
                    + new_status
                )

                st.rerun()

            else:

                st.error(
                    "Could not update the order."
                )


        st.divider()


# -------------------------------------------------
# EARNINGS
# -------------------------------------------------

st.header("💰 Earnings")

st.metric(
    "Total Confirmed/Completed Earnings",
    "₹" + str(earnings)
)

st.write(
    "Earnings are calculated from confirmed "
    "and completed orders."
)


# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.divider()

st.caption(
    "HomeMeal • Cook Dashboard • SIH MVP"
)
