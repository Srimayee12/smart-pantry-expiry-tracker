from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import date
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import Session
from fastapi import Depends
from database import Base, engine, get_db

app = FastAPI()

# 🛡️ 1. Allow the frontend to talk to the backend securely (CORS configuration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows everything for testing locally
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 1. Define what an incoming Item looks like (Pydantic Schema)
class PantryItemInput(BaseModel):
    name: str
    expiry_date: date

# 🗄️ Database Table Structure (SQLAlchemy Model)
class PantryItem(Base):
    __tablename__ = "pantry_items"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    expiry_date = Column(Date)

# Create the database tables automatically on startup
Base.metadata.create_all(bind=engine)

# 🌐 2. Tell the home route ("/") to send back your new dashboard file!
@app.get("/", response_class=HTMLResponse)
def home():
    return FileResponse("index.html")

# 📥 1. Read / Get Sorted Items
@app.get("/items/sorted")
def get_sorted_items(db: Session = Depends(get_db)):
    # Query the database and sort items by expiry_date ascending
    return db.query(PantryItem).order_by(PantryItem.expiry_date.asc()).all()

# 📤 2. Create / Add New Item
@app.post("/items")
def add_pantry_item(item: PantryItemInput, db: Session = Depends(get_db)):
    # Map incoming JSON data to our Database structure
    db_item = PantryItem(name=item.name, expiry_date=item.expiry_date)
    
    db.add(db_item)      # Stage it
    db.commit()         # Save it permanently to the file
    db.refresh(db_item) # Load the generated auto-incrementing ID
    return {"message": "Item added successfully!", "added_item": db_item}

# 🗑️ 3. Delete Item
@app.delete("/items/{item_id}")
def delete_pantry_item(item_id: int, db: Session = Depends(get_db)):
    # Search the database for the item by ID
    db_item = db.query(PantryItem).filter(PantryItem.id == item_id).first()
    
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
        
    db.delete(db_item)  # Remove it
    db.commit()         # Save changes
    return {"message": f"Successfully removed item!"}
            
    # If we looped through everything and didn't find the ID
    raise HTTPException(status_code=404, detail="Item not found")

if __name__ == "__main__":
    import webbrowser
    import uvicorn
    # Automatically open Google Chrome to your API endpoint
    webbrowser.open("http://127.0.0.1:8000/")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)