import random
from typing import Any, Dict, Tuple

from flask import Blueprint, Response, jsonify, render_template, url_for

# Create blueprint
main = Blueprint("main", __name__)


def get_food_data() -> Dict[str, Any]:
    """Import data loader from app context."""
    from flask import current_app

    # Use getattr to safely access the attribute and cast the result
    loader = getattr(current_app, "food_data_loader", None)
    if loader is None:
        raise RuntimeError("food_data_loader not found on app")

    result = loader()
    # Type assertion to help mypy understand the return type
    return result  # type: ignore[no-any-return]


@main.route("/")
def index() -> str:
    """Render main application page."""
    return render_template("index.html")


@main.route("/api/categories")
def get_categories() -> Response:
    """Return all available food categories."""
    data = get_food_data()
    categories = list(data.keys())
    return jsonify(
        {
            "categories": [
                {"id": cat, "display": cat.replace("_", " ").title()}
                for cat in categories
            ]
        }
    )


@main.route("/api/subcategories/<category>")
def get_subcategories(category: str) -> Tuple[Response, int]:
    """Return subcategories for a given category."""
    data = get_food_data()
    if category in data:
        subcategories = list(data[category].keys())
        return (
            jsonify(
                {
                    "subcategories": [
                        {"id": sub, "display": sub.replace("_", " ").title()}
                        for sub in subcategories
                    ]
                }
            ),
            200,
        )
    return jsonify({"error": "Category not found"}), 404


@main.route("/api/random-item/<category>/<subcategory>")
def get_random_item(category: str, subcategory: str) -> Tuple[Response, int]:
    """Return a random food item from specified category and subcategory."""
    data = get_food_data()
    try:
        items = data[category][subcategory].get("makanan", [])

        if items:
            source_item = random.choice(items)
            random_item = {
                "name": source_item["name"],
                "description": source_item.get("description", ""),
                "image": url_for("static", filename=f"images/{source_item['image']}"),
            }
            return (
                jsonify(
                    {
                        "item": random_item,
                        "category": category,
                        "subcategory": subcategory,
                    }
                ),
                200,
            )
        return jsonify({"error": "No items found"}), 404
    except KeyError:
        return jsonify({"error": "Invalid category or subcategory"}), 404
