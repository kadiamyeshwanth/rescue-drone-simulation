#!/usr/bin/env cmd
REM Quick Setup Script for Windows
REM Run this first to set up Python environment

@echo off
echo.
echo ========================================
echo Search & Rescue Drone Simulation - Setup
echo ========================================
echo.

REM Check Python
echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found! Install from https://python.org
    pause
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created!
) else (
    echo Virtual environment already exists
)

REM Activate venv
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Download YOLO model
echo Downloading YOLOv8 model (this may take a minute)...
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Open Colosseum\build.cmd to build the simulator
echo 2. Create a C++ Unreal Engine 5 project
echo 3. Copy Colosseum\Unreal\Plugins to your project
echo 4. Run: python search_and_rescue.py
echo.
echo For detailed guide, see README.md
echo.
pause
