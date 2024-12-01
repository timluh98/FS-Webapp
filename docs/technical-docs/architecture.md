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
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## Overview

PartWatch is a Flask-based web application that facilitates the buying and selling of automotive parts. It implements a B2C marketplace model where suppliers can list parts and customers can browse and purchase them. The application uses SQLAlchemy for database operations, WTForms for form handling, and Bootstrap for the frontend UI.

```mermaid
graph TD
    A[User] --> B[Flask App]
    B --> C[SQLite Database]
    B --> D[Static Files]
    C --> E[User Table]
    C --> F[Part Table]
    C --> G[Purchase Table]

Codemap
The application follows a typical Flask project structure:

PartWatch/
├── app.py              # Main application entry point
├── templates/          # Jinja2 HTML templates
│   ├── base.html      # Base template with common layout
│   ├── catalogue/     # Part browsing templates
│   └── auth/         # Authentication templates
├── static/            # Static assets
│   ├── css/          # Stylesheets
│   └── images/       # Uploaded part images
├── models/           # SQLAlchemy database models
└── forms/            # WTForms form definitions

Key components:

Authentication: Uses Flask-Login for session management with supplier/customer roles
Database: SQLite with SQLAlchemy ORM for data persistence
Forms: WTForms for input validation and CSRF protection
Templates: Jinja2 templates with Bootstrap styling
Cross-cutting concerns
Authentication & Authorization

Users must be logged in to access most features
Role-based access control (supplier vs customer)
Session management via Flask-Login
Data Flow

Parts listing: Suppliers create listings → stored in database → displayed in catalogue
Purchases: Customer orders → update stock → create purchase record
File Handling

Part images are stored in static/images
Filenames are sanitized for security
Security

CSRF protection on all forms
Password hashing
Input validation
Secure file uploads
For detailed implementation decisions, see our design decisions.

This architecture document provides a clear overview of the application structure while focusing on the most important technical aspects that a new developer would need to understand to contribute effectively.