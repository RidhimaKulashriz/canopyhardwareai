from ai_agent.graph import agent_graph
from ai_agent.state import AgentState
from datetime import datetime

def main():
    print("Smart Cane AI Agent Starting...")
    print("=" * 50)
    
    # Test with sample data
    test_state: AgentState = {
        'sensor_data': {
            'distance': 0.8,
            'acceleration': 1.2,
            'gyroscope': None,
            'timestamp': datetime.now(),
            'location': {'lat': 37.7749, 'lng': -122.4194}
        },
        'alerts': [],
        'user_feedback': [],
        'ai_response': None,
        'actions_taken': [],
        'conversation_history': [],
        'context': {}
    }
    
    print("Processing sensor data...")
    result = agent_graph.invoke(test_state)
    
    print(f"\nResults:")
    print(f"  - Alerts: {len(result.get('alerts', []))}")
    print(f"  - AI Response: {result.get('ai_response', 'No response')}")
    print(f"  - Actions: {result.get('actions_taken', [])}")
    print("\nAgent test complete!")

if __name__ == "__main__":
    main()
