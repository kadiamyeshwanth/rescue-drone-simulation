# Troubleshooting Guide - Search & Rescue Drone Simulation

## Common Issues and Solutions

---

## 1. Drone Connection Issues

### ❌ Error: "ConnectionRefusedError" or "Cannot connect to AirSim"

**Causes:**
- Unreal Engine is not running
- AirSim plugin not properly installed
- Wrong game mode selected

**Solutions:**
```bash
# Step 1: Verify Unreal is running
# - Start your SARDroneSim project in Unreal Editor
# - Press Play button (or ▶ in viewport)

# Step 2: Check Game Mode
# - Window > World Settings
# - Under "Game Mode Override" > select "AirSimGameMode"

# Step 3: Test connection directly
python -c "import airsim; client = airsim.MultirotorClient(); print('Connected!' if client.confirmConnection() else 'Failed')"
```

---

## 2. YOLO Model Issues

### ❌ Error: "ModuleNotFoundError: No module named 'ultralytics'"

**Solution:**
```bash
pip install ultralytics
```

### ❌ Error: "Cannot find YOLO model"

**Solution:**
```bash
# Pre-download the model
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"

# Or run setup script
python setup.py
```

### ❌ YOLOv8 runs very slowly

**Solution:**
- Using CPU instead of GPU (normal, will be slow)
- Install CUDA toolkit for GPU support:
  ```bash
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
  ```

---

## 3. Camera/Image Issues

### ❌ Error: "image_data_uint8 is None"

**Causes:**
- Camera not properly configured in Unreal
- No valid image being captured

**Solutions:**
```bash
# Check if your drone has a camera
# In Unreal: Select your drone pawn, check components
# Should have a Camera or CameraPawn component

# Try the simpler camera setup:
# Window > World Settings > Pawn Class
# Make sure it's set to a valid pawn with camera
```

### ❌ Black or corrupted images

**Solution:**
- Restart Unreal Engine
- Check image request parameters:
  ```python
  # In search_and_rescue.py, try:
  responses = client.simGetImages([
      airsim.ImageRequest(0, airsim.ImageType.Scene, False, False)
  ])
  ```

---

## 4. Visual Studio Build Issues

### ❌ Error: "build.cmd: The term is not recognized"

**Solution:**
```bash
# Must run from Developer Command Prompt for VS 2022, NOT PowerShell
# Or use full path:
"C:\Program Files (x86)\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat" x64
build.cmd
```

### ❌ Error: "Unreal Engine source not found"

**Solution:**
- Reinstall UE5.2 or 5.3 from Epic Games Launcher
- Make sure to select "Source Code" during installation

---

## 5. Python Virtual Environment Issues

### ❌ Error: "venv\Scripts\activate not found"

**Solution (Windows):**
```bash
# Create new venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Solution (Mac/Linux):**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### ❌ Wrong Python version in venv

**Solution:**
```bash
# Delete old venv and recreate
rmdir /s venv          # Windows
rm -rf venv            # Mac/Linux

python -m venv venv
```

---

## 6. Plugin Installation Issues

### ❌ Error: "AirSim plugin not found in project"

**Solution:**
```bash
# Make sure plugins folder exists
cd C:\Projects\SARDroneSim

# If not, copy from Colosseum
xcopy ..\Colosseum\Unreal\Plugins Plugins /E /I /Y

# Regenerate Visual Studio files
# Right-click SARDroneSim.uproject > Generate Visual Studio project files

# Rebuild in Visual Studio (F7)
```

### ❌ Compilation errors after plugin copy

**Solution:**
```bash
# In Visual Studio:
# 1. Build > Clean Solution
# 2. Build > Rebuild Solution
# 3. Or use:
del /Q Binaries
del /Q Intermediate
del /Q Saved
# Then F5 to rebuild
```

---

## 7. Disk Space Issues

### ❌ Error: "Insufficient disk space"

**What uses space:**
- Unreal Engine: ~30GB
- Visual Studio: ~15GB
- Colosseum build: ~20GB
- Intermediate files: ~50GB+

**Solution:**
- Ensure 150GB free space
- Clean build files:
  ```bash
  cd Colosseum
  clean.cmd
  ```

---

## 8. Performance Issues

### ⚠️ Drone moves slowly / simulator lags

**Causes:**
- CPU or GPU at 100%
- Insufficient RAM
- Many background apps

**Solutions:**
```bash
# Close unnecessary applications
# Run in lower quality mode:
# Unreal Editor > Settings > Engine > Rendering > Lower preview quality

# Or reduce search area in Python:
drone.search_mission(search_area_size=50)  # Smaller area
```

### ⚠️ Python script runs slowly

**Solution:**
```bash
# Use faster YOLO version:
# In search_and_rescue.py, change:
self.model = YOLO("yolov8n.pt")  # Already using nano (fastest)

# Or disable vision to test audio:
# Comment out: results = model(image)
```

---

## 9. Audio Sensor Not Working

### ❌ "Audio detection not working"

**Causes:**
- Victim actor not created
- Wrong actor name
- Wrong threshold distance

**Solutions:**
```bash
# In Unreal Editor:
# 1. Add a Mannequin or character to your map
# 2. In Details panel, rename it to: "VictimActor_1"
# 3. Place it somewhere in your search area

# Test distance threshold:
# In search_and_rescue.py, lower threshold:
heard_scream, distance = self.check_audio_sensor(
    drone_pos, 
    victim_name="VictimActor_1",
    threshold=50.0  # Increased from 15m
)
```

---

## 10. Mission Not Completing

### ❌ Script hangs or doesn't finish

**Solution:**
```bash
# Press Ctrl+C to interrupt

# Check what step it's stuck on:
# Look at the [INFO] messages in terminal

# Try simpler mission first:
drone.search_mission(search_area_size=20, altitude=10)

# Add timeout:
import signal
signal.alarm(300)  # 5 minute timeout
```

---

## 11. Git/GitHub Issues

### ❌ Error: "fatal: not a git repository"

**Solution:**
```bash
cd rescue-drone-simulation
git status
```

### ❌ Failed to push to GitHub

**Solution:**
```bash
# Check remote URL
git remote -v

# Set correct URL
git remote set-url origin https://github.com/yourusername/rescue-drone-simulation.git

# Try push again
git push origin main
```

---

## 12. Recording/Demo Issues

### ⚠️ Can't record screen properly

**Solution:**
Use OBS Studio (Free):
1. Download: https://obsproject.com/
2. Add sources: "Game Capture" for Unreal, "Window Capture" for Terminal
3. Start Recording
4. Run Python script

---

## Debug Mode

Enable detailed logging:

```python
# In search_and_rescue.py, add at top:
import logging
logging.basicConfig(level=logging.DEBUG)

# Run with debug output
python search_and_rescue.py 2>&1 | tee mission_log.txt
```

---

## Still Stuck?

1. **Check the terminal output** - read error messages carefully
2. **Check the Unreal output log** - Window > Output Log
3. **Search existing issues:**
   - [Colosseum Issues](https://github.com/CodexLabsLLC/Colosseum/issues)
   - [AirSim Issues](https://github.com/microsoft/AirSim/issues)
4. **Restart everything** - Unreal, Python, Visual Studio
5. **Try a fresh clone** - Sometimes files get corrupted

---

**Last Updated:** February 2025
