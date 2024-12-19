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

## [Joe Doe]

Contributions
: Diam nonumy eirmod
: Tempor invidunt ut labore
: ...
