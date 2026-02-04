# API Reference - Search & Rescue Drone Simulation

## SearchAndRescueDrone Class

Main class for controlling the autonomous search and rescue drone.

### Initialization

```python
from search_and_rescue import SearchAndRescueDrone

# Create drone instance
drone = SearchAndRescueDrone(drone_name="Drone1")
```

---

## Methods

### Connection Management

#### `connect()`
Connects to AirSim simulator and arms the drone.

```python
drone.connect()
# Output:
# [INFO] Connecting to AirSim simulator...
# [SUCCESS] Connected to AirSim!
# [SUCCESS] Drone armed and ready!
```

**Raises:** `SystemExit` if connection fails

---

#### `disarm()`
Disarms the drone and disables API control.

```python
drone.disarm()
# Output:
# [INFO] Drone disarmed and API control disabled
```

---

### Flight Operations

#### `takeoff(altitude=10)`
Take off to specified altitude.

**Parameters:**
- `altitude` (float): Target altitude in meters (default: 10m)

```python
drone.takeoff(altitude=15)
# Output:
# [MISSION] Taking off to altitude 15m...
# [SUCCESS] Takeoff complete. Current position: (0.00, 0.00, -15.00)
```

---

#### `get_drone_position()`
Get current drone position.

**Returns:**
- Position object with attributes: `x_val`, `y_val`, `z_val`

```python
pos = drone.get_drone_position()
print(f"Position: ({pos.x_val}, {pos.y_val}, {pos.z_val})")
```

---

#### `return_to_base()`
Return drone to starting position.

```python
drone.return_to_base()
# Output:
# [MISSION] Returning to base...
# [SUCCESS] Returned to base!
```

---

#### `land()`
Land the drone.

```python
drone.land()
# Output:
# [MISSION] Landing...
# [SUCCESS] Landed successfully!
```

---

### Sensor Operations

#### `load_yolo_model()`
Load YOLOv8 model for person detection.

```python
drone.load_yolo_model()
# Output:
# [INFO] Loading YOLOv8 model...
# [SUCCESS] YOLOv8 model loaded!
```

---

#### `capture_and_analyze_frame(camera_id=0)`
Capture frame from drone camera and detect humans.

**Parameters:**
- `camera_id` (int): Camera index (0=front camera, default: 0)

**Returns:**
```python
{
    'success': bool,              # Whether capture succeeded
    'image': np.ndarray,          # OpenCV image (BGR format)
    'detections': list,           # List of detected persons
    'timestamp': float            # Timestamp of capture
}
```

**Example:**
```python
result = drone.capture_and_analyze_frame()
if result['success']:
    print(f"Found {len(result['detections'])} people")
    for det in result['detections']:
        print(f"  Confidence: {det['confidence']:.2%}")
```

---

#### `check_audio_sensor(drone_pos, victim_name="VictimActor_1", threshold=15.0)`
Simulate audio sensor by checking distance to victim.

**Parameters:**
- `drone_pos`: Current drone position (from `get_drone_position()`)
- `victim_name` (str): Name of victim actor in Unreal (default: "VictimActor_1")
- `threshold` (float): Detection threshold in meters (default: 15m)

**Returns:**
- `(detected: bool, distance: float)` - Tuple of detection status and distance

**Example:**
```python
pos = drone.get_drone_position()
heard_scream, distance = drone.check_audio_sensor(pos)
if heard_scream:
    print(f"Victim detected at {distance:.2f}m!")
```

---

#### `detect_humans_in_image(image)`
Detect humans in image using YOLOv8.

**Parameters:**
- `image`: OpenCV/NumPy image (RGB format)

**Returns:**
```python
[
    {
        'bbox': [x1, y1, x2, y2],     # Bounding box coordinates
        'confidence': float,           # 0.0-1.0 confidence score
        'class': 'person'             # Class name
    },
    ...
]
```

**Example:**
```python
import cv2
img = cv2.imread('test.jpg')
detections = drone.detect_humans_in_image(img)
for det in detections:
    print(f"Person found with {det['confidence']:.2%} confidence")
```

---

### Mission Operations

#### `search_mission(search_area_size=100, altitude=30, speed=10)`
Execute lawnmower search pattern.

