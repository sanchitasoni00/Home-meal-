import streamlit as st
from logic.order_logic import create_order, confirm_subscription, get_orders_for_student

def render_student_app(cooks):
    st.header("🍱 Find Your Home-Cooked Meal")

    location = st.text_input("📍 College / Area", value="Panchkula")
    max_price = st.number_input("💰 Maximum price per meal (₹)", min_value=1, value=100, step=10)
    food = st.selectbox(
        "🥗 Food preference",
        ["Any", "North Indian", "South Indian", "Punjabi", "Vegetarian"]
    )
    meal = st.selectbox("🍽️ Meal", ["Any", "Lunch", "Dinner"])
    spice = st.selectbox("🌶️ Spice level", ["Any", "Mild", "Medium", "Spicy"])

    filtered = []
    for cook in cooks:
        if cook.get("price", 0) > max_price:
            continue
        if food != "Any" and cook.get("food_preference") != food:
            continue
        if meal != "Any" and meal not in cook.get("meals", []):
            continue
        if spice != "Any" and cook.get("spice_level") != spice:
            continue
        filtered.append(cook)

    st.subheader("👩‍🍳 Available Home Cooks")

    if not filtered:
        st.warning("No cooks match these filters. Try increasing your budget or changing a filter.")
        return

    for cook in filtered:
        with st.container():
            c1, c2, c3 = st.columns([3, 2, 1])
            with c1:
                st.subheader(cook.get("name", "Home Cook"))
                st.write(cook.get("description", "Fresh home-cooked meals."))
                st.write("🍛 " + cook.get("food_preference", "Home food"))
            with c2:
                st.write("⭐ Rating:", cook.get("rating", 0))
                st.write("📍 Distance:", cook.get("distance_km", 0), "km")
                st.write("💰 Price:", "₹" + str(cook.get("price", 0)))
            with c3:
                if st.button("View", key="view_" + str(cook["id"])):
                    st.session_state["selected_cook"] = cook

    selected = st.session_state.get("selected_cook")
    if selected:
        st.divider()
        st.header("🍽️ " + selected["name"] + " — Menu")

        st.write("**Food:**", selected.get("food_preference"))
        st.write("**Available meals:**", ", ".join(selected.get("meals", [])))
        st.write("**Spice level:**", selected.get("spice_level"))
        st.write("**Price:** ₹" + str(selected.get("price", 0)) + " / meal")

        student_name = st.text_input("Your name", key="student_name")
        plan = st.selectbox("Choose a meal plan", ["1 Meal", "3 Meals", "7 Meals"])
        meal_choice = st.selectbox(
            "Choose meal",
            selected.get("meals", ["Lunch", "Dinner"])
        )

        count = {"1 Meal": 1, "3 Meals": 3, "7 Meals": 7}[plan]
        total = selected.get("price", 0) * count

        st.info("Total: ₹" + str(total))

        if st.button("✅ Confirm Subscription", type="primary"):
            if not student_name.strip():
                st.error("Please enter your name first.")
            else:
                order = create_order(
                    student_name=student_name.strip(),
                    cook_id=selected["id"],
                    cook_name=selected["name"],
                    plan=plan,
                    meal_type=meal_choice,
                    total=total,
                )
                confirm_subscription(order["order_id"])
                st.session_state["last_order_id"] = order["order_id"]
                st.success("Subscription confirmed!")
                st.write("Order ID:", order["order_id"])
                st.write("Status: Confirmed")

    student = st.session_state.get("student_name", "")
    if student:
        orders = get_orders_for_student(student)
        if orders:
            st.divider()
            st.subheader("📦 Your Orders")
            for order in orders:
                st.write(
                    "**{}** — {} — {} — ₹{}"
                    .format(
                        order["order_id"],
                        order["cook_name"],
                        order["status"],
                        order["total"],
                    )
                )
