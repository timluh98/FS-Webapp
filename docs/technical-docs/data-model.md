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
+ [Purchase Table](#purchase-table)
+ [Relationships](#relationships)
+ [Additional Considerations](#additional-considerations)
{: toc }
</details>

The **PartWatch** data model is composed of three primary tables: `User`, `Part`, and `Purchase`. These tables work together to support the main functionalities of the application, including user management, part listing, and transaction tracking. This section provides an overview of each table and their relationships within the application.

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

## Purchase Table

The `Purchase` table logs transactions between customers and suppliers, including buyer details and payment information.

| Column         | Type          | Description                                      |
|----------------|---------------|--------------------------------------------------|
| `id`           | Integer       | Primary key for each purchase.                   |
| `part_id`      | Integer       | Foreign key linking to the purchased part.       |
| `user_id`      | Integer       | Foreign key linking to the buyer (User).         |
| `name`         | String (150)  | Name of the buyer.                               |
| `address`      | String (300)  | Shipping address for the purchase.               |
| `card_number`  | String (20)   | Encrypted or hashed credit card number.          |
| `cvc`          | String (4)    | Encrypted CVC code for the card.                 |
| `exp_date`     | DateTime      | Expiration date of the card.                     |
| `quantity`     | Integer       | Quantity of parts purchased.                     |
| `total_price`  | Float         | Total cost of the purchase.                      |
| `purchase_date`| DateTime      | Date and time of the transaction.                |

## Relationships

- **User ↔ Part**: One-to-many relationship where each user (supplier) can offer multiple parts.
- **Part ↔ Purchase**: One-to-many relationship where each part can have multiple purchases associated with it.
- **User ↔ Purchase**: One-to-many relationship where each user can make multiple purchases.

## Additional Considerations

- **Security**: Sensitive fields like `card_number` and `cvc` should be encrypted or hashed for secure storage.
- **Data Validation**: Enforce validation on fields like `quantity` and `price` to ensure data integrity.
- **Indexing**: Fields such as `email` in `User` and `id` in all tables can be indexed to improve query performance.

This data model structure allows **PartWatch** to efficiently manage users, automotive parts, and purchase transactions, ensuring data consistency and security throughout the application.
