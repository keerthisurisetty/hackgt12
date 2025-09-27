# 🏥 Hospital Cyber Resilience Simulator

An AI-powered platform helping hospitals recover financially from cyberattacks through data-driven financial planning and operational continuity strategies.

## 🚀 Quick Start

### Prerequisites
- A modern web browser
- OpenAI API key (for AI recommendations - optional)

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/keerthisurisetty/hackgt12.git
   cd hackgt12
   ```

2. **Configure OpenAI API Key (Optional)**
   
   **Option A: Using .env file (Recommended)**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

   **Option B: Direct configuration**
   - Open `hospital-simulator.html`
   - Find the `CONFIG` object around line 420
   - Replace `'YOUR_OPENAI_API_KEY_HERE'` with your actual OpenAI API key

3. **Run the simulator**
   ```bash
   # Start a simple HTTP server
   python3 -m http.server 8080
   
   # Open in browser
   open http://localhost:8080/hospital-simulator.html
   ```

## 🏥 Features

### Core Functionality
- **Hospital Selection**: Choose between Rural General Hospital (150 beds) or Urban Medical Center (400 beds)
- **Cyberattack Impact Assessment**: Configure attack scenarios with custom financial losses (default: $7M)
- **6-Week Recovery Simulation**: Interactive timeline showing financial recovery phases
- **AI-Powered Recommendations**: OpenAI-generated recovery strategies tailored to hospital profile

### Hospital Profiles
- **Rural General Hospital**
  - 150 beds, $61M annual revenue
  - $190K daily operating costs
  - 26/100 cyber readiness score
  - 55 days operating runway

- **Urban Medical Center**
  - 400 beds, $230M annual revenue
  - $656K daily operating costs
  - 42/100 cyber readiness score
  - 99 days operating runway

### Technical Features
- Single-file HTML solution (no server dependencies)
- Chart.js visualizations for recovery timelines
- Real-time financial impact calculations
- Department-by-department vulnerability analysis
- OpenAI integration with fallback mock recommendations

## 📊 Demo Workflow

1. **Select Hospital Profile**: Choose between rural or urban hospital
2. **Configure Attack**: Set financial loss amount and recovery timeline
3. **View Impact Analysis**: See immediate financial impact metrics
4. **Recovery Timeline**: Interactive Chart.js visualization of 6-week recovery
5. **AI Recommendations**: Get personalized recovery strategies

## 🛠 Development

### Project Structure
```
hackgt12/
├── hospital-simulator.html    # Single-file application
├── .env                      # API keys (ignored by git)
├── .env.example             # API key template
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

### Key Technologies
- **Frontend**: HTML5, CSS3, JavaScript ES6+
- **Visualization**: Chart.js
- **AI**: OpenAI GPT-3.5-turbo API (optional)
- **Deployment**: Static file hosting

## 🎯 HackGT12 Submission

**Track**: The Curator's Cause Track - Building solutions that make the world better through healthcare cybersecurity resilience.

**Problem Statement**: Helping hospitals recover from the financial strain of cyberattacks, which cost hospitals an average of $7 million and require 6+ weeks to fully recover from.

**Solution**: AI-powered financial recovery simulation platform that provides:
- Real-time impact assessment
- Data-driven recovery planning
- Personalized AI recommendations
- Emergency fund planning guidance

## 🔒 Security Notes

- API keys are stored in `.env` file (git-ignored)
- No sensitive data is stored permanently
- All calculations performed client-side
- Mock recommendations available if API unavailable

## 📝 License

This project was created for HackGT12 and is available for educational and demonstration purposes.

---
Built with ❤️ for HackGT12 - Making healthcare more resilient against cyber threats.