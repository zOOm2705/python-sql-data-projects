import sqlite3

from fastapi import APIRouter, HTTPException, Query, Path
from typing import Optional

from database import get_connection

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)


@router.get("")
def get_tickets(
    priority: Optional[str] = Query(
        default=None,
        pattern="^(high|medium|normal)$"
    )
):
    conn = get_connection()

    if priority:
        cursor = conn.execute(
            "SELECT * FROM tickets WHERE priority = ?",
            (priority,)
        )
    else:
        cursor = conn.execute("SELECT * FROM tickets")

    result = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return result


@router.get("/{ticket_id}")
def get_ticket(ticket_id: int = Path(..., gt=0)):
    conn = get_connection()

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