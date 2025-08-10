# SocialConnect Deployment Guide

## 🌐 Backend Deployment Options (Django API)


### 1. **Heroku (Easiest for beginners)**
```bash
# Install Heroku CLI first, then:
pip install gunicorn
pip freeze > requirements.txt

# Create Procfile
echo "web: gunicorn socialconnect.wsgi --log-file -" > Procfile

# Create runtime.txt
echo "python-3.9.6" > runtime.txt

# Deploy
git add .
git commit -m "Deploy to Heroku"
heroku create your-socialconnect-api
heroku config:set DEBUG=False
heroku config:set SECRET_KEY='your-secret-key-here'
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### 2. **Railway (Modern alternative)**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway add
railway deploy
```

### 3. **Render (Free tier available)**
- Go to render.com
- Connect your GitHub repo
- Choose "Web Service"
- Set build command: `pip install -r requirements.txt`
- Set start command: `gunicorn socialconnect.wsgi:application`

### 4. **DigitalOcean App Platform**
- Upload your code to GitHub
- Connect to DigitalOcean App Platform
- Auto-detects Django and deploys

## 🎨 Frontend Deployment (For Netlify)

Create a React/Vue/Next.js frontend that consumes your API:

### React Frontend Example:
```bash
npx create-react-app socialconnect-frontend
cd socialconnect-frontend

# Install axios for API calls
npm install axios

# Build and deploy to Netlify
npm run build
# Upload dist/build folder to Netlify
```

## 🔧 Preparing Django for Production

### 1. Create production settings
