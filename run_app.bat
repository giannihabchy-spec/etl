@echo off
cd /d "%~dp0"
:: Force the theme to dark via the command line flag
uv run streamlit run gui.py --theme.base="dark" --server.headless=true
pause