---
title: Design Decisions
nav_order: 3
---

{: .label }
[Johann Estrada Pox & Tim Luhmann]

{: .no_toc }
# Design decisions

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## 01: Using Flask with SQLAlchemy for Database Management

### Meta

Status
: **Decided**

Updated
: 21-Oct-2024

### Problem statement

We need a way to handle database operations for our motorcycle parts application, **PartWatch**. The application includes user registration, roles, parts listings and purchases. We need to decide on an efficient way to interact with our SQLite database that will also support future scalability when we move to a more robust database.

### Decision

We decided to use **SQLAlchemy** as our Object Relational Mapper (ORM) to manage database interactions. This decision was made because of SQLAlchemy's compatibility with Flask, its support for an ORM layer, and its flexibility to work with multiple database engines in the future. The decision was made by the development team.

### Regarded options

1. **Plain SQL** - Direct SQL queries embedded in the code.
2. **SQLAlchemy ORM** - Use SQLAlchemy ORM for a more Pythonic database interaction.

| Criterion              | Plain SQL                       | SQLAlchemy ORM                      |
|------------------------|---------------------------------|-------------------------------------|
| **Ease of Use**        | Requires raw SQL for each query | Provides a high-level API for CRUD  |
| **Future Scalability** | Limited                         | Easily switchable to other DBs      |
| **Readability**        | Complex with inline SQL         | More readable with Python classes   |
| **Learning Curve**     | None if SQL is known           | Moderate, but well-documented       |

---

## 02: User Roles and Permissions (Customer vs. Supplier)

### Meta

Status
: **Decided**

Updated
: 24-Oct-2024

### Problem statement

The application requires different user roles: **Suppliers**, who can list parts, and **Customers**, who can browse and order parts. We need a system to enforce these permissions based on the user’s role.

### Decision

We implemented a **role-based access control** system by adding a `role` column to the `User` model in the database. This allows us to differentiate permissions in the app, such as allowing only suppliers to add new parts. 

The decision was made to simplify role management without creating overly complex permissions and is in line with our initial project requirements.

### Regarded options

1. **Role-based access control (simpler)** - Add a `role` attribute to users to control permissions.
2. **Advanced Permissions System (complex)** - Implement a detailed permissions matrix for each action.

| Criterion             | Simple Role System         | Advanced Permissions System         |
|-----------------------|----------------------------|-------------------------------------|
| **Implementation**    | Easy to set up             | Requires detailed permission checks |
| **Flexibility**       | Sufficient for two roles   | Better for complex permissions      |
| **Performance**       | Lightweight                | Higher processing for permissions   |

---

## 03: Image Upload and Storage for Part Listings

### Meta

Status
: **Decided**

Updated
: 29-Oct-2024

### Problem statement

Suppliers need to upload images of motorcycle parts for their listings. We need a reliable way to handle image uploads and storage within the app.

### Decision

We chose to store images locally in the `static/images` directory. When a user uploads an image, it is saved directly to this folder, and the file path is stored in the database. This approach keeps the app lightweight and avoids the need for third-party storage services during development.

### Regarded options

1. **Local Storage** - Store images in a local directory within the project.
2. **Cloud Storage (e.g., AWS S3)** - Use a cloud service to store and retrieve images.

| Criterion              | Local Storage               | Cloud Storage                   |
|------------------------|-----------------------------|---------------------------------|
| **Setup Complexity**   | Simple                      | More complex                    |
| **Cost**               | Free                        | Potential costs                 |
| **Scalability**        | Limited by server capacity  | Scalable with storage service   |

---

## 04: Using WTForms and Bootstrap for User Interface

### Meta

Status
: **Decided**

Updated
: 21-Oct-2024

### Problem statement

To create a consistent and user-friendly interface for form submissions, we need a framework for form handling and styling.

### Decision

We chose **WTForms** for form handling and **Bootstrap** for styling to make the forms more accessible and responsive. WTForms integrates well with Flask, and Bootstrap provides a modern, responsive design that enhances user experience. This combination was chosen to save development time while maintaining a professional look and feel.

### Regarded options

1. **WTForms + Bootstrap** - Use WTForms for form processing and Bootstrap for styling.
2. **Custom HTML/CSS** - Create custom forms without a framework.

| Criterion              | WTForms + Bootstrap         | Custom HTML/CSS                |
|------------------------|-----------------------------|---------------------------------|
| **Ease of Integration**| Seamless with Flask         | Requires more custom code       |
| **Design Consistency** | Uniform with Bootstrap      | Requires detailed CSS work      |
| **Development Speed**  | Faster setup                | More time-intensive             |