**Parameters:**
- `search_area_size` (float): Size of search area in meters (default: 100m)
- `altitude` (float): Search altitude in meters (default: 30m)
- `speed` (float): Flight speed in m/s (default: 10 m/s)

**Example:**
```python
drone.search_mission(
    search_area_size=50,      # 50x50m area
    altitude=20,              # 20m altitude
    speed=5                   # Slower, more careful search
)
```

**Output:**
```
[MISSION] Starting search pattern...
[INFO] Search area: 50x50m, Altitude: 20m
[NAVIGATION] Waypoint 1/5: (0, 0, 20m)
[ALERT] 🚨 VISUAL DETECTION at Waypoint 1!
  └─ Person detected (confidence: 87.34%)
```

---

#### `run_full_mission()`
Execute complete search and rescue mission (all phases).

```python
drone.run_full_mission()
# Executes:
# 1. Connection
# 2. Model loading
# 3. Takeoff
# 4. Search pattern
# 5. Return to base
# 6. Landing
# 7. Report generation
```

---

### Reporting

#### `generate_report()`
Generate mission report with findings.

```python
drone.generate_report()
# Output:
# ============================================================
# MISSION REPORT
# ============================================================
# Victims Found: 2
# 
# 1. Detection Type: VISUAL
#    Waypoint: 1
#    Position: (0, 0, 20)
#    Confidence: 87.34%
# 
# 2. Detection Type: AUDIO
#    Waypoint: 3
#    Position: (50, 50, 20)
#    Distance: 12.45m
# ============================================================
```

---

## Properties

### `victims_found`
List of detected victims during mission.

**Type:** `list` of dictionaries

```python
drone.victims_found
# Returns:
# [
#     {
#         'type': 'visual',
#         'waypoint': 1,
#         'position': (0, 0, 20),
#         'confidence': 0.8734
#     },
#     {
#         'type': 'audio',
#         'waypoint': 3,
#         'position': (50, 50, 20),
#         'distance': 12.45
#     }
# ]
```

---

## Common Usage Patterns

### Minimal Mission
```python
from search_and_rescue import SearchAndRescueDrone

drone = SearchAndRescueDrone()
drone.run_full_mission()
```

### Custom Search Pattern
```python
drone = SearchAndRescueDrone()
drone.connect()
drone.load_yolo_model()
drone.takeoff(altitude=20)

# Fly to specific location
drone.search_mission(search_area_size=30, altitude=20, speed=8)

drone.return_to_base()
drone.land()
drone.disarm()
drone.generate_report()
```

### Manual Flight Control
```python
drone = SearchAndRescueDrone()
drone.connect()
drone.takeoff()

# Move to point
pos = drone.get_drone_position()
print(f"Current: {pos}")

# Check sensors
analysis = drone.capture_and_analyze_frame()
print(f"Detections: {len(analysis['detections'])}")

drone.land()
drone.disarm()
```

### Vision-Only Search
```python
drone = SearchAndRescueDrone()
drone.connect()
drone.load_yolo_model()
drone.takeoff()

# Search without audio
for x in range(0, 100, 20):
    drone.client.moveToPositionAsync(x, 0, -30, 5).join()
    result = drone.capture_and_analyze_frame()
    if result['detections']:
        print(f"Found {len(result['detections'])} people at x={x}")

drone.land()
drone.disarm()
```

---

## Error Handling

All methods that interact with AirSim may raise exceptions:

```python
from search_and_rescue import SearchAndRescueDrone
import sys

try:
    drone = SearchAndRescueDrone()
    drone.connect()
    drone.takeoff()
    drone.search_mission()
    drone.return_to_base()
    drone.land()
except Exception as e:
    print(f"[ERROR] Mission failed: {e}")
    drone.land()
    drone.disarm()
    sys.exit(1)
finally:
    drone.disarm()
```

---

## Performance Tips

1. **Faster Detection:** Use `yolov8n.pt` (nano, fastest)
2. **Larger Coverage:** Increase `search_area_size`
3. **Smoother Flight:** Decrease `speed` value
4. **Better Detection:** Place victim in well-lit areas
5. **Debugging:** Add prints in mission execution

---

## See Also

- [README.md](README.md) - Project overview
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues
- [AirSim Python API](https://microsoft.github.io/AirSim/)
- [YOLOv8 Documentation](https://docs.ultralytics.com/)

---

**Last Updated:** February 2025
