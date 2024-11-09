# PartWatch Repository

**PartWatch** is an automotive parts tracking web application built with Flask, SQLAlchemy, WTForms, and Bootstrap. Developed as part of the Full-Stack Web Development course at HWR Berlin, this repository contains the full codebase and documentation with GitHub Pages.

## Repository Contents

> **Note:** 
In addition to code, this repository includes a basic setup for GitHub Pages documentation in the **`/docs`** folder or at [GitHub Pages](https://timluh98.github.io/FS-Webapp/).

## Steps to Execute the App

### Step 1: Set up a Python Virtual Environment

\`\`\`bash
python3 -m venv venv
source venv/bin/activate  # For Windows use 'venv\Scripts\activate'
\`\`\`

### Step 2: Install Requirements

Install the necessary Python packages with:

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### Step 3: Start the Development Server

Run the server using:

\`\`\`bash
python app.py
\`\`\`

**Expected output:**

\`\`\`plaintext
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment.
Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
\`\`\`

### Step 4: Access the Application

Go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) to view the main page and start using PartWatch after registering and logging in.

## Features

- **User Authentication**: Secure login and registration, with separate roles for "customer" and "supplier".
- **Part Offering**: Suppliers can add new automotive parts with details like price, quantity, and estimated delivery.
- **Catalogue**: Customers can browse available parts and view detailed information if logged in.
- **Buying and Selling**: Facilitates transactions through PartWatch’s marketplace.
