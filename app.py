import os
import tempfile
import uuid
from datetime import datetime
from flask import Flask, render_template, request, send_file, flash, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import subprocess
import shutil

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'doc', 'docx'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def find_libreoffice():
    """Find LibreOffice installation"""
    import platform
    
    system = platform.system().lower()
    
    if system == "windows":
        # Windows paths
        possible_paths = [
            r"C:\Program Files\LibreOffice\program\soffice.exe",
            r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
            r"C:\Program Files\LibreOffice\program\libreoffice.exe",
            r"C:\Program Files (x86)\LibreOffice\program\libreoffice.exe",
            "libreoffice",  # If in PATH
            "soffice"       # If in PATH
        ]
    else:
        # Linux/Unix paths (including Render.com)
        possible_paths = [
            "/usr/bin/libreoffice",
            "/usr/bin/soffice",
            "/usr/local/bin/libreoffice",
            "/usr/local/bin/soffice",
            "/opt/libreoffice/program/soffice",
            "/opt/libreoffice/program/libreoffice",
            "libreoffice",  # If in PATH
            "soffice"       # If in PATH
        ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
        elif shutil.which(path):
            return path
    
    return None

def convert_with_docx2pdf(input_path, output_path):
    """Convert using docx2pdf library"""
    try:
        from docx2pdf import convert
        print(f"Converting with docx2pdf: {input_path} -> {output_path}")
        
        convert(input_path, output_path)
        
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"✅ docx2pdf conversion successful! Size: {file_size:,} bytes")
            return True
        else:
            print("❌ docx2pdf conversion failed - no output file")
            return False
            
    except ImportError:
        print("❌ docx2pdf not available")
        return False
    except Exception as e:
        print(f"❌ docx2pdf conversion failed: {e}")
        return False

def convert_with_libreoffice(input_path, output_path):
    """Convert using LibreOffice"""
    try:
        libreoffice_path = find_libreoffice()
        
        if not libreoffice_path:
            print("❌ LibreOffice not found")
            return False
        
        print(f"Converting with LibreOffice: {input_path} -> {output_path}")
        print(f"Using LibreOffice at: {libreoffice_path}")
        
        # Get output directory
        output_dir = os.path.dirname(output_path)
        
        # Run LibreOffice command with Linux-compatible arguments
        cmd = [
            libreoffice_path,
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', output_dir,
            '--norestore',
            '--nofirststartwizard',
            '--nologo',
            input_path
        ]
        
        print(f"Running command: {' '.join(cmd)}")
        
        # Set environment variables for better compatibility
        env = os.environ.copy()
        env['HOME'] = '/tmp'  # Set HOME to writable directory
        env['USER'] = 'render'  # Set user for LibreOffice
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120, env=env)
        
        print(f"Return code: {result.returncode}")
        if result.stdout:
            print(f"stdout: {result.stdout}")
        if result.stderr:
            print(f"stderr: {result.stderr}")
        
        if result.returncode == 0:
            # LibreOffice creates PDF with same name as input
            input_name = os.path.splitext(os.path.basename(input_path))[0]
            libreoffice_output = os.path.join(output_dir, f"{input_name}.pdf")
            
            if os.path.exists(libreoffice_output):
                # Move to desired output path
                os.rename(libreoffice_output, output_path)
                file_size = os.path.getsize(output_path)
                print(f"✅ LibreOffice conversion successful! Size: {file_size:,} bytes")
                return True
            else:
                print("❌ LibreOffice conversion failed - no output file created")
                return False
        else:
            print(f"❌ LibreOffice conversion failed with return code {result.returncode}")
            return False
        
    except subprocess.TimeoutExpired:
        print("❌ LibreOffice conversion timed out")
        return False
    except Exception as e:
        print(f"❌ LibreOffice conversion failed: {e}")
        return False

def convert_word_to_pdf(input_path, output_path):
    """Convert Word document to PDF using available methods"""
    print(f"\n🚀 Starting conversion: {input_path} -> {output_path}")
    print("=" * 50)
    
    # Method 1: Try docx2pdf (best quality)
    print("\n1️⃣ Trying docx2pdf (Microsoft Word backend)...")
    if convert_with_docx2pdf(input_path, output_path):
        print("✅ Conversion successful with docx2pdf")
        return True
    
    # Method 2: Try LibreOffice
    print("\n2️⃣ Trying LibreOffice...")
    if convert_with_libreoffice(input_path, output_path):
        print("✅ Conversion successful with LibreOffice")
        return True
    
    print("\n❌ All conversion methods failed")
    return False

