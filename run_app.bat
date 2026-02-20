@echo off
cd /d "%~dp0"
uv run streamlit run gui.py --browser.gatherUsageStats false
pause