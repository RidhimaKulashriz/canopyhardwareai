import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from ai_agent.graph import agent_graph
from ai_agent.state import AgentState
import pyperclip
import re
import threading
import time
import requests

# ========== CONFIGURATION ==========
FIREBASE_URL = "https://smart-cane-ai-default-rtdb.asia-southeast1.firebasedatabase.app"
FIREBASE_SECRET = "zrmDiimzcJkIoHwfQN8KEXZWUBxhO9S8Llv3tD9v"
USER_ID = "test_user"
# ===================================

auto_data = None
last_clipboard = ""

def monitor_clipboard():
    """Automatically monitor clipboard for Tinkercad data"""
    global auto_data, last_clipboard
    while True:
        try:
            # Get current clipboard content
            current = pyperclip.paste()
            
            # Check if it's new and contains DISTANCE
            if current != last_clipboard and "DISTANCE:" in current:
                last_clipboard = current
                match = re.search(r'DISTANCE:(\d+\.?\d*)', current)
                if match:
                    distance_cm = float(match.group(1))
                    auto_data = distance_cm
                    print(f"📡 Auto-detected from clipboard: {distance_cm}cm")
                    
                    # Update session state
                    try:
                        if 'auto_data' in st.session_state:
                            st.session_state.auto_data = distance_cm
                        if 'sensor_history' in st.session_state:
                            st.session_state.sensor_history.append({
                                'distance': distance_cm / 100,
                                'timestamp': datetime.now()
                            })
                    except:
                        pass
                    
                    # Save to Firebase
                    distance_m = distance_cm / 100
                    try:
                        url = f"{FIREBASE_URL}/users/{USER_ID}/sensors/latest.json?auth={FIREBASE_SECRET}"
                        requests.put(url, json={
                            "distance": distance_m,
                            "timestamp": datetime.now().isoformat()
                        }, timeout=2)
                    except:
                        pass
        except Exception as e:
            print(f"Clipboard error: {e}")
        time.sleep(0.5)  # Check every 0.5 seconds

st.set_page_config(page_title="CANOPY AI", layout="wide", page_icon="🦯")

st.title("🦯 CANOPY Smart Cane AI")
st.markdown("### Auto Tinkercad Reader - Just Copy from Serial Monitor!")

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'sensor_history' not in st.session_state:
    st.session_state.sensor_history = []
if 'auto_data' not in st.session_state:
    st.session_state.auto_data = None
if 'manual_distance' not in st.session_state:
    st.session_state.manual_distance = 1.2
if 'clipboard_started' not in st.session_state:
    thread = threading.Thread(target=monitor_clipboard, daemon=True)
    thread.start()
    st.session_state.clipboard_started = True

# Sidebar
with st.sidebar:
    st.header("📡 Tinkercad Connection")
    
    if st.session_state.auto_data:
        st.success("✅ Auto-Reader ACTIVE")
        st.metric("Current Distance", f"{st.session_state.auto_data:.1f} cm", 
                 f"{st.session_state.auto_data/100:.2f} m")
        
        # Risk indicator
        if st.session_state.auto_data < 50:
            st.error("🚨 CRITICAL - Obstacle very close!")
            st.progress(100)
        elif st.session_state.auto_data < 70:
            st.warning("⚠️ WARNING - Obstacle approaching")
            st.progress(70)
        else:
            st.success("✅ Path clear")
            st.progress(25)
    else:
        st.info("⏳ Waiting for Tinkercad data...")
        st.info("💡 How to use:")
        st.markdown("""
        1. Open Tinkercad simulation
        2. Open Serial Monitor
        3. **Select and Copy** (Ctrl+C) a line like `DISTANCE:41.11`
        4. Data appears here automatically!
        """)
    
    st.divider()
    
    st.header("📋 Manual Paste")
    tinkercad_paste = st.text_input("Or paste manually:", placeholder="DISTANCE:51.1")
    
    if st.button("📊 Update"):
        try:
            match = re.search(r'DISTANCE:(\d+\.?\d*)', tinkercad_paste)
            if match:
                distance_cm = float(match.group(1))
                distance_m = distance_cm / 100.0
                st.session_state.sensor_history.append({
                    'distance': distance_m,
                    'timestamp': datetime.now()
                })
                st.session_state.auto_data = distance_cm
                st.success(f"✅ Updated: {distance_cm}cm")
                st.rerun()
            else:
                st.error("❌ Use format: DISTANCE:51.1")
        except:
            st.error("Error")
    
    st.divider()
    
    st.header("🎮 Manual Control")
    st.session_state.manual_distance = st.slider("Distance (m)", 0.0, 3.0, st.session_state.manual_distance, 0.05)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 Simulate"):
            st.session_state.sensor_history.append({
                'distance': st.session_state.manual_distance,
                'timestamp': datetime.now()
            })
            st.success(f"Added: {st.session_state.manual_distance}m")
            st.rerun()
    with col2:
        if st.button("🗑️ Clear"):
            st.session_state.sensor_history = []
            st.success("Cleared")
            st.rerun()
    
    st.divider()
    
    st.header("🧪 Quick Tests")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔴 Critical (0.25m)"):
            st.session_state.sensor_history.append({
                'distance': 0.25,
                'timestamp': datetime.now()
            })
            st.session_state.auto_data = 25
            st.success("Critical test")
            st.rerun()
    with col2:
        if st.button("🟢 Safe (2.5m)"):
            st.session_state.sensor_history.append({
                'distance': 2.5,
                'timestamp': datetime.now()
            })
            st.session_state.auto_data = 250
            st.success("Safe test")
            st.rerun()

