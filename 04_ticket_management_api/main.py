import sqlite3
from fastapi import FastAPI, Query, Path, HTTPException
from pydantic import BaseModel, Field
from typing import Literal, Optional

app = FastAPI()

def init_db():
    conn = sqlite3.connect("tickets.db")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client TEXT NOT NULL,
            message TEXT NOT NULL,
            category TEXT NOT NULL,
            priority TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


init_db()

class TicketCreate(BaseModel):
    client: str = Field(min_length=2, max_length=50)
    message: str = Field(min_length=5, max_length=500)
    category: str = "general"

tickets = [
    {
        "id": 1,
        "client": "Иван",
        "message": "Не работает оплата",
        "priority": "high"
    }
]


def get_priority(message):
    urgent_words = ["оплата", "не работает", "ошибка"]
    medium_words = ["возврат", "доставка"]

    if not message.strip():
        return "unknown"

    for word in urgent_words:
        if word in message.lower():
            return "high"

    for word in medium_words:
        if word in message.lower():
            return "medium"

    return "normal"




@app.get("/tickets")
def get_tickets(
    priority: Optional[str] = Query(
        default=None,
        pattern="^(high|medium|normal)$"
    )
):
    conn = sqlite3.connect("tickets.db")
    conn.row_factory = sqlite3.Row

    if priority:
        cursor = conn.execute(
            "SELECT * FROM tickets WHERE priority = ?",
            (priority,)
        )
    else:
        cursor = conn.execute(
            "SELECT * FROM tickets"
        )

    result = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return result

@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int = Path(..., gt=0)):
    conn = sqlite3.connect("tickets.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.execute(
        "SELECT * FROM tickets WHERE id = ?",
        (ticket_id,)
    )

    ticket = cursor.fetchone()
    conn.close()

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    return dict(ticket)

@app.post("/tickets")
def create_ticket(ticket: TicketCreate):

    ticket_data = ticket.model_dump()

    priority = get_priority(ticket_data["message"])

    conn = sqlite3.connect("tickets.db")

    cursor = conn.execute(
        """
        INSERT INTO tickets (client, message, category, priority)
        VALUES (?, ?, ?, ?)
        """,
        (
            ticket_data["client"],
            ticket_data["message"],
            ticket_data["category"],
            priority
        )
    )

    ticket_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return {
        **ticket_data,
        "id": ticket_id,
        "priority": priority
    }