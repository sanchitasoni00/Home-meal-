# HomeMeal — Member 5 
# 🍱 HomeMeal

### 🏠 Connecting Students with Fresh, Affordable Home-Cooked Meals

HomeMeal is a smart food discovery platform designed to help students
find affordable and reliable home-cooked meals from local home chefs.

---

## 🎯 Problem

Many students living away from home struggle to find:

- Affordable meals
- Healthy home-style food
- Food matching their preferences
- Reliable local cooks

---

## 💡 Our Solution

HomeMeal connects students with local home cooks and helps students
discover meals based on their:

- 💰 Budget
- 🍛 Food preference
- 🍽️ Meal type
- 🌶️ Spice preference
- ⭐ Cook rating
- 📍 Distance

---

## 🤖 Smart Recommendation System

Our recommendation engine ranks available cooks using a
100-point scoring model.

| Factor | Points |
|---|---:|
| 💰 Price Match | 25 |
| 🍛 Food Preference | 25 |
| 🍽️ Meal Match | 20 |
| ⭐ Rating | 15 |
| 📍 Distance | 15 |
| **Total** | **100** |

The system scores available cooks and displays the best matches first.

---

## 🏗️ Project Structure

```text
HomeMeal/
│
├── app.py
├── recommendation.py
├── requirements.txt
│
└── data/
    └── cooks.json




