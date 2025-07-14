#!/bin/bash
pip install fastapi uvicorn httpx python-dotenv
uvicorn relay_server:app --host 0.0.0.0 --port 8000
