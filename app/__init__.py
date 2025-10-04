import json
import os
import random
import time

from flask import Flask, jsonify, render_template, url_for

from .config import config

_FOOD_DATA_CACHE = None
_CACHE_TIMESTAMP = 0.0
CACHE_TTL = 300  # 5 minutes


def create_app(config_name=None):
    app = Flask(__name__)

    if config_name is None:
        config_name = os.environ.get("CONFIG_ENV", "default")

    # prevent key error
    config_class = config.get(config_name, config["default"])
    app.config.from_object(config_class)

    # check which config loaded
    import logging

    logging.basicConfig(level=logging.INFO)
    logging.info("Loaded config: %s (DEBUG=%s)", config_name, app.config["DEBUG"])

    if config_name == "production" and not app.config.get("SECRET_KEY"):
        raise RuntimeError("SECRET_KEY must be set in production")

    def load_food_data():
        """Load food list once, time-based cache"""
        global _FOOD_DATA_CACHE, _CACHE_TIMESTAMP
        current_time = time.time()
        if _FOOD_DATA_CACHE is None or (current_time - _CACHE_TIMESTAMP) > CACHE_TTL:
            json_path = os.path.join(app.root_path, "data", "foodlist.json")
            with open(json_path, encoding="utf-8") as f:
                _FOOD_DATA_CACHE = json.load(f)
            _CACHE_TIMESTAMP = current_time
            app.logger.info(f"Food data cache refreshed at {current_time}")
        return _FOOD_DATA_CACHE

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/api/categories")
    def get_categories():
        data = load_food_data()
        categories = list(data.keys())
        return jsonify(
            {
                "categories": [
                    {"id": cat, "display": cat.replace("_", " ").title()}
                    for cat in categories
                ]
            }
        )

    @app.route("/api/subcategories/<category>")
    def get_subcategories(category):
        data = load_food_data()
        if category in data:
            subcategories = list(data[category].keys())
            return jsonify(
                {
                    "subcategories": [
                        {"id": sub, "display": sub.replace("_", " ").title()}
                        for sub in subcategories
                    ]
                }
            )
        return jsonify({"error": "Category not found"}), 404

    @app.route("/api/random-item/<category>/<subcategory>")
    def get_random_item(category, subcategory):
        data = load_food_data()
        try:
            items = data[category][subcategory].get("makanan", [])

            if items:
                source_item = random.choice(items)
                random_item = {
                    "name": source_item["name"],
                    "description": source_item.get("descrition", ""),
                    "image": url_for(
                        "static", filename=f"images/{source_item['image']}"
                    ),
                }
                return jsonify(
                    {
                        "item": random_item,
                        "category": category,
                        "subcategory": subcategory,
                    }
                )
            return jsonify({"error": "No items found"}), 404
        except KeyError:
            return jsonify({"error": "Invalid category or subcategory"}), 404

    return app
