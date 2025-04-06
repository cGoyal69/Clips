# Sound Clip API

A FastAPI backend for streaming sound clips with play tracking and metrics.

## Features

- **List Clips**: Get metadata for all available sound clips
- **Stream Clips**: Stream audio files with automatic play count tracking
- **Track Stats**: View play count statistics for each clip
- **Monitoring**: Prometheus metrics and Grafana dashboards
- **Database**: PostgreSQL for persistent storage
- **CI/CD**: GitHub Actions for testing and deployment

## Tech Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL
- **Monitoring**: Prometheus + Grafana
- **Deployment**: Render/Railway/Vercel

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.10+
- PostgreSQL (if running locally without Docker)

### Environment Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/sound-clip-api.git
   cd sound-clip-api
   ```

2. Create a `.env` file:
   ```
   DATABASE_URL=postgresql://postgres:postgres@postgres:5432/soundclip
   ```

3. Start services with Docker Compose:
   ```
   docker-compose up -d
   ```

4. Seed the database:
   ```
   docker-compose exec api python -m app.db.seed
   ```

### Running Locally (Without Docker)

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up PostgreSQL database and update `.env` with connection details.

4. Run the application:
   ```
   uvicorn app.main:app --reload
   ```

5. Seed the database:
   ```
   python -m app.db.seed
   ```

## API Documentation

Once running, API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Endpoints

- `GET /api/clips` - List all clips
- `GET /api/clips/{id}` - Get a specific clip
- `GET /api/clips/{id}/stream` - Stream a clip (increments play count)
- `GET /api/clips/{id}/stats` - Get play stats for a clip
- `POST /api/clips` - Add a new clip (optional)

## Monitoring

- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000` (default login: admin/password)

The Grafana dashboard shows:
- API request rates
- Response times
- Clip stream counts

## Deployment

This project can be deployed to:
- Render
- Railway
- Vercel Serverless Functions

### Deployment Process

1. Push your code to GitHub
2. Set up the service on your chosen platform
3. Configure environment variables including `DATABASE_URL`
4. Deploy (automated via GitHub Actions or manual)

## Development

### Running Tests

```
pytest
```

### Linting

```
flake8
```

## License

MIT