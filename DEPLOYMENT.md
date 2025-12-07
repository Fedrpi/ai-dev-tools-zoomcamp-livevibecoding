# Deployment Guide - Render

This guide explains how to deploy the LiveCoding Interview Platform to Render.

## Prerequisites

- GitHub account with this repository
- Render account (free tier) - https://render.com

## Deployment Options

### Option 1: Blueprint (Recommended - One-Click Deploy)

1. **Push code to GitHub**
   ```bash
   git push origin init
   ```

2. **Connect to Render**
   - Go to https://render.com
   - Click "New Blueprint Instance"
   - Connect your GitHub repository
   - Select `render-blueprint.yaml`

3. **Configure Environment Variables**

   Render will automatically:
   - Create PostgreSQL database
   - Create backend service
   - Create frontend static site
   - Set up environment variables

4. **Update Frontend URLs**

   After backend deploys, update the frontend environment variables:
   - Go to frontend service settings
   - Update `VITE_API_BASE_URL` to your backend URL (e.g., `https://livecoding-backend.onrender.com`)
   - Update `VITE_WS_BASE_URL` to your backend WebSocket URL (e.g., `wss://livecoding-backend.onrender.com`)

5. **Update CORS**

   Go to backend service settings and update `CORS_ORIGINS` to your frontend URL:
   ```
   https://livecoding-frontend.onrender.com
   ```

6. **Run Database Migrations**

   After backend is deployed:
   - Go to backend service
   - Open "Shell" tab
   - Run:
     ```bash
     alembic upgrade head
     ```

### Option 2: Manual Setup

#### Step 1: Create PostgreSQL Database

1. Go to Render Dashboard
2. Click "New +" → "PostgreSQL"
3. Configure:
   - Name: `livecoding-db`
   - Database: `livecoding_db`
   - User: `livecoding`
   - Plan: **Free**
4. Click "Create Database"
5. Save the **Internal Database URL** for later

#### Step 2: Deploy Backend

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `livecoding-backend`
   - **Runtime**: Docker
   - **Docker Build Context Directory**: `backend`
   - **Dockerfile Path**: `backend/Dockerfile`
   - **Plan**: Free
4. Add Environment Variables:
   - `DATABASE_URL`: (paste Internal Database URL from Step 1)
   - `CORS_ORIGINS`: `*` (will update later)
5. Advanced Settings:
   - **Health Check Path**: `/health`
6. Click "Create Web Service"

#### Step 3: Run Database Migrations

1. Wait for backend to deploy
2. Go to backend service → "Shell" tab
3. Run migrations:
   ```bash
   alembic upgrade head
   ```
4. Verify seed data:
   ```bash
   python -c "from app.database import engine; from sqlalchemy import text; with engine.connect() as conn: print(conn.execute(text('SELECT COUNT(*) FROM problems')).scalar())"
   ```
   Should return `9` (9 coding problems seeded)

#### Step 4: Deploy Frontend

##### Option A: Static Site (Recommended for Free Tier)

1. Click "New +" → "Static Site"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `livecoding-frontend`
   - **Build Command**: `cd frontend && npm ci && npm run build`
   - **Publish Directory**: `frontend/dist`
4. Add Environment Variables:
   - `VITE_API_BASE_URL`: `https://livecoding-backend.onrender.com` (your backend URL)
   - `VITE_WS_BASE_URL`: `wss://livecoding-backend.onrender.com`
5. Configure Rewrites:
   - Source: `/*`
   - Destination: `/index.html`
   - Action: Rewrite
6. Click "Create Static Site"

##### Option B: Web Service with Docker (More Resources)

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `livecoding-frontend`
   - **Runtime**: Docker
   - **Docker Build Context Directory**: `frontend`
   - **Dockerfile Path**: `frontend/Dockerfile.render`
   - **Plan**: Free
4. Add Build-time Environment Variables:
   - `VITE_API_BASE_URL`: `https://livecoding-backend.onrender.com`
   - `VITE_WS_BASE_URL`: `wss://livecoding-backend.onrender.com`
5. Click "Create Web Service"

#### Step 5: Update CORS

1. Go to backend service settings
2. Update `CORS_ORIGINS` environment variable:
   ```
   https://livecoding-frontend.onrender.com
   ```
   (replace with your actual frontend URL)
3. Save and redeploy

## Post-Deployment

### Verify Deployment

1. **Backend Health Check**
   ```bash
   curl https://livecoding-backend.onrender.com/health
   ```
   Should return: `{"status":"healthy"}`

2. **API Documentation**
   Visit: `https://livecoding-backend.onrender.com/docs`

3. **Frontend**
   Visit: `https://livecoding-frontend.onrender.com`

4. **Test Full Flow**
   - Login as interviewer
   - Create session
   - Join as candidate (open in incognito)
   - Test code execution
   - Complete session

### Monitor Services

- Check logs in Render dashboard for each service
- Monitor memory and CPU usage (free tier limits)
- Watch for cold starts (services sleep after 15 min inactivity on free tier)

## Important Notes

### Free Tier Limitations

- **Services sleep after 15 minutes** of inactivity
- Cold start takes **30-60 seconds**
- **750 hours/month** total across all services
- PostgreSQL: **90 days retention**, then deleted if inactive

### Production Recommendations

For production use, upgrade to paid plans:
- Backend: Starter plan ($7/month) - no sleep
- Database: Starter plan ($7/month) - persistent
- Frontend: Free static site is fine

## Troubleshooting

### Backend Won't Start

Check logs for:
- Database connection errors → verify DATABASE_URL
- Migration errors → run `alembic upgrade head` in shell
- Port binding → Render uses `$PORT` env variable (should be handled in code)

### Frontend Shows API Errors

- Verify `VITE_API_BASE_URL` is correct
- Check CORS settings in backend
- Ensure backend is running (not sleeping)

### WebSocket Connection Fails

- Verify `VITE_WS_BASE_URL` uses `wss://` (not `ws://`)
- Check backend logs for WebSocket errors
- Ensure Render plan supports WebSocket (all plans do)

### Database Migrations Failed

1. Connect to database via Shell:
   ```bash
   psql $DATABASE_URL
   ```

2. Check if tables exist:
   ```sql
   \dt
   ```

3. If empty, run migrations manually:
   ```bash
   alembic upgrade head
   ```

## Updating Deployment

### Auto-Deploy (Recommended)

Enable auto-deploy in service settings:
- Any push to `main`/`init` branch triggers deployment

### Manual Deploy

1. Push changes to GitHub
2. Go to Render service
3. Click "Manual Deploy" → "Deploy latest commit"

## Cost Estimate

**Free Tier:**
- Backend: Free (sleeps after 15 min)
- Frontend: Free (static site, always on)
- Database: Free (90 days, then deleted)
- **Total: $0/month**

**Recommended Production:**
- Backend: Starter ($7/month)
- Frontend: Free
- Database: Starter ($7/month)
- **Total: $14/month**

## Support

For Render-specific issues:
- https://render.com/docs
- https://community.render.com

For application issues:
- Check this repository's GitHub Issues
