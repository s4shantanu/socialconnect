# SocialConnect Project Setup & Testing Guide

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.8+ installed
- pip package manager
- Terminal/Command prompt

### 1. Project Setup (Already Done)
```bash
cd /Users/apple/Desktop/socialconnect
pip install -r requirements..txt
python3 manage.py makemigrations
python3 manage.py migrate
```

### 2. Create Admin User (Essential)
```bash
python3 manage.py createsuperuser
```
Enter:
- Username: admin
- Email: admin@example.com
- Password: admin123

### 3. Start Development Server
```bash
python3 manage.py runserver 8000
```

Your API will be available at: http://localhost:8000

## 🧪 Testing the API Step by Step

### Phase 1: Authentication Testing

#### 1.1 Register a New User
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser1",
    "email": "test1@example.com",
    "password": "securepass123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

Expected Response:
```json
{
  "user": {
    "username": "testuser1",
    "email": "test1@example.com",
    "first_name": "Test",
    "last_name": "User"
  },
  "message": "User created successfully. Please check your email for verification."
}
```

#### 1.2 Verify Email (Check Console)
Look at your terminal running the server. You'll see an email verification link like:
```
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: Verify your email
From: noreply@socialconnect.local
To: test1@example.com

Click here to verify your email: http://localhost:3000/verify-email?token=SOME_TOKEN
```

Extract the token and verify:
```bash
curl -X POST http://localhost:8000/api/auth/verify-email/ \
  -H "Content-Type: application/json" \
  -d '{"token": "YOUR_TOKEN_FROM_CONSOLE"}'
```

#### 1.3 Login to Get JWT Token
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser1",
    "password": "securepass123"
  }'
```

Expected Response:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "testuser1",
    "email": "test1@example.com",
    "first_name": "Test",
    "last_name": "User",
    "is_email_verified": true,
    "is_staff": false
  }
}
```

**⚠️ Important:** Copy the `access` token - you'll need it for authenticated requests!

### Phase 2: Profile Management

#### 2.1 Get Current User Profile
```bash
curl -X GET http://localhost:8000/api/users/me/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### 2.2 Update Profile
```bash
curl -X PUT http://localhost:8000/api/users/me/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "bio": "I love building APIs with Django!",
    "website": "https://testuser1.dev",
    "location": "San Francisco, CA",
    "visibility": "public"
  }'
```

### Phase 3: Content Creation

#### 3.1 Create a Post
```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "content": "Hello world! This is my first post on SocialConnect! 🚀",
    "category": "general"
  }'
```

#### 3.2 Get All Posts
```bash
curl -X GET http://localhost:8000/api/posts/
```

#### 3.3 Like a Post (use post ID from previous response)
```bash
curl -X POST http://localhost:8000/api/posts/1/like/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### 3.4 Add Comment to Post
```bash
curl -X POST http://localhost:8000/api/posts/1/comments/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{"content": "Great first post! Welcome to SocialConnect!"}'
```

### Phase 4: Social Features

#### 4.1 Register Another User (for testing follow feature)
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser2",
    "email": "test2@example.com",
    "password": "securepass123",
    "first_name": "Second",
    "last_name": "User"
  }'
```

#### 4.2 Follow Another User
```bash
curl -X POST http://localhost:8000/api/users/2/follow/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### 4.3 Get Personalized Feed
```bash
curl -X GET http://localhost:8000/api/feed/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### 4.4 Get Notifications
```bash
curl -X GET http://localhost:8000/api/notifications/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Phase 5: Admin Features (Use admin credentials)

#### 5.1 Login as Admin
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

#### 5.2 Get System Statistics
```bash
curl -X GET http://localhost:8000/api/admin/stats/ \
  -H "Authorization: Bearer YOUR_ADMIN_ACCESS_TOKEN"
```

#### 5.3 List All Users (Admin Only)
```bash
curl -X GET http://localhost:8000/api/admin/users/ \
  -H "Authorization: Bearer YOUR_ADMIN_ACCESS_TOKEN"
```

## 🎯 Success Checklist

- [ ] ✅ User registration works
- [ ] ✅ Email verification works  
- [ ] ✅ Login returns JWT tokens
- [ ] ✅ Profile creation and updates work
- [ ] ✅ Post creation works
- [ ] ✅ Like functionality works
- [ ] ✅ Comment system works
- [ ] ✅ Follow system works
- [ ] ✅ Feed shows followed users' posts
- [ ] ✅ Notifications are created
- [ ] ✅ Admin endpoints work

## 🔧 Troubleshooting

### Common Issues:

1. **Token Expired Error**
   - Use the refresh token endpoint to get a new access token

2. **Permission Denied**
   - Make sure you're using the correct access token
   - Check if your user has the required permissions

3. **User Not Active**
   - Make sure you verified the email after registration

4. **Import Errors**
   - Restart the Django server

### Useful Commands:
```bash
# Check server status
python3 manage.py check

# View database contents
python3 manage.py shell

# Create test data
python3 manage.py shell -c "
from api.models import User, Post
user = User.objects.create_user('testuser', 'test@example.com', 'password123')
user.is_active = True
user.is_email_verified = True
user.save()
Post.objects.create(content='Test post', author=user)
print('Test data created!')
"
```

## 🎉 You're All Set!

Your SocialConnect API is now fully functional with:
- ✅ 24 API endpoints
- ✅ JWT authentication
- ✅ Real-time notifications via signals
- ✅ Complete social media functionality
- ✅ Admin controls

Start testing and building your frontend! 🚀
