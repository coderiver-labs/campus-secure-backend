# Campus Secure Backend

A production-oriented school management backend built with **Django REST Framework**, designed with a strong focus on security, role-based authorization, asynchronous processing, observability, payment processing, and maintainable backend architecture.

---

## Overview

**Campus Secure Backend** is a school management REST API for managing users, students, teachers, staff, academics, examinations, fee payments, documents, and system auditing.

The project was designed beyond a basic CRUD application, with explicit separation of responsibilities, security controls, background processing, monitoring, centralized logging, error tracking, and database query optimization.

---

## Tech Stack

### Backend

- Python 3.12
- Django 5.2
- Django REST Framework
- Django Filter
- DRF Spectacular
- Access Policy based authorization

### Database & Storage

- PostgreSQL

### Background Processing

- Celery
- RabbitMQ

### Infrastructure

- Docker
- Docker Compose
- Nginx

### Monitoring & Observability

- Prometheus
- Grafana
- Loki
- Promtail
- Node Exporter
- Sentry

### Development & API Tooling

- uv
- Swagger / OpenAPI

---

## Core Features

### User Management

- Custom user model
- Email-based authentication
- Role-based user architecture
- User roles:
  - Admin
  - Staff
  - Teacher
  - Student
- Separate role-specific profiles
- Staff position management
- User activation and verification
- Role-based user visibility
- Protected administrative operations

### Authentication & Security

- Cookie-based authentication
- CSRF protection
- Role-based authorization
- Object-level authorization
- Access-policy based permission system
- API throttling
- Protected media handling
- Environment-based secret configuration
- Administrative boundary protection

### Academic Management

- Subjects
- Class levels
- Sections
- Student classes
- Student academic information
- Teacher assignments
- Teacher-to-class and subject relationships

### Examination System

- Exam lifecycle management
- Exam subjects
- Exam start/end periods
- Exam status management
- Student marks
- Teacher-based mark authorization

### Fee Payments

- Calendar-based monthly fee payment system
- 12-month calendar-based fee tracking
- January–December monthly payment tracking
- Payment tracking by calendar year and month
- Online payments via Stripe
- Offline cash payment support
- Multiple-month payment support
- Maximum 12 monthly payments per calendar year
- Prevents duplicate monthly fee payments
- Stripe Checkout integration
- Stripe webhook handling
- Payment status tracking
- Stripe transaction tracking

### Documents & Media

- Public media handling
- Protected media handling
- Nginx-based media serving
- Access-controlled protected files

### Background Tasks

Celery is used for asynchronous workloads such as:

- Email processing
- Password reset notifications
- Other background application tasks

RabbitMQ is used as the message broker.

### Observability & Error Tracking

The project includes an observability stack for application metrics, logs, infrastructure monitoring, and application error tracking.

```text
Django
   │
   ├── Prometheus ──→ Grafana
   │
   ├── Application Logs
   │        ↓
   │     Promtail
   │        ↓
   │       Loki
   │        ↓
   │     Grafana
   │
   └── Sentry ──→ Telegram Alerts
```

- Prometheus for application metrics
- Grafana for metrics visualization
- Loki for centralized log storage
- Promtail for log collection
- Node Exporter for host-level metrics
- Sentry for application error tracking
- Telegram notifications for Sentry error alerts

---

## Architecture

The project follows an explicit backend architecture with separation between API handling, validation, authorization, business logic, and data access.

```text
API Layer
    ↓
Serializer / Validation
    ↓
Permission / Authorization
    ↓
Service Layer
    ↓
Query / ORM Layer
    ↓
PostgreSQL
```

The project avoids unnecessary abstraction and focuses on keeping business logic, authorization, validation, and data access responsibilities clearly separated.

---

## Database Query Optimization

Database performance is considered at the ORM and query level.

The project uses:

- `select_related()`
- `prefetch_related()`
- Filtered querysets
- Pagination
- Appropriate database relationships
- Query inspection and profiling

Related data is loaded using optimized query patterns where appropriate to reduce unnecessary database queries.

PostgreSQL configuration was also profiled against the application's typical CRUD workload to avoid unnecessary query compilation overhead.

---

## Project Structure

```text
campus-secure-backend/
│
├── accounts/             # User and profile management
├── auth/                 # Authentication
├── audit/                # Audit functionality
├── celery_task/          # Celery tasks
├── config/               # Application configuration
├── documents/            # Document management
├── exams/                # Examination system
├── integrations/         # External service integrations
├── payment/              # Payment logic
├── permission/           # Authorization and access policies
├── school/               # School-related models and APIs
├── students/             # Student-related functionality
├── utils/                # Shared utilities
│
├── docs/                 # API Documentation
├── docker/               # Docker and infrastructure configuration
├── devtools/             # Development utilities
├── static/               # Static assets
├── templates/            # Django templates
│
├── CampusSecure/         # Django project configuration
├── manage.py
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── uv.lock
└── README.md
```
---

