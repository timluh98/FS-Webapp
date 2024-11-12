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
- **Documentation and Setup Instructions**: Provided instructions for setting up and initializing the project, including steps for environment setup, database creation, and sample data insertion.

### Tim Hendrik Luhmann

- Managed and adjusted `base.html`, `style.css`, and `catalogue_index.css`; responsible for all navigation in `base.html`
- Worked on templates: `login.html`, `register.html`, `catalogue_index.html`, `offer_part.html`, `catalogue.html`, `view_part.html`, and `my_orders.html`
- Created `OfferPartForm` and `PurchaseForm` in `forms.py`; implemented routes for `catalogue_index`, `view_part`, and `my_orders.html`