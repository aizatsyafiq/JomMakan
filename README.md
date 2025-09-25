# ApaSedap

A simple food decision helper web app that randomly selects what you should eat today.

## Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ApaSedap.git
cd ApaSedap
```

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
flask run
```

The app will start and be available at: **http://localhost:5000**

## foodlist.json

- Choices are fetched from `app/data/foodlist.json` with the following structure:
```json
{
  "category": {
    "subcategory": {
      "makanan": [
        {
          "name": "Food Name",
          "image": "image.jpg",
          "description": "Food description"
        }
      ]
    }
  }
}
```
- Add corresponding images to `app/static/images/food/`
- Changes are applied immediately