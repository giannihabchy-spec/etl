import streamlit as st
import sys
from pathlib import Path
import warnings

st.set_page_config(
    page_title="Auto Calc Pipeline",
    layout="wide",
    initial_sidebar_state="collapsed"
)

sys.path.append(str(Path(__file__).parent / "src"))

from etl.config import get_jobs
from etl.orchestrator import clean_folder
from etl.merger import merge
from etl.strip_all import strip_all
from etl.special_characters import special_char
from etl.saver import save_cleaned_data
from etl.reset_view import reset_workbook_view
from etl.end_to_beg import end_to_beg
from etl.prev_unit_cost import uc_pre_month
from etl.clearer import clear_all
from etl.writer import write_master

st.markdown("""
    <style>
        /* Force Dark Theme Vibe */
        .stApp { background-color: #0e1117; color: #ffffff; }
        /* Hide Streamlit branding for a "Desktop App" feel */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

warnings.filterwarnings(
    "ignore",
    message="Workbook contains no default style*",
    category=UserWarning,
)

st.title("Auto Calc Pipeline")
st.markdown("---")

col1, col2, col3 = st.columns(3)
with col1:
    folder_input = st.text_input("📁 Target Folder Path", placeholder="C:/Path/To/Folder")
with col2:
    mode = st.selectbox("⚙️ Mode", options=["all", "not-all"], index=0)
with col3:
    source = st.selectbox("🔀 Source", options=["cloud", "local"], index=0)

if st.button("▶ Run Pipeline", type="primary", use_container_width=True):
    base_folder = Path(folder_input).resolve()
    jobs = get_jobs(source)

    if not base_folder.is_dir():
        st.error(f"Error: '{base_folder}' is not a valid directory.")
    else:
        master_path = base_folder / "Auto Calc.xlsx"
        
        # --- BOX 1: INIT ---
        with st.status("Initializing ETL...", expanded=True) as status_init:
            st.write(f"Folder: `{base_folder.name}`")
            status_init.update(label="Initialization", state="complete", expanded=False)

        # --- BOX 2: CLEANING ---
        with st.status("Cleaning...", expanded=True) as status_clean:
            cleaned = clean_folder(base_folder, source=source, log_func=st.write)
            cleaned = merge(cleaned)
            cleaned = strip_all(cleaned)
            cleaned = special_char(cleaned)
            save_cleaned_data(cleaned, base_folder)
            st.write("Cleaned data is saved.")
            status_clean.update(label="Cleaning", state="complete", expanded=False)
            
        # --- SUBSEQUENT BOXES ---
        if mode == "all":
            with st.status("End -> Beg...", expanded=True) as status_eb:
                reset_workbook_view(master_path)
                end_to_beg(str(master_path))
                st.write("Completed")
                status_eb.update(label="End -> Beg", state="complete", expanded=False)

            with st.status("UNIT COST -> UC PRE MONTH...", expanded=True) as status_eb:
                uc_pre_month(str(master_path), log_func=st.write)
                st.write("Completed")
                status_eb.update(label="UNIT COST -> UC PRE MONTH", state="complete", expanded=False)

            with st.status("Clearing...", expanded=True) as status_clear:
                clear_all(str(master_path), jobs)
                st.write("Completed")
                status_clear.update(label="Clearing", state="complete", expanded=False)

            with st.status("Writing...", expanded=True) as status_write:    
                write_master(str(master_path), cleaned, jobs, clear_first=False, log_func=st.write)
                status_write.update(label="Writing", state="complete", expanded=False)
                st.write("Loaded all available data")
        else:
            with st.status("Writing...", expanded=True) as status_write:
                write_master(str(master_path), cleaned, jobs, clear_first=True, suppress_warnings=True, log_func=st.write)
                status_write.update(label="Writing", state="complete", expanded=False)
                st.write("Loaded all available data")           

        st.success("✅ Successfully updated 'Auto Calc.xlsx'")