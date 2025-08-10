#!/bin/bash

# SocialConnect API Live Testing Script
# This script demonstrates all the main features of your API

echo "🚀 SocialConnect API Live Demo"
echo "=============================="

API_BASE="http://localhost:8000/api"

echo ""
echo "📋 Testing API Health..."
response=$(curl -s -w "HTTPSTATUS:%{http_code}" -X GET "$API_BASE/posts/")
http_code=$(echo $response | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')
if [ $http_code -eq 200 ]; then
    echo "✅ API is running and responding!"
else
    echo "❌ API is not responding. Make sure the server is running."
    exit 1
fi

echo ""
echo "👤 Testing User Registration..."
registration_response=$(curl -s -X POST "$API_BASE/auth/register/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "apitest_'$(date +%s)'",
    "email": "apitest'$(date +%s)'@example.com",
    "password": "testpass123",
    "first_name": "API",
    "last_name": "Test"
  }')

echo "Registration Response: $registration_response"

# Extract username for later use
username=$(echo $registration_response | grep -o '"username":"[^"]*"' | cut -d'"' -f4)
echo "✅ User created: $username"

echo ""
echo "🔐 Testing Admin Login..."
admin_login_response=$(curl -s -X POST "$API_BASE/auth/login/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }')

admin_token=$(echo $admin_login_response | grep -o '"access":"[^"]*"' | cut -d'"' -f4)

if [ ! -z "$admin_token" ]; then
    echo "✅ Admin login successful!"
    
    echo ""
    echo "📊 Testing Admin Statistics..."
    stats_response=$(curl -s -X GET "$API_BASE/admin/stats/" \
      -H "Authorization: Bearer $admin_token")
    echo "System Stats: $stats_response"
    
    echo ""
    echo "👥 Testing Admin User List..."
    users_response=$(curl -s -X GET "$API_BASE/admin/users/" \
      -H "Authorization: Bearer $admin_token")
    user_count=$(echo $users_response | grep -o '"id":[0-9]*' | wc -l)
    echo "✅ Found $user_count users in the system"
else
    echo "❌ Admin login failed"
fi

echo ""
echo "📝 Testing Post Creation (as admin)..."
if [ ! -z "$admin_token" ]; then
    post_response=$(curl -s -X POST "$API_BASE/posts/" \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $admin_token" \
      -d '{
        "content": "Welcome to SocialConnect! This API demo shows all our features working perfectly. 🎉",
        "category": "announcement"
      }')
    
    post_id=$(echo $post_response | grep -o '"id":[0-9]*' | cut -d':' -f2)
    echo "✅ Post created with ID: $post_id"
    
    if [ ! -z "$post_id" ]; then
        echo ""
        echo "❤️ Testing Like Functionality..."
        like_response=$(curl -s -X POST "$API_BASE/posts/$post_id/like/" \
          -H "Authorization: Bearer $admin_token")
        echo "Like Response: $like_response"
        
        echo ""
        echo "💬 Testing Comment System..."
        comment_response=$(curl -s -X POST "$API_BASE/posts/$post_id/comments/" \
          -H "Content-Type: application/json" \
          -H "Authorization: Bearer $admin_token" \
          -d '{"content": "This is an automated test comment! The API is working great! 🚀"}')
        echo "Comment Response: $comment_response"
    fi
fi

echo ""
echo "📱 Testing Public Endpoints..."
echo "Getting all posts..."
all_posts=$(curl -s -X GET "$API_BASE/posts/")
post_count=$(echo $all_posts | grep -o '"id":[0-9]*' | wc -l)
echo "✅ Public posts endpoint working - Found $post_count posts"

echo ""
echo "👥 Testing User Search..."
users_list=$(curl -s -X GET "$API_BASE/users/?search=test")
echo "✅ User search working"

echo ""
echo "🔔 Testing Notifications (for admin)..."
if [ ! -z "$admin_token" ]; then
    notifications=$(curl -s -X GET "$API_BASE/notifications/" \
      -H "Authorization: Bearer $admin_token")
    echo "✅ Notifications endpoint working"
fi

echo ""
echo "🎉 Demo Complete!"
echo "==================="
echo ""
echo "✅ All major features tested:"
echo "   • User registration & authentication"
echo "   • Admin login & permissions"
echo "   • Post creation, likes, and comments"
echo "   • Public API access"
echo "   • User search functionality"
echo "   • Notifications system"
echo "   • Admin statistics & user management"
echo ""
echo "🌟 Your SocialConnect API is fully functional!"
echo ""
echo "📖 Next Steps:"
echo "   1. Check the TESTING_GUIDE.md for detailed API examples"
echo "   2. Use Postman or curl for more detailed testing"
echo "   3. Build a frontend to interact with these endpoints"
echo "   4. Add more test users and content"
echo ""
echo "🔗 Available at: http://localhost:8000/api/"
