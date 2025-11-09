#!/usr/bin/env python3
import uvicorn
import os

if __name__ == "__main__":
    os.environ['DEBUG'] = 'False'
    
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
        log_level="info",
        access_log=False
    )
