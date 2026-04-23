# IRCTC Backend System

A backend system that simulates railway ticket booking with real-world features like Confirmed tickets, RAC (Reservation Against Cancellation), and Waitlist handling.

---

## Features

* User Authentication (JWT-based login/signup)
* Train Search (source → destination → date)
* Ticket Booking System:

  *  Confirmed Tickets
  *  RAC (Reservation Against Cancellation)
  *  Waitlist
* Smart Cancellation Handling (automatically promotes passengers from Waitlist to RAC and RAC to Confirmed).
* Concurrency-safe booking using database row locking

---

##  Tech Stack

* **Framework:** Flask (Python)
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Auth:** Flask-JWT-Extended
* **Validation:** Marshmallow

---

##  Database Design

![ER Diagram](docs/er_diagram.png)

---

##  API Testing

Postman collection available in `/postman` folder.

---

##  Run Locally

1. Clone the repo:

```bash
git clone https://github.com/YOUR_USERNAME/irctc-backend.git
cd irctc-backend
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Setup environment variables (`.env`):

```env
DATABASE_URL=your_postgres_url
JWT_SECRET_KEY=your_secret_key
```

4. Run server:

```bash
python run.py
```

---

## Highlight

This project implements real-world railway booking logic including RAC and waitlist handling along with concurrency control, which is rarely covered in typical student projects.
