# Changelog

All notable changes to the WriteSpace project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.0.0] - 2024-06-01

### Added

- **Public Landing Page**
  - Hero section with gradient background and animated glow effect
  - Feature highlights showcasing Easy Writing, Role-Based Access, and Beautiful Design
  - Latest posts section displaying the six most recent blog entries
  - Responsive layout with mobile-first design

- **Authentication System**
  - User registration with display name, username, and password confirmation
  - Login with username and password credentials
  - Session-based authentication using Flask sessions
  - Logout functionality with session cleanup
  - `login_required` decorator for protecting authenticated routes
  - `admin_required` decorator for restricting admin-only routes

- **Blog CRUD Operations**
  - Create new blog posts with title and content
  - Read individual blog posts on a dedicated page
  - Edit existing posts with pre-populated form fields
  - Delete posts with confirmation modal
  - Character counters for title (100 max) and content (5000 max)
  - Posts sorted by creation date in descending order
  - Post cards with title, excerpt, author avatar, and date

- **Admin Dashboard**
  - Platform statistics overview: total posts, total users, admin count, viewer count
  - Quick action buttons for common admin tasks
  - Recent posts table with edit links
  - Accessible only to users with the admin role

- **User Management**
  - Admin interface for creating new users with role selection
  - User listing table with display name, username, role, and creation date
  - Delete users with confirmation modal
  - Protection against deleting the default admin account (id=1)
  - Protection against self-deletion

- **Role-Based Access Control**
  - Two roles: `admin` and `viewer`
  - Admins can manage users, access the admin dashboard, and edit or delete any post
  - Viewers can create, read, edit, and delete their own posts
  - Role badges displayed throughout the interface

- **Avatar System**
  - Emoji-based avatars determined by user role
  - Admin users display a crown emoji (👑) with indigo accent
  - Viewer users display a book emoji (📖) with teal accent
  - Multiple size variants: small, medium, large, extra-large
  - Avatar with name component for inline display

- **JSON File Storage**
  - File-based storage using `data/users.json` and `data/posts.json`
  - Atomic writes using temporary files and `os.replace` to prevent corruption
  - Automatic creation of data directory and default files on startup
  - Default admin account seeded on first run (username: `admin`, password: `adminpass`)

- **UI and Design**
  - Custom CSS design system with CSS custom properties
  - Gradient headers and hero sections
  - Responsive navigation bar with mobile hamburger menu
  - Flash message notifications with auto-dismiss and slide animations
  - Modal dialogs for delete confirmations
  - Error pages for 404 and 500 responses
  - Print-friendly styles
  - Responsive grid layouts for post cards, stat cards, and feature cards

- **Deployment**
  - Vercel deployment configuration with Python runtime
  - Environment variable support via `.env` file
  - Configurable secret key, debug mode, and storage backend