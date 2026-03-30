from typing import TypedDict, List, Dict, Any, Optional
from datetime import datetime

class SensorData(TypedDict):
    distance: float
    acceleration: Optional[float]
    gyroscope: Optional[List[float]]
    timestamp: datetime
    location: Optional[Dict[str, float]]

class Alert(TypedDict):
    type: str
    severity: str
    message: str
    timestamp: datetime

class UserFeedback(TypedDict):
    response: str
    helpful: bool
    timestamp: datetime

class AgentState(TypedDict):
    sensor_data: SensorData
    alerts: List[Alert]
    user_feedback: List[UserFeedback]
    ai_response: Optional[str]
    actions_taken: List[str]
    conversation_history: List[Dict[str, str]]
    context: Dict[str, Any]
