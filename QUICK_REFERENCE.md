# QUICK REFERENCE CARD

## Essential Commands

### Setup (Run Once)
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

### Build Colosseum (Run Once)
```bash
cd Colosseum
build.cmd
cd ..
```

### Every New Terminal Session
```bash
venv\Scripts\activate
```

### Run Mission
```bash
python search_and_rescue.py
```

---

## File Structure

```
rescue-drone-simulation/
├── search_and_rescue.py       # Main script - RUN THIS
├── setup.py                   # Python setup helper
├── setup.cmd                  # Windows setup batch file
├── requirements.txt           # Dependencies (pip install -r)
├── README.md                  # Project overview
├── SETUP_GUIDE.md             # Detailed step-by-step setup
├── TROUBLESHOOTING.md         # Common issues & fixes
├── API_REFERENCE.md           # Code documentation
└── Colosseum/                 # AirSim fork (don't modify)
```

---

## Key Scripts & Functions

### Main Mission
```python
from search_and_rescue import SearchAndRescueDrone

drone = SearchAndRescueDrone()
drone.run_full_mission()
```

### Custom Search
```python
drone = SearchAndRescueDrone()
drone.connect()
drone.load_yolo_model()
drone.takeoff(altitude=20)
drone.search_mission(search_area_size=100, altitude=20)
drone.return_to_base()
drone.land()
drone.generate_report()
```

---

## Workflow

1. **Start Unreal Editor** → Press Play
2. **Activate Python venv** → `venv\Scripts\activate`
3. **Run script** → `python search_and_rescue.py`
4. **Watch Unreal** → Drone flies autonomously
5. **Check terminal** → Mission report printed

---

## Debug

| Problem | Check |
|---------|-------|
| Drone won't connect | Is Unreal running with Play pressed? |
| No YOLO detections | Is mannequin in scene and visible? |
| Audio not detected | Is victim actor named "VictimActor_1"? |
| Very slow | Reduce search_area_size parameter |
| Python errors | Is venv activated? |

---

## GitHub Link
https://github.com/kadiamyeshwanth/rescue-drone-simulation

---

**Status:** ✅ Ready to Run!
**Last Updated:** February 2025
