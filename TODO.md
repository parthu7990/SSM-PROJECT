# Deployment - Task Checklist

## Railway Deployment (Primary Task)
- [x] 1. Verify `railway.json` configuration (Nixpacks build + gunicorn start)
- [x] 2. Verify `build.sh` (install deps, collectstatic, migrate, seed data)
- [x] 3. Verify `Procfile` (gunicorn web server)
- [x] 4. Verify `settings.py` for Railway (PostgreSQL via DATABASE_URL, ALLOWED_HOSTS, CSRF)
- [x] 5. Verify `requirements.txt` (gunicorn, psycopg2-binary, dj-database-url, whitenoise)
- [x] 6. Verify database migrations & seeding (`setup_initial_data`)
- [x] 7. Verify image/storage handling (Cloudinary + local fallback)
- [x] 8. Verify static files (collectstatic + WhiteNoise)
- [x] 9. Verify all pages render (homepage, admin, static assets)

## Vercel Deployment (Additional)
- [x] 1. Create `api/index.py` Vercel WSGI serverless handler
- [x] 2. Create/verify `vercel.json` configuration
- [x] 3. Update `requirements.txt` (removed unavailable `vercel-wsgi`)
- [x] 4. Update `settings.py` for Vercel (ALLOWED_HOSTS, CSRF, SSL redirect)
- [x] 5. Update `DEPLOYMENT.md` with Vercel instructions (incl. "How Vercel Deployment Works" section)
- [x] 6. Verify with `manage.py check` and handler test

## Admin Superuser Auto-Creation (Supabase/Deploy)
- [x] 1. Create `ensure_admin` management command (idempotent, env-based credentials)
- [x] 2. Wire `ensure_admin` into `build.sh` (runs on every Railway deploy)
- [x] 3. Add `ADMIN_USERNAME` / `ADMIN_EMAIL` / `ADMIN_PASSWORD` to `.env.example`
- [x] 4. Document `ensure_admin` in `DEPLOYMENT.md` (Vercel + Railway sections)
- [x] 5. Add Supabase database setup section to `DEPLOYMENT.md`
- [x] 6. Test `ensure_admin` on fresh DB (creates Parth/Parth@7990) and existing DB (updates)
- [x] 7. Verify superuser credentials work (login, is_staff, is_superuser)
