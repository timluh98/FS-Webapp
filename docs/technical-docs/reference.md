---
title: Reference
parent: Technical Docs
nav_order: 3
---

{: .label }
[Johann Estrada Pox]

{: .no_toc }
# Reference documentation

{: .attention }
> This page collects internal functions, routes with their functions, and APIs (if any).
> 
> See [Uber](https://developer.uber.com/docs/drivers/references/api) or [PayPal](https://developer.paypal.com/api/rest/) for exemplary high-quality API reference documentation.
>
> You may delete this `attention` box.

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## [Section / module]

## Public Routes

### `index()`
**Route:** `/`  
**Methods:** `GET`  
**Purpose:** Renders the homepage, showing featured parts loaded from "static/data/parts.json."  
**Sample output:** The rendered "catalogue_index.html" page.  

### `catalogue()`
**Route:** `/catalogue`  
**Methods:** `GET`  
**Purpose:** Lists all parts from the database, with optional filters (search, manufacturer, price).  
**Sample output:** The rendered "catalogue.html" page, showing a list of parts.

### `faq()`
**Route:** `/faq`  
**Methods:** `GET`  
**Purpose:** Displays frequently asked questions.  
**Sample output:** A static "faq.html" page with Q&A sections.

### `imprint()`
**Route:** `/imprint`  
**Methods:** `GET`  
**Purpose:** Shows legal information.  
**Sample output:** A static "imprint.html" page.

### `terms()`
**Route:** `/terms`  
**Methods:** `GET`  
**Purpose:** Displays terms & conditions of the platform.  
**Sample output:** A static "terms.html" page.

### `privacy()`
**Route:** `/privacy`  
**Methods:** `GET`  
**Purpose:** Shows the privacy policy.  
**Sample output:** A static "privacy.html" page.

---

## Authentication & Profile Routes

### `register()`
**Route:** `/register`  
**Methods:** `GET`, `POST`  
**Purpose:** Allows new users to sign up (customer or supplier).  
**Sample output:** On success, user is redirected to "login.html" with a success message.

### `login()`
**Route:** `/login`  
**Methods:** `GET`, `POST`  
**Purpose:** Authenticates existing users.  
**Sample output:** On success, redirects to "/" with a success message.  

### `logout()`
**Route:** `/logout`  
**Methods:** `GET`  
**Purpose:** Logs the current user out.  
**Sample output:** Redirects to "login.html" with an info message.

### `profile()`
**Route:** `/profile`  
**Methods:** `GET`, `POST`  
**Purpose:** Allows the user to update their email and password.  
**Sample output:** Shows a simple "profile.html" form; on success, redirects to "/" with a success message.

---

## Supplier Routes

### `offer_part()`
**Route:** `/offer-part`  
**Methods:** `GET`, `POST`  
**Purpose:** Allows suppliers to offer (create) new parts.  
**Sample output:** Renders "offer_part.html"; on success, redirects to "/" with a success message.

### `my_listings()`
**Route:** `/my_listings`  
**Methods:** `GET`  
**Purpose:** Lists all parts for the logged-in supplier.  
**Sample output:** Renders "my_listings.html" with part data.

### `edit_part(part_id)`
**Route:** `/edit-part/<int:part_id>`  
**Methods:** `GET`, `POST`  
**Purpose:** Edits an existing part’s data.  
**Sample output:** Renders "edit_part.html" with a form; on success, redirects to "my_listings.html."

### `delete_part(part_id)`
**Route:** `/delete-part/<int:part_id>`  
**Methods:** `POST`  
**Purpose:** Deletes a part owned by the current supplier.  
**Sample output:** On success, redirects to "/catalogue" with a success message.

---

## Shopping & Orders

### `add_to_cart(part_id)`
**Route:** `/add_to_cart/<int:part_id>`  
**Methods:** `POST`  
**Purpose:** Adds a specified part to the session cart.  
**Sample output:** Redirects to "/catalogue" with a success flash message.

### `remove_from_cart(part_id)`
**Route:** `/remove_from_cart/<int:part_id>`  
**Methods:** `POST`  
**Purpose:** Removes a part from the session cart.  
**Sample output:** Redirects to "/cart" with a success message.

### `cart()`
**Route:** `/cart`  
**Methods:** `GET`  
**Purpose:** Displays current items in the cart, displays total price, and shows a “Place Order” form.  
**Sample output:** Renders "cart.html," listing user-selected cart items.

### `purchase_cart()`
**Route:** `/purchase_cart`  
**Methods:** `POST`  
**Purpose:** Validates shipping information, creates a new order and purchase entries, and clears the cart.  
**Sample output:** Redirects to "my_orders.html" with a success message on completion.

### `my_orders()`
**Route:** `/my_orders`  
**Methods:** `GET`  
**Purpose:** Shows the current user’s orders (customer view), plus a supplier’s orders if the user is a supplier.  
**Sample output:** Renders "my_orders.html" with separate sections for the user’s orders and supplier orders.

### `confirm_payment(order_id)`
**Route:** `/confirm_payment/<int:order_id>`  
**Methods:** `POST`  
**Purpose:** Lets the customer mark an order as paid (payment_status = ‘paid’).  
**Sample output:** Redirects to "/my_orders" with a success message.

### `confirm_shipping(order_id)`
**Route:** `/confirm_shipping/<int:order_id>`  
**Methods:** `POST`  
**Purpose:** Allows the supplier to mark an order’s shipping status as “shipped.”  
**Sample output:** Updates the order in the DB, redirects to "/my_orders" with a success message.

### `confirm_completion(order_id)`
**Route:** `/confirm_completion/<int:order_id>`  
**Methods:** `POST`  
**Purpose:** Lets the customer confirm completion when the order is delivered, setting `completion_status` to “completed.”  
**Sample output:** Updates the order in the DB, redirects to "/my_orders" with a success message.