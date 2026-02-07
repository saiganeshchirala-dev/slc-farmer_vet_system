import sys
import os

# Get the absolute path of the project root
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the root and backend directories to the Python path
# This ensures that 'backend' can be imported and relative imports work
if root_path not in sys.path:
    sys.path.insert(0, root_path)

backend_path = os.path.join(root_path, "backend")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Import the actual FastAPI app from the backend folder
# Using absolute import through the 'backend' package
from backend.app.main import app

# This allows the command 'gunicorn app.main:app' to find the 'app' object
