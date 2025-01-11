---
title: Architecture
parent: Technical Docs
nav_order: 1
---

{: .label }
[Johann Estrada Pox & Tim Luhmann]

{: .no_toc }
# Architecture

<details open markdown="block">
  <summary>Table of contents</summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

## Overview

PartWatch is a Flask-based web application that facilitates the buying and selling of motorcycle parts. It implements a B2C marketplace model where suppliers list parts and customers can browse and purchase them. The application uses SQLAlchemy for database operations, WTForms for form handling, and Bootstrap for the frontend UI.

```mermaid
graph TD
    A[Client Browser] --> B[Flask Application]
    B --> |Manage Sessions & Auth| C[Flask-Login]
    B --> |Handle Forms| D[WTForms]
    B --> |ORM Queries| E[SQLAlchemy]
    B --> |Serve| F[Static Files]
    B --> |Render| G[Jinja Templates]

    E --> U[User]
    E --> P[Part]
    E --> O[Order]
    E --> R[Purchase]

    subgraph Tables
        U --> P
        O --> R
        P --> R
    end
```

## Codemap

The application follows a typical Flask project structure:

```
FS-Webapp/
├── app.py
├── db.py
├── forms.py
├── migrations/
├── models.py
├── static/
│   ├── css/
│   │   └── style.css
│   ├── data/
│   └── images/
├── templates/
│   ├── base.html
│   ├── catalogue.html
│   ├── catalogue_index.html
│   ├── my_orders.html
│   ├── login.html
│   ├── register.html
│   ├── my_listings.html
│   ├── edit_part.html
│   ├── cart.html
│   ├── view_part.html
│   ├── offer_part.html
│   ├── faq.html
│   ├── imprint.html
│   ├── terms.html
│   └── privacy.html
└── docs/
    ├── assets/
    ├── team-eval/
    ├── tecincal-focs/
    └── technical-docs/
```

Key components:

- **Authentication**: Uses Flask-Login for session management with supplier/customer roles
- **Database**: SQLite with SQLAlchemy ORM for data persistence
- **Forms**: WTForms for input validation and CSRF protection
- **Templates**: Jinja2 templates with Bootstrap styling

## Cross-cutting concerns

### Authentication & Authorization

- Users must be logged in to access most features
- Role-based access control (supplier vs customer)
- Session management via Flask-Login

### Data Flow

- Parts listing: Suppliers create listings → stored in database → displayed in catalogue
- Purchases: Customer orders → update stock → create purchase record

### File Handling

- Part images are stored in static/images
- Filenames are sanitized for security

### Security

- CSRF protection on all forms
- Password hashing
- Input validation
- Secure file uploads