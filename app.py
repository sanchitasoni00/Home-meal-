import json
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="HomeMeal", page_icon="🍱", layout="wide")
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "cooks.json"

@st.cache_data
def load_cooks():
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []

def filter_cooks(cooks, location, vegetarian, max_price):
    out = []
    for c in cooks:
        loc = str(c.get("location", "")).lower()
        food = str(c.get("food", "")).lower()
        if location and location.lower() not in loc:
            continue
        if vegetarian and "vegetarian" not in food:
            continue
        if float(c.get("price", 0)) > max_price:
            continue
        out.append(c)
    return sorted(out, key=lambda x: (float(x.get("distance", 999)), -float(x.get("rating", 0))))

def menu_items(cook):
    m = cook.get("menu", [])
    return [x.get("name", "Meal") if isinstance(x, dict) else str(x) for x in m] or ["Home-style Thali"]

if "page" not in st.session_state: st.session_state.page = "home"
if "location" not in st.session_state: st.session_state.location = ""
if "max_price" not in st.session_state: st.session_state.max_price = 100
if "vegetarian" not in st.session_state: st.session_state.vegetarian = False
if "selected_cook" not in st.session_state: st.session_state.selected_cook = None
if "selected_meal" not in st.session_state: st.session_state.selected_meal = None
if "plan" not in st.session_state: st.session_state.plan = None
if "confirmed" not in st.session_state: st.session_state.confirmed = False

cooks = load_cooks()

with st.sidebar:
    st.title("🍱 HomeMeal")
    st.caption("Fresh food. Local cooks. Smarter choices.")
    if st.button("🏠 Home", use_container_width=True): st.session_state.page = "home"; st.rerun()
    if st.button("🍛 Browse Cooks", use_container_width=True): st.session_state.page = "cooks"; st.rerun()
    if st.button("🧾 My Order", use_container_width=True): st.session_state.page = "order"; st.rerun()
    if st.button("👩‍🍳 Cook Dashboard", use_container_width=True): st.session_state.page = "dashboard"; st.rerun()

if st.session_state.page == "home":
    st.title("🍱 HomeMeal")
    st.subheader("Find affordable, reliable home-cooked meals near you.")
    st.divider()
    st.header("🏠 Find a meal that feels like home")
    a, b = st.columns(2)
    with a:
        location = st.text_input("📍 College / Area", st.session_state.location, placeholder="Example: Panchkula")
        max_price = st.number_input("💰 Maximum price per meal", 20, 1000, st.session_state.max_price, 10)
    with b:
        vegetarian = st.checkbox("🥗 Vegetarian only", st.session_state.vegetarian)
        meal_type = st.selectbox("🍽️ Meal", ["Lunch", "Dinner"])
    if st.button("🔍 Find Nearby Home Cooks", type="primary", use_container_width=True):
        st.session_state.location, st.session_state.max_price = location, max_price
        st.session_state.vegetarian = vegetarian
        st.session_state.meal_type = meal_type
        st.session_state.page = "cooks"
        st.rerun()
    st.divider()
    x = st.columns(4)
    for col, text in zip(x, ["1️⃣ Enter area", "2️⃣ Find cooks", "3️⃣ Choose meal", "4️⃣ Confirm order"]):
        col.info(text)

elif st.session_state.page == "cooks":
    st.title("🍛 Nearby Home Cooks")
    results = filter_cooks(cooks, st.session_state.location, st.session_state.vegetarian, st.session_state.max_price)
    st.caption(f"Area: {st.session_state.location or 'Any'} • Budget: ₹{st.session_state.max_price}")
    if not results:
        st.warning("No exact matches. Try increasing your budget or changing the area.")
        results = cooks
    for i, c in enumerate(results):
        with st.container(border=True):
            left, mid, right = st.columns([2.5, 2, 1])
            with left:
                st.subheader("👩‍🍳 " + c.get("name", "Home Cook"))
                st.write(f"📍 {c.get('location','Local')} • {float(c.get('distance',0)):.1f} km")
                st.write("🍛 " + c.get("food", "Home Food"))
                if c.get("verified", True): st.success("✓ Verified home cook")
            with mid:
                st.metric("⭐ Rating", f"{float(c.get('rating',0)):.1f}/5")
                st.metric("💰 Price", f"₹{c.get('price',0)}")
            with right:
                if st.button("View Menu", key=f"view_{i}"):
                    st.session_state.selected_cook = c
                    st.session_state.page = "menu"
                    st.rerun()

elif st.session_state.page == "menu":
    c = st.session_state.selected_cook
    if not c: st.session_state.page = "cooks"; st.rerun()
    st.title("👩‍🍳 " + c.get("name", "Home Cook"))
    st.write(f"⭐ {float(c.get('rating',0)):.1f} • 📍 {c.get('location','Local')} • ₹{c.get('price',0)} per meal")
    st.header("🍽️ Today's Menu")
    st.session_state.selected_meal = st.radio("Choose a meal", menu_items(c))
    if st.button("Continue to Meal Plan →", type="primary"):
        st.session_state.page = "subscription"; st.rerun()
    if st.button("← Back"): st.session_state.page = "cooks"; st.rerun()

elif st.session_state.page == "subscription":
    c = st.session_state.selected_cook
    st.title("🧾 Choose Your Meal Plan")
    price = float(c.get("price", 50))
    plan_name = st.radio("Plan", ["1 Meal", "3 Meals"], horizontal=True)
    count = 1 if plan_name == "1 Meal" else 3
    meal_time = st.selectbox("Meal time", ["Lunch", "Dinner"])
    st.write(f"**Cook:** {c.get('name')}")
    st.write(f"**Meal:** {st.session_state.selected_meal}")
    st.write(f"**Amount:** ₹{price*count:.0f}")
    if st.button("✅ Confirm Subscription", type="primary", use_container_width=True):
        st.session_state.plan = {"name": plan_name, "time": meal_time, "amount": price*count}
        st.session_state.confirmed = True
        st.session_state.page = "order"
        st.rerun()

elif st.session_state.page == "order":
    st.title("📦 Order Status")
    if not st.session_state.confirmed:
        st.info("No active order.")
    else:
        c = st.session_state.selected_cook
        p = st.session_state.plan
        st.success("🎉 Your HomeMeal order is confirmed!")
        st.write(f"**Cook:** {c.get('name')}")
        st.write(f"**Meal:** {st.session_state.selected_meal}")
        st.write(f"**Plan:** {p['name']} • {p['time']}")
        st.metric("Amount", f"₹{p['amount']:.0f}")
        st.write("✅ Subscription confirmed")
        st.write("🟡 Cook notified")
        st.write("⚪ Meal preparation")
        st.caption("Prototype: payment and delivery are simulated.")

elif st.session_state.page == "dashboard":
    st.title("👩‍🍳 Home Cook Dashboard")
    c = cooks[0] if cooks else {}
    a,b,d,e = st.columns(4)
    a.metric("⭐ Rating", c.get("rating", 4.7))
    b.metric("🍱 Today's Orders", 8 if st.session_state.confirmed else 7)
    d.metric("👥 Capacity", c.get("capacity", 20))
    e.metric("💰 Earnings", f"₹{(8 if st.session_state.confirmed else 7)*float(c.get('price',50)):.0f}")
    st.divider()
    st.subheader("🍛 Today's Menu")
    for item in menu_items(c): st.write("• " + item)
    st.subheader("📦 Recent Orders")
    st.success("New order received!" if st.session_state.confirmed else "No new orders in this demo session.")

st.divider()
st.caption("🍱 HomeMeal • SIH Internal Hackathon Prototype • Member 1")
