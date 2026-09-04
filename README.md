# Smart Pantry Expiry Tracker

A backend API built with FastAPI and SQLAlchemy that tracks pantry inventory and helps reduce food waste by surfacing items nearing expiry.

## Features
- Add, view, and delete pantry items
- Items automatically sorted by expiry date
- SQLite database with SQLAlchemy ORM
- CORS-enabled for frontend integration

## Tech stack
Python, FastAPI, SQLAlchemy, SQLite

## How to run
1. Install dependencies: `pip install fastapi uvicorn sqlalchemy`
2. Run: `python main.py`
3. Opens automatically at `http://127.0.0.1:8000`
