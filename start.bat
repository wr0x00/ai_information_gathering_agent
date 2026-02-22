@echo off
REM AI Information Gathering Agent Startup Script for Windows

setlocal enabledelayedexpansion

REM Colors for output (using PowerShell for colored output)
set "GREEN=[92m"
set "YELLOW=[93m"
set "RED=[91m"
set "NC=[0m"

REM Function to print colored output
goto :print_status
:print_status
echo %GREEN%[INFO]%NC% %~1
exit /b

goto :print_warning
:print_warning
echo %YELLOW%[WARNING]%NC% %~1
exit /b

goto :print_error
:print_error
echo %RED%[ERROR]%NC% %~1
exit /b

REM Check if we're in the correct directory
if not exist "manage.py" if not exist "django_ai_agent" (
    call :print_error "This script must be run from the project root directory"
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    call :print_warning "Virtual environment not found. Creating one..."
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install --upgrade pip
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

REM Check if Node.js dependencies are installed
if not exist "node_modules" (
    call :print_warning "Node.js dependencies not found. Installing..."
    npm install
)

REM Build frontend
call :print_status "Building frontend..."
npm run build

REM Check if database migrations are needed
call :print_status "Checking database migrations..."
python django_ai_agent\manage.py makemigrations --check --dry-run >nul 2>&1
if %errorlevel% neq 0 (
    call :print_warning "Database migrations needed. Applying migrations..."
    python django_ai_agent\manage.py migrate
) else (
    call :print_status "Database is up to date."
)

REM Collect static files
call :print_status "Collecting static files..."
python django_ai_agent\manage.py collectstatic --noinput -c

REM Start the development server
call :print_status "Starting development server..."
call :print_status "Access the application at http://localhost:8000"
python django_ai_agent\manage.py runserver 0.0.0.0:8000

pause
