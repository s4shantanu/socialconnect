# SocialConnect Backend API

A comprehensive social media backend application built with Django REST Framework featuring user authentication, profile management, posts, social interactions, and admin controls.
Link - https://joyful-longma-488159.netlify.app/

## Features

### 🔐 Authentication System
- JWT-based authentication with access & refresh tokens
- User registration with email verification
- Login with email OR username
- Password reset functionality
- Secure logout with token blacklisting

### 👤 User Management
- User profiles with bio, avatar, website, location
- Privacy settings (public, private, followers_only)
- User statistics (followers, following, posts count)
- User search functionality

### 📝 Content Management
- Create, read, update, delete posts (280 char limit)
- Image upload support (JPEG/PNG, max 2MB)
- Post categories (general, announcement, question)
- Soft delete for posts

### 🤝 Social Features
- Follow/unfollow users
- Like/unlike posts
- Comment system (200 char limit)
- Personalized feed from followed users

### 🔔 Real-time Notifications
- Follow notifications
- Like notifications  
- Comment notifications
- Mark as read functionality
- Real-time updates using Django signals

### 👨‍💼 Admin Features
- User management (list, view, deactivate)
- Content moderation (delete any post)
- System statistics
- Admin-only endpoints

## API Endpoints

### Authentication
```
POST /api/auth/register/                    # User registration
POST /api/auth/verify-email/                # Email verification
POST /api/auth/login/                       # Login (email or username)
POST /api/auth/token/refresh/               # Refresh JWT token
POST /api/auth/change-password/             # Change password
POST /api/auth/password-reset/              # Request password reset
POST /api/auth/password-reset-confirm/      # Confirm password reset
POST /api/auth/logout/                      # Logout
```

### User Profiles
```
GET  /api/users/me/                         # Get current user profile
PUT  /api/users/me/                         # Update current user profile
GET  /api/users/{user_id}/                  # Get user profile by ID
GET  /api/users/                            # List users (with search)
```

### Posts
```
GET    /api/posts/                          # List all posts (paginated)
POST   /api/posts/                          # Create new post
GET    /api/posts/{post_id}/                # Get specific post
PUT    /api/posts/{post_id}/                # Update own post
DELETE /api/posts/{post_id}/                # Delete own post
POST   /api/posts/{post_id}/like/           # Like post
DELETE /api/posts/{post_id}/like/           # Unlike post
GET    /api/posts/{post_id}/like-status/    # Check if user liked post
GET    /api/posts/{post_id}/comments/       # Get post comments
POST   /api/posts/{post_id}/comments/       # Add comment to post
```

### Social Features
```
POST   /api/users/{user_id}/follow/         # Follow user
DELETE /api/users/{user_id}/follow/         # Unfollow user
GET    /api/users/{user_id}/followers/      # Get user followers
GET    /api/users/{user_id}/following/      # Get users being followed
GET    /api/feed/                           # Get personalized feed
```

### Comments
```
DELETE /api/comments/{comment_id}/          # Delete own comment
```

### Notifications
```
GET  /api/notifications/                    # Get user notifications
POST /api/notifications/{id}/read/          # Mark notification as read
POST /api/notifications/mark-all-read/      # Mark all as read
```

### Admin Only
```
GET    /api/admin/users/                    # List all users
GET    /api/admin/users/{user_id}/          # Get user details
POST   /api/admin/users/{user_id}/deactivate/ # Deactivate user
GET    /api/admin/posts/                    # List all posts
DELETE /api/admin/posts/{post_id}/          # Delete any post
GET    /api/admin/stats/                    # Get system statistics
```

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements..txt
   ```

2. **Database Setup**
   ```bash
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```

3. **Create Superuser**
   ```bash
   python3 manage.py createsuperuser
   ```

4. **Run Development Server**
   ```bash
   python3 manage.py runserver
   ```

## Configuration

### Environment Variables
- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (True/False)
- `FRONTEND_URL`: Frontend URL for email links
- `EMAIL_BACKEND`: Email backend configuration

### Media Files
- Avatar uploads: `/media/avatars/`
- Post images: `/media/posts/`
- Maximum file size: 2MB
- Supported formats: JPEG, PNG

## Models

### User
- Custom user model with email verification
- Username, email, first_name, last_name
- is_email_verified field

### Profile
- One-to-one with User
- bio (160 chars), avatar, website, location
- visibility settings
- Auto-created via Django signals

### Post
- content (280 chars), author, timestamps
- image upload, category, like/comment counts
- Soft delete with is_active field

### Follow
- follower, following relationship
- Unique constraint to prevent duplicates

### Comment
- content (200 chars), author, post
- Flat structure (no nested replies)

### Notification
- recipient, sender, type, message
- Real-time via Django signals

## Features Implemented

✅ JWT Authentication with refresh tokens  
✅ Email verification system  
✅ Password reset functionality  
✅ User profiles with privacy settings  
✅ Post creation with image upload  
✅ Social follow system  
✅ Like and comment functionality  
✅ Personalized feed (20 posts/page)  
✅ Real-time notifications via signals  
✅ Admin user and content management  
✅ Comprehensive API documentation  
✅ Input validation and error handling  
✅ Soft delete for posts and comments  

## Technology Stack

- **Backend**: Django 4.2 + Django REST Framework
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: SQLite (development)
- **File Upload**: Pillow for image processing
- **Real-time**: Django signals for notifications

## API Response Format

All API responses follow a consistent format:

**Success Response:**
```json
{
  "data": {...},
  "message": "Success message"
}
```

**Error Response:**
```json
{
  "error": "Error message",
  "details": {...}
}
```

**Paginated Response:**
```json
{
  "count": 100,
  "next": "http://api/endpoint/?page=2",
  "previous": null,
  "results": [...]
}
```
