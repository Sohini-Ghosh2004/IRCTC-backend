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

![ER Diagram](docs/er_diagram_irctc.png)

---

##  API Testing

Postman collection available in `/postman` folder.
### How to Import
1. Open Postman
2. Click "Import"
3. Upload the JSON file
4. Start testing endpoints

---

### Example APIs Covered:
- User Registration & Login
- Train Search
- Ticket Booking (Confirmed / RAC / Waitlist)
- Cancel Booking
- Booking History

 **Note:** Some endpoints require JWT authentication.  
Login first and include the token in headers:

Authorization: Bearer <your_token>

##  Admin APIs
Certain endpoints are restricted to admin users:

- Add stations
- Add trains
- Create train schedules
- Add train stops

 These require an admin JWT token.

---

##  Run Locally

1. Clone the repo:

```bash
git clone https://github.com/Sohini-Ghosh2004/irctc-backend.git
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

