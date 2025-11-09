#!/usr/bin/env python3
import uvicorn
import os

if __name__ == "__main__":
    os.environ['DEBUG'] = 'False'
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=False,
        log_level="info",
        access_log=False
    )
