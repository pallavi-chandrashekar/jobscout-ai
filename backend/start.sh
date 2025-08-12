#!/bin/bash
# Navigate to backend directory
cd "$(dirname "$0")"

# Export PYTHONPATH and run Uvicorn
export PYTHONPATH=.
uvicorn app.main:app --reload
