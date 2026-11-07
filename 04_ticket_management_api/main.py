import sqlite3
from fastapi import FastAPI, Query, Path, HTTPException
from pydantic import BaseModel, Field
from typing import Literal, Optional
from database import get_connection
from schemas import TicketCreate, TicketUpdate, TicketPatch
from routers.tickets import router as tickets_router

app = FastAPI()
app.include_router(tickets_router)

DB_NAME = "tickets.db"

def init_db():
    conn = get_connection()

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



@app.post("/tickets")
def create_ticket(ticket: TicketCreate):

    ticket_data = ticket.model_dump()

    priority = get_priority(ticket_data["message"])

    conn = get_connection()

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


@app.put("/tickets/{ticket_id}")
def update_ticket(ticket_id: int, ticket: TicketUpdate):
    ticket_data = ticket.model_dump()

    conn = get_connection()

    cursor = conn.execute(
        """
        UPDATE tickets
        SET client = ?, message = ?, category = ?, priority = ?
        WHERE id = ?
        """,
        (
            ticket_data["client"],
            ticket_data["message"],
            ticket_data["category"],
            ticket_data["priority"],
            ticket_id
        )
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Ticket not found")

    conn.close()

    return {"id": ticket_id, **ticket_data}


@app.patch("/tickets/{ticket_id}")
def patch_ticket(ticket_id: int, ticket: TicketPatch):
    ticket_data = ticket.model_dump(exclude_unset=True)

    if not ticket_data:
        raise HTTPException(
            status_code=400,
            detail="No fields to update"
        )

    conn = get_connection()
    conn.row_factory = sqlite3.Row

    set_clause = ", ".join(
        f"{field} = ?" for field in ticket_data
    )

    values = list(ticket_data.values()) + [ticket_id]

    cursor = conn.execute(
        f"UPDATE tickets SET {set_clause} WHERE id = ?",
        values
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Ticket not found")

    cursor = conn.execute(
        "SELECT * FROM tickets WHERE id = ?",
        (ticket_id,)
    )

    result = dict(cursor.fetchone())
    conn.close()

    return result

@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: int):
    conn = get_connection()

    cursor = conn.execute(
        "DELETE FROM tickets WHERE id = ?",
        (ticket_id,)
    )

    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    return {"message": "Ticket deleted successfully"}


