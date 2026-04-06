# WriteSpace

A modern blogging platform built with Python and Flask where ideas come to life. Write, share, and discover stories that matter.

## Features

- **Public Landing Page** — Hero section with gradient background, feature highlights, and latest posts
- **Authentication System** — User registration, login, session-based auth, and logout
- **Blog CRUD Operations** — Create, read, edit, and delete blog posts with character counters
- **Admin Dashboard** — Platform statistics, quick actions, and recent posts overview
- **User Management** — Admin interface for creating, listing, and deleting users
- **Role-Based Access Control** — Admin and viewer roles with permission enforcement
- **Avatar System** — Emoji-based avatars determined by user role (👑 admin, 📖 viewer)
- **JSON File Storage** — File-based storage with atomic writes for data integrity
- **Responsive Design** — Mobile-first CSS design system with custom properties
- **Flash Notifications** — Auto-dismissing slide-in notifications for user feedback
- **Error Pages** — Custom 404 and 500 error pages
- **Vercel Deployment** — Serverless deployment configuration included

## Tech Stack

- **Backend:** Python 3.10+, Flask 3.0+
- **Templating:** Jinja2
- **Storage:** JSON file-based (local)
- **Styling:** Custom CSS design system with CSS custom properties
- **Deployment:** Vercel (serverless Python runtime)
- **Environment:** python-dotenv for configuration management

## Folder Structure

```
writespace-blog/
├── api/
│   └── index.py              # Vercel serverless entry point
├── data/                      # Auto-generated JSON data directory
│   ├── users.json             # User records
│   └── posts.json             # Blog post records
├── static/
│   └── css/
│       └── style.css          # Global stylesheet and design system
├── templates/
│   ├── macros/
│   │   ├── avatar.html        # Avatar rendering macros
│   │   └── cards.html         # Post card, stat card, and feature card macros
│   ├── 404.html               # Not found error page
│   ├── 500.html               # Internal server error page
│   ├── admin_dashboard.html   # Admin dashboard template
│   ├── base.html              # Base layout with navbar, flash messages, footer
│   ├── blogs.html             # Blog listing page
│   ├── index.html             # Public landing page
│   ├── login.html             # Login form
│   ├── read_blog.html         # Single blog post view
│   ├── register.html          # Registration form
│   ├── user_management.html   # Admin user management page
│   └── write_blog.html        # Create/edit blog post form
├── utils/
│   ├── __init__.py            # Utils package init
│   ├── admin.py               # Admin operations (stats, user CRUD)
│   ├── auth.py                # Authentication (login, register, decorators)
│   ├── avatar.py              # Avatar helper function
│   └── storage.py             # JSON file storage (read, write, atomic ops)
├── .env.example               # Example environment variables
├── app.py                     # Flask application and route definitions
├── config.py                  # Configuration class with env var loading
├── requirements.txt           # Python dependencies
├── vercel.json                # Vercel deployment configuration
├── CHANGELOG.md               # Project changelog
├── DEPLOYMENT.md              # Detailed deployment guide
└── README.md                  # Project documentation (this file)
```

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository:**

   ```bash
   git clone <your-repo-url>
   cd writespace-blog
   ```

2. **Create a virtual environment (recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate        # macOS / Linux
   venv\Scripts\activate           # Windows
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

### Environment Configuration

1. **Copy the example environment file:**

   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your settings:**

   ```
   SECRET_KEY=change-me-to-a-random-secret-key
   DEBUG=True
   STORAGE_BACKEND=local
   ```

3. **Generate a secure secret key for production:**

   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

| Variable | Description | Default |
|---|---|---|
| `SECRET_KEY` | Flask secret key for session signing | `change-me-to-a-random-secret-key` |
| `DEBUG` | Enable Flask debug mode (`True` or `False`) | `False` |
| `STORAGE_BACKEND` | Storage backend identifier (`local`) | `local` |

### Running Locally

```bash
python app.py
```

The application will start on [http://127.0.0.1:5000](http://127.0.0.1:5000).

On first run, WriteSpace automatically creates a `data/` directory with default JSON files and seeds a default admin account.

## Usage Guide

### Default Admin Credentials

| Field | Value |
|---|---|
| Username | `admin` |
| Password | `adminpass` |

> **Important:** Change the default admin password before deploying to production.

### User Roles

WriteSpace supports two roles:

| Role | Permissions |
|---|---|
| **Admin** (👑) | Full platform access — manage users, access admin dashboard, create/edit/delete any post |
| **Viewer** (📖) | Create, read, edit, and delete their own posts |

New accounts created through the registration page are assigned the **viewer** role by default. Admins can create users with either role through the User Management page.

### Blog Management

- **Create a post:** Navigate to **Write** from the navbar or click the "Write a Post" button on the blogs page. Fill in the title (max 100 characters) and content (max 5,000 characters), then publish.
- **Read a post:** Click any post title from the blogs listing or landing page to view the full content.
- **Edit a post:** Admins can edit any post. Viewers can edit only their own posts. Click the **Edit** button on the post card or the post detail page.
- **Delete a post:** Admins can delete any post. Viewers can delete only their own posts. Click the **Delete** button on the post detail page and confirm in the modal dialog.

### Admin Dashboard

Accessible to admin users via the **Admin** link in the navbar. The dashboard provides:

- Platform statistics (total posts, total users, admin count, viewer count)
- Quick action buttons for common tasks
- A table of the 10 most recent posts with edit links

### User Management

Accessible to admin users via the admin dashboard. Admins can:

- Create new users with a specified role
- View all registered users
- Delete users (with protection against deleting the default admin account or yourself)

## Deployment

WriteSpace includes a Vercel deployment configuration for serverless hosting. See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions covering:

- Vercel deployment steps
- Environment variable configuration
- JSON file storage limitations in serverless environments
- Migration guide for PostgreSQL (Supabase) for persistent storage

> **Note:** The default JSON file storage is ephemeral on serverless platforms. Data will not persist between function invocations. For production deployments on Vercel or similar platforms, migrate to an external database such as Supabase (PostgreSQL).

## License

This project is private and proprietary. All rights reserved. No part of this codebase may be reproduced, distributed, or transmitted in any form without prior written permission from the project owner.