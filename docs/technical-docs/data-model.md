---
title: Data Model
parent: Technical Docs
nav_order: 2
---

{: .label }
[PartWatch Documentation]

{: .no_toc }
# Data Model

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ [User Table](#user-table)
+ [Part Table](#part-table)
+ [Order Table](#order-table)
+ [Purchase Table](#purchase-table)
+ [Relationships](#relationships)
+ [Additional Considerations](#additional-considerations)
{: toc }
</details>

The **PartWatch** data model is composed of four primary tables: `User`, `Part`, `Order`, and `Purchase`. These tables work together to support the main functionalities of the application, including user management, part listing, order tracking, and transaction logging. This section provides an overview of each table and their relationships within the application.

---

## User Table

The `User` table stores information about the application's users, including their credentials and role (customer or supplier).

| Column       | Type          | Description                                       |
|--------------|---------------|---------------------------------------------------|
| `id`         | Integer       | Primary key, unique identifier for each user.      |
| `username`   | String (150)  | Unique username for each user.                    |
| `email`      | String (150)  | Unique email used for login purposes.             |
| `password`   | String (200)  | Hashed password for secure login.                 |
| `role`       | String (50)   | User role (`customer` or `supplier`).             |

## Part Table

The `Part` table contains detailed information about each automotive part listed by suppliers.

| Column         | Type          | Description                                      |
|----------------|---------------|--------------------------------------------------|
| `id`           | Integer       | Primary key, unique identifier for each part.    |
| `name`         | String (150)  | Name of the part.                                |
| `supplier_id`  | Integer       | Foreign key linking to the supplier (User).      |
| `price`        | Float         | Price of the part in USD.                        |
| `availability` | String (100)  | Stock status (e.g., `In Stock`, `Out of Stock`). |
| `quantity`     | Integer       | Available quantity of the part.                  |
| `delivery`     | String (100)  | Estimated delivery time for the part.            |
| `image`        | String (200)  | Path to the part image file.                     |
| `description`  | Text          | Detailed description of the part.                |
| `manufacturer` | String (100)  | Manufacturer of the part.                        |
| `model`        | String (100)  | Model of the part.                               |

## Order Table

The `Order` table tracks user orders, including total costs and payment status:

| Column           | Type          | Description                                            |
|------------------|---------------|--------------------------------------------------------|
| `id`             | Integer       | Primary key for each order.                           |
| `user_id`        | Integer       | Foreign key linking to the user who placed the order. |
| `order_date`     | DateTime      | Date and time the order was created.                  |
| `total_amount`   | Float         | Total amount of the order (sum of all purchases).     |
| `payment_status` | String (20)   | Payment status for the order (e.g., "pending").       |
| `payment_reference`| String (100)| Internal reference number for payment.                |
| `payment_date`   | DateTime      | Date and time the payment was completed.              |

## Purchase Table

The `Purchase` table logs item-level details within a specific order:

| Column       | Type          | Description                                          |
|--------------|---------------|------------------------------------------------------|
| `id`         | Integer       | Primary key for each purchase entry.                |
| `order_id`   | Integer       | Foreign key linking to the associated order.         |
| `part_id`    | Integer       | Foreign key linking to the purchased part.           |
| `user_id`    | Integer       | Foreign key linking to the user (buyer).             |
| `quantity`   | Integer       | Number of items purchased in this entry.             |
| `total_price`| Float         | Total price for this purchase line.                  |
| `purchase_date`| DateTime    | Date and time when the purchase was made.            |

## Relationships

- **User ↔ Part**: One-to-many relationship where each user (supplier) can offer multiple parts.
- **User ↔ Order**: One-to-many relationship where each user can have multiple orders.
- **Order ↔ Purchase**: One-to-many relationship where each order can consist of multiple purchase entries.
- **Part ↔ Purchase**: One-to-many relationship where each part can be purchased multiple times across different orders.

## Additional Considerations

- **Security**: Sensitive fields like `password` should be hashed for secure storage.
- **Data Validation**: Enforce validation on fields like `quantity` and `price` to ensure data integrity.
- **Indexing**: Fields such as `email` in `User` and `id` in all tables can be indexed to improve query performance.

This data model structure allows **PartWatch** to efficiently manage users, automotive parts, orders, and purchase transactions, ensuring data consistency and security throughout the application.