## 📖 API Documentation

The API can be explored using the included Postman or Reqable collection.

**Postman Collection:**  
`docs/api/postman/Campus-Secure-Backend.postman_collection.json`

**Reqable Collection:**  
`docs/api/reqable/Campus-Secure-Backend.reqable_collection.json`

---

# Installation

## Requirements

For the recommended setup:

- Git
- Docker
- Docker Compose

For local development without Docker:

- Python 3.12
- PostgreSQL
- RabbitMQ
- uv

The easiest way to run the complete system is **Docker Compose**.

---

## 1. Clone the Repository

```bash
git clone https://github.com/coderiver-labs/campus-secure-backend.git
cd campus-secure-backend
```

---

## 2. Create Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Update the values according to your environment.

Example:

```env
SECRET_KEY=your-secret-key

DEBUG=False

ALLOWED_HOSTS=localhost,127.0.0.1

DATABASE_URL=postgresql://user:password@postgres:5432/database

CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//

STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=

SENTRY_DSN=
```

Never commit `.env` or production secrets to Git.

---

# Running with Docker

Build the web application image:

```bash
docker build -t campus-secure-web:latest .
```

Start the application and supporting services:

```bash
docker compose up -d
```

Check running containers:

```bash
docker compose ps
```

View application logs:

```bash
docker compose logs -f web
```

The `web` container automatically runs:

```text
migrate
   ↓
collectstatic
   ↓
uvicorn
```

during startup.

Create a superuser:

```bash
docker compose exec web uv run python manage.py createsuperuser
```

---

# Running Without Docker

Install dependencies:

```bash
uv sync --locked
```

Run migrations:

```bash
uv run python manage.py migrate
```

Create a superuser:

```bash
uv run python manage.py createsuperuser
```

Run the development server:

```bash
uv run python manage.py runserver
```

Check Django configuration:

```bash
uv run python manage.py check
```

---

# API Documentation

The project uses **OpenAPI / DRF Spectacular** for API documentation.

Typical endpoints:

```text
/api/schema/
/api/docs/
/api/redoc/
```

Swagger UI can be used to explore and test the available API endpoints.

---

# Monitoring & Observability

The project includes several monitoring and observability components.

### Application Metrics

```text
Django
   ↓
Prometheus
   ↓
Grafana
```

Prometheus collects application metrics, while Grafana is used for visualization.

### Centralized Logging

```text
Application Logs
      ↓
   Promtail
      ↓
     Loki
      ↓
   Grafana
```

Promtail collects application logs and sends them to Loki for centralized log storage and querying.

### Infrastructure Metrics

```text
Node Exporter
      ↓
  Prometheus
      ↓
   Grafana
```

Node Exporter provides host-level system metrics.

### Application Error Tracking

```text
Django / Celery
      ↓
    Sentry
      ↓
 Telegram Notification
```

Sentry is used for application error tracking, with Telegram notifications configured for error alerts.

---

# Production Considerations

The project is structured with production deployment in mind.

Important production practices include:

- Environment-based secrets
- PostgreSQL as the primary relational database
- Nginx reverse proxy
- Protected media
- Cookie-based authentication
- CSRF protection
- API throttling
- Role-based authorization
- Database query optimization
- Background task processing
- Centralized logging
- Application monitoring
- Error tracking
- Containerized deployment

For an actual production deployment, additional configuration should include:

- HTTPS/TLS
- Secure cookie settings
- Proper `ALLOWED_HOSTS`
- Production database credentials
- Strong secret keys
- Proper CORS/CSRF configuration
- Secure Stripe webhook configuration
- Database backup strategy
- Monitoring and alerting configuration

---

# Design Principles

The project follows several backend engineering principles:

- Explicit over implicit behavior
- Separation of concerns
- Least-privilege authorization
- Reusable service-layer business logic
- Query optimization based on actual access patterns
- Secure-by-default configuration
- Observable production systems
- Avoid unnecessary abstraction

---

# Project Status

**Production-oriented backend — development completed.**

The project represents a completed backend implementation covering:

- Application architecture
- Authentication
- Authorization
- Database design
- Academic management
- Examination management
- Fee payments
- Asynchronous processing
- Stripe integration
- Containerization
- Reverse proxying
- Protected media
- Logging
- Monitoring
- Error tracking
- Sentry-to-Telegram alerting

Grafana is used for metrics visualization and monitoring. Grafana alerting rules are not included as a completed project feature.

---

# Author

**CodeRiver Labs**

GitHub:

https://github.com/coderiver-labs