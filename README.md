# 🏥 Clinic Financial Resilience Platform

**Empowering small clinics with cyber-financial resilience**

A Financial Resilience Web Application tailored for small clinics, helping them understand, recover from, and protect against cyber-related financial loss.

## Problem Statement

Small, private clinics are highly vulnerable to cyberattacks, which can disrupt services, drain finances, and compromise their ability to operate. Unlike larger institutions, these clinics often lack access to financial resilience and recovery planning tools. Insurance can be complex, expensive, and insufficient for their needs.

## Solution

Our platform provides proactive financial resilience tools specifically designed for small clinics (1-2 doctor practices), offering real-time insights and personalized recovery strategies instead of just waiting for insurance reimbursements.

## Key Features

### 📊 Before & After Financial View
- **Before Tab**: Shows typical clinic finances in normal operations
- **After Tab**: Displays post-cyberattack financial impact and recovery projections
- Clean tabbed interface matching modern UX standards

### 🤖 AI-Powered Recovery Assistant
- Interactive chatbot that explains how different factors impact recovery
- Suggests faster recovery strategies (cost-cutting, fund reallocation, risk diversification)
- Provides personalized recommendations based on clinic profile

### 💼 Risk Mitigation & Preparedness
- Savings guidance for future incidents  
- Scenario planning: "What happens if this occurs again?"
- Reduces reliance on traditional insurance through direct, data-driven strategies

## Target Market
- Private clinics with 1–2 doctors
- Clinics without in-house IT or financial recovery tools  
- Cost-conscious providers who need simple, actionable insights

## Differentiator vs Insurance
- **Insurance**: Reactive, delayed/limited payouts after losses
- **Our Platform**: Proactive, real-time insights, personalized strategies, future planning

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/keerthisurisetty/hackgt12.git
   cd hackgt12
   ```

2. **Set up OpenAI API Key (optional)**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

3. **Start local server**
   ```bash
   python3 -m http.server 8080
   ```

4. **Open in browser**
   ```
   http://localhost:8080/clinic-resilience.html
   ```

## Demo Workflow

1. **Select Clinic Type**: Choose between Solo Practice ($300K revenue) or Small Group Practice ($750K revenue)
2. **Input Attack Details**: Specify financial loss and target recovery time  
3. **View Financial Impact**: Compare before/after financial states using tabs
4. **Explore Recovery Plan**: Interactive timeline and AI-powered recommendations
5. **Chat with AI Assistant**: Get personalized recovery strategies and savings tips

## Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Visualization**: Chart.js for recovery timeline graphs
- **AI Integration**: OpenAI GPT-3.5-turbo (with fallback mock responses)
- **Deployment**: Python HTTP Server (no dependencies)

## Project Structure

```
├── clinic-resilience.html    # Main application file
├── clinic-styles.css         # Professional styling
├── .env.example             # Environment template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Features Showcase

### 🏥 **Clinic-Focused Data Models**
- **Solo Practice**: $300K annual revenue, $800 daily costs, 1 doctor
- **Small Group Practice**: $750K annual revenue, $2.1K daily costs, 2-3 doctors

### 📊 **Interactive Before/After Tabs**
- Clean comparison of normal vs post-attack finances
- Visual impact assessment with recovery projections
- Professional, minimal design perfect for presentations

### 🤖 **AI Recovery Assistant**
- Real-time chat interface for recovery guidance
- Simulation of recovery factors and smart savings recommendations
- Contextual advice based on clinic size and attack severity

### 📈 **Visual Recovery Timeline** 
- Interactive Chart.js powered recovery progression
- Week-by-week operational capacity restoration tracking
- Clear visualization of path back to financial health

## HackGT12 Submission

**Track**: Curator's Cause - Healthcare Technology Innovation  
**Problem**: Financial vulnerability of small clinics to cyber threats  
**Innovation**: Proactive financial resilience platform as alternative to traditional insurance  
**Demo**: `http://localhost:8080/clinic-resilience.html`

## Vision

Empower small clinics with technology-enabled resilience, ensuring they can continue to deliver care even in the face of cyber threats—while saving money, recovering faster, and planning for the future.

---

Built with ❤️ for HackGT12 by [Keerthi Surisetty](https://github.com/keerthisurisetty)