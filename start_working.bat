@echo off
echo Working Word to PDF Converter
echo =============================

echo.
echo Starting converter...

REM Try different Python commands
python app_working.py 2>nul
if %errorlevel% equ 0 goto :success

python3 app_working.py 2>nul
if %errorlevel% equ 0 goto :success

py app_working.py 2>nul
if %errorlevel% equ 0 goto :success

py -3 app_working.py 2>nul
if %errorlevel% equ 0 goto :success

echo.
echo ❌ Python not found
echo.
echo Please install Python from: https://python.org/downloads
echo Make sure to check "Add Python to PATH"
echo.
pause
exit /b 1

:success
echo.
echo ✅ Application started successfully!
echo.
echo Open your browser and go to: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
pause
