import streamlit as st
from recommendation import get_recommendation_inputs, get_top_cooks
from logic.order_logic import create_order, confirm_subscription


st.title("🍱 HomeMeal")
st.subheader("Find Your Perfect Home-Cooked Meal")

st.write(
    "Tell us your preferences and HomeMeal will find "
    "the best matching home cooks for you."
)

st.divider()

# -----------------------------
# STUDENT DETAILS
# -----------------------------

st.markdown("### 👨‍🎓 Student Details")

student_name = st.text_input(
    "Your name",
    placeholder="Enter your name"
)

# -----------------------------
# PREFERENCES
# -----------------------------

st.markdown("### 🍽️ Your Preferences")

col1, col2 = st.columns(2)

with col1:

    budget = st.number_input(
        "Budget (₹)",
        min_value=20,
        max_value=1000,
        value=100,
        step=10
    )

    food_preference = st.selectbox(
        "Food preference",
        [
            "North Indian",
            "South Indian",
            "Punjabi",
            "Chinese",
            "Vegetarian",
            "Any"
        ]
    )

    meal_type = st.selectbox(
        "Meal type",
        [
            "Lunch",
            "Dinner"
        ]
    )

with col2:

    spice_level = st.selectbox(
        "Spice level",
        [
            "Mild",
            "Medium",
            "Spicy"
        ]
    )

    min_rating = st.slider(
        "Minimum cook rating",
        1.0,
        5.0,
        3.0,
        0.1
    )

    max_distance = st.slider(
        "Maximum distance (km)",
        1.0,
        10.0,
        5.0,
        0.5
    )

st.divider()

# -----------------------------
# FIND MEALS
# -----------------------------

if st.button(
    "🔎 Find Best Meals",
    use_container_width=True
):

    if not student_name.strip():
        st.warning("Please enter your name first.")

    else:

        preferences = {
            "budget": budget,
            "food_preference": food_preference,
            "meal_type": meal_type,
            "spice_level": spice_level,
            "min_rating": min_rating,
            "max_distance": max_distance
        }

        try:

            inputs = get_recommendation_inputs(
                budget,
                meal_type,
                food_preference,
                spice_level,
                min_rating,
                max_distance
            )

            recommendations = get_top_cooks(
                inputs,
                limit=5
            )

            st.session_state["recommendations"] = recommendations
            st.session_state["student_name"] = student_name

        except Exception as e:

            st.error(
                "Could not generate recommendations."
            )

            st.write(
                "Please check that recommendation.py "
                "is correctly uploaded."
            )

# -----------------------------
# SHOW RECOMMENDATIONS
# -----------------------------

recommendations = st.session_state.get(
    "recommendations",
    []
)

if recommendations:

    st.markdown("## ⭐ Recommended Home Cooks")

    for index, result in enumerate(recommendations):

        cook = result.get("cook", result)

        score = result.get(
            "score",
            result.get("total_score", 0)
        )

        cook_name = cook.get(
            "name",
            "Home Cook"
        )

        price = cook.get(
            "price",
            0
        )

        rating = cook.get(
            "rating",
            "N/A"
        )

        food = cook.get(
            "food_preference",
            "Not specified"
        )

        distance = cook.get(
            "distance_km",
            "N/A"
        )

        description = cook.get(
            "description",
            ""
        )

        with st.container():

            st.markdown(
                "### 🍳 " + str(cook_name)
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Price",
                    "₹" + str(price)
                )

            with col2:
                st.metric(
                    "Rating",
                    str(rating) + " ⭐"
                )

            with col3:
                st.metric(
                    "Match Score",
                    str(score) + "/100"
                )

            st.write(
                "**Food:** " + str(food)
            )

            st.write(
                "**Distance:** " +
                str(distance) +
                " km"
            )

            if description:
                st.write(description)

            if st.button(
                "🍱 Select This Cook",
                key="select_" + str(index)
            ):

                st.session_state[
                    "selected_cook"
                ] = cook

            st.divider()

# -----------------------------
# ORDER SECTION
# -----------------------------

selected_cook = st.session_state.get(
    "selected_cook"
)

if selected_cook:

    st.markdown("## 🛒 Place Your Order")

    st.success(
        "Selected Cook: " +
        str(
            selected_cook.get(
                "name",
                "Home Cook"
            )
        )
    )

    plan = st.selectbox(
        "Choose your plan",
        [
            "Single Meal",
            "Weekly Plan",
            "Monthly Plan"
        ]
    )

    total = selected_cook.get(
        "price",
        0
    )

    if plan == "Weekly Plan":
        total = total * 7

    elif plan == "Monthly Plan":
        total = total * 30

    st.write(
        "### Total: ₹" + str(total)
    )

    if st.button(
        "🛍️ Place Order",
        use_container_width=True
    ):

        try:

            order = create_order(
                student_name=st.session_state.get(
                    "student_name",
                    student_name
                ),
                cook_id=selected_cook.get("id"),
                cook_name=selected_cook.get("name"),
                plan=plan,
                meal_type=meal_type,
                total=total
            )

            st.session_state[
                "last_order"
            ] = order

            st.success(
                "Order created successfully! 🎉"
            )

        except Exception as e:

            st.error(
                "Unable to create order."
            )

# -----------------------------
# CONFIRM ORDER
# -----------------------------

last_order = st.session_state.get(
    "last_order"
)

if last_order:

    st.markdown("## ✅ Confirm Subscription")

    st.write(
        "**Order ID:** " +
        str(last_order.get("order_id"))
    )

    st.write(
        "**Status:** " +
        str(last_order.get("status"))
    )

    if st.button(
        "✅ Confirm Subscription",
        use_container_width=True
    ):

        result = confirm_subscription(
            last_order.get("order_id")
        )

        if result:

            st.success(
                "Subscription confirmed successfully! 🎉"
            )

            st.balloons()

        else:

            st.error(
                "Could not confirm subscription."
            )

# -----------------------------
# FOOTER
# -----------------------------

st.divider()

st.caption(
    "HomeMeal • Affordable home-cooked meals "
    "for students 🏠🍱"
)
