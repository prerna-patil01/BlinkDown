# BlinkDown
# BlinkDown — Outage Intelligence Dashboard

BlinkDown is a data analytics dashboard designed to monitor, analyze, and interpret service outages across major cloud providers. It provides structured insights into reliability, financial impact, and system risk.

---

## Overview

The application aggregates outage data and presents it through interactive visualizations and analytical components. It includes a simulated AI analyst that generates context-aware insights based on system data.

---

## Features

- Interactive outage analytics dashboard
- Company-wise and service-level breakdown
- Financial impact and SLA breach analysis
- Root cause analysis of incidents
- Context-aware AI insights (demo mode, no external API required)
- Real-time filtering by company, severity, and date range

---

## Tech Stack

- Python
- Streamlit
- Pandas
- Plotly

---
## Project Structure
BlinkDown/
│── app/
│   ├── ui/
│   ├── backend/
│── assets/
│── requirements.txt
│── README.md---

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/prerna-patil01/BlinkDown.git
   cd BlinkDown	
2.	Create a virtual environment
python -m venv venv
source venv/bin/activate   # Mac/Linux

3. Install dependencies:
pip install -r requirements.txt
4.	Run the application:
AI Module

The AI component operates in a controlled demo mode and generates structured insights based on internal data. It does not rely on external APIs, ensuring reliability and zero runtime cost.

⸻

Notes
	•	The project follows a modular architecture separating UI and backend logic.
	•	The AI module can be extended to integrate external APIs if required.

⸻

Author

Prerna Patil
Computer Science Undergraduate — BVRIT