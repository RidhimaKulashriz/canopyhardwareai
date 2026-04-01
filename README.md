

# CANOPY Smart Cane AI
<img width="1536" height="632" alt="Copy of obstacle detector for visually impared people" src="https://github.com/user-attachments/assets/86404cea-646b-44df-9fdf-a30b2bc6124a" />

**AI-Powered Assistance for Visually Impaired Users | Auto Tinkercad Integration**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Overview

CANOPY is an intelligent system that reads distance data from an ultrasonic sensor (via Tinkercad simulation) and provides real-time AI-powered voice guidance for visually impaired users.

### Key Features
- **Auto Tinkercad Reader** - Automatically detects copied distance data
- **AI-Powered Guidance** - Uses Google Gemini 2.5 Flash for real-time advice
- **Live Dashboard** - Distance display, graphs, and risk indicators
- **Firebase Sync** - All data saved to cloud
- **Manual Control** - Simulate distances for testing
- **Chat Interface** - Ask questions anytime

---

## Tinkercad Circuit

### Circuit Link
**[Open in Tinkercad](https://www.tinkercad.com/things/97hywVMHFhc/editel)**

### Components Required
| Component | Quantity | Purpose |
|-----------|----------|---------|
| Arduino Uno R3 | 1 | Microcontroller |
| Ultrasonic Sensor (HC-SR04) | 1 | Distance measurement |
| Piezo Buzzer | 1 | Audio alerts |
| Jumper Wires | As needed | Connections |

### Wiring Diagram
```
Arduino Uno          Ultrasonic Sensor
   5V      ---------> VCC
   GND     ---------> GND
   Pin 11  ---------> TRIG
   Pin 12  ---------> ECHO

Arduino Uno          Piezo Buzzer
   Pin 13  ---------> Positive (+)
   GND     ---------> Negative (-)
```

### Arduino Code
```cpp
int trigPin = 11;
int echoPin = 12;
int buzzerPin = 13;
long duration;
float distance_cm;

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(buzzerPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  // Send ultrasonic pulse
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  // Read echo
  duration = pulseIn(echoPin, HIGH);
  
  // Calculate distance (cm)
  distance_cm = duration * 0.034 / 2;
  
  // Send to Serial Monitor
  Serial.print("DISTANCE:");
  Serial.println(distance_cm);
  
  // Buzzer alert for obstacles
  if(distance_cm < 70 && distance_cm > 0) {
    tone(buzzerPin, 500);
    delay(300);
    noTone(buzzerPin);
    delay(200);
  } else {
    noTone(buzzerPin);
  }
  
  delay(250);
}
```

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/RidhimaKulashriz/visuallyimpairedai.git
cd visuallyimpairedai
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
pip install pyperclip
```

### 4. Set Up API Keys

Create a `.env` file:
```bash
notepad .env
```

Add your credentials:
```
GEMINI_API_KEY=your_gemini_api_key_here
FIREBASE_DATABASE_URL=https://your-project.firebaseio.com/
FIREBASE_DATABASE_SECRET=your_database_secret
```

### 5. Run the Application
```bash
streamlit run canopy_final.py
```

---

## How to Use

### Step 1: Start Tinkercad Simulation
1. Open your Tinkercad circuit
2. Click "Start Simulation"
3. Open Serial Monitor (bottom of code editor)
4. You'll see data like `DISTANCE:41.11`

### Step 2: Copy Data
1. Click and select any line in Serial Monitor
2. Press Ctrl+C to copy

### Step 3: AI Auto-Detects
- The Streamlit app automatically detects the copied data
- Distance appears in the sidebar
- Graph updates automatically

### Step 4: Ask Questions
Type questions in the chat:
- "What's the current distance?"
- "Is there an obstacle ahead?"
- "Should I stop?"
- "Guide me forward"

---

## Manual Controls

| Control | Function |
|---------|----------|
| **Manual Paste** | Paste `DISTANCE:51.1` directly |
| **Distance Slider** | Simulate any distance |
| **Simulate Reading** | Add manual reading to history |
| **Clear History** | Reset all data |
| **Critical Test** | Test emergency scenario (0.25m) |
| **Safe Test** | Test safe scenario (2.5m) |

---

## Features in Detail

### AI Agent
- Powered by **Google Gemini 2.5 Flash**
- Provides calm, clear guidance
- Context-aware responses
- Handles emergencies automatically

### Data Visualization
- **Live Distance Display** - Real-time readings
- **Risk Indicators** - Critical (<50cm), Warning (<70cm), Safe (>70cm)
- **History Graph** - Plotly chart of all readings
- **Recent Readings** - Last 5 entries with icons

### Firebase Integration
- All readings saved to cloud
- Real-time sync across devices
- Alert history stored
- AI responses logged

---

## Project Structure

```
visuallyimpairedai/
│
├── canopy_final.py          # Main application
├── README.md                # Documentation
├── requirements.txt         # Dependencies
├── .env                     # API keys (ignored)
│
├── ai_agent/                # AI core
│   ├── graph.py             # LangGraph workflow
│   ├── nodes.py             # Gemini AI processing
│   ├── state.py             # State management
│   ├── config.py            # Configuration
│   ├── tools.py             # AI tools
│   └── firebase_client.py   # Firebase client
│
└── tests/                   # Test files
```

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| **AI Framework** | LangGraph |
| **LLM** | Google Gemini 2.5 Flash |
| **Frontend** | Streamlit |
| **Database** | Firebase Realtime Database |
| **Data Processing** | Pandas, Plotly |
| **Auto Reader** | PyAutoGUI, Pyperclip |

---

## Troubleshooting

### Auto Reader Not Working?
1. Make sure Serial Monitor is open in Tinkercad
2. Select and copy a line (Ctrl+C)
3. Check if data appears in app sidebar

### API Key Errors?
1. Get free key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Update `.env` file
3. Restart the app

### Firebase Not Connected?
1. Check your database URL
2. Verify database secret
3. Ensure database rules allow write access

---

## License

MIT License - Feel free to use and modify!

---

## Credits

- **Google Gemini AI** - Language model
- **Firebase** - Cloud database
- **Streamlit** - Web framework
- **LangGraph** - AI workflow
- **Tinkercad** - Circuit simulation

```



