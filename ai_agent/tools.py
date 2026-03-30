from langchain.tools import tool
from typing import Dict, Any
import json

@tool
def analyze_obstacle_distance(distance: float) -> str:
    """Analyze obstacle distance and return safety recommendation."""
    if distance < 0.5:
        return f"CRITICAL: Obstacle at {distance:.1f}m! STOP immediately!"
    elif distance < 1.0:
        return f"WARNING: Obstacle at {distance:.1f}m. Move slowly and carefully."
    elif distance < 1.5:
        return f"CAUTION: Obstacle at {distance:.1f}m. Prepare to stop."
    else:
        return f"Safe: Path clear for {distance:.1f}m."

@tool
def detect_fall(acceleration: float) -> str:
    """Detect if a fall has occurred based on acceleration data."""
    if acceleration > 2.0:
        return "FALL DETECTED! Emergency alert triggered!"
    elif acceleration > 1.5:
        return "Unusual movement detected. Please be careful."
    else:
        return "Movement normal."

@tool
def generate_voice_guidance(obstacle_distance: float, user_context: str = "") -> str:
    """Generate natural voice guidance for the user."""
    if obstacle_distance < 0.5:
        return "Stop! There is an obstacle directly in front of you."
    elif obstacle_distance < 1.0:
        return f"Careful. Obstacle ahead at {obstacle_distance:.1f} meters. Move slowly."
    elif obstacle_distance < 1.5:
        return f"Warning. Object detected {obstacle_distance:.1f} meters ahead."
    else:
        return "Path is clear. You can continue walking."

tools = [analyze_obstacle_distance, detect_fall, generate_voice_guidance]
