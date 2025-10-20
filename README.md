# Word to PDF Converter Tool

A secure, efficient, and fully functional Word to PDF Converter Tool built with Python Flask. This application allows users to upload Word (.doc/.docx) files, convert them to PDF on the server, and download the converted file.

## Features

- **Modern Web Interface**: Responsive design with drag-and-drop file upload
- **Secure Processing**: Files are processed securely and deleted immediately after conversion
- **Exact Format Preservation**: Maintains exact visual appearance including:
  - Font families, sizes, and colors
  - Text formatting (bold, italic, underline)
  - Paragraph alignment (left, center, right, justify)
  - Heading levels and styles
  - Table formatting and cell styling
  - Spacing and layout
- **File Validation**: Validates file type (.doc/.docx) and size (max 16MB)
- **Progress Indication**: Visual feedback during conversion process
- **Mobile Responsive**: Works perfectly on desktop, tablet, and mobile devices

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. **Clone or download the project files**

2. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Open your browser and navigate to:**
   ```
   http://localhost:5000
   ```

## Usage

1. **Upload File**: Drag and drop a Word document (.doc or .docx) onto the upload area, or click to browse and select a file.

2. **Convert**: Click the "Convert to PDF" button to start the conversion process.

3. **Download**: The converted PDF file will automatically download to your device.

## Enhanced Conversion Features

The enhanced converter now preserves the **exact visual appearance** of your Word documents:

### Text Formatting
- ✅ **Bold**, *italic*, and <u>underlined</u> text
- ✅ **Font families** and sizes
- ✅ **Text colors** and highlighting
- ✅ **Mixed formatting** within the same paragraph

### Layout and Structure
- ✅ **Paragraph alignment** (left, center, right, justify)
- ✅ **Heading levels** (H1-H6) with proper styling
- ✅ **Line spacing** and paragraph spacing
- ✅ **Page breaks** and section breaks

### Tables and Lists
- ✅ **Table formatting** with borders and cell styling
- ✅ **Cell content formatting** (bold, italic, colors)
- ✅ **Bullet points** and numbered lists
- ✅ **Nested lists** and indentation

### Advanced Features
- ✅ **Custom fonts** and font sizes
- ✅ **Text colors** and background colors
- ✅ **Character spacing** and kerning
- ✅ **Professional layout** preservation

## Supported File Types

- Microsoft Word 97-2003 (.doc)
- Microsoft Word 2007+ (.docx)
- Maximum file size: 16MB

## Technical Details

### Backend (Flask)
- **Framework**: Flask 2.3.3
- **File Processing**: python-docx for reading Word documents with full formatting extraction
- **PDF Generation**: WeasyPrint for high-quality HTML-to-PDF conversion
- **File Handling**: Secure file upload with validation
- **Format Preservation**: Advanced HTML/CSS rendering for exact visual reproduction

### Frontend
- **HTML5**: Modern semantic markup
- **CSS3**: Responsive design with custom styling
- **JavaScript**: Drag-and-drop functionality and progress indication
- **Bootstrap 5**: UI framework for responsive design

### Security Features
- File type validation
- File size limits
- Secure filename handling
- Automatic file cleanup
- No persistent storage of user files

## Project Structure

```
word_to_pdf/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   └── style.css         # Custom CSS styles
└── uploads/              # Temporary file storage (auto-created)
```

## API Endpoints

- `GET /` - Main page with upload form
- `POST /convert` - Handle file upload and conversion
- `GET /health` - Health check endpoint

## Error Handling

The application includes comprehensive error handling for:
- Invalid file types
- File size exceeded
- File processing errors
- PDF generation failures
- Network issues

## Browser Compatibility

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## Development

### Running in Development Mode

```bash
python app.py
```

The application will run in debug mode with auto-reload enabled.

### Production Deployment

For production deployment, consider using:
- Gunicorn or uWSGI as WSGI server
- Nginx as reverse proxy
- Environment variables for configuration
- Proper logging and monitoring

## License

This project is part of the Toolverse suite of tools.

## Support

For issues or questions, please contact the development team.

---

**Note**: This tool is designed for document conversion purposes. Always ensure you have the right to convert and distribute the documents you process.
