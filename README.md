# Autonomous Search & Rescue Drone Simulation

A complete autonomous search and rescue drone simulation built on **Colosseum** (UE5-compatible AirSim successor) with computer vision, audio sensing, and intelligent mission planning.

## 📋 Project Overview

This project demonstrates an autonomous drone system that can:
- ✈️ **Navigate** predefined search patterns
- 👁️ **Detect humans** using YOLOv8 computer vision
- 🔊 **Locate victims** with simulated audio sensors
- 📊 **Generate reports** on findings
- 🎯 **Execute rescue missions** with full mission planning

Perfect for presentations on robotics, AI, and autonomous systems!

---

## 🛠️ Prerequisites

### System Requirements
- **Windows 10/11** with Visual Studio 2022
- **16GB RAM** (minimum)
- **NVIDIA GPU** recommended (for YOLOv8 acceleration)
- **100GB free disk space** (for Unreal Engine)

### Required Software
1. **Visual Studio 2022**
   - Download: https://visualstudio.microsoft.com/
   - Install "Desktop development with C++"
   - ✅ Ensure Windows 10 SDK is selected

2. **Unreal Engine 5.2 or 5.3**
   - Download Epic Games Launcher
   - Install UE 5.2+ through the launcher

3. **Python 3.8+**
   - Download: https://www.python.org/
   - Add to PATH during installation

---

## 📦 Installation Guide

### Step 1: Build Colosseum (The Simulator)

```bash
# Open Developer Command Prompt for VS 2022
cd C:\Projects

# Clone this repository
git clone https://github.com/CodexLabsLLC/Colosseum.git
cd Colosseum

# Build (takes 20-30 minutes on first build)
build.cmd
```

### Step 2: Create Unreal Project

```bash
# In your projects folder
cd C:\Projects

# Create a new Unreal C++ project
# Use Unreal Engine launcher:
# 1. Click "Create" → Game → Blank
# 2. Select C++ (Important!)
# 3. Name: "SARDroneSim"
# 4. Create
```

### Step 3: Install AirSim Plugin

```bash
# In your Colosseum folder
cd Colosseum

# Copy the Unreal plugins to your project
xcopy Unreal\Plugins C:\Projects\SARDroneSim\Plugins /E /I /Y

# In your project folder
cd C:\Projects\SARDroneSim

# Generate Visual Studio files (right-click .uproject)
# Or use: 
"C:\Program Files\Epic Games\UE_5.3\Engine\Build\BatchFiles\Build.bat" SARDroneSim
```

### Step 4: Setup Python Environment

```bash
# Clone this repository
git clone https://github.com/yourusername/rescue-drone-simulation.git
cd rescue-drone-simulation

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download YOLOv8 model (first run only)
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

---

## 🚀 Running the Simulation

### 1. Start Unreal Engine with AirSim

```bash
# In your project folder
cd C:\Projects\SARDroneSim

# Open the project in editor
SARDroneSim.sln

# In Visual Studio:
# - Set configuration to "DebugGame Editor"
# - Set platform to "Win64"
# - Press F5 to build and launch
```

### 2. In Unreal Editor

1. **Set Up Game Mode:**
   - Go to World Settings
   - Under "Game Mode Override" → select "AirSimGameMode"

2. **Add Victim Actor (Optional):**
   - Place a Mannequin character in the scene
   - Rename to "VictimActor_1" in Details
   - This enables audio detection testing

3. **Play the Simulation:**
   - Press Play button (or click in viewport and press ▶)

### 3. Run the Python Script

```bash
# In a NEW terminal window
cd rescue-drone-simulation

# Activate virtual environment if needed
venv\Scripts\activate

# Run the autonomous mission
python search_and_rescue.py
```

You should see:
- ✈️ Drone takes off in Unreal
- 📍 Drone follows search pattern
- 👁️ Terminal prints "VISUAL DETECTION" if YOLO finds a person
- 🔊 Terminal prints "AUDIO DETECTION" if drone gets close to victim
- 📊 Mission report at the end

---

## 📝 Project Structure

```
rescue-drone-simulation/
├── search_and_rescue.py          # Main autonomy script
├── requirements.txt               # Python dependencies
├── README.md                      # This file
├── Colosseum/                     # AirSim fork with UE5 support
│   ├── Unreal/
│   │   ├── Plugins/              # AirSim plugin for Unreal
│   │   └── Environments/
│   └── ...
└── docs/                          # Additional documentation
    ├── SETUP_GUIDE.md            # Detailed setup instructions
    ├── TROUBLESHOOTING.md        # Common issues and fixes
    └── API_REFERENCE.md          # AirSim Python API docs
