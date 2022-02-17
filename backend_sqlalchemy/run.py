# add system path
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend_sqlalchemy.backend_app.api import app


if __name__ == "__main__":
    app.run(debug=True, port=5001)
