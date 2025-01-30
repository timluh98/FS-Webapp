---
title: Team Member Responsibilites 
nav_order: 6
---

## Team members

### Johann Estrada Pox

- **Database Management**: Created and configured the SQLite database for storing user, parts, and order data; defined database models for `User`, `Part`, and `Purchase` entities.
- **Form Handling and Validation**: Integrated CSRF protection, built secure form handling for login, registration, and part offerings, and troubleshooted validation issues.
- **Backend Routes and Logic**: Implemented backend routes for login, registration, offer part, and purchase functionality, ensuring correct user roles for `supplier` and `customer` actions.
- **Dynamic Content Rendering**: Designed and implemented logic to dynamically fetch parts data from the database and render it in templates like `catalogue.html` and `catalogue_index.html`.
- **User Authentication and Authorization**: Managed user roles (`supplier` and `customer`) and enforced role-specific permissions for part offerings and purchases; configured `flask-login` for session management.
- **Image Handling and File Management**: Enabled image upload functionality for part offerings, handled file saving in the `static/images` folder, and ensured image security with filename sanitization.
- **Error Handling and Debugging**: Identified and resolved key issues throughout the project, including debugging form validation issues and ensuring data persistence in the database.
- **Order Functionality**: Implemented the `my_orders` feature to track customer orders and save purchase details in the SQLite database under the "My Orders" tab.
- **Filter and Search Features**: Developed functionality for customers to filter motorcycle parts by price (ascending/descending) and manufacturer names in the catalogue.
- **Profile Management**: Implemented the `profile.html` feature to allow users to manage their profiles, including securely updating their passwords.
- **Documentation and Setup Instructions**: Provided instructions for setting up and initializing the project, including steps for environment setup, database creation, and sample data insertion.
- **Cart Implementation**: Designed and implemented the shopping cart feature, facilitating adding, removing, and finalizing purchases.
- **Modern UI Styling**: Updated various elements (forms, buttons, layout) to ensure a more modern and responsive user interface across pages.

### Tim Hendrik Luhmann

- **Frontend Development and Template Management**: Created and maintained the core template structure through base.html, implemented responsive navigation, and established consistent styling via style.css and catalogue_index.css.
Template Implementation: Developed and styled key user interface templates including:

- **User authentication interfaces**: (login.html, register.html)
Catalogue viewing systems (catalogue_index.html, catalogue.html)
Part management interfaces (offer_part.html, view_part.html)
Order tracking system (my_orders.html)


- **Form Development**: Designed and implemented critical form components:
Created the OfferPartForm for supplier part submissions
Developed the PurchaseForm for customer order processing


- **Route Implementation**: Built and managed essential application routes:
Catalogue index display and navigation
Detailed part view functionality
Order tracking and management system

