import os
from typing import Optional

from app import create_app

config_name: Optional[str] = os.environ.get("CONFIG_ENV", "development")
app = create_app(config_name)

if __name__ == "__main__":
    app.run(
        host=os.environ.get("HOST", "0.0.0.0"), port=int(os.environ.get("PORT", 5000))
    )
