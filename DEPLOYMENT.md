# Deployment Guide - SSM Future Innovation FZE Website

## Vercel Deployment

This project is fully configured for **Vercel** deployment as a Django serverless application.

### How It Works
- Vercel runs the Django app as a **serverless Python function** via `api/index.py`
- `api/index.py` exposes a `handler(request)` function that bridges Vercel's serverless request model to Django's WSGI application (no third-party wrapper needed)
- Static files are served by **WhiteNoise** through the WSGI application
- Media/uploads must use **Cloudinary** (serverless filesystem is read-only & ephemeral)

### 1. Prerequisites
- A [Vercel](https://vercel.com) account
- A managed PostgreSQL database (e.g., [Neon](https://neon.tech), [Supabase](https://supabase.com), or Railway Postgres)
- (Optional) A [Cloudinary](https://cloudinary.com) account for media storage
- The project pushed to a GitHub repository

### 2. Deploy to Vercel

#### Option A: Vercel Dashboard (Recommended)
1. Go to [Vercel](https://vercel.com) → **Add New** → **Project**
2. Import your GitHub repository
3. Vercel auto-detects the `vercel.json` config and Python build
4. Add the environment variables (see step 3)
5. Click **Deploy**

#### Option B: Vercel CLI
```bash
npm i -g vercel
vercel login
vercel
```

### 3. Configure Environment Variables

Add these in Vercel **Project → Settings → Environment Variables**:

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | ✅ | Django secret key (generate with: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`) |
| `DEBUG` | ✅ | Set to `False` |
| `DATABASE_URL` | ✅ | PostgreSQL connection string |
| `CLOUDINARY_CLOUD_NAME` | ⚠️ | Cloudinary cloud name (required for media uploads) |
| `CLOUDINARY_API_KEY` | ⚠️ | Cloudinary API key |
| `CLOUDINARY_API_SECRET` | ⚠️ | Cloudinary API secret |
| `EMAIL_HOST_USER` | Optional | SMTP email (e.g., gmail) |
| `EMAIL_HOST_PASSWORD` | Optional | SMTP password / app password |
| `ADMIN_EMAIL` | Optional | Where to receive inquiry emails |

> **Note:** `VERCEL` and `VERCEL_URL` are **auto-set** by Vercel — no need to add them manually. The settings automatically add your `*.vercel.app` domain to `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`.

> **⚠️ Critical — Database & Media:**
> - Vercel's serverless filesystem is **read-only and ephemeral**. SQLite will NOT work.
> - You **must** set `DATABASE_URL` to an external PostgreSQL database.
> - Uploaded media/images **must** use Cloudinary (set the 3 `CLOUDINARY_*` vars). Local `/media/` storage will not persist.

### 4. Run Database Migrations

Vercel doesn't run migrations automatically. After deploy, run them locally against your production DB:
```bash
# Set DATABASE_URL to your production PostgreSQL URL, then:
python manage.py migrate
python manage.py setup_initial_data
python manage.py createsuperuser
```
Or use a one-off script / admin command against the production database.

### 5. Access the App
- Your app will be available at `https://your-project.vercel.app`
- Admin panel: `https://your-project.vercel.app/admin/login/`
- Django admin (backup): `https://your-project.vercel.app/django-admin/`

### 6. Custom Domain (Optional)
1. In Vercel, go to Project → **Settings** → **Domains**
2. Add your custom domain
3. Update `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` env vars to include your domain

---

## How Vercel Deployment Works

### Serverless Entry Point (`api/index.py`)
- Vercel's `@vercel/python` builder invokes the `handler(request)` function in `api/index.py` for every request.
- The handler builds a WSGI `environ` from Vercel's request object and calls Django's WSGI `application` directly — **no third-party `vercel-wsgi` package is required** (that package does not exist on PyPI).
- It sets the `HTTP_X_FORWARDED_PROTO: https` header so Django's `SECURE_PROXY_SSL_HEADER` check passes, and `SECURE_SSL_REDIRECT` is disabled on Vercel to avoid redirect loops.

### Routing (`vercel.json`)
```json
{
  "builds": [
    { "src": "api/index.py", "use": "@vercel/python" }
  ],
  "routes": [
    { "src": "/(.*)", "dest": "api/index.py" }
  ]
}
```

### Static Files
- WhiteNoise serves collected static files through the WSGI application.
- `collectstatic` output is not committed to Git; Vercel collects static files during build via the Python build step.

### Database & Media (critical)
- **SQLite will NOT work** on Vercel because the serverless filesystem is read-only and ephemeral.
- You **must** set `DATABASE_URL` to an external PostgreSQL (Neon, Supabase, Railway Postgres, etc.).
- Uploaded media **must** use Cloudinary (set `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`). Local `/media/` storage will not persist.

### Auto-Domain Handling
- Vercel auto-sets `VERCEL=true` and `VERCEL_URL=<deployment-domain>`.
- `settings.py` automatically appends `VERCEL_URL` and `*.vercel.app` to `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`.

### Database Migrations
- Vercel does **not** run `migrate` automatically. Run migrations and seed data against your production database after deploy (see Step 4 above).

---

## Railway Deployment

This project is also fully configured for **Railway** deployment. Follow these steps:

### 1. Prerequisites
- A [Railway](https://railway.app) account
- The project pushed to a GitHub repository
- (Optional) A [Cloudinary](https://cloudinary.com) account for media storage

### 2. Set up the GitHub Repository

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/your-username/ssm-website.git
git push -u origin main
```

### 3. Deploy to Railway

#### Option A: Railway Dashboard (Recommended)
1. Go to [Railway](https://railway.app) → **New Project** → **Deploy from GitHub repo**
2. Select your repository
3. Railway will auto-detect the `railway.json` config

#### Option B: Railway CLI
```bash
railway login
railway init
railway up
```

### 4. Add a PostgreSQL Database
1. In Railway dashboard, click **New** → **Database** → **PostgreSQL**
2. Railway automatically adds the `DATABASE_URL` environment variable to your service
3. If not, add it manually:
   ```
   DATABASE_URL=postgresql://user:password@host:port/dbname
   ```

### 5. Configure Environment Variables

Add these variables in the Railway **Variables** tab:

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | ✅ | Django secret key (generate with: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`) |
| `DEBUG` | ✅ | Set to `False` |
| `CLOUDINARY_CLOUD_NAME` | ⚠️ | Cloudinary cloud name (for media) |
| `CLOUDINARY_API_KEY` | ⚠️ | Cloudinary API key |
| `CLOUDINARY_API_SECRET` | ⚠️ | Cloudinary API secret |
| `EMAIL_HOST_USER` | Optional | SMTP email (e.g., gmail) |
| `EMAIL_HOST_PASSWORD` | Optional | SMTP password / app password |
| `ADMIN_EMAIL` | Optional | Where to receive inquiry emails |

> **⚠️ Important about media files:**
> Railway filesystem is **ephemeral** — files uploaded to `/media/` are lost on every deploy/restart.
> **Use Cloudinary for persistent media storage.** Set the 3 `CLOUDINARY_*` variables.
> If you don't set Cloudinary, images will still work but won't persist across restarts.

### 6. Create Admin User

After first deploy, create a superuser:
```bash
railway run python manage.py createsuperuser
```
Or via Railway **Shell**:
```bash
python manage.py createsuperuser
```

### 7. Access the App
- Your app will be available at `https://your-project-name.up.railway.app`
- Admin panel: `https://your-project-name.up.railway.app/admin/login/`
- Django admin (backup): `https://your-project-name.up.railway.app/django-admin/`

### 8. Custom Domain (Optional)
1. In Railway, go to your service → **Settings** → **Networking** → **Generate Domain**
2. Add a custom domain and set `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` env vars

---

## How Railway Deployment Works

### Build Process (`build.sh`)
1. Install dependencies
2. `collectstatic` — collect static files
3. `migrate` — apply database migrations
4. `setup_initial_data` — seed initial data (services, clients, etc.)

### Runtime (`Procfile` / `railway.json`)
- Uses Gunicorn to serve the app
- Reads `PORT` from Railway automatically

### Configuration (`railway.json`)
```json
{
  "build": { "builder": "NIXPACKS", "buildCommand": "bash build.sh" },
  "deploy": {
    "startCommand": "gunicorn ssm_config.wsgi:application --bind 0.0.0.0:$PORT --workers 2",
    "healthcheckPath": "/",
    "healthcheckTimeout": 300
  }
}
```

---

## Configuration Details

### Environment Variables (`.env.example`)
```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=*
DATABASE_URL=   # Railway sets this automatically
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
EMAIL_HOST_USER=info@pskfutureinnovation.com
EMAIL_HOST_PASSWORD=
ADMIN_EMAIL=info@pskfutureinnovation.com
CSRF_TRUSTED_ORIGINS=https://*.up.railway.app,https://*.railway.app
```

### Static Files
- **WhiteNoise** serves static files directly (no extra CDN needed)
- Static files are collected to `staticfiles/` during build

### Media Files
- **Cloudinary** (recommended) — persistent, cloud-hosted media
- **Local** (development) — stored in `/media/`, lost on Railway restarts

### Database
- **PostgreSQL** (via Railway) — recommended for production
- **SQLite** (local dev) — automatic fallback when `DATABASE_URL` is empty

---

## Local Development

```bash
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py migrate

# 4. Create superuser
python manage.py createsuperuser

# 5. Seed initial data
python manage.py setup_initial_data

# 6. Run server
python manage.py runserver
```

---

## Troubleshooting

### Static files not loading
```bash
python manage.py collectstatic --noinput
```

### Database migration errors
```bash
python manage.py migrate --noinput
python manage.py makemigrations --check
```

### Media images not persisting
Ensure `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET` are set.

### CSRF errors on custom domain
Add your domain to `CSRF_TRUSTED_ORIGINS` env var.

### Health check timeout
The healthcheck path is `/`. If the homepage takes >300s to load on first deploy, increase `healthcheckTimeout` in `railway.json`.

---

## Support

For deployment assistance, contact: info@pskfutureinnovation.com
