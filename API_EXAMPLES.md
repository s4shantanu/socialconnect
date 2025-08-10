# API Testing Examples

Here are some example API requests you can test with curl or Postman:

## Authentication

### 1. Register a new user
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe", 
    "email": "john@example.com",
    "password": "securepass123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### 2. Verify email (use token from email/console)
```bash
curl -X POST http://localhost:8000/api/auth/verify-email/ \
  -H "Content-Type: application/json" \
  -d '{"token": "YOUR_EMAIL_TOKEN_HERE"}'
```

### 3. Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepass123"
  }'
```

### 4. Login with email
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com", 
    "password": "securepass123"
  }'
```

### 5. Password reset request
```bash
curl -X POST http://localhost:8000/api/auth/password-reset/ \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com"}'
```

### 6. Password reset confirm
```bash
curl -X POST http://localhost:8000/api/auth/password-reset-confirm/ \
  -H "Content-Type: application/json" \
  -d '{
    "token": "YOUR_RESET_TOKEN_HERE",
    "new_password": "newpassword123"
  }'
```

## Posts

### 7. Get all posts (public)
```bash
curl -X GET http://localhost:8000/api/posts/
```

### 8. Create a post (requires auth)
```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "content": "This is my first post!",
    "category": "general"
  }'
```

### 9. Like a post
```bash
curl -X POST http://localhost:8000/api/posts/1/like/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 10. Add comment to post
```bash
curl -X POST http://localhost:8000/api/posts/1/comments/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{"content": "Great post!"}'
```

## Users & Profiles

### 11. Get current user profile
```bash
curl -X GET http://localhost:8000/api/users/me/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 12. Update profile
```bash
curl -X PUT http://localhost:8000/api/users/me/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "bio": "Software developer passionate about Python!",
    "website": "https://johndoe.dev",
    "location": "San Francisco, CA"
  }'
```

### 13. Follow a user
```bash
curl -X POST http://localhost:8000/api/users/2/follow/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 14. Get personalized feed
```bash
curl -X GET http://localhost:8000/api/feed/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Notifications

### 15. Get notifications
```bash
curl -X GET http://localhost:8000/api/notifications/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 16. Mark notification as read
```bash
curl -X POST http://localhost:8000/api/notifications/1/read/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Admin (requires admin user)

### 17. Get system stats
```bash
curl -X GET http://localhost:8000/api/admin/stats/ \
  -H "Authorization: Bearer YOUR_ADMIN_ACCESS_TOKEN"
```

### 18. List all users
```bash
curl -X GET http://localhost:8000/api/admin/users/ \
  -H "Authorization: Bearer YOUR_ADMIN_ACCESS_TOKEN"
```

## Image Upload Example

### 19. Create post with image
```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "content=Check out this photo!" \
  -F "category=general" \
  -F "image=@/path/to/your/image.jpg"
```

## Error Responses

All endpoints return consistent error responses:

```json
{
  "error": "Error message here",
  "detail": "Additional details if available"
}
```

## Authentication Notes

1. After registration, check your console for email verification link
2. Access tokens expire in 8 hours
3. Refresh tokens expire in 7 days  
4. Include `Authorization: Bearer YOUR_TOKEN` in all authenticated requests
5. Use refresh endpoint to get new access tokens

## Testing Workflow

1. Register a user
2. Verify email (check console output)
3. Login to get access token
4. Create some posts
5. Follow other users
6. Check your personalized feed
7. Test notifications by liking/commenting

## File Upload Limits

- Maximum file size: 2MB
- Supported formats: JPEG, PNG
- Files uploaded to `/media/posts/` for posts, `/media/avatars/` for profiles
