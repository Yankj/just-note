from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid
import json
import os

app = FastAPI(title="Just Note API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data storage (in-memory for MVP, can be replaced with SQLite)
notes_db = []

# Models
class NoteCreate(BaseModel):
    type: str
    title: str
    content: str
    tags: List[str] = []
    amount: Optional[float] = None
    currency: Optional[str] = None
    dayId: str
    relatedIds: Optional[List[str]] = []
    aiSummary: Optional[str] = None

class Note(NoteCreate):
    id: str
    createdAt: str
    updatedAt: str

# Routes
@app.get("/")
def root():
    return {"message": "Just Note API", "version": "1.0.0"}

@app.get("/api/notes", response_model=List[Note])
def get_notes():
    return sorted(notes_db, key=lambda x: x['createdAt'], reverse=True)

@app.post("/api/notes", response_model=Note)
def create_note(note: NoteCreate):
    now = datetime.utcnow().isoformat() + "Z"
    new_note = Note(
        id=str(uuid.uuid4()),
        **note.dict(),
        createdAt=now,
        updatedAt=now
    )
    notes_db.append(new_note.dict())
    return new_note

@app.get("/api/notes/{note_id}", response_model=Note)
def get_note(note_id: str):
    for note in notes_db:
        if note['id'] == note_id:
            return note
    raise HTTPException(status_code=404, detail="Note not found")

@app.put("/api/notes/{note_id}", response_model=Note)
def update_note(note_id: str, note: NoteCreate):
    for i, existing_note in enumerate(notes_db):
        if existing_note['id'] == note_id:
            updated_note = {
                **existing_note,
                **note.dict(),
                'updatedAt': datetime.utcnow().isoformat() + "Z"
            }
            notes_db[i] = updated_note
            return updated_note
    raise HTTPException(status_code=404, detail="Note not found")

@app.delete("/api/notes/{note_id}")
def delete_note(note_id: str):
    for i, note in enumerate(notes_db):
        if note['id'] == note_id:
            notes_db.pop(i)
            return {"message": "Note deleted"}
    raise HTTPException(status_code=404, detail="Note not found")

@app.get("/api/notes/diary/{date}")
def get_diary(date: str):
    day_notes = [note for note in notes_db if note['dayId'] == date]
    return {
        "date": date,
        "count": len(day_notes),
        "notes": sorted(day_notes, key=lambda x: x['createdAt'])
    }

@app.get("/api/notes/stats")
def get_stats():
    total = len(notes_db)
    by_type = {}
    by_day = {}
    
    for note in notes_db:
        # By type
        note_type = note['type']
        by_type[note_type] = by_type.get(note_type, 0) + 1
        
        # By day
        day_id = note['dayId']
        by_day[day_id] = by_day.get(day_id, 0) + 1
    
    # Calculate streak
    unique_days = sorted(set(note['dayId'] for note in notes_db), reverse=True)
    streak = 0
    from datetime import timedelta
    current_date = datetime.utcnow().date()
    
    for day in unique_days:
        expected_date = current_date - timedelta(days=streak)
        if day == expected_date.strftime('%Y-%m-%d'):
            streak += 1
        else:
            break
    
    return {
        "total": total,
        "byType": by_type,
        "byDay": by_day,
        "streak": streak
    }

@app.post("/api/ai/classify")
def classify_content(content: str):
    # TODO: Integrate with OpenClaw LLM
    # For now, return a simple classification
    return {
        "type": "other",
        "title": content[:50],
        "tags": [],
        "aiSummary": "AI classification will be integrated soon"
    }

@app.post("/api/ai/summary")
def generate_summary(notes: List[str]):
    # TODO: Integrate with OpenClaw LLM
    return {
        "summary": "AI summary will be integrated soon"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
