# MediMatch - Medicine Recommendation System

## Railway Deployment

This application is configured for Railway deployment.

### Environment Variables Required:

```bash
SECRET_KEY=your-secret-key-here-min-50-characters
DEBUG=False
ALLOWED_HOSTS=.railway.app
RAILWAY_ENVIRONMENT=production
```

### Deployment Steps:

1. Go to [Railway.app](https://railway.app)
2. Login with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Add PostgreSQL database from "New" → "Database" → "PostgreSQL"
6. Set environment variables in the Variables tab
7. Railway will automatically deploy

### Database:
Railway automatically provides `DATABASE_URL` when PostgreSQL is added.

### Build & Start Commands:
The `nixpacks.toml` file configures:
- **Build**: Install packages, collect static files, run migrations
- **Start**: Run gunicorn server

Your app will be live at: `https://your-app.railway.app`
