# HospitalManagmentSystem AMAN KUMAR MORYA
# Hospital Management System

A backend Hospital Management System built using **Django REST Framework** with **JWT authentication**, **role-based access control**, **Google Calendar integration**, and a separate **Flask-based email notification service**.

---

# ## Setup and Run

### Prerequisites

* Python 3.11+
* Git
* Google Calendar API credentials (Desktop OAuth Client)
* Gmail App Password (for email service)

---

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/HospitalManagementSystem.git

cd HospitalManagementSystem
```

---

### 2. Create virtual environment

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux/macOS

```bash
source venv/bin/activate
```

---

### 3. Install Django dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Google Calendar

Place the downloaded OAuth Desktop credentials file in the project root as:

```
client_secret.json
```

The first successful authentication will automatically generate:

```
token.json
```

---

### 5. Run database migrations

```bash
python manage.py migrate
```

---

### 6. Create administrator

```bash
python manage.py createsuperuser
```

---

### 7. Start the Django backend

```bash
python manage.py runserver
```

Backend runs at

```
http://127.0.0.1:8000
```

---

### 8. Start the Email Service

Open another terminal.

```bash
cd email_service
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run

```bash
python app.py
```

Email service runs at

```
http://127.0.0.1:5000
```

---

### 9. Test APIs

Use Thunder Client or Postman.

Authentication uses JWT.

Include:

```
Authorization: Bearer <access_token>
```

---

# ## System Architecture

The project is divided into independent modules.

### Django Backend

The Django REST Framework application is responsible for:

* User registration
* Authentication
* Doctor management
* Patient management
* Appointment booking
* Availability management
* Google Calendar integration

Business logic is centralized inside Django views while serializers validate incoming data.

---

### Email Service

The email notification service is implemented as a separate Flask application.

Instead of embedding email logic inside Django, it runs independently and exposes an HTTP endpoint that accepts:

* recipient email
* subject
* message

This separation allows the email component to be deployed independently without modifying the Django backend.

---

### Data Model

The application contains four primary models.

**User**

Stores authentication information together with the application role.

Roles:

* Doctor
* Patient

Additional attributes include specialization, phone number and address.

---

**Availability**

Each availability belongs to exactly one doctor.

It stores

* doctor
* start time
* end time
* booking status

---

**Booking**

Each booking links

* one patient
* one availability slot

This avoids duplicate appointment information and guarantees that appointments reference existing availability.

---

### Role-Based Access

Role-based authorization is enforced using custom Django REST Framework permission classes.

```
IsDoctor
```

Only doctors can

* create availability
* view doctor bookings

```
IsPatient
```

Only patients can

* book appointments
* view personal appointments

JWT authentication identifies the logged-in user before permissions are evaluated.

---

### Google Calendar Integration

Google Calendar integration is implemented inside a dedicated module:

```
calendar_service/
```

After a successful booking:

1. Appointment is saved.
2. Google Calendar OAuth credentials are loaded.
3. An event is created.
4. The event appears in the authenticated Google Calendar.

Keeping the integration inside its own module prevents Google API code from mixing with booking logic.

---

# ## The Design Decision

### Decision

Separate the email notification service into an independent Flask application instead of implementing email delivery directly inside Django.

### Option 1

Implement email functionality directly in Django.

Advantages

* simpler deployment
* fewer services
* less configuration

Disadvantages

* tightly couples business logic and notification logic
* difficult to scale independently
* harder to replace the notification system later

---

### Option 2 (Chosen)

Implement email delivery as an independent Flask service.

Advantages

* clear separation of responsibilities
* easier maintenance
* independent deployment
* can later be replaced by AWS Lambda or another microservice without changing Django business logic

Disadvantages

* additional service to run
* requires HTTP communication between services

---

### Reasoning

The Flask service was chosen because it follows a microservice architecture. Notification systems often evolve independently from business logic, so isolating the email functionality reduces coupling and makes future scaling or migration significantly easier.

---

# ## Limitations

The current implementation is designed primarily for development and academic demonstration.

Current limitations include:

* SQLite is used instead of PostgreSQL, limiting concurrent write performance.
* Google Calendar authentication depends on Desktop OAuth and is not configured for production deployment.
* Gmail SMTP requires a manually generated App Password.
* The email service does not implement retries or asynchronous job queues.
* Secrets are currently configured manually and should be moved to environment variables or a secure secrets manager.
* There is no Docker configuration or containerized deployment.
* Error handling for external services such as Google Calendar and email delivery can be improved.
* Appointment booking currently assumes a single application instance and would require stronger concurrency handling for high-traffic production environments.

The first production improvement would be replacing SQLite with PostgreSQL and introducing a proper asynchronous task queue (such as Celery with Redis) for email delivery and calendar synchronization. This would improve reliability, scalability, and user experience under heavy load.
