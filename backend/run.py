import uvicorn
import os
import sys

# Add the current directory to path so the app package is found
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

if __name__ == "__main__":
    print("Starting Farmers Vet System Backend...")
    print("Docs available at: http://127.0.0.1:8000/docs")
    # Run the app from the backend directory
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
