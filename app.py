import streamlit as st

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


def go_to(page):
    st.session_state.page = page


# =========================================================
# HOME PAGE
# =========================================================

def home_page():

    # =====================================================
    # CUSTOM CSS + ANIMATIONS
    # =====================================================

    st.markdown("""
    <style>

    /* =====================================================
       HERO SECTION
       ===================================================== */

    .hero {
        text-align: center;
        padding: 35px 20px 30px 20px;
        animation: heroFade 1.2s ease-out;
    }


    /* Floating food icon */

    .hero-icon {
        font-size: 70px;
        display: inline-block;
        animation: floatLogo 3s ease-in-out infinite;
    }


    /* Main heading */

    .hero-title {
        font-size: 52px;
        font-weight: 800;
        margin: 5px 0 10px 0;

        background: linear-gradient(
            90deg,
            #166534,
            #22c55e,
            #15803d
        );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }


    /* Tagline */

    .hero-tagline {
        font-size: 22px;
        font-weight: 600;
        color: #374151;
        margin-bottom: 12px;
    }


    /* Description */

    .hero-description {
        font-size: 17px;
        color: #6b7280;
        max-width: 750px;
        margin: auto;
        line-height: 1.6;
    }


    /* Small badge */

    .hero-badge {
        display: inline-block;
        margin-top: 18px;
        padding: 8px 18px;
        border-radius: 30px;

        background: #dcfce7;
        color: #166534;

        font-size: 14px;
        font-weight: 600;
    }


    /* Hero entrance animation */

    @keyframes heroFade {

        from {
            opacity: 0;
            transform: translateY(-30px);
        }

        to {
            opacity: 1;
            transform: translateY(0);
        }

    }


    /* Food icon animation */

    @keyframes floatLogo {

        0% {
            transform: translateY(0px);
        }

        50% {
            transform: translateY(-10px);
        }

        100% {
            transform: translateY(0px);
        }

    }


    /* =====================================================
       FEATURE CARDS
       ===================================================== */

    .feature-card {

        background: linear-gradient(
            135deg,
            #f0fff4,
            #ffffff
        );

        padding: 25px;

        border-radius: 20px;

        text-align: center;

        border: 2px solid #d8f3dc;

        box-shadow:
            0 5px 15px rgba(0, 0, 0, 0.08);

        transition: all 0.3s ease;

        min-height: 180px;
    }


    /* Card hover animation */

    .feature-card:hover {

        transform:
            translateY(-10px)
            scale(1.03);

        box-shadow:
            0 15px 30px rgba(0, 0, 0, 0.15);
    }


    /* Card icons */

    .icon {

        font-size: 45px;

        display: inline-block;

        animation:
            floatCardIcon 2s ease-in-out infinite;
    }


    @keyframes floatCardIcon {

        0% {
            transform: translateY(0px);
        }

        50% {
            transform: translateY(-8px);
        }

        100% {
            transform: translateY(0px);
        }

    }


    .feature-card h3 {

        color: #166534;

        margin-bottom: 8px;
    }


    .feature-card p {

        color: #555;

        font-size: 15px;
    }


    /* =====================================================
       GET STARTED
       ===================================================== */

    .get-started {

        text-align: center;

        padding: 15px;
    }


    </style>
    """, unsafe_allow_html=True)


    # =====================================================
    # HERO SECTION
    # =====================================================

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

        <div class="hero-badge">
            🏠 Made with care by local home cooks
        </div>

    </div>
    """)


    st.divider()


    # =====================================================
    # FEATURE CARDS
    # =====================================================

    col1, col2, col3 = st.columns(3)


    # -----------------------------
    # AFFORDABLE
    # -----------------------------

    with col1:

        st.html("""
        <div class="feature-card">

            <div class="icon">
                💰
            </div>

            <h3>
                Affordable
            </h3>

            <p>
                Find meals that fit your budget.
            </p>

        </div>
        """)


    # -----------------------------
    # HOME COOKED
    # -----------------------------

    with col2:

        st.html("""
        <div class="feature-card">

            <div class="icon">
                🏠
            </div>

            <h3>
                Home-Cooked
            </h3>

            <p>
                Fresh meals prepared by local home cooks.
            </p>

        </div>
        """)


    # -----------------------------
    # TRUSTED
    # -----------------------------

    with col3:

        st.html("""
        <div class="feature-card">

            <div class="icon">
                ❤️
            </div>

            <h3>
                Trusted
            </h3>

            <p>
                Connect with reliable local cooks.
            </p>

        </div>
        """)


    # =====================================================
    # GET STARTED
    # =====================================================

    st.divider()

    st.markdown("""
    <div class="get-started">
        <h1>🚀 Get Started</h1>
    </div>
    """, unsafe_allow_html=True)


    user_type = st.radio(
        "I am a:",
        ["User", "Home Cook"],
        horizontal=True
    )


    st.write("")


    # =====================================================
    # USER OPTION
    # =====================================================

    if user_type == "User":

        st.info(
            "🎓 User can search for meals, compare "
            "cooks and place orders."
        )


        if st.button(
            "🍱 Open User Dashboard",
            use_container_width=True
        ):

            go_to("User")

            st.rerun()


    # =====================================================
    # HOME COOK OPTION
    # =====================================================

    else:

        st.info(
            "👨‍🍳 Home cooks can view orders, manage meals "
            "and track earnings."
        )


        if st.button(
            "👨‍🍳 Open Cook Dashboard",
            use_container_width=True
        ):

            go_to("cook")

            st.rerun()


# =========================================================
# STUDENT DASHBOARD
# =========================================================

def User_dashboard():

    st.title("👨‍🎓 User Dashboard")


    st.write(
        "Welcome to HomeMeal! Find fresh and affordable "
        "home-cooked meals near you."
    )


    if st.button("⬅️ Back to Home"):

        go_to("home")

        st.rerun()


    st.divider()


    # =====================================================
    # STUDENT PROFILE
    # =====================================================

    st.subheader("👤 User Profile")


    col1, col2 = st.columns(2)


    with col1:

        name = st.text_input(
            "Your Name",
            placeholder="Enter your name"
        )


    with col2:

        budget = st.selectbox(
            "Meal Budget",
            [
                "Under ₹50",
                "₹50 - ₹100",
                "₹100 - ₹150",
                "Above ₹150"
            ]
        )


    st.divider()


    # =====================================================
    # AVAILABLE MEALS
    # =====================================================

    st.subheader("🍱 Available Home Meals")


    meal1, meal2, meal3 = st.columns(3)


    # -----------------------------
    # RAJMA
    # -----------------------------

    with meal1:

        st.markdown("### 🍛 Rajma Chawal")

        st.write("👨‍🍳 Home Cook: Priya")

        st.write("⭐ 4.8/5")

        st.write("💰 ₹70")


        if st.button(
            "🛒 Order Rajma Chawal",
            key="rajma"
        ):

            st.success(
                "Rajma Chawal added to your order!"
            )


    # -----------------------------
    # THALI
    # -----------------------------

    with meal2:

        st.markdown("### 🥗 Veg Thali")

        st.write("👨‍🍳 Home Cook: Neha")

        st.write("⭐ 4.7/5")

        st.write("💰 ₹90")


        if st.button(
            "🛒 Order Veg Thali",
            key="thali"
        ):

            st.success(
                "Veg Thali added to your order!"
            )


    # -----------------------------
    # PASTA
    # -----------------------------

    with meal3:

        st.markdown("### 🍝 Pasta")

        st.write("👨‍🍳 Home Cook: Anjali")

        st.write("⭐ 4.6/5")

        st.write("💰 ₹100")


        if st.button(
            "🛒 Order Pasta",
            key="pasta"
        ):

            st.success(
                "Pasta added to your order!"
            )


    st.divider()


    # =====================================================
    # SEARCH
    # =====================================================

    st.subheader("🔎 Find Your Meal")


    search = st.text_input(
        "Search meals",
        placeholder="Example: Rajma, Thali, Pasta..."
    )


    if search:

        st.info(
            f"Searching HomeMeal for: **{search}**"
        )


    st.divider()


    # =====================================================
    # STUDENT ORDERS
    # =====================================================

    st.subheader("📦 My Orders")


    st.success(
        "No active orders right now. Start exploring meals!"
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


    col1, col2 = st.columns(2)


    with col1:

        cook_name = st.text_input(
            "Cook Name",
            placeholder="Enter your name"
        )


    with col2:

        location = st.text_input(
            "Location",
            placeholder="Enter your area"
        )


    st.divider()


    # =====================================================
    # DASHBOARD STATS
    # =====================================================

    st.subheader("📊 Today's Overview")


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "🍱 Orders",
            "8"
        )


    with col2:

        st.metric(
            "💰 Earnings",
            "₹640"
        )


    with col3:

        st.metric(
            "⭐ Rating",
            "4.8"
        )


    with col4:

        st.metric(
            "👥 Customers",
            "12"
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

        if meal_name.strip():

            st.success(
                f"{meal_name} has been added successfully!"
            )

        else:

            st.warning(
                "Please enter a meal name."
            )


    st.divider()


    # =====================================================
    # RECENT ORDERS
    # =====================================================

    st.subheader("📦 Recent Orders")


    order1, order2, order3 = st.columns(3)


    # -----------------------------
    # ORDER 1
    # -----------------------------

    with order1:

        st.markdown("### Order #001")

        st.write("🍛 Rajma Chawal")

        st.write("👤 Student")

        st.write("💰 ₹70")


        if st.button(
            "✅ Accept",
            key="accept1"
        ):

            st.success(
                "Order accepted!"
            )


    # -----------------------------
    # ORDER 2
    # -----------------------------

    with order2:

        st.markdown("### Order #002")

        st.write("🥗 Veg Thali")

        st.write("👤 Student")

        st.write("💰 ₹90")


        if st.button(
            "✅ Accept",
            key="accept2"
        ):

            st.success(
                "Order accepted!"
            )


    # -----------------------------
    # ORDER 3
    # -----------------------------

    with order3:

        st.markdown("### Order #003")

        st.write("🍝 Pasta")

        st.write("👤 Student")

        st.write("💰 ₹100")


        if st.button(
            "✅ Accept",
            key="accept3"
        ):

            st.success(
                "Order accepted!"
            )


# =========================================================
# PAGE ROUTER
# =========================================================

if st.session_state.page == "home":

    home_page()


elif st.session_state.page == "student":

    student_dashboard()


elif st.session_state.page == "cook":

    cook_dashboard()