```

---

## 🎯 Features Explained

### 🛸 Drone Control
- **Takeoff/Landing:** Automated vertical movement
- **Navigation:** Point-to-point autonomous flight
- **Stabilization:** Hover at waypoints for analysis

### 👁️ Computer Vision (YOLOv8)
- **Real-time Detection:** Identifies people at 30+ FPS
- **Confidence Scoring:** Returns detection confidence
- **On-board Processing:** Runs on drone's simulated computer

### 🔊 Audio Sensing (Simulated)
- **Distance-based Detection:** Simulates victim cries
- **Victim Actor Integration:** Uses Unreal Engine objects
- **Threshold Detection:** 15-meter detection radius

### 📊 Mission Planning
- **Lawnmower Pattern:** Systematic search coverage
- **Adaptive Behavior:** Changes plan on victim detection
- **Logging:** Detailed mission reports with timestamps

---

## 🧪 Testing

### Manual Testing Checklist

- [ ] Drone connects to simulator successfully
- [ ] Drone takes off and reaches target altitude
- [ ] Drone follows waypoint navigation
- [ ] Camera captures frames correctly
- [ ] YOLOv8 detects person (place mannequin in scene)
- [ ] Audio sensor detects victim actor
- [ ] Drone returns to starting position
- [ ] Mission report generates correctly

### Debugging

**Drone doesn't connect:**
```bash
python -c "import airsim; client = airsim.MultirotorClient(); print(client.confirmConnection())"
```

**YOLO model not found:**
```bash
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

**No camera frames:**
- Ensure "AirSimGameMode" is set in World Settings
- Check that a "Pawn" blueprint with camera is spawned

---

## 📚 Documentation

- [Setup Troubleshooting Guide](docs/TROUBLESHOOTING.md)
- [Colosseum Documentation](https://github.com/CodexLabsLLC/Colosseum)
- [AirSim Python API](https://microsoft.github.io/AirSim/apis_cpp/)
- [YOLOv8 Documentation](https://docs.ultralytics.com/)

---

## 🎓 Learning Resources

### Understanding the Code

1. **Drone Physics:** See `get_drone_position()` - queries current state
2. **Sensor Fusion:** See `check_audio_sensor()` - combines multiple sensor inputs
3. **Computer Vision:** See `detect_humans_in_image()` - YOLOv8 integration
4. **Mission Planning:** See `search_mission()` - autonomous decision making

### Extending the Project

Modify `search_and_rescue.py` to:
- Add GPS waypoint loading from files
- Implement path planning with obstacles
- Add thermal camera detection
- Create swarm multi-drone missions
- Log all data to files for analysis

---

## 🏆 Demo Video Tips

Record a video showing:
1. **Split Screen:** Unreal window (left) + Python terminal (right)
2. **Sequence:**
   - Show initial "Connecting..." message
   - Show drone takeoff in Unreal
   - Show drone flying search pattern
   - Show "VISUAL DETECTION" or "AUDIO DETECTION" print
   - Show mission report at end

**Pro Tip:** Use OBS Studio (free) for professional screen recording!

---

## 🤝 Contributing

Found a bug? Want to add features?
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit changes: `git commit -am 'Add my feature'`
4. Push: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

This project is built on **Colosseum** and **AirSim** (MIT Licensed).

---

## ❓ FAQ

**Q: Can I use this on Linux/Mac?**
A: Yes, but Unreal Engine 5 is limited. See Colosseum docs for platform support.

**Q: Do I need a powerful GPU?**
A: GPU helps but isn't required. CPU will be slower (~5 FPS). Test first!

**Q: Can I use different drone models?**
A: Yes! Edit `settings.json` in your Unreal project to change drone type.

**Q: How do I add more victims?**
A: Create more Mannequin actors named `VictimActor_2`, `VictimActor_3`, etc.

---

## 📞 Support

Having issues? Check:
1. [Troubleshooting Guide](docs/TROUBLESHOOTING.md)
2. [Colosseum Issues](https://github.com/CodexLabsLLC/Colosseum/issues)
3. [AirSim Issues](https://github.com/microsoft/AirSim/issues)

---

## 🎉 Show Your Work!

Built something cool? Tweet it with #SARDroneSim and tag us!

Good luck with your presentation! 🚀

---

**Last Updated:** February 2025  
**Version:** 1.0.0  
**Status:** ✅ Production Ready
