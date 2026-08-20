import streamlit as st

st.set_page_config(
    page_title="HomeMeal",
    page_icon="🍱",
    layout="wide"
)

# -----------------------------
# HOME PAGE
# -----------------------------

st.title("🍱 Ghar Ka Khana , Ghar Se Khamai")

st.subheader(
    "Fresh, Affordable & Home-Cooked Meals for Students"
)

st.write(
    "HomeMeal connects students with trusted local home cooks "
    "and helps students discover meals based on their preferences."
)

st.divider()

# -----------------------------
# INTRODUCTION
# -----------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 💰 Affordable")
    st.write(
        "Find meals that fit your budget."
    )

with col2:
    st.markdown("### 🏠 Home-Cooked")
    st.write(
        "Discover fresh meals prepared by local home cooks."
    )

with col3:
    st.markdown("### ⭐ Smart Matching")
    st.write(
        "Get recommendations based on your preferences."
    )

st.divider()

# -----------------------------
# CHOOSE USER TYPE
# -----------------------------

st.markdown("## 🚀 Get Started")

user_type = st.radio(
    "I am a:",
    [
        "Student",
        "Home Cook"
    ],
    horizontal=True
)

st.write("")

if user_type == "Student":

    st.info(
        "Students can search for meals, compare cooks "
        "and place orders."
    )

    if st.button(
        "🍱 Open Student App",
        use_container_width=True
    ):
        st.session_state["page"] = "student"

elif user_type == "Home Cook":

    st.info(
        "Home cooks can view orders, manage orders "
        "and track earnings."
    )

    if st.button(
        "👨‍🍳 Open Cook Dashboard",
        use_container_width=True
    ):
        st.session_state["page"] = "cook"


# -----------------------------
# NAVIGATION
# -----------------------------

page = st.session_state.get(
    "page",
    "home"
)

if page == "student":

    st.divider()

    import student_app

elif page == "cook":

    st.divider()

    import cook_dashboard
