# Todo App - Deployment Guide

## Frontend Deployment (Vercel)

This is a Next.js application that can be deployed directly to Vercel.

### Deploy to Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Hafsaa56/The-Evolution-of-Todo)

### Environment Variables

After deployment, you'll need to set the following environment variable in your Vercel project settings:

- `NEXT_PUBLIC_API_URL`: The URL of your deployed backend API (e.g., `https://your-backend-app.herokuapp.com`)

## Backend Deployment

The backend FastAPI application needs to be deployed separately. Here are some options:

### Option 1: Deploy to Render
1. Create an account at [Render](https://render.com)
2. Create a new Web Service
3. Connect to your GitHub repository
4. Set the build command: `pip install -r requirements.txt`
5. Set the start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Option 2: Deploy to Railway
1. Create an account at [Railway](https://railway.app)
2. Create a new project
3. Connect to your GitHub repository
4. Add your backend files to the deployment

## Architecture

- Frontend: Next.js (deployed on Vercel)
- Backend: FastAPI (deployed separately)
- Database: PostgreSQL (Neon.tech recommended)

## API Configuration

When both frontend and backend are deployed:

1. Deploy the backend and note the URL
2. Deploy the frontend to Vercel
3. In Vercel project settings, add the environment variable:
   - `NEXT_PUBLIC_API_URL` = your backend URL (e.g., `https://your-backend.onrender.com`)

## Important Notes

- The frontend makes API calls to `/api/` endpoints
- These need to be updated to point to your deployed backend
- CORS is configured to allow your frontend domain after deployment