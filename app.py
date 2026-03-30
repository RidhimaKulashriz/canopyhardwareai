import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from ai_agent.graph import agent_graph
from ai_agent.state import AgentState
from ai_agent.firebase_client import FirebaseClient

# Page config
st.set_page_config(page_title="Smart Cane AI Agent", layout="wide", page_icon=":cane:")

# Title
st.title("Smart Cane AI Agent")
st.markdown("### AI-Powered Assistance for Visually Impaired Users")

# Initialize Firebase client
firebase = FirebaseClient()

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'sensor_history' not in st.session_state:
    st.session_state.sensor_history = []

# Sidebar - Sensor Simulation
with st.sidebar:
    st.header("Sensor Data Simulation")
    
    distance = st.slider("Obstacle Distance (meters)", 0.0, 3.0, 1.2, 0.05)
    acceleration = st.slider("Acceleration (g-force)", 0.0, 3.0, 1.0, 0.05)
    
    st.divider()
    
    if st.button("Simulate Sensor Reading", type="primary"):
        sensor_data = {
            'distance': distance,
            'acceleration': acceleration,
            'timestamp': datetime.now(),
            'location': {'lat': 37.7749, 'lng': -122.4194}
        }
        st.session_state.sensor_history.append(sensor_data)
        st.success(f"Sensor reading recorded: {distance:.2f}m, {acceleration:.2f}g")
    
    st.divider()
    
    st.header("Live Status")
    if st.session_state.sensor_history:
        latest = st.session_state.sensor_history[-1]
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Distance", f"{latest['distance']:.2f} m")
        with col2:
            st.metric("G-Force", f"{latest['acceleration']:.2f} g")
        
        if latest['distance'] < 0.5 or latest['acceleration'] > 2.0:
            st.error("CRITICAL RISK")
        elif latest['distance'] < 1.0:
            st.warning("CAUTION")
        else:
            st.success("SAFE")

# Main area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("AI Agent Response")
    
    chat_container = st.container(height=400)
    with chat_container:
        for msg in st.session_state.messages:
            if msg['role'] == 'user':
                st.chat_message("user").write(msg['content'])
            else:
                st.chat_message("assistant").write(msg['content'])
    
    user_query = st.chat_input("Ask the AI agent anything...")
    
    if user_query:
        st.session_state.messages.append({'role': 'user', 'content': user_query})
        
        latest_sensor = st.session_state.sensor_history[-1] if st.session_state.sensor_history else {'distance': 1.0, 'acceleration': 1.0}
        
        state: AgentState = {
            'sensor_data': {
                'distance': latest_sensor['distance'],
                'acceleration': latest_sensor['acceleration'],
                'gyroscope': None,
                'timestamp': datetime.now(),
                'location': latest_sensor.get('location', None)
            },
            'alerts': [],
            'user_feedback': [],
            'ai_response': None,
            'actions_taken': [],
            'conversation_history': [],
            'context': {'user_query': user_query}
        }
        
        result = agent_graph.invoke(state)
        response = result.get('ai_response', "I'm analyzing your situation. Please stay safe.")
        
        st.session_state.messages.append({'role': 'assistant', 'content': response})
        st.rerun()

with col2:
    st.header("Sensor History")
    
    if st.session_state.sensor_history:
        df = pd.DataFrame(st.session_state.sensor_history)
        
        fig_distance = go.Figure()
        fig_distance.add_trace(go.Scatter(
            x=list(range(len(df))), y=df['distance'],
            mode='lines+markers', name='Distance (m)',
            line=dict(color='blue', width=2)
        ))
        fig_distance.add_hline(y=1.0, line_dash="dash", line_color="orange")
        fig_distance.add_hline(y=0.5, line_dash="dash", line_color="red")
        fig_distance.update_layout(title="Obstacle Distance", height=250)
        st.plotly_chart(fig_distance, width='stretch')  # Fixed: use width instead of use_container_width
        
        fig_accel = go.Figure()
        fig_accel.add_trace(go.Scatter(
            x=list(range(len(df))), y=df['acceleration'],
            mode='lines+markers', name='Acceleration (g)',
            line=dict(color='red', width=2)
        ))
        fig_accel.add_hline(y=2.0, line_dash="dash", line_color="red")
        fig_accel.update_layout(title="Acceleration", height=250)
        st.plotly_chart(fig_accel, width='stretch')  # Fixed: use width instead of use_container_width
    else:
        st.info("No sensor data yet. Use the sidebar to simulate readings.")

st.divider()
st.caption(f"Smart Cane AI Agent v1.0 | LangGraph Powered")
