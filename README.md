# JomMakan

A simple food decision helper web app that randomly selects what you should eat today.

## Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/JomMakan.git
cd JomMakan
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

### 3. Create Environment File
```bash
# Copy the example environment file
cp app/.env.example app/.env

# Edit app/.env and set your SECRET_KEY (optional for development)
# Example: SECRET_KEY=your-random-secret-key-here
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```
or for development
```bash
pip install -r requirements-dev.txt
```

### 5. Run the Application
```bash
flask run
```

The app will start and be available at: **http://localhost:5000**

### 6. Verify Installation
Open your browser and navigate to `http://localhost:5000`. You should see:
- The JomMakan home screen with "Makan Apa Hari Ni?" heading
- Two category buttons: "Dapur Time" and "Tapau"
- Click through to test the random food selection

If you see errors, check the [Troubleshooting](#troubleshooting) section below.

## Updating Food Data

### foodlist.json Structure
Choices are fetched from `app/data/foodlist.json` with the following structure:
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
- Changes are applied immediately (no restart needed)

## Troubleshooting

**App won't start / shows errors:**
- Ensure virtual environment is activated (you should see `(venv)` in terminal)
- Check `app/.env` file exists
- Verify Flask is installed: `pip list | grep Flask`

**"No module named 'app'" error:**
- Run from the project root directory (where `run.py` is located)
- Set FLASK_APP: `export FLASK_APP=run.py` (Mac/Linux) or `set FLASK_APP=run.py` (Windows)

**Images not loading:**
- Check image filename matches exactly in `foodlist.json`
- Verify image exists in `app/static/images/food/`
- Images must be `.jpg` or `.png` format

**Port 5000 already in use:**
- Change port: `flask run --port 5001`
- Or kill the process using port 5000

**Still having issues?**
- Check console output for detailed error messages
- Enable debug mode by setting `DEBUG=True` in `app/.env`