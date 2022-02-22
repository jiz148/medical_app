# add system path
import sys
import os
backend_path = os.path.dirname(os.path.abspath(__file__))
project_path = os.path.dirname(backend_path)
sys.path.append(backend_path)
sys.path.append(project_path)
from backend_sqlalchemy.backend_app.api import app


if __name__ == "__main__":
    app.run(debug=True, port=5001)
