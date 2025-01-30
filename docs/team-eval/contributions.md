---
title: Contributions
parent: Team Evaluation
nav_order: 4
---

{: .label }
[PartWatch]

{: .no_toc }
# Summary of individual contributions

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## [Tim Luhmann]

Contributions
: # Motorcycle Parts Marketplace - Entwicklungstagebuch

## Oktober 2024

### October 13 - GitHub Pages and Homepage
- Creation of GitHub Pages
- Modification of `index.md` with general information

### October 21 - Login and Registration
- Removal of unnecessary template HTMLs
- Creation of `login.html` and `register.html`
- Reference: [DigitalOcean Tutorial](https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login), Perplexity - Prompt: What could an example register.html page look like for a Flask app?
- Adaptation of `base.html` for login status
 - Dynamic display of Login/Logout/Register
 - Basic framework for additional pages
- Reference: Copilot - Prompt: Can you provide an example of how to create `login.html` and `egister.html` pages for a Flask application, and how to adapt `base.html` to dynamically display Login/Logout/Register links based on user authentication status?

### October 24 - User Roles
- Addition of "Customer" and "Supplier" roles
- Integration into `base.html` and `register.html`
- Reference: Copilot - Prompt: How can I implement role-based access control in a Flask application, specifically adding 'Customer' and 'Supplier' roles, and integrate this functionality into `base.html` and `register.html`?

### October 25 - Offer Functionality
- "+ Motorcycle Part" button for Suppliers
- New route in `app.py`
- Creation of `catalogue_index`
 - Login button in top right
 - Placeholder for logo
 - Two sections with hidden information

### October 26 - Offer Creation
- "Offer New Motorcycle Part" page
- Form with fields:
 - Supplier
 - Price
 - Availability
 - Quantity
 - Estimated delivery time
- Image upload functionality
- Creation of `OfferPartForm` in `forms.py`
 - Integration of FloatField, SelectField, FileField
- Reference: Copilot - Prompt: How do I implement Image upload functionalty in my form via WTForms and app.py route?

### October 29 - Catalog Development
- Creation of `catalogue.html`
- Database query for parts
- Linking between catalog pages

### November 1 - Additional Features
- Planned:
 - Filter option by model/manufacturer
 - Search bar positioning
 - Background color adjustment

### November 4 - Navigation
- Implemented navbar dropdown
- Bootstrap structure
- References:
 - [Bootstrap Navbar](https://getbootstrap.com/docs/4.0/components/navbar/)
 - [Dropdown Tutorial](https://www.youtube.com/watch?v=VQWu4e6agPc)

### November 5 - Purchase Process
- Purchase form in `forms.py`
- New database model
- Route for article details
- `view_item.html` with:
 - Product details
 - Purchase form
 - Credit card options

### November 6 - User Guidance
- "How to use" button
- Speech bubble with tutorial
- Context-dependent display

### November 9 - Enhancements
- "How to use" only for authenticated users
- CSS optimization
- "My Orders" page
 - Display of user purchases

### December 1 - Further Improvements
- Out-of-stock banner
- "My Listings" for Suppliers
 - View own listings
 - Edit/delete articles
- Created architecture documentation

### December 14 - Payment Process
- Advance payment only
- Simplified database storage
- Combining multiple parts per order
- Reference: CoPilot - Prompt: How do add new attributes to my databese in sqlite without removing existing data?

### January 10 - Imprint, Terms and Privacy
- Added `imprint.html`, `terms.html` and `privacy.html` pages and linked them in the footer of the `base.html`
- A note has been added to inform the supplier that a 5% free will be taken upon successful purchases
- Added logic for confirming payments, shipping and completion. Implemented this through the use of buttons in the orders section and new attributes in the databse (shipping_status and so on)
- Reference: CoPilot - Prompt: How could I implement a payment system that confirms the payment and the shipping. How do I achieve that the Buttons for confirming that only shows for the right user?

## [Johann Estrada Pox]

Contributions
: # Motorcycle Parts Marketplace - Development Timeline

## October 2024

### October 10 - Initial Database Setup
- Configured the SQLite database and ensured model relationships (User, Part, Order, Purchase) followed best practices.
- Defined foreign keys and cascade rules to handle supplier-part relationships and automatic removal of orphaned records.
- Reference: [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/), GitHub Copilot - Prompt: How to set up proper cascade rules for SQLAlchemy models with supplier-part relationships?

### October 16 - Data Migration & Environment Setup
- Established a consistent environment setup to allow teammates to run migrations without conflicts.
- Verified database integrity by creating test records and removing outdated schema definitions.
- Reference: Perplexity - Prompt: What's the best way to handle SQLite migrations in a team environment?, ChatGPT - Prompt: How to ensure database integrity when removing outdated schemas?

### October 19 - Form Handling & Validation
- Created robust `RegistrationForm` and `LoginForm` with enforcing validators.
- Ensured secure password hashing with `werkzeug.security`.
- Reference: GitHub Copilot - Prompt: How to implement secure password validation in Flask-WTF forms?, [Stack Overflow](https://stackoverflow.com/questions/flask-login-best-practices)

### October 21 - Authorization & Role Management
- Implemented logic for restricting supplier-only actions.
- Set up dynamic navigation based on user roles.
- Reference: ChatGPT - Prompt: What's the most efficient way to implement role-based access control in Flask?, Microsoft Copilot - Prompt: How to create dynamic navigation links based on user roles?

### October 24 - Backend Routes & Logic
- Coordinated routing for core functionalities.
- Implemented user feedback system.
- Reference: [DigitalOcean Flask tutorials], GitHub Copilot - Prompt: How to structure Flask routes for optimal user feedback?

## November 2024

### November 12 - Order & Purchase Flow
- Finalized multi-item order handling system.
- Ensured proper tracking of orders and inventory.
- Reference: [Stack Overflow](https://stackoverflow.com/questions/sqlalchemy-relationships), ChatGPT - Prompt: How to handle complex order relationships in SQLAlchemy?

### November 24 - Search & Filter Features, Profile Management & Debugging
- Built advanced search and filter functionality.
- Created secure profile management system.
- Reference: Perplexity - Prompt: What's the most efficient way to implement search filters in SQLAlchemy?, GitHub Copilot - Prompt: How to optimize database queries for search functionality?

## December 2024

### December 13 - Cart & Checkout Refactoring
- Introduced session-based shopping cart system.
- Implemented cart quantity management.
- Reference: Microsoft Copilot - Prompt: What's the best way to manage shopping cart data in Flask sessions?, ChatGPT - Prompt: How to handle concurrent cart updates securely?

### December 14 - Image Handling & File Management, Final Setup & Documentation
- Integrated secure file upload system.
- Finalized documentation and testing.
- Reference: GitHub Copilot - Prompt: How to implement secure file uploads in Flask?, Perplexity - Prompt: What are the best practices for handling image uploads in a Flask application?
