#!/usr/bin/env python3
"""
Autonomous Search & Rescue Drone Simulation
============================================
This script controls a drone in the Colosseum simulator to:
1. Search for victims using a lawnmower pattern
2. Detect humans using YOLOv8 vision
3. Locate victims using simulated audio sensors
4. Return to base when mission is complete
"""

import airsim
import cv2
import numpy as np
from ultralytics import YOLO
import math
import time
import sys

class SearchAndRescueDrone:
    """Main class for autonomous search and rescue drone operations"""
    
    def __init__(self, drone_name="Drone1"):
        """
        Initialize the drone and connect to AirSim simulator
        
        Args:
            drone_name (str): Name of the drone in the simulator
        """
        self.drone_name = drone_name
        self.client = None
        self.model = None
        self.start_position = None
        self.victims_found = []
        
    def connect(self):
        """Connect to AirSim simulator"""
        print("[INFO] Connecting to AirSim simulator...")
        try:
            self.client = airsim.MultirotorClient()
            self.client.confirmConnection()
            print("[SUCCESS] Connected to AirSim!")
            
            # Enable API control and arm the drone
            self.client.enableApiControl(True)
            self.client.armDisarm(True)
            print("[SUCCESS] Drone armed and ready!")
        except Exception as e:
            print(f"[ERROR] Failed to connect: {e}")
            sys.exit(1)
    
    def load_yolo_model(self):
        """Load YOLOv8 model for person detection"""
        print("[INFO] Loading YOLOv8 model...")
        try:
            self.model = YOLO("yolov8n.pt")  # Nano version (fastest)
            print("[SUCCESS] YOLOv8 model loaded!")
        except Exception as e:
            print(f"[ERROR] Failed to load YOLO model: {e}")
            print("[WARNING] Continuing without vision detection...")
            self.model = None
    
    def takeoff(self, altitude=10):
        """
        Take off to specified altitude
        
        Args:
            altitude (float): Takeoff altitude in meters (negative value)
        """
        print(f"[MISSION] Taking off to altitude {altitude}m...")
        try:
            self.client.takeoffAsync().join()
            
            # Move to hover position
            self.client.moveToPositionAsync(0, 0, -altitude, 5).join()
            
            # Store starting position
            state = self.client.getMultirotorState()
            self.start_position = state.kinematics_estimated.position
            print(f"[SUCCESS] Takeoff complete. Current position: "
                  f"({self.start_position.x_val:.2f}, "
                  f"{self.start_position.y_val:.2f}, "
                  f"{self.start_position.z_val:.2f})")
        except Exception as e:
            print(f"[ERROR] Takeoff failed: {e}")
            sys.exit(1)
    
    def get_drone_position(self):
        """Get current drone position"""
        state = self.client.getMultirotorState()
        pos = state.kinematics_estimated.position
        return pos
    
    def check_audio_sensor(self, drone_pos, victim_name="VictimActor_1", threshold=15.0):
        """
        Simulate audio sensor by checking distance to victim actor
        
        Args:
            drone_pos: Current drone position
            victim_name (str): Name of victim actor in Unreal
            threshold (float): Detection threshold in meters
            
        Returns:
            tuple: (detected: bool, distance: float)
        """
        try:
            # Query victim position from Unreal Engine
            victim_pose = self.client.simGetObjectPose(victim_name)
            
            # Calculate Euclidean distance
            dx = victim_pose.position.x_val - drone_pos.x_val
            dy = victim_pose.position.y_val - drone_pos.y_val
            dz = victim_pose.position.z_val - drone_pos.z_val
            distance = math.sqrt(dx*dx + dy*dy + dz*dz)
            
            if distance < threshold:
                return True, distance
            return False, distance
        except Exception as e:
            # Victim actor may not exist yet
            return False, 0.0
    
    def detect_humans_in_image(self, image):
        """
        Detect humans in image using YOLOv8
        
        Args:
            image: OpenCV image
            
        Returns:
            list: List of detections (boxes and confidence scores)
        """
        if self.model is None:
            return []
        
        try:
            results = self.model(image, verbose=False)
            detections = []
            
            for result in results:
                for box in result.boxes:
                    cls_id = int(box.cls)
                    confidence = float(box.conf)
                    
                    # Check if detection is a person (class 0 in COCO dataset)
                    if cls_id == 0:  # Person class
                        bbox = box.xyxy[0].cpu().numpy()
                        detections.append({
                            'bbox': bbox,
                            'confidence': confidence,
                            'class': 'person'
                        })
            
            return detections
        except Exception as e:
            print(f"[WARNING] Error in detection: {e}")
            return []
    
    def capture_and_analyze_frame(self, camera_id=0):
        """
        Capture frame from drone camera and analyze for humans
        
        Args:
            camera_id (int): Camera index (0=front)
            
        Returns:
            dict: Analysis results
        """
        try:
            # Get image from drone camera
            responses = self.client.simGetImages(
                [airsim.ImageRequest(camera_id, airsim.ImageType.Scene, False, False)]
            )
            
            if not responses or responses[0].image_data_uint8 is None:
                return {'success': False, 'detections': []}
            
            response = responses[0]
            
            # Convert to OpenCV format
            img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8)
            img_rgb = img1d.reshape(response.height, response.width, 3)
            img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
            
            # Detect humans
            detections = self.detect_humans_in_image(img_rgb)
            
            return {
                'success': True,
                'image': img_bgr,
                'detections': detections,
                'timestamp': time.time()
            }
        except Exception as e:
            print(f"[WARNING] Frame capture error: {e}")
            return {'success': False, 'detections': []}
    
    def search_mission(self, search_area_size=100, altitude=30, speed=10):
        """
        Execute lawnmower search pattern
        
        Args:
            search_area_size (float): Size of search area in meters
            altitude (float): Search altitude (positive value)
            speed (float): Flight speed
        """
        print(f"\n[MISSION] Starting search pattern...")
        print(f"[INFO] Search area: {search_area_size}x{search_area_size}m, Altitude: {altitude}m")
        
        # Define lawnmower pattern waypoints
        waypoints = [
            (0, 0, -altitude, speed),
            (search_area_size, 0, -altitude, speed),
            (search_area_size, search_area_size, -altitude, speed),
            (0, search_area_size, -altitude, speed),
            (search_area_size//2, search_area_size//2, -altitude, speed),  # Center
        ]
        
        for i, (x, y, z, spd) in enumerate(waypoints):
            print(f"\n[NAVIGATION] Waypoint {i+1}/{len(waypoints)}: ({x}, {y}, {-z}m)")
            
            try:
                self.client.moveToPositionAsync(x, y, z, spd).join()
                
                # Analyze frame at waypoint
                analysis = self.capture_and_analyze_frame()
                
                if analysis['success']:
                    if analysis['detections']:
                        print(f"[ALERT] 🚨 VISUAL DETECTION at Waypoint {i+1}!")
                        for det in analysis['detections']:
                            conf = det['confidence']
                            print(f"  └─ Person detected (confidence: {conf:.2%})")
                            self.victims_found.append({
                                'type': 'visual',
                                'waypoint': i+1,
                                'position': (x, y, -z),
                                'confidence': conf
                            })
                
                # Check audio sensor
                drone_pos = self.get_drone_position()
                heard_scream, distance = self.check_audio_sensor(drone_pos)
                
                if heard_scream:
                    print(f"[ALERT] 🔊 AUDIO DETECTION at distance {distance:.2f}m!")
                    self.victims_found.append({
                        'type': 'audio',
                        'waypoint': i+1,
                        'position': (x, y, -z),
                        'distance': distance
                    })
                    print("[MISSION] Switching to rescue mode...")
                    break
                    
            except Exception as e:
                print(f"[WARNING] Navigation error: {e}")
                continue
    
    def return_to_base(self):
        """Return drone to starting position"""
        print("\n[MISSION] Returning to base...")
        try:
            if self.start_position:
                self.client.moveToPositionAsync(
                    self.start_position.x_val,
                    self.start_position.y_val,
                    self.start_position.z_val,
                    10
                ).join()
            print("[SUCCESS] Returned to base!")
        except Exception as e:
            print(f"[WARNING] Return to base error: {e}")
    
    def land(self):
        """Land the drone"""
        print("[MISSION] Landing...")
        try:
            self.client.landAsync().join()
            print("[SUCCESS] Landed successfully!")
        except Exception as e:
            print(f"[ERROR] Landing error: {e}")
    
    def disarm(self):
        """Disarm the drone"""
        try:
            self.client.armDisarm(False)
            self.client.enableApiControl(False)
            print("[INFO] Drone disarmed and API control disabled")
        except Exception as e:
            print(f"[WARNING] Disarm error: {e}")
    
    def generate_report(self):
        """Generate mission report"""
        print("\n" + "="*60)
        print("MISSION REPORT")
        print("="*60)
        print(f"Victims Found: {len(self.victims_found)}")
        
        if self.victims_found:
            for i, victim in enumerate(self.victims_found, 1):
                print(f"\n{i}. Detection Type: {victim['type'].upper()}")
                print(f"   Waypoint: {victim['waypoint']}")
                print(f"   Position: {victim['position']}")
                if 'confidence' in victim:
                    print(f"   Confidence: {victim['confidence']:.2%}")
                if 'distance' in victim:
                    print(f"   Distance: {victim['distance']:.2f}m")
        else:
            print("No victims detected during search mission")
        
        print("="*60 + "\n")
    
    def run_full_mission(self):
        """Execute complete search and rescue mission"""
        try:
            print("\n" + "="*60)
            print("AUTONOMOUS SEARCH & RESCUE DRONE MISSION")
            print("="*60)
            
            # Phase 1: Initialization
            self.connect()
            self.load_yolo_model()
            
            # Phase 2: Takeoff
            self.takeoff(altitude=10)
            time.sleep(2)
            
            # Phase 3: Search
            self.search_mission(search_area_size=100, altitude=30, speed=10)
            
            # Phase 4: Return
            self.return_to_base()
            time.sleep(2)
            
            # Phase 5: Landing
            self.land()
            time.sleep(1)
            
            # Phase 6: Disarm
            self.disarm()
            
            # Phase 7: Report
            self.generate_report()
            
        except KeyboardInterrupt:
            print("\n[INTERRUPT] Mission interrupted by user!")
            self.land()
            self.disarm()
        except Exception as e:
            print(f"\n[CRITICAL ERROR] {e}")
            self.land()
            self.disarm()


def main():
    """Main entry point"""
    print("\n[STARTUP] Initializing Search & Rescue Drone System...")
    
    # Create drone controller
    drone = SearchAndRescueDrone(drone_name="SARDrone")
    
    # Run mission
    drone.run_full_mission()


if __name__ == "__main__":
    main()
