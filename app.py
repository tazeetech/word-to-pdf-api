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
    """Find LibreOffice installation with enhanced debugging"""
    import platform
    import subprocess
    
    system = platform.system().lower()
    print(f"🔍 Detecting LibreOffice on {system} system...")
    
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
            "/snap/bin/libreoffice",  # Snap package
            "libreoffice",  # If in PATH
            "soffice"       # If in PATH
        ]
    
    print(f"🔍 Checking {len(possible_paths)} possible LibreOffice paths...")
    
    for i, path in enumerate(possible_paths, 1):
        print(f"  {i}. Checking: {path}")
        
        if os.path.exists(path):
            print(f"    ✅ Found at: {path}")
            return path
        elif shutil.which(path):
            print(f"    ✅ Found in PATH: {path}")
            return path
        else:
            print(f"    ❌ Not found")
    
    # Additional debugging for Render.com
    print("🔍 Additional debugging for Render.com...")
    
    # Check if we can run libreoffice directly
    try:
        result = subprocess.run(['which', 'libreoffice'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0 and result.stdout.strip():
            libreoffice_path = result.stdout.strip()
            print(f"✅ Found via 'which libreoffice': {libreoffice_path}")
            return libreoffice_path
    except Exception as e:
        print(f"❌ 'which libreoffice' failed: {e}")
    
    # Check if we can run soffice directly
    try:
        result = subprocess.run(['which', 'soffice'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0 and result.stdout.strip():
            soffice_path = result.stdout.strip()
            print(f"✅ Found via 'which soffice': {soffice_path}")
            return soffice_path
    except Exception as e:
        print(f"❌ 'which soffice' failed: {e}")
    
    # List all files in common LibreOffice directories
    common_dirs = ['/usr/bin', '/usr/local/bin', '/opt/libreoffice/program']
    for dir_path in common_dirs:
        if os.path.exists(dir_path):
            print(f"🔍 Contents of {dir_path}:")
            try:
                files = os.listdir(dir_path)
                libreoffice_files = [f for f in files if 'libre' in f.lower() or 'office' in f.lower()]
                if libreoffice_files:
                    print(f"    Found LibreOffice files: {libreoffice_files}")
                else:
                    print(f"    No LibreOffice files found")
            except Exception as e:
                print(f"    Error listing directory: {e}")
    
    print("❌ LibreOffice not found in any expected location")
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

def convert_with_weasyprint(input_path, output_path):
    """Convert using WeasyPrint (currently disabled to avoid dependency issues)"""
    print("❌ WeasyPrint temporarily disabled to avoid dependency conflicts")
    print("💡 Using LibreOffice as primary conversion method")
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
    
    # Method 1: Try LibreOffice (primary method - best quality and reliability)
    print("\n1️⃣ Trying LibreOffice (primary conversion method)...")
    if convert_with_libreoffice(input_path, output_path):
        print("✅ Conversion successful with LibreOffice")
        return True
    
    # Method 2: Try WeasyPrint (fallback - pure Python)
    print("\n2️⃣ Trying WeasyPrint (fallback method)...")
    if convert_with_weasyprint(input_path, output_path):
        print("✅ Conversion successful with WeasyPrint")
        return True
    
    # Method 3: Try docx2pdf (fallback - requires Windows/Word)
    print("\n3️⃣ Trying docx2pdf (fallback method)...")
    if convert_with_docx2pdf(input_path, output_path):
        print("✅ Conversion successful with docx2pdf")
        return True
    
    print("\n❌ All conversion methods failed")
    print("💡 Tip: Check /debug endpoint for detailed troubleshooting information")
    return False

def check_conversion_tools():
    """Check which conversion tools are available"""
    tools = {
        'libreoffice': False,
        'weasyprint': False,
        'docx2pdf': False
    }
    
    # Check LibreOffice (primary method)
    libreoffice_path = find_libreoffice()
    if libreoffice_path:
        tools['libreoffice'] = True
        print(f"✅ LibreOffice available at: {libreoffice_path}")
    else:
        print("❌ LibreOffice not found")
    
    # Check WeasyPrint (currently disabled)
    tools['weasyprint'] = False
    print("❌ WeasyPrint temporarily disabled to avoid dependency conflicts")
    
    # Check docx2pdf (fallback method)
    try:
        import docx2pdf
        tools['docx2pdf'] = True
        print("✅ docx2pdf available")
    except ImportError:
        print("❌ docx2pdf not available")
    
    return tools

@app.route('/')
def index():
    """Main page with upload form"""
    try:
        tools = check_conversion_tools()
    except Exception as e:
        print(f"Error checking conversion tools: {e}")
        tools = {'libreoffice': False, 'weasyprint': False, 'docx2pdf': False}
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
    try:
        tools = check_conversion_tools()
        return jsonify({
            'status': 'healthy', 
            'timestamp': datetime.now().isoformat(),
            'conversion_tools': tools
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'timestamp': datetime.now().isoformat(),
            'error': str(e),
            'conversion_tools': {'libreoffice': False, 'weasyprint': False, 'docx2pdf': False}
        }), 500

@app.route('/debug')
def debug_info():
    """Debug endpoint to troubleshoot LibreOffice issues"""
    try:
        import platform
        import subprocess
        
        debug_info = {
            'system': platform.system(),
            'platform': platform.platform(),
            'python_version': platform.python_version(),
            'libreoffice_detection': {},
            'environment': {},
            'file_system': {}
        }
    
    # LibreOffice detection details
    libreoffice_path = find_libreoffice()
    debug_info['libreoffice_detection'] = {
        'found_path': libreoffice_path,
        'exists': os.path.exists(libreoffice_path) if libreoffice_path else False,
        'is_executable': os.access(libreoffice_path, os.X_OK) if libreoffice_path else False
    }
    
    # Environment variables
    debug_info['environment'] = {
        'PATH': os.environ.get('PATH', 'Not set'),
        'HOME': os.environ.get('HOME', 'Not set'),
        'USER': os.environ.get('USER', 'Not set'),
        'PORT': os.environ.get('PORT', 'Not set')
    }
    
    # File system checks
    common_paths = ['/usr/bin', '/usr/local/bin', '/opt/libreoffice/program']
    debug_info['file_system'] = {}
    
    for path in common_paths:
        if os.path.exists(path):
            try:
                files = os.listdir(path)
                libreoffice_files = [f for f in files if 'libre' in f.lower() or 'office' in f.lower()]
                debug_info['file_system'][path] = {
                    'exists': True,
                    'libreoffice_files': libreoffice_files,
                    'all_files_count': len(files)
                }
            except Exception as e:
                debug_info['file_system'][path] = {
                    'exists': True,
                    'error': str(e)
                }
        else:
            debug_info['file_system'][path] = {'exists': False}
    
    # Try to run LibreOffice commands
    try:
        result = subprocess.run(['which', 'libreoffice'], capture_output=True, text=True, timeout=5)
        debug_info['which_libreoffice'] = {
            'returncode': result.returncode,
            'stdout': result.stdout.strip(),
            'stderr': result.stderr.strip()
        }
    except Exception as e:
        debug_info['which_libreoffice'] = {'error': str(e)}
    
    try:
        result = subprocess.run(['which', 'soffice'], capture_output=True, text=True, timeout=5)
        debug_info['which_soffice'] = {
            'returncode': result.returncode,
            'stdout': result.stdout.strip(),
            'stderr': result.stderr.strip()
        }
    except Exception as e:
        debug_info['which_soffice'] = {'error': str(e)}
    
    return jsonify(debug_info)
    except Exception as e:
        return jsonify({
            'error': f'Debug endpoint failed: {str(e)}',
            'system': 'Unknown',
            'platform': 'Unknown',
            'python_version': 'Unknown'
        }), 500


if __name__ == '__main__':
    print("=" * 60)
    print("Word to PDF Converter")
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
        print("LibreOffice should be installed via Docker")
    elif working_tools == 1:
        print(f"\n✅ {working_tools} conversion tool available")
    else:
        print(f"\n✅ {working_tools} conversion tools available - Excellent!")
    
    # Check if LibreOffice is available (primary method)
    if tools.get('libreoffice', False):
        print("\n🎯 LibreOffice is ready - Primary conversion method active!")
    else:
        print("\n⚠️  LibreOffice not available - Using fallback methods")
    
    # Get port from environment variable (for Render.com) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    
    print("\n" + "=" * 60)
    print(f"🚀 Starting server on http://0.0.0.0:{port}")
    print(f"Debug mode: {debug_mode}")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
