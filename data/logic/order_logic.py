import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
ORDERS_FILE = DATA_DIR / "orders.json"
SUBSCRIPTIONS_FILE = DATA_DIR / "subscriptions.json"

def _load(path, default):
    if not path.exists():
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default

def _save(path, data):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def get_cooks():
    path = DATA_DIR / "cooks.json"
    return _load(path, [])

def create_order(student_name, cook_id, cook_name, plan, meal_type, total):
    orders = _load(ORDERS_FILE, [])
    order_id = "HM-" + datetime.now().strftime("%Y%m%d%H%M%S%f")[-10:]

    order = {
        "order_id": order_id,
        "student_name": student_name,
        "cook_id": cook_id,
        "cook_name": cook_name,
        "plan": plan,
        "meal_type": meal_type,
        "total": total,
        "status": "Pending",
        "created_at": datetime.now().isoformat(),
    }

    orders.append(order)
    _save(ORDERS_FILE, orders)
    return order

def confirm_subscription(order_id):
    orders = _load(ORDERS_FILE, [])
    subscriptions = _load(SUBSCRIPTIONS_FILE, [])

    for order in orders:
        if order["order_id"] == order_id:
            order["status"] = "Confirmed"

            subscription = {
                "subscription_id": "SUB-" + order_id.replace("HM-", ""),
                "order_id": order["order_id"],
                "student_name": order["student_name"],
                "cook_id": order["cook_id"],
                "plan": order["plan"],
                "meal_type": order["meal_type"],
                "status": "Active",
                "created_at": datetime.now().isoformat(),
            }
            subscriptions.append(subscription)
            _save(ORDERS_FILE, orders)
            _save(SUBSCRIPTIONS_FILE, subscriptions)
            return order

    return None

def update_order_status(order_id, new_status):
    orders = _load(ORDERS_FILE, [])

    for order in orders:
        if order["order_id"] == order_id:
            order["status"] = new_status
            _save(ORDERS_FILE, orders)
            return order

    return None

def get_orders_for_student(student_name):
    orders = _load(ORDERS_FILE, [])
    return [
        o for o in orders
        if o.get("student_name", "").lower() == student_name.lower()
    ]

def get_orders_for_cook(cook_id):
    orders = _load(ORDERS_FILE, [])
    return [o for o in orders if o.get("cook_id") == cook_id]

def calculate_earnings(cook_id):
    orders = get_orders_for_cook(cook_id)
    return sum(
        o.get("total", 0)
        for o in orders
        if o.get("status") in ("Confirmed", "Completed")
    )

