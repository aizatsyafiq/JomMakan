from flask import Flask, render_template, jsonify
import json
import random
import os

def create_app():
    app = Flask(__name__)
    
    # Load food data
    def load_food_data():
        json_path = os.path.join(app.root_path, 'data', 'foodlist.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/api/categories')
    def get_categories():
        data = load_food_data()
        categories = list(data.keys())
        return jsonify({
            'categories': [
                {'id': cat, 'display': cat.replace('_', ' ').title()} 
                for cat in categories
            ]
        })
    
    @app.route('/api/subcategories/<category>')
    def get_subcategories(category):
        data = load_food_data()
        if category in data:
            subcategories = list(data[category].keys())
            return jsonify({
                'subcategories': [
                    {'id': sub, 'display': sub.replace('_', ' ').title()} 
                    for sub in subcategories
                ]
            })
        return jsonify({'error': 'Category not found'}), 404
    
    @app.route('/api/random-item/<category>/<subcategory>')
    def get_random_item(category, subcategory):
        data = load_food_data()
        try:
            # Look for 'makanan' key since that's what your JSON uses
            items = data[category][subcategory].get('makanan', [])
            
            if items:
                random_item = random.choice(items)
                # Check image path if needed
                if random_item.get('image'):
                    if not random_item['image'].startswith('/'):
                        random_item['image'] = f"/static/images/food/{random_item['image']}"
                return jsonify({'item': random_item, 'category': category, 'subcategory': subcategory})
            return jsonify({'error': 'No items found'}), 404
        except KeyError:
            return jsonify({'error': 'Invalid category or subcategory'}), 404
    return app