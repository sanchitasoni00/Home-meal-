import json
from pathlib import Path

import streamlit as st

from recommendation import (
    get_recommendation_inputs,
    get_top_cooks,
)

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "cooks.json"


@st.cache_data
def load_cooks():
    """Load cook information from the shared JSON file."""
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    st.set_page_config(
        page_title="HomeMeal - Smart Recommendations",
        page_icon="🍱",
        layout="wide",
    )

    st.title("🍱 HomeMeal")
    st.subheader("Smart Meal Recommendation")
    st.write(
        "Tell us what you want, and HomeMeal will rank the best matching "
        "home cooks using the project's 100-point recommendation model."
    )

    try:
        cooks = load_cooks()
    except FileNotFoundError:
        st.error("Cook data file was not found: data/cooks.json")
        st.stop()
    except json.JSONDecodeError:
        st.error("Cook data contains invalid JSON.")
        st.stop()

    if not cooks:
        st.warning("No cooks are currently available.")
        st.stop()

    st.divider()

    st.header("1. Your Preferences")

    prices = []
    for cook in cooks:
        try:
            prices.append(float(cook.get("price", 0)))
        except (TypeError, ValueError):
            pass

    default_budget = min(prices) if prices else 100
    max_budget = max(500, int(max(prices)) + 100) if prices else 500

    col1, col2 = st.columns(2)

    with col1:
        budget = st.number_input(
            "Budget (₹)",
            min_value=1,
            max_value=10000,
            value=int(default_budget),
            step=10,
        )

        meal_options = sorted(
            {
                meal
                for cook in cooks
                for meal in (
                    cook.get("meals", [])
                    if isinstance(cook.get("meals", []), list)
                    else [cook.get("meal_type", "")]
                )
                if meal
            }
        )
        meal_type = st.selectbox(
            "What type of meal?",
            meal_options or ["Lunch", "Dinner"],
        )

    with col2:
        food_options = sorted(
            {
                cook.get("food_preference", cook.get("food_type", ""))
                for cook in cooks
                if cook.get("food_preference", cook.get("food_type", ""))
            }
        )
        food_preference = st.selectbox(
            "Food preference",
            food_options or ["North Indian", "South Indian"],
        )

        spice_options = sorted(
            {
                cook.get("spice_level", "")
                for cook in cooks
                if cook.get("spice_level", "")
            }
        )
        spice_level = st.selectbox(
            "Spice level",
            spice_options or ["Mild", "Medium", "Spicy"],
        )

    st.caption(
        "The spice level is collected as required by the MVP. "
        "The provided scoring plan does not assign spice a separate weight, "
        "so the score remains out of 100."
    )

    recommend = st.button(
        "🔎 Find Best Cooks",
        type="primary",
        use_container_width=True,
    )

    if recommend:
        preferences = get_recommendation_inputs(
            budget=budget,
            meal_type=meal_type,
            food_preference=food_preference,
            spice_level=spice_level,
        )

        recommendations = get_top_cooks(cooks, preferences, limit=3)

        st.divider()
        st.header("2. Recommended Cooks")

        if not recommendations:
            st.warning("No recommendations are available.")
            return

        for index, cook in enumerate(recommendations, start=1):
            score = cook["score"]
            breakdown = cook["score_breakdown"]

            with st.container(border=True):
                left, right = st.columns([4, 1])

                with left:
                    st.subheader(
                        f"{index}. {cook.get('name', 'Unknown Cook')}"
                    )
                    st.write(cook.get("description", "Home-cooked meals"))
                    st.write(
                        f"**₹{cook.get('price', 'N/A')}** per meal  •  "
                        f"⭐ {cook.get('rating', 'N/A')}  •  "
                        f"📍 {cook.get('distance_km', 'N/A')} km"
                    )
                    st.write(
                        f"**Food:** {cook.get('food_preference', 'N/A')}  |  "
                        f"**Meals:** {', '.join(cook.get('meals', []))}  |  "
                        f"**Spice:** {cook.get('spice_level', 'N/A')}"
                    )

                with right:
                    st.metric("Match Score", f"{score}/100")

                with st.expander("Why this cook was recommended"):
                    st.write(
                        f"Price match: **{breakdown['price']}/25**"
                    )
                    st.write(
                        f"Food preference: **"
                        f"{breakdown['food_preference']}/25**"
                    )
                    st.write(
                        f"Meal match: **{breakdown['meal']}/20**"
                    )
                    st.write(
                        f"Rating: **{breakdown['rating']}/15**"
                    )
                    st.write(
                        f"Distance: **{breakdown['distance']}/15**"
                    )

                    if cook["spice_match"]:
                        st.success("Spice level matches your preference.")
                    else:
                        st.info(
                            "Spice level differs from your preference; "
                            "it was not added as a separate score component."
                        )

    st.divider()
    st.caption(
        "HomeMeal Member 5 • Recommendation Engine MVP • "
        "Simple scoring first, AI API later."
    )


if __name__ == "__main__":
    main()
