# Deployment Guide

This document covers how to run WriteSpace locally, deploy it to Vercel, and important notes about storage limitations in serverless environments.

---

## Table of Contents

- [Local Development Setup](#local-development-setup)
- [Environment Variables](#environment-variables)
- [Vercel Deployment](#vercel-deployment)
- [JSON File Storage Limitations](#json-file-storage-limitations)
- [Migrating to a Database (Supabase)](#migrating-to-a-database-supabase)

---

## Local Development Setup

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd writespace-blog
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:

- `flask>=3.0.0` — the web framework
- `python-dotenv>=1.0.0` — for loading environment variables from `.env`

### 4. Configure Environment Variables

Copy the example environment file and adjust values as needed:

```bash
cp .env.example .env
```

Edit `.env` with your preferred settings:

```
SECRET_KEY=change-me-to-a-random-secret-key
DEBUG=True
STORAGE_BACKEND=local
```

See the [Environment Variables](#environment-variables) section below for details on each variable.

### 5. Run the Application

```bash
python app.py
```

The application will start on `http://127.0.0.1:5000` by default.

### 6. Default Admin Account

On first run, WriteSpace automatically creates a `data/` directory with default JSON files. A default admin account is seeded:

| Field    | Value       |
|----------|-------------|
| Username | `admin`     |
| Password | `adminpass` |

> **Important:** Change the default admin password in a production environment by editing `data/users.json` or by deleting the file and modifying the `DEFAULT_USERS` list in `utils/storage.py` before first run.

---

## Environment Variables

| Variable          | Description                                      | Default                            |
|-------------------|--------------------------------------------------|------------------------------------|
| `SECRET_KEY`      | Flask secret key used for session signing. Must be a long, random string in production. | `change-me-to-a-random-secret-key` |
| `DEBUG`           | Enable Flask debug mode. Set to `True` for development, `False` for production. | `False`                            |
| `STORAGE_BACKEND` | Storage backend identifier. Currently only `local` (JSON file storage) is implemented. | `local`                            |

### Generating a Secure Secret Key

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Use the output as your `SECRET_KEY` value.

---

## Vercel Deployment

WriteSpace includes a `vercel.json` configuration for deploying to [Vercel](https://vercel.com/) as a serverless Python application.

### Project Structure for Vercel

The following files are relevant to the Vercel deployment:

```
├── api/
│   └── index.py          # Vercel serverless entry point
├── vercel.json            # Vercel build and routing configuration
├── requirements.txt       # Python dependencies
├── app.py                 # Flask application
└── ...
```

### How It Works

**`vercel.json`** configures the build and routing:

- The `builds` section tells Vercel to use the `@vercel/python` runtime for `api/index.py`.
- The `rewrites` section routes all incoming requests (`/(.*)`) to the `/api/index` serverless function.

**`api/index.py`** imports the Flask `app` object from `app.py` and exposes it as the WSGI application that Vercel invokes.

### Deployment Steps

1. **Install the Vercel CLI** (if not already installed):

   ```bash
   npm install -g vercel
   ```

2. **Log in to Vercel:**

   ```bash
   vercel login
   ```

3. **Deploy from the project root:**

   ```bash
   vercel
   ```

   Follow the prompts to link or create a new Vercel project.

4. **Set environment variables** in the Vercel dashboard or via the CLI:

   ```bash
   vercel env add SECRET_KEY
   vercel env add DEBUG
   vercel env add STORAGE_BACKEND
   ```

   - Set `SECRET_KEY` to a secure random string.
   - Set `DEBUG` to `False` for production.
   - Set `STORAGE_BACKEND` to `local` (or your chosen backend).

5. **Deploy to production:**

   ```bash
   vercel --prod
   ```

### Vercel Environment Variable Configuration

You can also set environment variables through the Vercel web dashboard:

1. Go to your project on [vercel.com](https://vercel.com/).
2. Navigate to **Settings** → **Environment Variables**.
3. Add `SECRET_KEY`, `DEBUG`, and `STORAGE_BACKEND` for the appropriate environments (Production, Preview, Development).

---

## JSON File Storage Limitations

WriteSpace uses a JSON file-based storage system (`data/users.json` and `data/posts.json`) by default. While this is simple and works well for local development, there are significant limitations to be aware of in certain deployment environments.

### Serverless Environments (Vercel, AWS Lambda, etc.)

**Serverless functions have an ephemeral filesystem.** This means:

- **Data is not persisted between invocations.** Each time a serverless function cold-starts, the filesystem is reset to the original deployment state. Any data written to `data/users.json` or `data/posts.json` during a request will be lost when the function instance is recycled.

- **Concurrent writes are unsafe.** Multiple serverless function instances may run simultaneously, each with their own copy of the filesystem. There is no shared state between instances, so concurrent writes will result in data loss or corruption.

- **The `data/` directory may not be writable.** Some serverless platforms mount the deployment bundle as a read-only filesystem (with the exception of `/tmp`), which would cause write operations to fail entirely.

### Implications

If you deploy WriteSpace to Vercel (or any serverless platform) with the default JSON file storage:

- The default admin account will be available on every cold start.
- Any new users, posts, or edits will persist only for the lifetime of that particular function instance.
- Data will appear to "reset" unpredictably as instances are recycled.

### When JSON File Storage Works Well

- **Local development** — running `python app.py` on your machine.
- **Single-server deployments** — running on a traditional VPS or VM where the filesystem is persistent and there is only one application process (or processes share the same filesystem with proper locking).

---

## Migrating to a Database (Supabase)

For production deployments — especially on serverless platforms like Vercel — you should replace the JSON file storage with a proper database. [Supabase](https://supabase.com/) (managed PostgreSQL) is a recommended option that pairs well with Vercel.

### High-Level Migration Steps

1. **Create a Supabase project** at [supabase.com](https://supabase.com/) and note your database connection string.

2. **Create database tables** for `users` and `posts` matching the current JSON schema:

   ```sql
   CREATE TABLE users (
       id SERIAL PRIMARY KEY,
       display_name TEXT NOT NULL,
       username TEXT UNIQUE NOT NULL,
       password TEXT NOT NULL,
       role TEXT NOT NULL DEFAULT 'viewer',
       created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
   );

   CREATE TABLE posts (
       id SERIAL PRIMARY KEY,
       title TEXT NOT NULL,
       content TEXT NOT NULL,
       author_id INTEGER NOT NULL REFERENCES users(id),
       author_name TEXT NOT NULL,
       author_role TEXT NOT NULL DEFAULT 'viewer',
       created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
   );
   ```

3. **Seed the default admin user:**

   ```sql
   INSERT INTO users (display_name, username, password, role, created_at)
   VALUES ('Admin', 'admin', 'adminpass', 'admin', '2024-06-01T12:00:00Z');
   ```

   > **Note:** In a real production setup, you should hash passwords rather than storing them in plain text.

4. **Add a database client** to `requirements.txt` (e.g., `psycopg2-binary` or `supabase`).

5. **Implement a new storage backend** in `utils/storage.py` that reads from and writes to the Supabase PostgreSQL database instead of JSON files. The `STORAGE_BACKEND` environment variable is already defined in `config.py` and can be used to switch between `local` (JSON) and a new `supabase` backend.

6. **Set the database connection string** as an environment variable in Vercel:

   ```bash
   vercel env add DATABASE_URL
   ```

7. **Update `utils/storage.py`** to check `Config.STORAGE_BACKEND` and route calls to either the JSON file functions or the database functions accordingly.

### Why Supabase?

- **Managed PostgreSQL** — no database administration required.
- **Generous free tier** — suitable for small projects and prototyping.
- **Works with Vercel** — connect via standard PostgreSQL connection strings.
- **Built-in auth** (optional) — could replace the custom auth system in the future.

---

## Summary

| Deployment Target       | Storage Recommendation       | Notes                                                    |
|------------------------|------------------------------|----------------------------------------------------------|
| Local development       | JSON files (default)         | Simple, no setup required.                               |
| Single VPS / VM         | JSON files or PostgreSQL     | JSON works if single-process; database recommended.      |
| Vercel (serverless)     | PostgreSQL (e.g., Supabase)  | JSON files will not persist. Database swap is required.   |
| AWS Lambda / GCP Cloud Functions | PostgreSQL or DynamoDB | Ephemeral filesystem; external database required.        |