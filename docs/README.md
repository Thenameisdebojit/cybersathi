# 🛡️ CyberSathi - Cybercrime Helpline Assistant

CyberSathi is an intelligent WhatsApp chatbot system designed to assist citizens in reporting cybercrimes and interfacing with India's National Cybercrime Reporting Portal (1930 Helpline).

## 🌟 Features

- **Multi-language Support**: English, Hindi, Odia, and more
- **Intelligent Complaint Registration**: NLP-powered form assistance
- **Real-time Tracking**: Track complaint status via reference ID
- **CyberPortal Integration**: Seamless submission to cybercrime.gov.in
- **WhatsApp Interface**: Accessible via WhatsApp for wide reach
- **Admin Dashboard**: Web-based management interface
- **Escalation Support**: Direct escalation to 1930 helpline

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  WhatsApp   │────▶│   Backend    │────▶│  CyberPortal    │
│   Users     │     │   (FastAPI)  │     │  (cybercrime.   │
└─────────────┘     └──────────────┘     │   gov.in)       │
                           │              └─────────────────┘
                           ▼
                    ┌──────────────┐
                    │  PostgreSQL  │
                    │   Database   │
                    └──────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   Rasa NLP   │
                    │    Engine    │
                    └──────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Docker Desktop (or Docker + Docker Compose)
- 4GB RAM minimum
- Ports 8000, 5173, 5432 available

### Installation

**Linux/Mac:**
```bash
git clone <repository-url>
cd CyberSathi
bash scripts/startup_complete.sh
```

**Windows:**
```cmd
git clone <repository-url>
cd CyberSathi
scripts\startup_complete.bat
```

### Verify Installation
```bash
bash scripts/verify_installation.sh
```

## 📡 Access Points

Once running, access these services:

- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Frontend Dashboard**: http://localhost:5173
- **PostgreSQL**: localhost:5432 (admin/admin123)

## 🔧 Development

### Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt
python -m app.main
```

### Frontend (React + Vite)
```bash
cd frontend
npm install
npm run dev
```

### Database
```bash
python scripts/db_migrate.py
```

## 📚 Documentation

- **[Setup Guide](SETUP_GUIDE.md)** - Detailed installation instructions
- **[Quick Reference](QUICK_REFERENCE.md)** - Common commands and API endpoints
- **[Troubleshooting](TROUBLESHOOTING.md)** - Solutions to common issues
- **[Architecture](docs/architecture.md)** - System design and components

## 🧪 Testing

### Run Backend Tests
```bash
cd backend
pytest
```

### Test API
```bash
curl http://localhost:8000/health
bash scripts/demo.sh
```

## 📝 API Examples

### Register a Complaint
```bash
curl -X POST http://localhost:8000/api/v1/complaints/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "phone": "+919999999999",
    "incident_type": "upi_scam",
    "description": "Lost money via UPI scam",
    "amount": 5000
  }'
```

### Track Complaint
```bash
curl http://localhost:8000/api/v1/tracking/{reference_id}
```

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM
- **PostgreSQL** - Primary database
- **Rasa** - NLP and dialogue management
- **JWT** - Authentication

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **React Router** - Navigation
- **Axios** - HTTP client

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Kubernetes/Helm** - Production deployment
- **Terraform** - Infrastructure as Code
- **GitHub Actions** - CI/CD

## 🔒 Security

- JWT-based authentication
- Secure password hashing
- CORS protection
- SQL injection prevention via ORM
- Input validation with Pydantic

## 🌐 Integration Points

### WhatsApp (Meta Cloud API / Twilio)
Configure in `backend/.env`:
```env
WHATSAPP_API_URL=https://graph.facebook.com/...
WHATSAPP_API_TOKEN=your_token_here
```

### CyberPortal API
```env
CYBERPORTAL_API_URL=https://cybercrime.gov.in/api
CYBERPORTAL_API_KEY=your_api_key
```

## 📊 Project Structure

```
CyberSathi/
├── backend/
│   ├── app/
│   │   ├── models/          # Data models
│   │   ├── routers/         # API endpoints
│   │   ├── services/        # Business logic
│   │   ├── config.py        # Configuration
│   │   └── main.py          # Application entry
│   ├── rasa/                # NLP models
│   ├── tests/               # Unit tests
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   └── services/        # API services
│   ├── package.json
│   └── vite.config.js
├── infra/
│   ├── docker-compose.yml   # Local deployment
│   ├── helm/                # Kubernetes charts
│   └── terraform/           # Cloud infrastructure
├── scripts/                 # Utility scripts
└── docs/                    # Documentation
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Known Issues

- Rasa integration is optional and can be disabled
- WhatsApp integration requires API credentials
- CyberPortal API mock mode is default (requires real credentials for production)

## 📞 Support

For issues and questions:
1. Check [Troubleshooting Guide](TROUBLESHOOTING.md)
2. Review logs: `docker-compose logs -f`
3. Run verification: `bash scripts/verify_installation.sh`
4. Open an issue on GitHub

## 📜 License

[Add your license here]

## 🙏 Acknowledgments

- Built to support India's National Cybercrime Reporting Portal
- Supports the 1930 Helpline initiative
- Designed for citizen accessibility and ease of use

## 🚧 Roadmap

- [ ] Advanced analytics dashboard
- [ ] Multi-tenancy support
- [ ] Mobile app (React Native)
- [ ] Voice complaint registration
- [ ] Integration with more regional languages
- [ ] Real-time notifications
- [ ] Export reports (PDF, Excel)

## 📈 Status

- ✅ Core API functionality
- ✅ Database integration
- ✅ Docker deployment
- ✅ Basic admin dashboard
- 🚧 WhatsApp integration (requires credentials)
- 🚧 Rasa NLP (optional component)
- 🚧 CyberPortal live integration (requires API access)

---

**Made with ❤️ for a safer digital India**