@echo off
REM Medical Knowledge Portal - Quick Setup Script (Windows)

echo.
echo 🏥 Medical Knowledge Portal Setup
echo ==================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8+
    exit /b 1
)

echo ✓ Python found

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements_enhanced.txt

REM Create .env file
if not exist .env (
    echo Creating .env file...
    copy .env.example_enhanced .env
    echo.
    echo ⚠️  IMPORTANT: Edit .env with your credentials:
    echo    - MongoDB URI
    echo    - Gmail SMTP password  
    echo    - Flask secret key
    echo.
    echo Then run: python app_enhanced.py
) else (
    echo ✓ .env file already exists
)

echo.
echo ✅ Setup complete!
echo.
echo Next steps:
echo 1. Edit .env with your credentials
echo 2. Run: python app_enhanced.py
echo 3. Visit: http://localhost:5000/register
echo.

pause
