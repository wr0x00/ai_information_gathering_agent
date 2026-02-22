@echo off
REM AI Information Gathering Agent - Startup Script for Windows

REM Check if we're running in a virtual environment
if "%VIRTUAL_ENV%"=="" (
    echo Warning: Not running in a virtual environment
) else (
    echo Running in virtual environment: %VIRTUAL_ENV%
)

REM Check if required files exist
if not exist "manage.py" (
    echo Error: manage.py not found. Please run this script from the project root directory.
    pause
    exit /b 1
)

REM Check if dependencies are installed
echo Checking dependencies...
python -c "import django" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Apply database migrations
echo Applying database migrations...
python manage.py migrate

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput

REM Start the Django development server
echo Starting Django development server...
echo Access the application at http://localhost:8080
python manage.py runserver 127.0.0.1:8080

pause
