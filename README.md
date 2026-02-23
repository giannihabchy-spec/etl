# Setup:
  uv sync

# Requirements:
  folder containg raw files + 'Auto Calc.xlsx'
  
# Terminal Run:
  uv run python scripts/run_etl.py 'folder_path' <br>
  (streamlit) uv run streamlit run scripts/gui.py

# Create Shortcut:
  Adjust gui.py path in run_gui.vbs <br>
  Create shortcut for run_gui.vbs