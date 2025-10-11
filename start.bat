@echo off
setlocal

REM Set Python version and installer URL
set PYTHON_VERSION=3.13.0
set PYTHON_INSTALLER_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-amd64.exe
set PYTHON_INSTALLER_FILENAME=python_installer.exe

REM Check for Python in PATH
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found in PATH.
    echo Downloading Python %PYTHON_VERSION%...
    powershell -Command "Invoke-WebRequest -Uri '%PYTHON_INSTALLER_URL%' -OutFile '%PYTHON_INSTALLER_FILENAME%'"
    if %errorlevel% neq 0 (
        echo Failed to download Python installer. Please check your internet connection.
        pause
        exit /b 1
    )

    echo Installing Python...
    start /wait %PYTHON_INSTALLER_FILENAME% /quiet InstallAllUsers=0 PrependPath=1
    del %PYTHON_INSTALLER_FILENAME%

    echo.
    echo Python installation complete.
    echo PLEASE RE-RUN THIS SCRIPT in a new command prompt to ensure Python is available in the PATH.
    echo.
    pause
    exit /b 0
) else (
    echo Python is already installed.
)

REM Check if uv is installed
uv --version >nul 2>&1
if %errorlevel% neq 0 (
    echo uv not found, installing/updating...
    pip install -U uv
) else (
    echo uv is already installed.
)

REM Check for virtual environment
if not exist .venv (
    echo Creating virtual environment with uv...
    uv .venv
)

REM Activate virtual environment, install dependencies, and run script
echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Installing dependencies from pyproject.toml...
uv sync

echo Running main.py...
python main.py

echo.
echo Script finished.
pause
endlocal
