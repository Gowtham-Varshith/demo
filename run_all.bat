@echo off

start cmd /k "cd backend && python -m uvicorn main:app --reload"
start cmd /k "cd frontend && npm start"
start cmd /k "streamlit run app.py"