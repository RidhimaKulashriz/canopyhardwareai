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
    global auto_data, last_clipboard
    while True:
        try:
            current = pyperclip.paste()
            if current != last_clipboard and "DISTANCE:" in current:
                last_clipboard = current
                match = re.search(r'DISTANCE:(\d+\.?\d*)', current)
                if match:
                    distance_cm = float(match.group(1))
                    auto_data = distance_cm
                    print(f"Auto-detected: {distance_cm}cm")
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
                    try:
                        distance_m = distance_cm / 100
                        url = f"{FIREBASE_URL}/users/{USER_ID}/sensors/latest.json?auth={FIREBASE_SECRET}"
                        requests.put(url, json={
                            "distance": distance_m,
                            "timestamp": datetime.now().isoformat()
                        }, timeout=2)
                    except:
                        pass
        except:
            pass
        time.sleep(0.5)

st.set_page_config(page_title="CANOPY AI", layout="wide")
st.title("CANOPY Smart Cane AI")
st.markdown("### Auto Tinkercad Reader - Just Copy from Serial Monitor")

if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'sensor_history' not in st.session_state:
    st.session_state.sensor_history = []
if 'auto_data' not in st.session_state:
    st.session_state.auto_data = None
if 'clipboard_started' not in st.session_state:
    thread = threading.Thread(target=monitor_clipboard, daemon=True)
    thread.start()
    st.session_state.clipboard_started = True

with st.sidebar:
    st.header("Tinkercad Status")
    if st.session_state.auto_data:
        st.success("Auto-Reader ACTIVE")
        st.metric("Distance", f"{st.session_state.auto_data:.1f} cm")
        if st.session_state.auto_data < 50:
            st.error("CRITICAL - Obstacle!")
        elif st.session_state.auto_data < 70:
            st.warning("WARNING")
        else:
            st.success("Safe")
    else:
        st.info("Waiting for Tinkercad...")
        st.markdown("1. Open Tinkercad\n2. Open Serial Monitor\n3. Copy DISTANCE:xx.xx")
    
    st.divider()
    st.header("Manual Paste")
    tinkercad_paste = st.text_input("Paste:", placeholder="DISTANCE:51.1")
    if st.button("Update"):
        try:
            match = re.search(r'DISTANCE:(\d+\.?\d*)', tinkercad_paste)
            if match:
                cm = float(match.group(1))
                st.session_state.sensor_history.append({'distance': cm/100, 'timestamp': datetime.now()})
                st.session_state.auto_data = cm
                st.success(f"Updated: {cm}cm")
                st.rerun()
        except:
            st.error("Use: DISTANCE:51.1")
    
    st.divider()
    st.header("Manual Control")
    manual = st.slider("Distance (m)", 0.0, 3.0, 1.2, 0.05)
    if st.button("Simulate"):
        st.session_state.sensor_history.append({'distance': manual, 'timestamp': datetime.now()})
        st.rerun()
    if st.button("Clear"):
        st.session_state.sensor_history = []
        st.rerun()

col1, col2 = st.columns([2, 1])

with col1:
    st.header("AI Chat")
    for msg in st.session_state.messages:
        st.chat_message(msg['role']).write(msg['content'])
    
    query = st.chat_input("Ask AI...")
    if query:
        st.session_state.messages.append({'role': 'user', 'content': query})
        current = st.session_state.auto_data/100 if st.session_state.auto_data else 1.0
        if st.session_state.sensor_history:
            current = st.session_state.sensor_history[-1]['distance']
        state = {
            'sensor_data': {'distance': current, 'acceleration': 1.0},
            'alerts': [], 'user_feedback': [], 'ai_response': None,
            'actions_taken': [], 'conversation_history': [], 'context': {'user_query': query}
        }
        resp = agent_graph.invoke(state).get('ai_response', '')
        st.session_state.messages.append({'role': 'assistant', 'content': resp})
        st.rerun()

with col2:
    if st.session_state.auto_data:
        st.metric("Distance", f"{st.session_state.auto_data:.1f} cm")
    if st.session_state.sensor_history:
        df = pd.DataFrame(st.session_state.sensor_history)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=list(range(len(df))), y=df['distance'], mode='lines+markers'))
        fig.add_hline(y=0.5, line_dash="dash", line_color="red")
        fig.add_hline(y=1.0, line_dash="dash", line_color="orange")
        st.plotly_chart(fig, use_container_width=True)

st.caption("Copy DISTANCE:xx.xx from Tinkercad - AI responds automatically!")
