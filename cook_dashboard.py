import streamlit as st
from logic.order_logic import (
    get_cooks,
    get_orders_for_cook,
    update_order_status,
    calculate_earnings
)

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------

st.set_page_config(
    page_title="HomeMeal - Cook Dashboard",
    page_icon="🍱",
    layout="wide"
)

# -----------------------------
# HEADER
# -----------------------------

st.title("🍳 HomeMeal")
st.subheader("Cook Dashboard")

st.write(
    "Manage your meal orders, check students' requests, "
    "and track your earnings."
)

st.divider()

# -----------------------------
# LOAD COOKS
# -----------------------------

cooks = get_cooks()

if not cooks:
    st.warning("No cooks found in the system.")
    st.info("Please add cooks to data/cooks.json first.")
    st.stop()

# -----------------------------
# SELECT COOK
# -----------------------------

cook_names = []

for cook in cooks:
    cook_names.append(
        str(cook.get("name", "Unknown Cook"))
    )

selected_name = st.selectbox(
    "👨‍🍳 Select Cook",
    cook_names
)

# Find selected cook
selected_cook = None

for cook in cooks:
    if cook.get("name") == selected_name:
        selected_cook = cook
        break

if selected_cook is None:
    st.error("Cook could not be found.")
    st.stop()

cook_id = selected_cook.get("id")

# -----------------------------
# COOK INFORMATION
# -----------------------------

st.markdown("### 👤 Cook Information")

info1, info2, info3 = st.columns(3)

with info1:
    st.metric(
        "Cook",
        selected_cook.get("name", "Unknown")
    )

with info2:
    st.metric(
        "Food Type",
        selected_cook.get(
            "food_preference",
            "Not specified"
        )
    )

with info3:
    st.metric(
        "Rating",
        str(selected_cook.get("rating", "N/A"))
    )

st.divider()

# -----------------------------
# GET ORDERS
# -----------------------------

orders = get_orders_for_cook(cook_id)

# -----------------------------
# DASHBOARD STATISTICS
# -----------------------------

pending_orders = [
    order for order in orders
    if order.get("status") == "Pending"
]

confirmed_orders = [
    order for order in orders
    if order.get("status") == "Confirmed"
]

completed_orders = [
    order for order in orders
    if order.get("status") == "Completed"
]

earnings = calculate_earnings(cook_id)

st.markdown("### 📊 Dashboard Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📦 Total Orders",
        len(orders)
    )

with col2:
    st.metric(
        "⏳ Pending",
        len(pending_orders)
    )

with col3:
    st.metric(
        "✅ Completed",
        len(completed_orders)
    )

with col4:
    st.metric(
        "💰 Earnings",
        "₹" + str(earnings)
    )

st.divider()

# -----------------------------
# ORDERS
# -----------------------------

st.markdown("### 📋 Orders")

if not orders:

    st.info(
        "No orders have been placed for this cook yet."
    )

else:

    for order in orders:

        with st.container():

            st.markdown(
                "#### 🍱 Order " +
                str(order.get("order_id", "Unknown"))
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.write(
                    "**Student:**",
                    order.get(
                        "student_name",
                        "Unknown"
                    )
                )

                st.write(
                    "**Meal:**",
                    order.get(
                        "meal_type",
                        "Not specified"
                    )
                )

            with col2:
                st.write(
                    "**Plan:**",
                    order.get(
                        "plan",
                        "Not specified"
                    )
                )

                st.write(
                    "**Total:** ₹",
                    order.get("total", 0)
                )

            with col3:

                current_status = order.get(
                    "status",
                    "Pending"
                )

                st.write(
                    "**Status:**",
                    current_status
                )

                # Status buttons

                if current_status == "Pending":

                    if st.button(
                        "✅ Confirm Order",
                        key="confirm_" +
                        str(order.get("order_id"))
                    ):

                        update_order_status(
                            order.get("order_id"),
                            "Confirmed"
                        )

                        st.success(
                            "Order confirmed!"
                        )

                        st.rerun()

                elif current_status == "Confirmed":

                    if st.button(
                        "🍱 Mark Completed",
                        key="complete_" +
                        str(order.get("order_id"))
                    ):

                        update_order_status(
                            order.get("order_id"),
                            "Completed"
                        )

                        st.success(
                            "Order marked as completed!"
                        )

                        st.rerun()

                elif current_status == "Completed":

                    st.success(
                        "Order completed ✓"
                    )

            st.divider()

# -----------------------------
# EARNINGS
# -----------------------------

st.markdown("### 💰 Earnings")

st.write(
    "Your current earnings from confirmed and "
    "completed orders:"
)

st.success(
    "₹" + str(earnings)
)

# -----------------------------
# COOK DETAILS
# -----------------------------

st.divider()

st.markdown("### 🏠 Kitchen Details")

st.write(
    "**Kitchen:**",
    selected_cook.get("name", "Not available")
)

st.write(
    "**Food Preference:**",
    selected_cook.get(
        "food_preference",
        "Not specified"
    )
)

st.write(
    "**Meals:**",
    ", ".join(
        selected_cook.get("meals", [])
    )
)

st.write(
    "**Spice Level:**",
    selected_cook.get(
        "spice_level",
        "Not specified"
    )
)

st.write(
    "**Distance:**",
    str(
        selected_cook.get(
            "distance_km",
            "N/A"
        )
    ) + " km"
)

st.write(
    selected_cook.get(
        "description",
        ""
    )
)

# -----------------------------
# FOOTER
# -----------------------------

st.divider()

st.caption(
    "HomeMeal • Connecting students with "
    "affordable home-cooked meals 🏠🍱"
)
