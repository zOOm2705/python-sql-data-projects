from fastapi.testclient import TestClient
from main import app
import pytest
import sqlite3
from pathlib import Path
import database
import main

print("MAIN FILE:", main.__file__)
print("HAS DB_NAME:", hasattr(main, "DB_NAME"))

client = TestClient(app)


@pytest.fixture
def test_db(tmp_path, monkeypatch):
    db_path = tmp_path / "test_tickets.db"
    
    monkeypatch.setattr(database, "DB_NAME", str(db_path))

    conn = sqlite3.connect(db_path)

    conn.execute("""
        CREATE TABLE tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client TEXT NOT NULL,
            message TEXT NOT NULL,
            category TEXT NOT NULL,
            priority TEXT NOT NULL
        )
    """)

    conn.execute(
        """
        INSERT INTO tickets (client, message, category, priority)
        VALUES (?, ?, ?, ?)
        """,
        ("Иван", "Не работает оплата", "payments", "high")
    )

    conn.commit()
    conn.close()

    return db_path

def test_get_tickets(test_db):
    response = client.get("/tickets")

    assert response.status_code == 200

    data = response.json()

    for ticket in data:
        assert "id" in ticket
        assert isinstance(ticket["id"], int)
        assert ticket["id"] > 0

    assert isinstance(data, list)
    assert len(data) >= 1

    print(data)

def test_get_ticket(test_db):
    response = client.get("/tickets/1")

    assert response.status_code == 200

    ticket = response.json()

    assert "client" in ticket
    assert "message" in ticket

def test_get_ticket_not_found(test_db):
    response = client.get("/tickets/999")

    assert response.status_code == 404

def test_create_ticket(test_db):
    response = client.post(
        "/tickets",
        json={
            "client": "Мария",
            "message": "Не работает оплата",
            "category": "payments"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 2
    assert data["client"] == "Мария"
    assert data["category"] == "payments"
    assert data["priority"] == "high"


def test_create_ticket_invalid_data(test_db):
    response = client.post(
        "/tickets",
        json={
            "client": "A",
            "message": "Нет",
            "category": "payments"
        }
    )

    assert response.status_code == 422

def test_patch_ticket(test_db):
    response = client.patch(
        "/tickets/1",
        json={
            "priority": "medium"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["priority"] == "medium"
    assert data["client"] == "Иван"
    assert data["message"] == "Не работает оплата"


def test_update_ticket(test_db):
    response = client.put(
        "/tickets/1",
        json={
            "client": "Пётр",
            "message": "Проблема с доставкой",
            "category": "delivery",
            "priority": "medium"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["client"] == "Пётр"
    assert data["message"] == "Проблема с доставкой"
    assert data["category"] == "delivery"
    assert data["priority"] == "medium"


def test_delete_ticket(test_db):
    response = client.delete("/tickets/1")

    assert response.status_code == 200
    assert response.json()["message"] == "Ticket deleted successfully"

    response = client.get("/tickets/1")
    assert response.status_code == 404