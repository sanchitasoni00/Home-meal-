"""
HomeMeal - Member 5
Recommendation engine.

Scoring model from the Member 5 project guide:
    Price match      = 25 points
    Food preference = 25 points
    Meal match      = 20 points
    Rating          = 15 points
    Distance        = 15 points
    Maximum         = 100 points

Spice level is collected because it is part of the required preference form.
The project guide does not assign a score weight to spice level, so it is
reported as a compatibility field instead of changing the 100-point model.
"""

from typing import Dict, List, Any


PRICE_WEIGHT = 25
FOOD_WEIGHT = 25
MEAL_WEIGHT = 20
RATING_WEIGHT = 15
DISTANCE_WEIGHT = 15


def normalize_text(value: Any) -> str:
    """Convert a value to clean lowercase text for comparisons."""
    return str(value).strip().lower()


def price_match_score(cook: Dict[str, Any], preferences: Dict[str, Any]) -> int:
    """Give +25 when the cook's price is within the student's budget."""
    try:
        price = float(cook.get("price", 0))
        budget = float(preferences.get("budget", 0))
    except (TypeError, ValueError):
        return 0

    return PRICE_WEIGHT if price <= budget else 0


def food_preference_score(
    cook: Dict[str, Any], preferences: Dict[str, Any]
) -> int:
    """Give +25 when food preference matches."""
    wanted = normalize_text(preferences.get("food_preference", ""))
    offered = cook.get("food_preference", cook.get("food_type", ""))

    if isinstance(offered, list):
        offered_values = [normalize_text(item) for item in offered]
        return FOOD_WEIGHT if wanted in offered_values else 0

    return FOOD_WEIGHT if wanted == normalize_text(offered) else 0


def meal_match_score(cook: Dict[str, Any], preferences: Dict[str, Any]) -> int:
    """Give +20 when the requested meal is offered by the cook."""
    wanted = normalize_text(preferences.get("meal_type", ""))
    offered = cook.get("meal_type", cook.get("meals", []))

    if isinstance(offered, str):
        offered = [offered]

    offered_values = [normalize_text(item) for item in offered]
    return MEAL_WEIGHT if wanted in offered_values else 0


def rating_score(cook: Dict[str, Any]) -> int:
    """
    Convert a 0-5 cook rating into the team's 15-point rating component.
    Example: 5.0 -> 15, 4.0 -> 12.
    """
    try:
        rating = float(cook.get("rating", 0))
    except (TypeError, ValueError):
        return 0

    rating = max(0.0, min(5.0, rating))
    return round((rating / 5.0) * RATING_WEIGHT)


def distance_score(
    cook: Dict[str, Any], cooks: List[Dict[str, Any]]
) -> int:
    """
    Give the closest cook the full 15 distance points and scale other cooks
    between 0 and 15 using the distances in the current cook dataset.

    This keeps the distance component inside the 100-point model without
    requiring live GPS.
    """
    try:
        distance = float(cook.get("distance_km", 0))
    except (TypeError, ValueError):
        return 0

    distances = []
    for item in cooks:
        try:
            distances.append(float(item.get("distance_km", 0)))
        except (TypeError, ValueError):
            pass

    if not distances:
        return 0

    max_distance = max(distances)

    if max_distance <= 0:
        return DISTANCE_WEIGHT

    score = DISTANCE_WEIGHT * (1 - (max(distance, 0) / max_distance))
    return round(max(0, min(DISTANCE_WEIGHT, score)))


def spice_compatible(
    cook: Dict[str, Any], preferences: Dict[str, Any]
) -> bool:
    """Return whether the cook's spice level matches the preference."""
    wanted = normalize_text(preferences.get("spice_level", ""))
    offered = normalize_text(cook.get("spice_level", ""))

    if not wanted or not offered:
        return True

    return wanted == offered


def calculate_score(
    cook: Dict[str, Any],
    preferences: Dict[str, Any],
    cooks: List[Dict[str, Any]] | None = None,
) -> Dict[str, Any]:
    """Calculate one cook's score and return a detailed score breakdown."""
    if cooks is None:
        cooks = [cook]

    price = price_match_score(cook, preferences)
    food = food_preference_score(cook, preferences)
    meal = meal_match_score(cook, preferences)
    rating = rating_score(cook)
    distance = distance_score(cook, cooks)

    total = price + food + meal + rating + distance

    result = dict(cook)
    result["score_breakdown"] = {
        "price": price,
        "food_preference": food,
        "meal": meal,
        "rating": rating,
        "distance": distance,
    }
    result["score"] = max(0, min(100, total))
    result["spice_match"] = spice_compatible(cook, preferences)

    return result


def rank_cooks(
    cooks: List[Dict[str, Any]], preferences: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """Score every cook and return them from highest to lowest score."""
    scored = [
        calculate_score(cook, preferences, cooks)
        for cook in cooks
    ]

    # Highest score first. Rating is used as a secondary tie-breaker.
    scored.sort(
        key=lambda item: (
            item.get("score", 0),
            float(item.get("rating", 0) or 0),
            -float(item.get("distance_km", 0) or 0),
        ),
        reverse=True,
    )
    return scored


def get_top_cooks(
    cooks: List[Dict[str, Any]],
    preferences: Dict[str, Any],
    limit: int = 3,
) -> List[Dict[str, Any]]:
    """Return the best matching cooks."""
    if limit < 1:
        return []

    return rank_cooks(cooks, preferences)[:limit]


def get_recommendation_inputs(
    budget: float,
    meal_type: str,
    food_preference: str,
    spice_level: str,
) -> Dict[str, Any]:
    """Prepare the four student preference inputs required by the MVP."""
    return {
        "budget": float(budget),
        "meal_type": meal_type,
        "food_preference": food_preference,
        "spice_level": spice_level,
    }
