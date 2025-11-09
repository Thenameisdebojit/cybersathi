#!/bin/bash
# Start the backend server

cd backend

# Kill any existing backend processes
pkill -f "app.main" 2>/dev/null || true

# Start backend
python -c "
from app.main import app
import uvicorn
uvicorn.run(app, host='127.0.0.1', port=8000, reload=False, log_level='warning')
"
