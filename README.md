# Content Recommender System

Sistem rekomendasi konten untuk kreator menggunakan TF-IDF dan Cosine Similarity.

## 📋 Features

- ✅ Sistem rekomendasi berbasis TF-IDF & Cosine Similarity
- ✅ Support 3 platform: YouTube, TikTok, Instagram
- ✅ User authentication (JWT)
- ✅ Favorites management
- ✅ Activity logging
- ✅ RESTful API
- ✅ Docker support
- ✅ Modular architecture

## 🛠️ Tech Stack

**Backend:**
- Python 3.10
- Flask 3.0
- MySQL 8.0
- scikit-learn (TF-IDF)
- JWT Authentication

**Frontend:**
- HTML5
- Tailwind CSS
- Vanilla JavaScript

**DevOps:**
- Docker & Docker Compose
- Gunicorn (Production server)

## 📁 Project Structure
```
content-recommender/
├── backend/              # Backend package
│   ├── api/             # API routes
│   ├── core/            # Business logic
│   ├── models/          # Database models
│   ├── middleware/      # Middleware
│   ├── config/          # Configuration
│   └── utils/           # Utilities
├── frontend/            # Frontend files
├── tests/               # Unit tests
├── data/                # Dataset
├── docs/                # Documentation
└── scripts/             # Utility scripts
```

## 🚀 Installation

### Local Development

1. **Clone repository**
```bash
   git clone <repository-url>
   cd content-recommender
```

2. **Create virtual environment**
```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
```

3. **Install dependencies**
```bash
   pip install -r requirements/development.txt
   pip install -e .
```

4. **Setup environment variables**
```bash
   cp .env.example .env
   # Edit .env with your configuration
```

5. **Setup database**
```bash
   mysql -u root -p < scripts/setup_database.sql
```

6. **Run application**
```bash
   python backend/app.py
```

### Docker Deployment

1. **Build and run with Docker Compose**
```bash
   docker-compose up -d
```

2. **Check logs**
```bash
   docker-compose logs -f backend
```

3. **Stop services**
```bash
   docker-compose down
```

## 📡 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user

### Recommendations
- `POST /api/recommend/` - Get recommendations (requires auth)

### Favorites
- `GET /api/favorites/` - Get user favorites (requires auth)
- `POST /api/favorites/` - Add to favorites (requires auth)
- `DELETE /api/favorites/<id>` - Remove from favorites (requires auth)

## 🧪 Testing
```bash
# Run tests
pytest

# Run with coverage
pytest --cov=backend tests/

# Run specific test
pytest tests/test_recommender.py
```

## 📦 Import Data
```bash
python scripts/import_data.py
```

## 👥 Authors

- Your Name - Initial work

## 📄 License

This project is licensed under the MIT License.