def check_conversion_tools():
    """Check which conversion tools are available"""
    tools = {
        'docx2pdf': False,
        'libreoffice': False
    }
    
    # Check docx2pdf
    try:
        import docx2pdf
        tools['docx2pdf'] = True
        print("✅ docx2pdf available")
    except ImportError:
        print("❌ docx2pdf not available")
    
    # Check LibreOffice
    libreoffice_path = find_libreoffice()
    if libreoffice_path:
        tools['libreoffice'] = True
        print(f"✅ LibreOffice available at: {libreoffice_path}")
    else:
        print("❌ LibreOffice not found")
    
    return tools

@app.route('/')
def index():
    """Main page with upload form"""
    tools = check_conversion_tools()
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_file():
    """Handle file upload and conversion"""
    try:
        print("\n" + "=" * 60)
        print("NEW CONVERSION REQUEST")
        print("=" * 60)
        
        # Check if file was uploaded
        if 'word_file' not in request.files:
            flash('No file selected', 'error')
            return redirect(url_for('index'))
        
        file = request.files['word_file']
        
        # Check if file is selected
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('index'))
        
        print(f"📁 File selected: {file.filename}")
        
        # Check file type and size
        if not allowed_file(file.filename):
            flash('Invalid file type. Please upload .doc or .docx files only.', 'error')
            return redirect(url_for('index'))
        
        # Check file size
        file.seek(0, 2)  # Seek to end
        file_size = file.tell()
        file.seek(0)  # Reset to beginning
        
        print(f"📏 File size: {file_size:,} bytes")
        
        if file_size > MAX_FILE_SIZE:
            flash('File too large. Maximum size is 16MB.', 'error')
            return redirect(url_for('index'))
        
        if file_size == 0:
            flash('File is empty. Please select a valid Word document.', 'error')
            return redirect(url_for('index'))
        
        if file and allowed_file(file.filename):
            # Generate unique filename
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
            
            print(f"💾 Saving file to: {file_path}")
            
            # Save uploaded file
            file.save(file_path)
            
            try:
                # Generate PDF filename
                pdf_filename = f"{os.path.splitext(filename)[0]}_converted.pdf"
                pdf_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_{pdf_filename}")
                
                print(f"📄 Target PDF: {pdf_filename}")
                
                # Convert using available methods
                if convert_word_to_pdf(file_path, pdf_path):
                    print("🎉 Conversion completed successfully!")
                    
                    # Clean up original file
                    os.remove(file_path)
                    
                    # Return PDF file
                    return send_file(
                        pdf_path,
                        as_attachment=True,
                        download_name=pdf_filename,
                        mimetype='application/pdf'
                    )
                else:
                    print("❌ All conversion methods failed")
                    flash('Conversion failed. Please check that Microsoft Word or LibreOffice is installed.', 'error')
                    return redirect(url_for('index'))
            
            except Exception as e:
                print(f"❌ Error during conversion: {e}")
                flash(f'Error processing file: {str(e)}', 'error')
                return redirect(url_for('index'))
            
            finally:
                # Clean up uploaded file
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"🧹 Cleaned up uploaded file: {file_path}")
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('index'))
    
    return redirect(url_for('index'))

@app.route('/health')
def health_check():
    """Health check endpoint"""
    tools = check_conversion_tools()
    return jsonify({
        'status': 'healthy', 
        'timestamp': datetime.now().isoformat(),
        'conversion_tools': tools
    })

if __name__ == '__main__':
    print("=" * 60)
    print("Working Word to PDF Converter")
    print("=" * 60)
    
    # Check available tools
    print("\n🔍 Checking available conversion tools...")
    tools = check_conversion_tools()
    
    print("\n📊 Tool Status Summary:")
    for tool, available in tools.items():
        status = "✅ Available" if available else "❌ Not available"
        print(f"  {tool}: {status}")
    
    working_tools = sum(tools.values())
    
    if working_tools == 0:
        print("\n⚠️  WARNING: No conversion tools available!")
        print("Please install Microsoft Word or LibreOffice")
    elif working_tools == 1:
        print(f"\n✅ {working_tools} conversion tool available")
    else:
        print(f"\n✅ {working_tools} conversion tools available - Excellent!")
    
    # Get port from environment variable (for Render.com) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    
    print("\n" + "=" * 60)
    print(f"🚀 Starting server on http://0.0.0.0:{port}")
    print(f"Debug mode: {debug_mode}")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
