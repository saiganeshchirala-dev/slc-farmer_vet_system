import sys
import os

# Add the 'backend' directory to the Python path
# This allows 'import app' or 'from app.main import app' to work
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "backend"))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Now we can import the app from the backend/app folder
try:
    from app.main import app
except ImportError as e:
    print(f"Error importing app: {e}")
    # Fallback to absolute path if needed
    try:
        from backend.app.main import app
    except ImportError:
        raise e

# This file can be used by Gunicorn: gunicorn wsgi:app
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
