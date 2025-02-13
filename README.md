# Employee Sentiment Analysis

## Overview
This project analyzes employee feedback using AI to determine sentiment and assess attrition risk. The backend is built with **FastAPI** and integrates with **Google Gemini API**, while the frontend is a simple **HTML + JavaScript** interface.

## Features
✅ Supports free-text employee feedback  
✅ Uses Google Gemini API for sentiment analysis  
✅ Displays structured sentiment analysis results  
✅ Simple web frontend for easy interaction  

## Tech Stack
- **Backend:** FastAPI, Google Gemini API  
- **Frontend:** HTML, JavaScript, CSS  

---

## 🚀 Setup Guide

### 1️⃣ Clone the Repository  
**Run in terminal**
git clone https://github.com/yourusername/employee-sentiment-analysis.git
cd employee-sentiment-analysis

python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

## Fetch requirements via pip
pip install -r requirements.txt 

## Setup environment secrets (Gemini key)
Create a .env file in the root directory and add:
GEMINI_API_KEY=your_api_key_here

##  Run the Backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

## Frontend startup
Open index.html in the browser to startup the frontend


The app is now ready to experiment and test.
Could not deploy it because backend hosting needed more time to setup.
 
## !! Please note:
## Gemini sometimes returns outputs without json, which are not accessible to the frontend. Just resubmit