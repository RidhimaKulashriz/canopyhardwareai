import requests
import json
from datetime import datetime
from typing import Dict, Any, Optional
from .config import config

class FirebaseClient:
    def __init__(self):
        self.database_url = config.FIREBASE_DATABASE_URL
        self.database_secret = config.FIREBASE_DATABASE_SECRET
        self.initialized = bool(self.database_url and self.database_secret)
        
        if self.initialized:
            print("✓ Firebase REST API client initialized")
            print(f"  Database: {self.database_url}")
            # Test connection
            self._test_connection()
        else:
            print("⚠️ Firebase credentials not found. Running in mock mode.")
    
    def _test_connection(self):
        """Test Firebase connection"""
        try:
            result = self._make_request('/test', 'PUT', {'status': 'connected'})
            if result is not None:
                print("✓ Firebase connection test passed!")
            else:
                print("⚠️ Firebase connection test failed")
        except Exception as e:
            print(f"⚠️ Connection test error: {e}")
    
    def _make_request(self, path: str, method: str = 'GET', data: Any = None) -> Optional[Dict]:
        """Make HTTP request to Firebase REST API"""
        if not self.initialized:
            return None
        
        # Ensure path starts with /
        if not path.startswith('/'):
            path = '/' + path
        
        # Build URL with auth token
        url = f"{self.database_url.rstrip('/')}{path}.json?auth={self.database_secret}"
        
        try:
            if method == 'GET':
                response = requests.get(url, timeout=5)
            elif method == 'PUT':
                response = requests.put(url, json=data, timeout=5)
            elif method == 'POST':
                response = requests.post(url, json=data, timeout=5)
            elif method == 'PATCH':
                response = requests.patch(url, json=data, timeout=5)
            else:
                return None
            
            if response.status_code in [200, 201]:
                return response.json() if response.text else {}
            else:
                print(f"Firebase error ({response.status_code}): {response.text[:100]}")
                return None
        except requests.exceptions.Timeout:
            print("Request timeout")
            return None
        except Exception as e:
            print(f"Request failed: {e}")
            return None
    
    def send_sensor_data(self, user_id: str, distance: float, acceleration: float = 1.0) -> bool:
        """Send sensor data to Firebase"""
        if not self.initialized:
            print(f"[MOCK] Sensor data to {user_id}: {distance}m, {acceleration}g")
            return True
        
        # Calculate vibration intensity (0-100)
        if distance < 0.3:
            vibration = 100
        elif distance < 0.5:
            vibration = 80
        elif distance < 0.8:
            vibration = 60
        elif distance < 1.0:
            vibration = 40
        elif distance < 1.5:
            vibration = 20
        else:
            vibration = 0
        
        data = {
            'distance': round(distance, 2),
            'acceleration': round(acceleration, 2),
            'vibration': vibration,
            'timestamp': datetime.now().isoformat(),
            'status': 'critical' if distance < 0.5 else 'warning' if distance < 1.0 else 'safe'
        }
        
        path = f"/users/{user_id}/sensors/latest"
        result = self._make_request(path, 'PUT', data)
        
        if result is not None:
            print(f"✓ Data sent to Firebase: {distance}m, {acceleration}g, vibration: {vibration}%")
            return True
        else:
            print(f"✗ Failed to send data to Firebase")
            return False
    
    def get_sensor_data(self, user_id: str) -> Optional[Dict]:
        """Get latest sensor data from Firebase"""
        if not self.initialized:
            return {"distance": 1.2, "acceleration": 1.0, "timestamp": datetime.now().isoformat(), "status": "safe"}
        
        path = f"/users/{user_id}/sensors/latest"
        result = self._make_request(path, 'GET')
        
        if result:
            print(f"✓ Retrieved data from Firebase")
            return result
        return None
    
    def send_ai_response(self, user_id: str, response: str) -> bool:
        """Save AI response to Firebase"""
        if not self.initialized:
            print(f"[MOCK] AI Response to {user_id}: {response[:50]}...")
            return True
        
        data = {
            'response': response,
            'timestamp': datetime.now().isoformat(),
            'read': False,
            'type': 'voice_guidance'
        }
        
        path = f"/users/{user_id}/ai_responses"
        result = self._make_request(path, 'POST', data)
        
        if result is not None:
            print("✓ AI response saved to Firebase")
            return True
        return False
    
    def send_alert(self, user_id: str, alert_type: str, message: str) -> bool:
        """Send alert to Firebase"""
        if not self.initialized:
            print(f"[MOCK] Alert to {user_id}: {alert_type} - {message}")
            return True
        
        data = {
            'type': alert_type,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'read': False,
            'severity': 'high' if alert_type in ['critical_obstacle', 'fall_detected'] else 'medium'
        }
        
        path = f"/users/{user_id}/alerts"
        result = self._make_request(path, 'POST', data)
        
        if result is not None:
            print(f"✓ Alert saved to Firebase: {alert_type}")
            return True
        return False
    
    def get_alerts(self, user_id: str, limit: int = 10) -> Optional[list]:
        """Get recent alerts from Firebase"""
        if not self.initialized:
            return []
        
        path = f"/users/{user_id}/alerts"
        result = self._make_request(path, 'GET')
        
        if result and isinstance(result, dict):
            # Convert to list and sort by timestamp
            alerts = list(result.values())
            alerts.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            return alerts[:limit]
        return []
