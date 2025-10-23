# Word to PDF Converter

A Flask-based web application for converting Word documents (.doc/.docx) to PDF format, optimized for deployment on Render.com with Docker.

## Features

- ✅ Convert Word documents to PDF
- ✅ Support for .doc and .docx files  
- ✅ Multiple conversion methods (LibreOffice, WeasyPrint, docx2pdf)
- ✅ File size validation (max 16MB)
- ✅ Clean, responsive web interface
- ✅ Docker-ready for reliable deployment
- ✅ LibreOffice pre-installed in container

## Quick Start

### Local Development

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open `http://localhost:5000` in your browser

### Docker Deployment

1. Build the Docker image:
```bash
docker build -t word-to-pdf .
```

2. Run the container:
```bash
docker run -p 8000:8000 -e PORT=8000 word-to-pdf
```

## Render.com Deployment

1. Push your code to GitHub
2. Connect your repository to Render.com
3. Select "Docker" as the environment
4. Render will automatically detect the Dockerfile
5. Deploy!

**Build Command**: (Leave empty - Docker handles this)
**Start Command**: (Leave empty - Docker handles this)

## API Endpoints

- `GET /` - Main upload page
- `POST /convert` - Convert uploaded file
- `GET /health` - Health check with tool status
- `GET /debug` - Debug information

## Project Structure

```
word-to-pdf/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── render.yaml           # Render.com configuration
├── templates/
│   └── index.html        # Web interface
├── static/
│   └── style.css         # Styling
└── uploads/              # Temporary file storage
```

## Conversion Methods

The application tries multiple conversion methods in order:

1. **docx2pdf** - Best quality (requires Windows/Word)
2. **WeasyPrint** - Pure Python, works everywhere
3. **LibreOffice** - Reliable fallback (installed in Docker)

## Requirements

- Python 3.11+
- LibreOffice (installed via Dockerfile)
- Flask 2.3.3
- Gunicorn 23.0.0

## License

MIT License