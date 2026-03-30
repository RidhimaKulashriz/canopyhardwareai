from typing import Dict, Any
from .state import AgentState
from .config import config
import os

# YOUR DIRECT API KEY
API_KEY = "AIzaSyBl6X_pyHH6HLnzrA9W1emEP5M1jrYxdK0"

# Try to import Gemini
try:
    import google.generativeai as genai
    
    if API_KEY:
        genai.configure(api_key=API_KEY)
        
        # Use the latest stable model from the list
        MODEL_NAME = 'models/gemini-2.5-flash'
        
        try:
            model = genai.GenerativeModel(MODEL_NAME)
            # Test the model
            test_response = model.generate_content("Say OK")
            print(f"✓ Gemini AI initialized successfully with {MODEL_NAME}!")
            print(f"  Test response: {test_response.text}")
        except Exception as e:
            print(f"Error with {MODEL_NAME}: {e}")
            # Fallback to another model
            try:
                model = genai.GenerativeModel('models/gemini-2.0-flash')
                test_response = model.generate_content("Say OK")
                print(f"✓ Using fallback model: models/gemini-2.0-flash")
            except:
                model = None
                print("No working model found. Using mock responses.")
        
except Exception as e:
    model = None
    print(f"Error loading Gemini: {e}")
    print("Using mock responses instead.")

def create_llm():
    return model

def process_sensor_data(state: AgentState) -> Dict[str, Any]:
    """Process incoming sensor data"""
    sensor = state['sensor_data']
    alerts = []
    
    distance = sensor.get('distance', 999)
    if distance < config.CRITICAL_DISTANCE:
        alerts.append({
            'type': 'critical_obstacle',
            'severity': 'high',
            'message': f'CRITICAL: Obstacle at {distance:.1f}m! STOP immediately!',
            'timestamp': sensor['timestamp']
        })
    elif distance < config.ALERT_THRESHOLD_DISTANCE:
        alerts.append({
            'type': 'warning_obstacle',
            'severity': 'medium',
            'message': f'WARNING: Object detected at {distance:.1f}m',
            'timestamp': sensor['timestamp']
        })
    
    accel = sensor.get('acceleration', 0)
    if accel and accel > config.FALL_THRESHOLD:
        alerts.append({
            'type': 'fall_detected',
            'severity': 'high',
            'message': 'FALL DETECTED! Emergency services alerted!',
            'timestamp': sensor['timestamp']
        })
    
    return {'alerts': alerts}

def generate_ai_response(state: AgentState) -> Dict[str, Any]:
    """Generate AI response using Gemini"""
    
    alerts = state.get('alerts', [])
    sensor = state.get('sensor_data', {})
    distance = sensor.get('distance', 1.0)
    user_query = state.get('context', {}).get('user_query', '')
    
    alert_messages = [a['message'] for a in alerts]
    
    prompt = f"""You are a helpful AI assistant for a smart cane for visually impaired users.
    
Current sensor data:
- Distance to obstacle: {distance:.2f} meters
- Active alerts: {', '.join(alert_messages) if alert_messages else 'No active alerts'}
- User question: {user_query if user_query else 'None (just provide guidance)'}

Provide short, clear, and actionable voice guidance (2-3 sentences max). Be calm and supportive.
"""
    
    # Try using Gemini
    if model:
        try:
            response = model.generate_content(prompt)
            ai_response = response.text
            print(f"✓ AI Response generated using Gemini")
        except Exception as e:
            print(f"Gemini error: {e}")
            ai_response = f"AI temporarily unavailable. Current status: {alert_messages[0] if alert_messages else 'Path appears clear'}"
    else:
        # Enhanced mock responses
        if any('critical' in a['type'] for a in alerts):
            ai_response = f"Emergency! Obstacle at {distance:.1f} meters. Stop immediately and check your surroundings."
        elif any('warning' in a['type'] for a in alerts):
            ai_response = f"Caution. Object detected {distance:.1f} meters ahead. Move slowly and use your cane."
        elif any('fall' in a['type'] for a in alerts):
            ai_response = "Fall detected! Stay calm. Help is being notified of your location."
        elif user_query:
            ai_response = f"I understand your question. Right now, you have a clear path for {distance:.1f} meters. Keep walking safely."
        else:
            import random
            responses = [
                f"Path clear for {distance:.1f} meters. You can walk safely.",
                f"All good ahead for {distance:.1f} meters. Keep moving.",
                f"Safe path ahead. Distance to nearest object: {distance:.1f} meters.",
                f"The way is clear for {distance:.1f} meters. Continue walking."
            ]
            ai_response = random.choice(responses)
    
    return {'ai_response': ai_response}

def execute_actions(state: AgentState) -> Dict[str, Any]:
    """Execute actions based on AI response"""
    actions_taken = state.get('actions_taken', [])
    alerts = state.get('alerts', [])
    
    for alert in alerts:
        if alert['severity'] == 'high':
            if 'critical_obstacle' in alert['type']:
                actions_taken.append('EMERGENCY_BUZZER')
                actions_taken.append('ALERT_CAREGIVER')
            elif 'fall_detected' in alert['type']:
                actions_taken.append('EMERGENCY_SERVICES')
        elif alert['severity'] == 'medium':
            actions_taken.append('HAPTIC_FEEDBACK')
    
    return {'actions_taken': list(set(actions_taken)) if actions_taken else ['NORMAL_MODE']}
