# Railway Deployment - Task Checklist

## Steps
- [x] 1. Create `.gitignore` to prevent committing venv, db.sqlite3, .env, __pycache__
- [x] 2. Update `requirements.txt` for reliable Railway installation
- [x] 3. Create `railway.json` config for Railway deployment
- [x] 4. Update `build.sh` for Railway
- [x] 5. Update `Procfile` for Railway
- [x] 6. Fix `settings.py` for Railway (Cloudinary env bug, static storage, hosts, CSRF)
- [x] 7. Fix `favicon.png` reference / add default favicon
- [x] 8. Fix hardcoded `/static/js/admin.js` in custom_admin/base.html
- [x] 9. Clean up duplicate nested `migrations/migrations/` directories
- [x] 10. Add `.env.example` with Railway-compatible variables
- [x] 11. Update `DEPLOYMENT.md` with Railway instructions
- [x] 12. Verify with `manage.py check` and `collectstatic`
