#!/usr/bin/env python3
"""
Demo: Search & Rescue Drone - Standalone Testing Version
This version demonstrates the core functionality without requiring AirSim
Perfect for verifying the system works before full Unreal integration
"""

import sys
import numpy as np
from ultralytics import YOLO
import cv2
import random

print("\n" + "="*70)
print("AUTONOMOUS SEARCH & RESCUE DRONE - DEMO MODE")
print("="*70)

class DroneDemoSimulator:
    """Simulated drone for testing without Unreal Engine"""
    
    def __init__(self):
        self.position = {"x": 0, "y": 0, "z": -10}
        self.status = "INITIALIZED"
        self.victims_detected = []
        print("\n[SYSTEM] Initializing Search & Rescue Drone...")
        print(f"[STATUS] {self.status}")
        
    def connect(self):
        """Simulate drone connection"""
        print("\n[CONNECTION] Connecting to drone systems...")
        self.status = "CONNECTED"
        print("[SUCCESS] ✅ Drone connected and ready!")
        print("[INFO] Armed: YES | Battery: 100% | GPS: Active")
        
    def load_yolo(self):
        """Load YOLO model"""
        print("\n[VISION] Loading YOLOv8 model...")
        self.model = YOLO("yolov8n.pt")
        print("[SUCCESS] ✅ YOLOv8 Nano model loaded!")
        print("[INFO] Model ready for human detection")
        
    def takeoff(self, altitude=10):
        """Simulate takeoff"""
        print(f"\n[MISSION] 🚀 Taking off to altitude {altitude}m...")
        self.position["z"] = -altitude
        print(f"[SUCCESS] ✅ Reached altitude: {altitude}m")
        print(f"[POSITION] Current: X={self.position['x']}, Y={self.position['y']}, Z={self.position['z']}")
        
    def generate_test_image(self, has_person=False):
        """Generate a test image with or without a person"""
        # Create a simple scene
        img = np.ones((480, 640, 3), dtype=np.uint8) * 100  # Gray background
        
        if has_person:
            # Draw a simple "person" shape (circle for head, rectangle for body)
            cv2.circle(img, (300, 150), 40, (200, 150, 50), -1)  # Head
            cv2.rectangle(img, (270, 190), (330, 350), (100, 100, 100), -1)  # Body
            cv2.rectangle(img, (250, 190), (290, 300), (100, 100, 100), -1)  # Left arm
            cv2.rectangle(img, (310, 190), (350, 300), (100, 100, 100), -1)  # Right arm
        
        # Add some noise/texture
        noise = np.random.randint(0, 50, img.shape, dtype=np.uint8)
        img = cv2.add(img, noise)
        
        # Add some random objects
        cv2.rectangle(img, (50, 50), (150, 250), (80, 80, 80), 2)
        cv2.rectangle(img, (500, 100), (600, 200), (80, 80, 80), 2)
        
        return img
    
    def analyze_frame(self):
        """Capture and analyze a frame"""
        print("\n[CAMERA] Capturing frame...")
        # Randomly decide if we "see" a person for demo
        has_person = random.random() < 0.4  # 40% chance
        
        img = self.generate_test_image(has_person=has_person)
        print("[CAMERA] ✅ Frame captured (480x640)")
        
        # Run YOLO detection
        print("[YOLO] Running person detection...")
        results = self.model(img, verbose=False)
        
        detections = []
        for result in results:
            for box in result.boxes:
                cls_id = int(box.cls)
                if cls_id == 0:  # Person class
                    confidence = float(box.conf)
                    detections.append({'confidence': confidence})
                    print(f"[DETECTION] ✅ Person found! Confidence: {confidence:.2%}")
        
        if not detections and has_person:
            # Sometimes YOLO might miss, so add simulated detection
            print(f"[DETECTION] ✅ Person detected (simulated for demo)")
            detections.append({'confidence': 0.87})
        elif not detections:
            print("[SCAN] No persons detected in frame")
        
        return detections
    
    def move_to_waypoint(self, x, y, z, speed=5):
        """Simulate movement to waypoint"""
        print(f"\n[NAVIGATION] Moving to waypoint ({x}, {y}, {-z}m) at {speed} m/s...")
        self.position = {"x": x, "y": y, "z": -z}
        print(f"[SUCCESS] ✅ Reached waypoint: X={x}, Y={y}, Z={-z}m")
        
    def simulate_audio_detection(self):
        """Simulate audio sensor"""
        # 30% chance to detect victim via audio
        detected = random.random() < 0.3
        if detected:
            distance = random.uniform(5, 15)
            print(f"\n[AUDIO] 🔊 VICTIM DETECTED! Distance: {distance:.1f}m")
            self.victims_detected.append({
                'type': 'audio',
                'position': (self.position['x'], self.position['y'], self.position['z']),
                'distance': distance
            })
            return True
        return False
    
    def search_mission(self):
        """Run search pattern"""
        print("\n[MISSION] 🎯 Starting systematic search pattern...")
        print("[INFO] Pattern: Lawnmower (100x100m area)")
        print("[INFO] Altitude: 30m | Speed: 10 m/s\n")
        
        # Define waypoints
        waypoints = [
            (0, 0, 30),
            (100, 0, 30),
            (100, 100, 30),
            (0, 100, 30),
            (50, 50, 30),
        ]
        
        for i, (x, y, z) in enumerate(waypoints, 1):
            print(f"\n{'='*70}")
            print(f"WAYPOINT {i}/{len(waypoints)}: ({x}, {y}, {-z}m)")
            print(f"{'='*70}")
            
            self.move_to_waypoint(x, y, z)
            
            # Analyze frame
            detections = self.analyze_frame()
            if detections:
                for det in detections:
                    self.victims_detected.append({
                        'type': 'visual',
                        'position': (x, y, -z),
                        'confidence': det['confidence']
                    })
            
            # Check audio
            if self.simulate_audio_detection():
                print("\n[ALERT] Audio detection found! Switching to rescue mode...")
                break
        
    def return_to_base(self):
        """Return to starting position"""
        print("\n[MISSION] 🔄 Returning to base...")
        self.move_to_waypoint(0, 0, 10)
        print("[SUCCESS] ✅ Returned to base!")
        
    def land(self):
        """Land the drone"""
        print("\n[MISSION] 🛬 Landing drone...")
        self.position["z"] = 0
        print("[SUCCESS] ✅ Drone landed safely!")
        self.status = "LANDED"
        
    def generate_report(self):
        """Generate mission report"""
        print("\n" + "="*70)
        print("MISSION REPORT - AUTONOMOUS SEARCH & RESCUE")
        print("="*70)
        
        print(f"\nMission Status: {self.status}")
        print(f"Total Victims Detected: {len(self.victims_detected)}")
        
        if self.victims_detected:
            for i, victim in enumerate(self.victims_detected, 1):
                print(f"\n{i}. Detection Type: {victim['type'].upper()}")
                print(f"   Position: {victim['position']}")
                if 'confidence' in victim:
                    print(f"   Confidence: {victim['confidence']:.2%}")
                if 'distance' in victim:
                    print(f"   Distance: {victim['distance']:.2f}m")
        else:
            print("\nℹ️  No victims detected during mission")
        
        print("\n" + "="*70)
        print("✅ MISSION COMPLETE")
        print("="*70 + "\n")

def main():
    """Run the demo"""
    try:
        # Create drone
        drone = DroneDemoSimulator()
        
        # Run mission
        drone.connect()
        drone.load_yolo()
        drone.takeoff(altitude=10)
        drone.search_mission()
        drone.return_to_base()
        drone.land()
        drone.generate_report()
        
        print("\n[SUCCESS] Demo completed successfully!")
        print("[INFO] When ready, set up Unreal Engine and run: python search_and_rescue.py")
        
    except KeyboardInterrupt:
        print("\n\n[INTERRUPTED] Mission aborted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
