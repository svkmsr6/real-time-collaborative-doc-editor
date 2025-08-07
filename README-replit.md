# Redis Document Management API - Replit Deployment

A RESTful API for managing JSON documents in Redis with full-text search capabilities, designed for deployment on Replit.

## 🚀 Quick Deploy to Replit

1. **Fork/Import this repository** to your Replit account
2. **Set up Redis Cloud** (free tier available)
3. **Configure environment variables** in Replit Secrets
4. **Run the application**

## 📋 Environment Setup

### Required Secrets in Replit:

```bash
RDS_HOST=your-redis-host.redis.cloud
RDS_PORT=6379
RDS_PASSWORD=your-redis-password
```

### Get Redis Cloud Credentials:
1. Go to [Redis Cloud](https://redis.com/try-free/)
2. Create a free account and database
3. Copy the host, port, and password to Replit Secrets

## 🔧 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` or `/health` | Health check |
| POST | `/docs` | Create new document |
| PUT | `/docs/{id}` | Update document |
| GET | `/docs/search?q=...` | Search documents |
| GET | `/docs/{id}/audit` | Get edit history |

## 📡 Features

- ✅ CORS enabled for web applications
- ✅ Full-text search with Redis Search
- ✅ Real-time updates via Pub/Sub
- ✅ Document change auditing
- ✅ JSON document storage
- ✅ Auto-scaling on Replit

## 🧪 Testing

Once deployed, test the health endpoint:
```bash
curl https://your-repl-name.your-username.repl.co/health
```

## 📚 Example Usage

### Create a document:
```bash
curl -X POST https://your-repl-name.your-username.repl.co/docs \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Doc", "body": "Content here"}'
```

### Search documents:
```bash
curl "https://your-repl-name.your-username.repl.co/docs/search?q=test"
```

## 🔗 Integration

This API works with any frontend framework:
- React/Vue/Angular applications
- Mobile apps
- Postman/API testing tools
- Swagger UI for documentation

## 📝 Notes

- Uses Redis Cloud for data persistence
- Optimized for Replit's environment
- Includes automatic dependency management
- Production-ready configuration
