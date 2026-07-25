import os
import subprocess
import sys
import time

def main():
    port = os.environ.get("PORT", "8501")
    backend_port = "8000"
    
    print(f"Starting FastAPI Backend with uv on port {backend_port}...")
    backend_proc = subprocess.Popen([
        "uv", "run", "uvicorn", "app.main:app",
        "--host", "0.0.0.0",
        "--port", backend_port
    ])
    
    # Give backend a moment to initialize
    time.sleep(2)
    
    print(f"Starting Streamlit Frontend with uv on port {port}...")
    frontend_proc = subprocess.Popen([
        "uv", "run", "streamlit", "run", "frontend/app.py",
        "--server.port", str(port),
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
        "--server.enableCORS", "false"
    ])
    
    try:
        frontend_proc.wait()
    except KeyboardInterrupt:
        print("Shutting down AIMap processes...")
        backend_proc.terminate()
        frontend_proc.terminate()

if __name__ == "__main__":
    main()