---

## 05: Order Tracking and My Orders Feature

### Meta

Status
: **Decided**

Updated
: 07-Nov-2024

### Problem statement

The application needs to allow customers to place orders for parts and view their orders under a "My Orders" tab. This requires order data to be stored persistently in the SQLite database, linking each order to a user and a specific part.

### Decision

We added a `Purchase` model to the database to store each order. When a customer places an order, the details are saved in the `Purchase` table, which links the order to the user and the specific part they ordered. Customers can view their past orders in the "My Orders" tab.

### Regarded options

1. **Database Table for Purchases** - Store each order as a record in a `Purchase` table within SQLite.
2. **Session-based Order Tracking** - Track orders only within the user session without permanent storage.

| Criterion              | Database Table              | Session-based Tracking          |
|------------------------|-----------------------------|---------------------------------|
| **Persistence**        | Permanent in SQLite         | Temporary in session            |
| **Scalability**        | Suitable for multiple users | Limited to active session       |
| **User Experience**    | View past orders anytime    | Only viewable in-session        |

---

## 06: Filtering Parts in the Catalogue

### Meta

Status
: **Decided**

Updated
: 24-Nov-2024

### Problem statement

Customers need the ability to filter the catalogue to quickly find parts by price (ascending or descending) and manufacturer.

### Decision

We implemented a filtering system in the catalogue view, allowing customers to filter by price or manufacturer name. This was chosen for its simplicity and to enhance the user experience when browsing parts.

### Regarded options

1. **Basic Filters** - Add basic filtering for price and manufacturer.
2. **Advanced Filtering** - Add multiple, complex filters for detailed searches.

| Criterion              | Basic Filters               | Advanced Filters                |
|------------------------|-----------------------------|---------------------------------|
| **Ease of Use**        | Simple interface for users  | Could overwhelm users           |
| **Implementation Time**| Short                       | Long                            |
| **Performance**        | Lightweight                | Could slow down for large data  |

---

## 07: Part Deletion and Stock Management

### Meta

Status
: **Decided**

Updated
: 27-Nov-2024

### Problem statement

Suppliers need the ability to delete their part listings. Additionally, the system should prevent the quantity of parts from going below zero and automatically update the availability status to "Out of Stock" when the quantity reaches zero.

### Decision

We implemented a delete button for suppliers to remove their part listings. We also added logic to ensure that the quantity of parts cannot go below zero and that the availability status is automatically updated to "Out of Stock" when the quantity reaches zero.

### Regarded options

1. **Manual Deletion and Stock Management** - Allow suppliers to manually delete parts and manage stock.
2. **Automated Deletion and Stock Management** - Implement automated deletion and stock management logic.

| Criterion              | Manual Deletion and Stock Management | Automated Deletion and Stock Management |
|------------------------|--------------------------------------|----------------------------------------|
| **Ease of Use**        | Requires manual intervention         | Automated and user-friendly            |
| **Implementation Time**| Short                                | Moderate                               |
| **Error Prevention**   | Prone to human error                 | Reduces human error                    |

---

## 08: Shopping Cart Implementation

### Meta

Status
: **Decided**

Updated
: 13-Dec-2024

### Problem statement

Users need the ability to add, view, and remove parts from a shopping cart before proceeding to checkout. The cart should persist across user interactions within a session and dynamically update prices based on quantities.

### Decision

We implemented a session-based shopping cart that allows users to add, view, and remove parts. The cart dynamically updates the total price as quantities are adjusted. The cart persists within the same session, ensuring a seamless user experience.

### Regarded options

1. **Session-Based Cart Management** - Store cart data in the session to maintain state across user interactions.
2. **Database-Based Cart Management** - Store cart data in the database to persist across sessions and devices.

| Criterion              | Session-Based Cart Management | Database-Based Cart Management |
|------------------------|-------------------------------|--------------------------------|
| **Ease of Use**        | Simple and quick to implement | Requires more complex logic    |
| **Persistence**        | Limited to session            | Persistent across sessions     |
| **Scalability**        | Suitable for small to medium  | Suitable for large-scale       |
| **Implementation Time**| Short                         | Longer                         |

---

This document outlines the principal design decisions made for **PartWatch**, together with an overview of the options considered. The decisions reflect the project's current requirements and priorities, and they strike a balance between simplicity and scalability for future growth.
