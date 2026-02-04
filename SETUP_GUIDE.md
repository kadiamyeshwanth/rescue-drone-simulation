# SETUP GUIDE - Autonomous Search & Rescue Drone Simulation

## ⚡ Quick Setup (15 minutes)

### For Experienced Developers:

```bash
# 1. Install dependencies
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# 2. Build Colosseum
cd Colosseum
build.cmd
cd ..

# 3. Download YOLOv8
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"

# 4. Run tests
python -c "import airsim; print('✅ AirSim OK')"
python -c "from ultralytics import YOLO; print('✅ YOLO OK')"
```

---

## 📋 Full Step-by-Step Setup

### **Phase 1: System Prerequisites** (30 minutes)

#### Windows Installation

1. **Visual Studio 2022**
   ```
   - Download: https://visualstudio.microsoft.com/
   - Run installer
   - ✅ Check "Desktop development with C++"
   - ✅ Check "Windows 10 SDK" (17763+)
   - Click Install (takes ~20 minutes)
   ```

2. **Unreal Engine 5.2+**
   ```
   - Go: https://www.unrealengine.com/
   - Download Epic Games Launcher
   - Sign in / Create account
   - Click "Unreal Engine" tab
   - Click "Install Engine"
   - Select version 5.2 or 5.3
   - Click Install (takes ~30 minutes, 30GB)
   ```

3. **Python 3.8+**
   ```
   - Download: https://www.python.org/downloads/
   - Run installer
   - ✅ Check "Add Python to PATH"
   - Click Install
   - Verify: python --version
   ```

---

### **Phase 2: Build the Simulator** (30-60 minutes)

#### Open Developer Command Prompt

**Windows:**
- Press `Win + X` → Select "Terminal (Admin)"
- Or: Press `Win` → Type "Native Tools" → Open "x64 Native Tools Command Prompt for VS 2022"

#### Build Colosseum

```bash
# Navigate to project
cd C:\Users\kadia\OneDrive\Documents\Github\rescue-drone-simulation

# Build (takes 30-60 minutes first time)
cd Colosseum
build.cmd
```

**Wait for completion.** You'll see:
```
...
Build succeeded!
Output: C:\...\..\build\windows\cmake\AirLib\Release\AirLib.lib
...
```

---

### **Phase 3: Setup Python Environment** (10 minutes)

#### Create Virtual Environment

```bash
# From project root
cd C:\Users\kadia\OneDrive\Documents\Github\rescue-drone-simulation

# Create venv
python -m venv venv

# Activate (IMPORTANT - do this every new terminal!)
venv\Scripts\activate

# You should see (venv) at the start of your prompt
```

#### Install Dependencies

```bash
# Make sure venv is activated!
pip install --upgrade pip

# Install all packages
pip install -r requirements.txt

# Download YOLOv8 model (200MB)
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

**Verify installation:**
```bash
python -c "import airsim; print('✅ AirSim')"
python -c "from ultralytics import YOLO; print('✅ YOLO')"
python -c "import cv2; print('✅ OpenCV')"
python -c "import numpy; print('✅ NumPy')"
```

---

### **Phase 4: Create Unreal Project** (20 minutes)

#### Launch Unreal Engine

1. Open **Epic Games Launcher**
2. Click **Unreal Engine** (left sidebar)
3. Click **Launch** next to UE 5.2 or 5.3

#### Create New Project

```
1. Click "New Project"
2. Select "Game"
3. Select "Blank" template
4. Engine: 5.2 (or 5.3)
5. Project Settings:
   - Project Name: SARDroneSim
   - Location: C:\Projects\SARDroneSim
   - Project Type: C++
   - Quality: High
   - Ray Tracing: No (faster)
   - Starter Content: No
6. Click "Create"
```

Wait for project to open in Unreal Editor...

---

### **Phase 5: Install AirSim Plugin** (15 minutes)

#### Copy Plugin Files

```bash
# Open a new Command Prompt

# Go to Colosseum
cd Colosseum

# Copy plugins to your new project
xcopy Unreal\Plugins C:\Projects\SARDroneSim\Plugins /E /I /Y
```

#### Regenerate Project Files

```bash
# Still in Command Prompt, go to project
cd C:\Projects\SARDroneSim

# Right-click the .uproject file
# Select: Generate Visual Studio project files

# Or run from command line:
"C:\Program Files\Epic Games\UE_5.3\Engine\Build\BatchFiles\Build.bat" SARDroneSim
```

#### Build Project

```bash
# Open SARDroneSim.sln in Visual Studio

