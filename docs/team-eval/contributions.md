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
: # Automotive Parts Marketplace - Entwicklungstagebuch

## Oktober 2024

### October 13 - GitHub Pages and Homepage
- Creation of GitHub Pages
- Modification of `index.md` with general information

### October 21 - Login and Registration
- Removal of unnecessary template HTMLs
- Creation of `login.html` and `register.html`
- Reference: [DigitalOcean Tutorial](https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login), [Perplexity](Prompt: What could an example register.html page look like for a Flask app?)
- Adaptation of `base.html` for login status
 - Dynamic display of Login/Logout/Register
 - Basic framework for additional pages

### October 24 - User Roles
- Addition of "Customer" and "Supplier" roles
- Integration into `base.html` and `register.html`

### October 25 - Offer Functionality
- "+ Automotive Part" button for Suppliers
- New route in `app.py`
- Creation of `catalogue_index`
 - Login button in top right
 - Placeholder for logo
 - Two sections with hidden information

### October 26 - Offer Creation
- "Offer New Automotive Part" page
- Form with fields:
 - Supplier
 - Price
 - Availability
 - Quantity
 - Estimated delivery time
- Image upload functionality
- Creation of `OfferPartForm` in `forms.py`
 - Integration of FloatField, SelectField, FileField

## November 2024

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

## [Johann Estrada Pox]

Contributions
: # Automotive Parts Marketplace - Development Timeline

## October 2024

### October 10 - Initial Database Setup
- Configured the SQLite database and ensured model relationships (User, Part, Order, Purchase) followed best practices.
- Defined foreign keys and cascade rules to handle supplier-part relationships and automatic removal of orphaned records.
- Referenced official Flask-SQLAlchemy docs for best practices on session handling and object instantiation.

### October 16 - Data Migration & Environment Setup
- Established a consistent environment setup to allow teammates to run migrations without conflicts.
- Verified database integrity by creating test records and removing outdated schema definitions.
- Assisted team members in troubleshooting environment issues on different operating systems.

### October 19 - Form Handling & Validation
- Created robust `RegistrationForm` and `LoginForm` with enforcing validators (e.g., InputRequired, Email, Length).
- Ensured secure password hashing with `werkzeug.security`, including error handling for mismatched or weak passwords.
- Incorporated CSRF protection for all user-facing forms and tested the forms with various input boundary conditions.

### October 21 - Authorization & Role Management
- Implemented logic for restricting supplier-only actions (e.g., offering new parts) with role checks in `app.py`.
- Set up dynamic navigation in `base.html` to show supplier/customer-specific links based on user role.
- Built custom decorators to streamline permission checking throughout the application (later removed in favor of simpler role checks).

### October 24 - Backend Routes & Logic
- Coordinated routing for user registration, login, order creation, and cart management sessions.
- Implemented user feedback via `flash` messages and standardized success/error routes for consistent UX.
- Used references such as [DigitalOcean’s Flask tutorials] and Flask-Login’s official documentation to integrate session-based authentication.

## November 2024

### November 2 - Search & Filter Features
- Built advanced search and filter functionality on `catalogue.html` with manufacturer dropdown, text search, and ascending/descending price sort.
- Performed query optimization, ensuring minimal overhead when fetching parts from the database.
- Conducted user acceptance testing to refine search behaviors and address edge cases (e.g., zero search results).

### November 8 - Cart & Checkout Refactoring
- Restructured the cart system to maintain items in session, simplifying the path to purchase pages.
- Added form fields to handle variations in quantity ordering and integrated partial updates for cart quantities.
- Coordinated with the front-end to ensure consistent feedback, including success flash messages after adding items to the cart.

### November 12 - Order & Purchase Flow
- Finalized multi-item order handling by mapping each cart item to a `Purchase` record linked to a single `Order`.
- Ensured the system tracked total order cost, payment status, and locked item quantity upon checkout.
- Employed references to community Q&A forums (Stack Overflow) and SQLAlchemy docs for solving commit/flush issues.

### November 20 - Profile Management & Debugging
- Created a dedicated `ProfileForm` with fields for email, current password, and new password, enabling secure updates.
- Implemented thorough logging (info, warning, error) to diagnose session-based anomalies during form submissions.
- Pinpointed and resolved concurrency issues that arose when multiple items were purchased within short time intervals.

## December 2024

### December 3 - Image Handling & File Management
- Integrated file uploads for part images in `OfferPartForm`, storing sanitized filenames in `static/images`.
- Validated image extensions (PNG, JPG, JPEG, GIF) to prevent malicious file uploads.
- Implemented fallback images for parts without an uploaded image, ensuring uniform presentation in the catalogue.

### December 10 - Supplier Listings & Maintenance
- Built “My Listings” page for suppliers to manage their offered parts, including edit/delete routes.
- Enhancements to “Edit Part” form that let suppliers override existing images or keep them as-is.
- Added rigorous error reporting on part edit failures, rolling back database changes to maintain data integrity.

### December 14 - Final Setup & Documentation
- Documented final instructions for installing dependencies, environment setup, and running the app in production-like conditions.
- Contributed to last-mile bug fixes, verifying that user flows (log in → add cart items → purchase → view orders) worked end-to-end without errors.
- Organized a final code review session with the team to ensure consistent coding style and readiness for project submission.
