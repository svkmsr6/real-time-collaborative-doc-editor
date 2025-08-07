# Redis Document Management API

A RESTful API for managing JSON documents in Redis with full-text search capabilities using Redisearch. Features real-time updates via Pub/Sub and comprehensive document change auditing.

[![Deploy to Replit](https://replit.com/badge)](https://replit.com/github/your-username/redis-document-api)

## 🚀 Features

- ✅ **JSON Document Storage** - Store and manage flexible JSON documents
- ✅ **Full-Text Search** - Powered by Redis Search with wildcards and phrase matching
- ✅ **Real-Time Updates** - Pub/Sub notifications for document changes
- ✅ **Audit Trail** - Complete edit history using Redis Streams
- ✅ **CORS Enabled** - Ready for web application integration
- ✅ **RESTful API** - Clean, predictable endpoints
- ✅ **Cloud Ready** - Optimized for Redis Cloud and Replit deployment

## 📋 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` or `/health` | Health check and API info |
| POST | `/docs` | Create new document |
| PUT | `/docs/{id}` | Update existing document |
| GET | `/docs/search?q=...` | Search documents |
| GET | `/docs/{id}/audit` | Get document edit history |

## 🛠 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/redis-document-api.git
   cd redis-document-api
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv redis-docenv
   # Windows
   redis-docenv\Scripts\activate
   # Mac/Linux
   source redis-docenv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your Redis credentials
   ```

5. **Run the application**
   ```bash
   python start_server.py
   ```

### Deploy to Replit

1. **Import from GitHub**
   - Go to [Replit](https://replit.com)
   - Click "Create Repl" → "Import from GitHub"
   - Enter this repository URL

2. **Set up Redis Cloud**
   - Create account at [Redis Cloud](https://redis.com/try-free/)
   - Create a free database
   - Note the connection details

3. **Configure Secrets in Replit**
   ```
   RDS_HOST=your-redis-host.redis.cloud
   RDS_PORT=6379
   RDS_PASSWORD=your-redis-password
   ```

4. **Run the app**
   - Replit will automatically start with `main.py`
   - Your API will be live at your Replit URL

## 📚 Usage Examples

### Create a Document
```bash
curl -X POST https://your-api-url.com/docs \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Meeting Notes",
    "body": "Discussed project timeline and deliverables",
    "author": "John Doe",
    "tags": ["meeting", "project"]
  }'
```

Response:
```json
{"doc_id": 1}
```

### Search Documents
```bash
curl "https://your-api-url.com/docs/search?q=meeting"
```

Response:
```json
[
  {
    "title": "Meeting Notes",
    "body": "Discussed project timeline and deliverables",
    "author": "John Doe",
    "tags": ["meeting", "project"]
  }
]
```

### Update a Document
```bash
curl -X PUT https://your-api-url.com/docs/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Meeting Notes - Updated",
    "body": "Updated discussion about project timeline",
    "author": "John Doe",
    "status": "reviewed"
  }'
```

### Get Audit History
```bash
curl "https://your-api-url.com/docs/1/audit"
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `RDS_HOST` | Redis server hostname | `localhost` |
| `RDS_PORT` | Redis server port | `6379` |
| `RDS_PASSWORD` | Redis password | `""` |
| `FLASK_ENV` | Flask environment | `development` |
| `PORT` | Server port (Replit auto-sets) | `5000` |

### Redis Requirements

- Redis with JSON module (Redis Stack or Redis Cloud)
- Redis Search module for full-text search
- Redis Streams for audit logging

## 📖 API Documentation

Full OpenAPI 3.0 documentation is available:
- **Swagger YAML**: [`swagger.yaml`](./swagger.yaml)
- **Swagger JSON**: [`swagger.json`](./swagger.json)
- **Interactive Docs**: Import the Swagger file into [Swagger Editor](https://editor.swagger.io/)

## 🏗 Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Client    │    │   Mobile App    │    │   Backend API   │
│                 │    │                 │    │                 │
└─────┬───────────┘    └─────┬───────────┘    └─────┬───────────┘
      │                      │                      │
      └──────────────────────┼──────────────────────┘
                             │
                   ┌─────────▼─────────┐
                   │  Flask API Server │
                   │  (CORS Enabled)   │
                   └─────────┬─────────┘
                             │
                   ┌─────────▼─────────┐
                   │   Redis Cloud     │
                   │ ┌───────────────┐ │
                   │ │ JSON Storage  │ │
                   │ │ Search Index  │ │
                   │ │ Pub/Sub       │ │
                   │ │ Streams       │ │
                   │ └───────────────┘ │
                   └───────────────────┘
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/your-username/redis-document-api/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/redis-document-api/discussions)
- **Redis Cloud Support**: [Redis Support](https://redis.com/support/)

## 🔗 Related Links

- [Redis JSON Documentation](https://redis.io/docs/data-types/json/)
- [Redis Search Documentation](https://redis.io/docs/interact/search-and-query/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Replit Documentation](https://docs.replit.com/)
