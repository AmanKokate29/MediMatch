# Deploying MediMatch on Vercel

This repository is configured for deployment on [Vercel](https://vercel.com/).

---

## 1. Project Configuration Files Included

- [`vercel.json`](vercel.json): Configures the Python 3.9 WSGI runtime and static file routing.
- [`build_files.sh`](build_files.sh): Installs requirements and runs `collectstatic`.
- [`medicine_project/wsgi.py`](medicine_project/wsgi.py): Exports `app = application` for Vercel.
- [`medicine_project/settings.py`](medicine_project/settings.py): Automatically handles `.vercel.app` domains, CSRF trusted origins, WhiteNoise static files, and serverless database storage.

---

## 2. Important: Database on Vercel

> **Serverless Filesystem Note:**  
> Vercel functions run in a read-only environment (except `/tmp`). Any local SQLite file in the project folder cannot be written to.
> 
> **For production on Vercel, use an external hosted database:**
> - **PostgreSQL (Recommended):** [Neon](https://neon.tech/) (Free), [Supabase](https://supabase.com/) (Free), or Railway.
> - Provide the connection string via the `DATABASE_URL` environment variable in Vercel.

---

## 3. Environment Variables to Set in Vercel

In your Vercel Project Settings under **Settings > Environment Variables**, add the following:

| Key | Example / Description |
|---|---|
| `SECRET_KEY` | `django-insecure-m3d1m@tch-x#9q7k2p8r5t1w4y6z0b-localkey!` (or your own random key) |
| `DEBUG` | `False` |
| `DATABASE_URL` | Your PostgreSQL/MySQL connection string (e.g. from Neon, Supabase, or Railway) |
| `GROQ_API_KEY` | Your Groq API key |
| `GROQ_MODEL` | `openai/gpt-oss-20b` |
| `LOCATIONIQ_API_KEY` | Your LocationIQ API key |

---

## 4. Deployment Steps

### Option A: Via GitHub (Recommended)

1. Commit and push your changes to GitHub:
   ```bash
   git add .
   git commit -m "Configure Vercel deployment"
   git push
   ```
2. Go to [vercel.com/new](https://vercel.com/new).
3. Import your `MediMatch` GitHub repository.
4. Add the **Environment Variables** listed above.
5. Click **Deploy**.

### Option B: Via Vercel CLI

1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```
2. In the project root, run:
   ```bash
   vercel
   ```
3. Follow the prompts and set your environment variables when requested.
