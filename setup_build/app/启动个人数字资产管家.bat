@echo off
cd /d "%~dp0"
start "" http://localhost:8501
"%~dp0..\python.exe" -m streamlit run "%~dp0dashboard.py" --server.port 8501