# Build (F7) or Build > Build Solution

# Wait for compilation to complete
```

---

### **Phase 6: Configure Unreal World** (10 minutes)

#### Launch Unreal Editor

```bash
# In Visual Studio:
# Set configuration: DebugGame Editor
# Set platform: Win64
# Press F5 (or Build > Build and Run)
```

#### Setup World Settings

In Unreal Editor:
1. **Window** → **World Settings**
2. Find "Game Mode Override"
3. Set to: **AirSimGameMode**
4. Save the level (Ctrl+S)

#### (Optional) Add Victim Actor

1. **Content Browser** (bottom panel)
2. Search: "Mannequin" (free humanoid character)
3. Drag into viewport
4. In **Details** panel:
   - Find "Display Name"
   - Change to: **VictimActor_1**
5. Position it in your map

---

### **Phase 7: Run the Simulation** (First test)

#### Terminal 1: Start Unreal

```bash
# Already running from Phase 6
# Keep Unreal Editor open with Play pressed
```

#### Terminal 2: Run Python Script

```bash
# NEW COMMAND PROMPT

# Go to project
cd C:\Users\kadia\OneDrive\Documents\Github\rescue-drone-simulation

# Activate venv (if not already active)
venv\Scripts\activate

# Run mission
python search_and_rescue.py
```

**Expected output:**
```
============================================================
AUTONOMOUS SEARCH & RESCUE DRONE MISSION
============================================================
[STARTUP] Initializing Search & Rescue Drone System...
[INFO] Connecting to AirSim simulator...
[SUCCESS] Connected to AirSim!
[SUCCESS] Drone armed and ready!
[INFO] Loading YOLOv8 model...
[SUCCESS] YOLOv8 model loaded!
[MISSION] Taking off to altitude 10m...
[SUCCESS] Takeoff complete. Current position: (0.00, 0.00, -10.00)
[MISSION] Starting search pattern...
...
```

**In Unreal window:** You should see the drone take off and fly in a pattern!

---

## ⚠️ Common Issues During Setup

### "build.cmd: Command not recognized"
→ Use **x64 Native Tools Command Prompt**, not PowerShell!

### "python: command not found"
→ Add Python to PATH:
```bash
# Rerun Python installer → Modify → Add python.exe to PATH
```

### "Module not found" error
→ Make sure venv is activated:
```bash
# Check for (venv) at start of prompt
# If not there:
venv\Scripts\activate
```

### "Unreal Editor won't start"
→ Verify UE5 installation, try reinstalling from Epic Games Launcher

### "Drone doesn't connect"
→ Make sure "AirSimGameMode" is set in World Settings

---

## 🚀 Quick Testing

### Test 1: Connection
```bash
python -c "import airsim; client = airsim.MultirotorClient(); print('Connected!' if client.confirmConnection() else 'Failed')"
```

### Test 2: YOLO Loading
```bash
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt'); print('✅ YOLO Ready')"
```

### Test 3: Full Mission
```bash
python search_and_rescue.py
```

---

## 📞 Getting Help

| Issue | Solution |
|-------|----------|
| Build errors | Check TROUBLESHOOTING.md |
| Drone won't connect | See FAQ in README.md |
| Vision not working | Verify camera in Unreal |
| Slow performance | Reduce search_area_size in script |

---

## ✅ Verification Checklist

- [ ] Visual Studio 2022 installed with C++
- [ ] Unreal Engine 5.2+ installed
- [ ] Python 3.8+ installed and in PATH
- [ ] Colosseum built successfully (build.cmd completed)
- [ ] Virtual environment created
- [ ] Dependencies installed (pip install -r requirements.txt)
- [ ] YOLOv8 model downloaded
- [ ] SARDroneSim project created in C++
- [ ] AirSim plugin copied to project
- [ ] Project files regenerated
- [ ] World Settings > Game Mode Override = AirSimGameMode
- [ ] Test script runs without errors

---

## 🎉 You're Ready!

Once all steps complete, you can:

1. **Run missions:** `python search_and_rescue.py`
2. **Modify search patterns:** Edit `search_and_rescue.py`
3. **Add features:** See API_REFERENCE.md
4. **Record demos:** Use OBS Studio for split-screen recording

---

**Need more help?** See README.md or TROUBLESHOOTING.md

**Last Updated:** February 2025