# Main area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("💬 AI Agent Chat")
    
    chat_container = st.container(height=400)
    with chat_container:
        for msg in st.session_state.messages:
            if msg['role'] == 'user':
                st.chat_message("user").write(msg['content'])
            else:
                st.chat_message("assistant").write(msg['content'])
    
    query = st.chat_input("Ask the AI agent anything...")
    
    if query:
        st.session_state.messages.append({'role': 'user', 'content': query})
        
        current_dist = st.session_state.auto_data / 100 if st.session_state.auto_data else 1.0
        if st.session_state.sensor_history:
            current_dist = st.session_state.sensor_history[-1]['distance']
        
        state = {
            'sensor_data': {
                'distance': current_dist,
                'acceleration': 1.0,
                'gyroscope': None,
                'timestamp': datetime.now(),
                'location': None
            },
            'alerts': [],
            'user_feedback': [],
            'ai_response': None,
            'actions_taken': [],
            'conversation_history': [],
            'context': {'user_query': query}
        }
        
        with st.spinner("🤔 AI is thinking..."):
            result = agent_graph.invoke(state)
            response = result.get('ai_response', "I'm analyzing your situation.")
        
        st.session_state.messages.append({'role': 'assistant', 'content': response})
        st.rerun()

with col2:
    st.header("📡 Live Tinkercad Data")
    
    if st.session_state.auto_data:
        st.metric("Distance", f"{st.session_state.auto_data:.1f} cm")
        if st.session_state.auto_data < 50:
            st.error("⚠️ STOP! Obstacle very close!")
        elif st.session_state.auto_data < 70:
            st.warning(f"⚠️ Caution! {st.session_state.auto_data:.1f}cm")
        else:
            st.success(f"✅ Safe: {st.session_state.auto_data:.1f}cm")
    else:
        st.info("💡 Copy from Tinkercad Serial Monitor")
        st.code("DISTANCE:41.11", language="text")
    
    st.divider()
    
    st.header("📈 Sensor History")
    
    if st.session_state.sensor_history:
        df = pd.DataFrame(st.session_state.sensor_history)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(range(len(df))), 
            y=df['distance'], 
            mode='lines+markers', 
            name='Distance (m)',
            line=dict(color='blue', width=2)
        ))
        fig.add_hline(y=0.5, line_dash="dash", line_color="red", annotation_text="Critical")
        fig.add_hline(y=1.0, line_dash="dash", line_color="orange", annotation_text="Warning")
        fig.update_layout(height=250, title="Distance History")
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("**Recent:**")
        for row in df.tail(3).iterrows():
            d = row[1]['distance']
            icon = "🔴" if d < 0.5 else "🟡" if d < 1.0 else "🟢"
            st.text(f"{icon} {d:.2f}m")
    else:
        st.info("No data yet")

st.divider()
st.caption("🦯 CANOPY AI | Auto Clipboard Reader | Copy from Tinkercad, AI Responds!")
