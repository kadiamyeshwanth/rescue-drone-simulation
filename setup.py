#!/usr/bin/env python3
"""
Setup script for Autonomous Search & Rescue Drone Simulation
Handles Python environment configuration and dependency installation
"""

import subprocess
import sys
import os
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def check_python_version():
    """Verify Python version is 3.8 or higher"""
    print_header("Checking Python Version")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required, you have {version.major}.{version.minor}")
        sys.exit(1)
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")

def create_virtual_environment():
    """Create virtual environment if it doesn't exist"""
    print_header("Setting Up Virtual Environment")
    
    venv_path = Path("venv")
    
    if venv_path.exists():
        print(f"✅ Virtual environment already exists at {venv_path}")
        return venv_path
    
    print("Creating virtual environment...")
    subprocess.check_call([sys.executable, "-m", "venv", str(venv_path)])
    print(f"✅ Virtual environment created at {venv_path}")
    
    return venv_path

def get_pip_executable(venv_path):
    """Get the pip executable for the virtual environment"""
    if sys.platform == "win32":
        return venv_path / "Scripts" / "pip.exe"
    else:
        return venv_path / "bin" / "pip"

def install_dependencies(venv_path):
    """Install Python dependencies"""
    print_header("Installing Dependencies")
    
    pip_exe = get_pip_executable(venv_path)
    
    print("Upgrading pip...")
    subprocess.check_call([str(pip_exe), "install", "--upgrade", "pip"])
    
    req_file = Path("requirements.txt")
    if not req_file.exists():
        print("❌ requirements.txt not found!")
        sys.exit(1)
    
    print("Installing packages from requirements.txt...")
    subprocess.check_call([str(pip_exe), "install", "-r", str(req_file)])
    
    print("✅ All dependencies installed!")

def download_yolo_model():
    """Pre-download YOLO model"""
    print_header("Downloading YOLOv8 Model")
    
    print("This may take a few minutes...")
    print("Downloading YOLOv8 Nano model...")
    
    try:
        subprocess.check_call([
            sys.executable, "-c",
            "from ultralytics import YOLO; YOLO('yolov8n.pt')"
        ])
        print("✅ YOLOv8 model downloaded successfully!")
    except subprocess.CalledProcessError:
        print("⚠️  Could not download YOLO model, will download on first run")

def print_next_steps():
    """Print next steps for user"""
    print_header("Setup Complete! 🎉")
    
    print("Next Steps:")
    print("\n1. Build Colosseum Simulator:")
    print("   cd Colosseum")
    print("   build.cmd")
    
    print("\n2. Create Unreal Project:")
    print("   - Open Epic Games Launcher")
    print("   - Create new project: Game > Blank > C++")
    print("   - Name it 'SARDroneSim'")
    
    print("\n3. Inject AirSim Plugin:")
    print("   xcopy Colosseum\\Unreal\\Plugins SARDroneSim\\Plugins /E /I /Y")
    
    print("\n4. Build and Run Unreal Project:")
    print("   cd SARDroneSim")
    print("   Start Visual Studio (F5)")
    
    print("\n5. Run the Python Script:")
    if sys.platform == "win32":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("   python search_and_rescue.py")
    
    print("\n" + "="*60)
    print("Documentation: See README.md for full setup guide")
    print("="*60 + "\n")

def main():
    """Main setup flow"""
    print_header("Search & Rescue Drone Simulation - Setup")
    
    try:
        # Step 1: Check Python
        check_python_version()
        
        # Step 2: Create venv
        venv_path = create_virtual_environment()
        
        # Step 3: Install dependencies
        install_dependencies(venv_path)
        
        # Step 4: Download YOLO model
        download_yolo_model()
        
        # Step 5: Print next steps
        print_next_steps()
        
        print("✅ Setup completed successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Setup failed with error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
